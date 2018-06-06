from cmd_breaker import cmd_breaker
from ns_cmd_parser import show_plat_int_counters_port_detail, \
                            show_plat_int_ns_counters_mac_asic_0_detail
from bcm_cmd_parser import ps, show_c_all
from tah_cmd_parser import show_plat_int_counters_port_detail_TAHOE, \
                            show_plat_int_hal_counters_usdcounters
import argparse, sys, time, json


def prettyDict(d, indent=0):
   for key, value in d.items():
      sys.stdout.write('\t' * indent + str(key))
      if isinstance(value, dict):
         print("")
         prettyDict(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))



parser = argparse.ArgumentParser(description='Generate')
parser.add_argument('--file', dest='file', action='store', default=None, help='input file')
parser.add_argument('--list', dest='list', action='store_true', help='list the supported commands')
parser.add_argument('--json', dest='json', action='store', help='parse the selected command output and export it to \
                                                                        a given file in JSON format')

parser.add_argument('--raw_json', dest='raw_json', action='store_true', help='print out the raw command line output\
                                                                               in JSON format')
supportedCmd = ["vsh_lc -c 'show platform internal counters port detail' (NS)",
                "vsh_lc -c 'show plat int ns counters mac asic 0 detail' (NS)",
                "bcm-shell-hw 'ps' (BCM)",
                "bcm-shell-hw 'show c all' (BCM)",
                "vsh_lc -c 'show platform internal counters port detail' (Tahoe)",
                "show plat int hal counters usdcounters (Tahoe)"
                ]


pmptText = "Which command do you want to parse:"
pmptText += "\n"

for i, cmd in enumerate(supportedCmd):
    pmptText+=" [" + str(i) + "]"
    pmptText+=cmd
    pmptText+="\n"
pmptText += "   Type Q to quit\n"

optionSelected=""
cmdOutputDict = {}
args = parser.parse_args()


if args.file is not None:
    f = open(args.file, 'r')
    cmdOutputDict = cmd_breaker(f)
    if args.raw_json == False:
        isToplevel = True
        tmpOutput = {}
        while True:
            if(isToplevel):
                optionSelected = raw_input(pmptText)
                if optionSelected == "0":
                    print("You selected: " + supportedCmd[int(optionSelected)])
                    tmpOutput = show_plat_int_counters_port_detail(cmdOutputDict["vsh_lc -c 'show plat int counters port detail'"])
                    if args.json is not None:
                        with open(args.json, "w") as f:
                            f.write(json.dumps(tmpOutput, indent = 4))
                        break
                    #print(tmpOutput)
                    isToplevel = False
                    continue
                elif optionSelected == "1":
                    print("You selected: " + supportedCmd[int(optionSelected)])
                    tmpOutput = show_plat_int_ns_counters_mac_asic_0_detail(cmdOutputDict["vsh_lc -c 'show plat int ns counters mac asic 0 detail'"])
                    if args.json is not None:
                        with open(args.json, "w") as f:
                            f.write(json.dumps(tmpOutput, indent = 4))
                        break
                    isToplevel = False
                    continue
                elif optionSelected == "2":
                    print("You selected: " + supportedCmd[int(optionSelected)])
                    tmpOutput = ps(cmdOutputDict["bcm-shell-hw 'ps'"])
                    if args.json is not None:
                        with open(args.json, "w") as f:
                            f.write(json.dumps(tmpOutput, indent = 4))
                        break
                    isToplevel = False
                    continue
                elif optionSelected == "3":
                    print("You selected: " + supportedCmd[int(optionSelected)])
                    tmpOutput = show_c_all(cmdOutputDict["bcm-shell-hw 'show c all'"])
                    if args.json is not None:
                        with open(args.json, "w") as f:
                            f.write(json.dumps(tmpOutput, indent = 4))
                        break
                    isToplevel = False
                    continue
                elif optionSelected == "4":
                    print("You selected: " + supportedCmd[int(optionSelected)])
                    tmpOutput = show_plat_int_counters_port_detail_TAHOE(cmdOutputDict["vsh_lc -c 'show plat int counters port detail'"])
                    if args.json is not None:
                        with open(args.json, "w") as f:
                            f.write(json.dumps(tmpOutput, indent = 4))
                        break
                    isToplevel = False
                    continue
                elif optionSelected == "5":
                    print("You selected: " + supportedCmd[int(optionSelected)])
                    tmpOutput = show_plat_int_hal_counters_usdcounters(cmdOutputDict["vsh_lc -c 'show plat int hal counters usdcounters'"])
                    if args.json is not None:
                        with open(args.json, "w") as f:
                            f.write(json.dumps(tmpOutput, indent = 4))
                        break
                    isToplevel = False
                    continue
                elif optionSelected == "q":
                    break
                else:
                    print("Invalid Selection")
                    time.sleep(1)
                    continue
            else:
                if isinstance(tmpOutput, dict):
                    for i, key in enumerate(tmpOutput.keys()):
                        print("Key [" + str(i) +"]: " + key)
                    try:
                        print("#################################################################")
                        optionSelected = raw_input("Please select a key you want to query:(CTRL+C to start over)\n")
                    except KeyboardInterrupt:
                        isToplevel = True
                        print()
                        print("###########Starting Over###########")
                        continue
                    try:
                        keySelected = tmpOutput.keys()[int(optionSelected)]
                        tmpOutput = tmpOutput[keySelected]
                        print("You have selected: " + keySelected)
                        print("#################################################################")
                    except(KeyError, ValueError, IndexError):
                        print("Invalid Selection, try again")
                        time.sleep(1)
                        continue
                else:
                    print("Result: " + tmpOutput)
                    time.sleep(2)
                    print("###########Starting Over###########")
                    isToplevel = True
    if args.raw_json:
        print(json.dumps(cmdOutputDict,indent=4))
        """
    if args.json:
        parsedDict = {}
        if  "vsh_lc -c 'show plat int counters port detail'" in cmdOutputDict:
                parsedDict["vsh_lc -c 'show plat int counters port detail'"] = show_plat_int_counters_port_detail(cmdOutputDict["vsh_lc -c 'show plat int counters port detail'"])
        if "vsh_lc -c 'show plat int ns counters mac asic 0 detail'" in cmdOutputDict:
            parsedDict["vsh_lc -c 'show plat int ns counters mac asic 0 detail'"] = show_plat_int_ns_counters_mac_asic_0_detail(cmdOutputDict["vsh_lc -c 'show plat int ns counters mac asic 0 detail'"])
        if "bcm-shell-hw 'ps'" in cmdOutputDict:
            parsedDict["bcm-shell-hw 'ps'"]=ps(cmdOutputDict["bcm-shell-hw 'ps'"])
        if "bcm-shell-hw 'show c all'" in cmdOutputDict:
            parsedDict["bcm-shell-hw 'show c all'"]=show_c_all(cmdOutputDict["bcm-shell-hw 'show c all'"])
        if "vsh_lc -c 'show plat int hal counters usdcounters'" in cmdOutputDict:
            parsedDict["vsh_lc -c 'show plat int hal counters usdcounters'"] = show_plat_int_hal_counters_usdcounters(cmdOutputDict["vsh_lc -c 'show plat int hal counters usdcounters'"])
        print(json.dumps(parsedDict,indent=4))        
        """

if args.list:
    for line in supportedCmd:
        print("CMD: " + line)



