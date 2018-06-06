#!/bin/bash

# leaf credentials
username=""
password=""

local_apic=0
local_apic_tep=0
user_directory=`pwd`
filtered_pod=""
fld="/data/techsupport/_counters"
logfile="collection.log"

# globals
declare -a ns_tor=(
    "N9K-C9332PQ" "N9K-C9396PX" "N9K-C9396TX" "N9K-C9372PX" "N9K-C9372PX-E"
    "N9K-C9372TX" "N9K-C9372TX-E" "N9K-C93128TX" "N9K-C93120TX"
)   
declare -a sb_tor=(
    "N9K-C93180YC-EX" "N9K-C93108TC-EX" "N9K-C93180LC-EX"
)
declare -a alp_tor=(
    "N9K-C9336PQ"
)
declare -A map_ns_tor 
for key in "${!ns_tor[@]}"; do map_ns_tor[${ns_tor[$key]}]="$key"; done  
declare -A map_sb_tor 
for key in "${!sb_tor[@]}"; do map_sb_tor[${sb_tor[$key]}]="$key"; done  
declare -A map_alp_tor 
for key in "${!alp_tor[@]}"; do map_alp_tor[${alp_tor[$key]}]="$key"; done  
 
ns_tor_cmds=(
    " vsh_lc -c 'show clock'"
    " vsh_lc -c 'show plat int counters port detail'"
    " vsh_lc -c 'show plat int ns counters mac asic 0 detail'"
    " bcm-shell-hw 'ps'"
    " bcm-shell-hw 'show c all'"
)
tah_tor_cmds=(
    " vsh_lc -c 'show clock'"
    " vsh_lc -c 'show plat int counters port detail'"
    " vsh_lc -c 'show plat int hal counters usdcounters'"
)
# baby spine only - N9K-C9336PQ
alp_tor_cmds=(
    " vsh_lc -c 'show clock'"
    " vsh_lc -c 'show plat int counters port detail'"
    " vsh_lc -c 'show plat int al counters asic-block all asic 0 detail'"
    " vsh_lc -c 'show plat int al counters asic-block all asic 1 detail'"
    " vsh_lc -c 'show platform internal alp interrupts'"
    " bcm-shell-hw \"0: ps\""
    " bcm-shell-hw \"0: show c all\""
    " bcm-shell-hw \"1: ps\""
    " bcm-shell-hw \"1: show c all\""
)

function log() {
    ts=`date '+%Y-%m-%dT%H:%M:%S'`
    echo "$ts $1"
    if [ -e $logfile ] ; then
        echo "$ts $1" >> collection.log 2> /dev/null
    fi
}

function get_apic_tep() {
    log "getting local APIC info"
    local_apic=`moquery -c topInfo | egrep "^id" | egrep -o [0-9]+`
    local_apic_tep=`moquery -c topSystem -f 'top.System.id=="1"' | egrep "^address" | egrep -o [0-9\.]+`
    log "running on apic node-$local_apic address=$local_apic_tep"
}

function background_collect() {
    # forked process to collect required commands
    # receives line from fnvreadex
    l="$1"
    nodeId=`echo "$l" | egrep -o nodeId=[0-9]+ | egrep -o [0-9]+`
    if [ "$nodeId" ] ; then
        podId=`echo "$l" | egrep -o podId=[0-9]+ | egrep -o [0-9]+`
        address=`echo "$l" | egrep -o address=[0-9\.]+ | egrep -o [0-9\.]+`
        model=`echo "$l" | egrep -o "model=[^ ]+" | egrep -o "=.*" | egrep -o "[^=]+"`
        name=`echo "$l" | egrep -o "name=[^ ]+" | egrep -o "=.*"  | egrep -o "[^=]+"`

        # skip if filtered_pod is set
        if [ "$filtered_pod" ] && [ "$podId" != "$filtered_pod" ] ; then
            log "Skipping collection (pod=$podId, node=$nodeId, $address, $name, $model)"
            continue
        fi
        # skip if unable to determine model
        if ! [ "$model" ] ; then
            log "Skipping collection (pod=$podId, node=$nodeId, $address, $name, $model)"
            continue
        fi
        IFS=$';'
        if [[ -n "${map_ns_tor[$model]}" ]] ; then
            log "Start collection    (pod=$podId, node=$nodeId, $address, $name, $model) (NS)"
            ccmds=("${ns_tor_cmds[@]}")
        elif [[ -n "${map_sb_tor[$model]}" ]] ; then
            log "Start collection    (pod=$podId, node=$nodeId, $address, $name, $model) (SB)"
            ccmds=("${tah_tor_cmds[@]}")
        elif [[ -n "${map_alp_tor[$model]}" ]] ; then
            log "Start collection    (pod=$podId, node=$nodeId, $address, $name, $model) (ALP)"
            ccmds=("${alp_tor_cmds[@]}")
        else
            log "Skipping collection (pod=$podId, node=$nodeId, $address, $name, $model)"
            continue
        fi
        # build list of commands with echo
        cmds=""
        for i in "${ccmds[@]}" ; do 
            cmds="$cmds echo \"##############################\" ; "
            cmds="$cmds echo \"# CMD: $i\" ; "
            cmds="$cmds echo \"##############################\" ; "
            cmds="$cmds $i ; "
        done

        local fname="pod-$podId-node-$nodeId.collection.log"
        echo "##### (pod=$podId, node=$nodeId, $address, $name)" > $fname
        echo "##### `date '+%Y-%m-%dT%H:%M:%S'`" >> $fname
        echo "" >> $fname
        sshpass -p$password ssh -tt -o ConnectTimeout=5 $username@$address -b $local_apic_tep "$cmds" >> $fname 2>> $fname 
        # use sed to remove terminal special characters
        sed -i 's/[^[:print:]\t]//g' $fname
        log "Collection complete (pod=$podId, node=$nodeId, $address, $name, $model)"
    fi
}

function collect_counters() {
 
    log "Collecting switch counters"


    # start collection process for each switch
    local IFS=$'\n'
    for l in `acidiag fnvreadex`; do
        background_collect $l &
    done
    local fail_count=0
    for job in `jobs -p`; do
        wait $job || let "fail_count+=1"
    done

    # create bundle
    log "bundling results"
    ts=`date '+%Y-%m-%dT%H-%M-%S'`
    local fname="collection.$ts.tgz"
    mkdir data
    mv *.log data/
    tar --force-local -zcf $fname data/*
    mv $fname $user_directory/

    # cleanup tmp directories
    rm -rf $fld 

    # completed
    log "results saved to $fname"
}

function display_help() {
    echo -e \\n"Help documentation for $0"\\n
    echo "    -u username (prompted if not provided)"
    echo "    -p password (prompted if not provided)"
    echo "    -P podId to collect output (defaults to all pods)"
    echo ""
    exit 0
}

optspec=":u:p:P:h"
while getopts "$optspec" optchar; do
  case $optchar in
    u)  
        username=$OPTARG
        ;;
    p)  
        password=$OPTARG
        ;;
    P)
        filtered_pod=$OPTARG
        ;;
    h)
        display_help
        exit 0
        ;;
    :)
        echo "Option $OPTARG requires an argument." >&2
        exit 1
        ;;
    \?)
        echo "Invalid option: \"-$OPTARG\"" >&2
        exit 1
        ;;
  esac
done

# if no username provided, then prompt user for it
if [ "$username" == "" ] ; then
    echo -n "Enter switch username: "
    read username
fi
# if no password provided, then prompt user for it
if [ "$password" == "" ] ; then
    read -s -p "Enter switch password: " password
    echo ""
fi

# do everything in tmp directory
mkdir -p $fld
cd $fld
touch $logfile

get_apic_tep
collect_counters


