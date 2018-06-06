import re


def show_plat_int_counters_port_detail_TAHOE(inputList):

    cmdContentLns = inputList
    finalOutputDict = {}
    intf = ""
    for line in cmdContentLns:

        """
            eth-1/3      3  Total        161684085  12713710177     152701847   12084235993
        """
        if "eth-" in line:
            intf = line.split()[0]
            totalInputPkts = line.split()[3]
            totalInputBytes = line.split()[4]
            totalOutputPkts = line.split()[5]
            totalOutputBytes = line.split()[6]
            finalOutputDict[intf] = {}
            finalOutputDict[intf]["totalInputPkts"] = totalInputPkts
            finalOutputDict[intf]["totalInputBytes"] = totalInputBytes
            finalOutputDict[intf]["totalOutputPkts"] = totalOutputPkts
            finalOutputDict[intf]["totalOutputBytes"] = totalOutputBytes

            """
                   Unicast   161629355  12710068651     152672573   12082365456
                   Multicast        0           0        29273      1873472
                   Flood            6         384            8          512
                Total Drops     54729                        5
                   Buffer           0                        0
                   Error            0                        5
                   Forward      54729
                   LB               0
                   AFD RED                                   0

            """

        elif "                   Unicast" in line:
            ucastInputPkts = line.split()[1]
            ucastInputBytes = line.split()[2]
            ucastOutputPkts = line.split()[3]
            ucastOutputBytes = line.split()[4]
            finalOutputDict[intf]["ucastInputPkts"] = ucastInputPkts
            finalOutputDict[intf]["ucastInputBytes"] = ucastInputBytes
            finalOutputDict[intf]["ucastOutputPkts"] = ucastOutputPkts
            finalOutputDict[intf]["ucastOutputBytes"] = ucastOutputBytes
        elif "                   Multicast" in line:
            mcastInputPkts = line.split()[1]
            mcastInputBytes = line.split()[2]
            mcastOutputPkts = line.split()[3]
            mcastOutputBytes = line.split()[4]
            finalOutputDict[intf]["mcastInputPkts"] = mcastInputPkts
            finalOutputDict[intf]["mcastInputBytes"] = mcastInputBytes
            finalOutputDict[intf]["mcastOutputPkts"] = mcastOutputPkts
            finalOutputDict[intf]["mcastOutputBytes"] = mcastOutputBytes

        elif "                   Flood" in line:
            floodInputPkts = line.split()[1]
            floodInputBytes = line.split()[2]
            floodOutputPkts = line.split()[3]
            floodOutputBytes = line.split()[4]
            finalOutputDict[intf]["floodInputPkts"] = floodInputPkts
            finalOutputDict[intf]["floodInputBytes"] = floodInputBytes
            finalOutputDict[intf]["floodOutputPkts"] = floodOutputPkts
            finalOutputDict[intf]["floodOutputBytes"] = floodOutputBytes

            """
                Total Drops     54729                        5
                   Buffer           0                        0
                   Error            0                        5
                   Forward      54729
                   LB               0
                   AFD RED                                   0           
            """
        elif "                Total Drop" in line:
            totalInputPktDrop = line.split()[1]
            totalOutputPktDrop = line.split()[2]
            finalOutputDict[intf]["totalInputPktDrop"] = totalInputPktDrop
            finalOutputDict[intf]["totalOutputPktDrop"] = totalOutputPktDrop
        elif "                   Buffer" in line:
            inputBufferDrop = line.split()[1]
            outputBufferDrop = line.split()[2]
            finalOutputDict[intf]["inputBufferDrop"] = inputBufferDrop
            finalOutputDict[intf]["outputBufferDrop"] = outputBufferDrop
        elif "                   Error" in line:
            inputErrorDrop = line.split()[1]
            outputErrorDrop = line.split()[2]
            finalOutputDict[intf]["inputErrorDrop"] = inputErrorDrop
            finalOutputDict[intf]["outputErrorDrop"] = outputErrorDrop
        elif "                   Forward" in line:
            inputForwardDrop = line.split()[1]
            finalOutputDict[intf]["inputForwardDrop"] = inputForwardDrop
        elif "                   LB" in line:
            inputLBDrop = line.split()[1]
            finalOutputDict[intf]["inputLBDrop"] = inputLBDrop
        elif "                   AFD RED" in line:
            outputAFREDDrop = line.split()[2]
            finalOutputDict[intf]["outputAFREDDrop"] = outputAFREDDrop
            """
                Class 0
                   Admit     161629361                 147283218
                   Drop        593531                        5
                Class 1
                   Admit            0                        0
                   Drop             0                        0
                Class 2
                   Admit            0                        0
                   Drop             0                        0


                     ########## Logic ########
                     - first hit Class x 
                     - set the dictionary key, cls, to the class name
                     - the next line must be one of two:
                        -Admit     161629361                 147283218
                        -Drop        593531                        5
                     - the logic is relying on the lines coming in sequential order
                     - debug might be needed if the input dictionary 
                       comes in wrong order.
                     #########################
            """
        elif "                Class" in line:
            cls = "class" + line.split()[1]
            finalOutputDict[intf][cls] = {}
        elif "Admit" in line:
            admitInput = line.split()[1]
            admitOutput = line.split()[2]
            finalOutputDict[intf][cls]["admitInput"] = admitInput
            finalOutputDict[intf][cls]["admitOutput"] = admitOutput
        elif "Drop" in line:
            dropInput = line.split()[1]
            dropOutput = line.split()[2]
            finalOutputDict[intf][cls]["dropInput"] = dropInput
            finalOutputDict[intf][cls]["dropOutput"] = dropOutput

            """
                Mac RMON
                 RX_PKTOK      161684085
                 RX_PKTTOTAL   161684085
                 RX_FCS_ERR           0
                 RX_ANY_ERR           0
                 RX_OCTETSOK   12713710177
                 RX_OCTETS     12713710177
                 RX_UCAST      161684078
                 RX_MCAST             0
                 RX_BCAST             7
                 RX_PAUSE             0
                 RX_INRANGEERR        0
                        <snip>
                 ############  Logic  ##############
                 - First match "Mac RMON"
                    - continue, jump to next line
                 - go through each subsequent lines
                    - first column goes to key
                    - second column goes to value
                 - Don't worry about when to stop as 
                   the interface name would be matched in 
                   the next section
                    - this again would rely on lines coming
                      in correct order
                    - additional debug might be required if otherwise      
            """
        elif "Mac RMON" in line:
            continue  # skip this line
        elif "RX_" in line or "TX_" in line:
            key = line.split()[0]
            value = line.split()[1]
            finalOutputDict[intf][key] = value
    return finalOutputDict


def show_plat_int_hal_counters_usdcounters(inputList):
    finalOutputDict = {}

    #################################################
    ##                                             ##
    ##               Segmentation                  ##
    ##                                             ##
    #################################################


    starsFound = 0
    perMacChannelSRMCnterList = []
    perSliceCnterList = []
    perSlicePerPortCnterList = []
    perSlicePerOpcodeCnterList = []
    perSliceIOCnterList = []
    nextLine = 0
    ######### populating perMacChannelSRMCnterList ########
    for i, line in enumerate(inputList):
        """
        extract lines between two
        *************** PER MAC/CH SRAM COUNTERS ****************  << starsFound = 1
        blah blah blah   <<< extract everthing between these two lines as per MAC/CH SRAM Counter
        *************** PER MAC/CH SRAM COUNTERS ****************  << starsFound = 2
        """


        if "*************** PER MAC/CH SRAM COUNTERS ****************" in line:
            starsFound +=1
            continue
        if starsFound == 1:
            if "GBL_C++" not in line:
                perMacChannelSRMCnterList.append(line)
        if starsFound == 2:
            nextLine += (i + 1)
            break


        """
        GBL_C++: 1520554482.248456 s :  [MSG] Printing both sug_0 slice based and per port counters for all slices <<< gotcha=True
        <snip>
        GBL_C++: 1520554482.439499 s :  [MSG]  TAH_MAC_API 2 tx rx 1 good cnt 1208000724total cnt 1208000724
        GBL_C++: 1520554482.439653 s :  [MSG]  TAH_MAC_API 4 tx rx 1 good cnt 0total cnt 0
        GBL_C++: 1520554482.439789 s :  [MSG]  TAH_MAC_API 6 tx rx 1 good cnt 3994566total cnt 3994566
        GBL_C++: 1520554482.439930 s :  [MSG] generic_reg_display: increased number width to 21 from 10
        REG_NAME                 0                    1    <<<< regNameFound = 1, start populating perSliceCnterList
        -------------------------------------------------------------------
        MAC_RX_TOTAL             270018147451         622027241582
        <snip....>
        RWX_IN                   807294876486         480435470850
        RWX_OUT                  747811177724         470192976906
        MAC_TX_TOTAL             373961718008         466707298173
        MAC_TX_GOOD              373961718007         466707298171
        <snip....>
        GBL_C++: 1520554482.441295 s :  [MSG] generic_reg_display: increased number width to 13 from 10
        REG_NAME                 0            1            2      .........  <<< regNameFound = 2, break
        ---------------------------------------------------------------------
        """

    ######### populating perSliceCnterList ########
    gotcha = False
    markFound = 0
    for i, line in enumerate(inputList[nextLine:]):
        if "GBL_C++" in line:
            if "Printing both sug_0 slice based and per port counters for all slice" in line:
                gotcha = True
            if markFound == 1:
                markFound +=1  # to mark the first GBL_C found after the real content
            else:
                continue # other GBL lines, skip
        if "REG_NAME" in line:
            markFound += 1
        if gotcha:
            if markFound == 1:
                perSliceCnterList.append(line)
            if markFound == 2:
                nextLine += i
                break

    ######### populating perSlicePerPortCnterList ########
    gotcha = False
    for i, line in enumerate(inputList[nextLine:]):
        if "PRINTING PER-PORT COUNTERS FOR SLICE" in line:
            gotcha = True
            perSlicePerPortCnterList.append(line)
        if "Printing per slice per opcode in out stats" in line:
            gotcha = False
            nextLine += i
            break
        if gotcha:
            if "GBL_C++" in line:
                continue
            else:
                perSlicePerPortCnterList.append(line)

    ######### populating perSlicePerOpcodeCnterList ########
    for i, line in enumerate(inputList[nextLine:]):
        if "Printing per slice per opcode in out stats" in line:
            gotcha = True
        if "Printing per slice in out stats" in line:
            gotcha = False
            nextLine += i
            break
        if gotcha:
            if "GBL_C++" in line:
                continue
            else:
                perSlicePerOpcodeCnterList.append(line)


    ######### populating perSlicePerIOCnterList ########
    perSliceIOCnterList = inputList[nextLine:]



    #################################################
    ##                                             ##
    ##                  Parsing                    ##
    ##                                             ##
    #################################################


    ######### parsing perMacChannelSRMCnter #########
    if len(perMacChannelSRMCnterList) != 0:
        finalOutputDict["per Mac Channel SRM Counters"] = {}
        mac = ""
        channel = ""

        for line in perMacChannelSRMCnterList:
            """
                REG_NAME                 M0,0-25G        M0,2-25G        M0,4-25G        M0,6-25G        M1,0-25G        M1,2-25G        M1,4-25G        M1,6-25G
                ---------------------------------------------------------------------------------------------------------------------------------------------------------
                00-RX Frm O.K            ....            ....            ....            ....            ....            ....            ....            ....
                01-RX Frm All(Good/Bad)  ....            ....            ....            ....            ....            ....            ....            ....
                02-RX Frm with FCS Err   ....            ....            ....            ....            ....            ....            ....            ....
                03-RX Frm with any Err   ....            ....            ....            ....            ....            ....            ....            ....
                04-RX Oct in Good Frm    ....            ....            ....            ....            ....            ....            ....            ....
                05-RX Oct(Good/Bad Frm)  ....            ....            ....            ....            ....            ....            ....            ....
                06-RX Frm with UC Addr   ....            ....            ....            ....            ....            ....            ....            ....
                07-RX Frm with MC Addr   ....            ....            ....            ....            ....            ....            ....            ....
                08-RX Frm with BC Addr   ....            ....            ....            ....            ....            ....            ....            ....
                09-RX Frm of type PAUSE  ....            ....            ....            ....            ....            ....            ....            ....
                10-RX Frm with Len Err   ....            ....            ....            ....            ....            ....            ....            ....
                11-RX Frm Undersz(No Err)....            ....            ....            ....            ....            ....            ....            ....
                12-RX Frm Oversz(No Err) ....            ....            ....            ....            ....            ....            ....            ....
                13-RX Fragments          ....            ....            ....            ....            ....            ....            ....            ....
                14-RX Jabber             ....            ....            ....            ....            ....            ....            ....            ....
    
            """

            if "REG_NAME" in line:  # REG_NAME                 M0,0-25G        M0,2-25G        M0,4-25G        M0,6-25G        M1,0-25G        M1,2-25G        M1,4-25G        M1,6-25G
                mac_channel_list = []
                for header in line.split():
                    if header == "REG_NAME":
                        continue
                    else:
                        mac = "mac" + header.split(",")[0].replace("M", "")
                        if mac not in finalOutputDict["per Mac Channel SRM Counters"]:
                            finalOutputDict["per Mac Channel SRM Counters"][mac] = {}

                        channel = "channel" + header.split(",")[1].split("-")[0]
                        if channel not in finalOutputDict["per Mac Channel SRM Counters"][mac]:
                            finalOutputDict["per Mac Channel SRM Counters"][mac][channel] = {}

                        mac_channel_list.append([mac, channel])

                        speed = header.split(",")[1].split("-")[1]
                        finalOutputDict["per Mac Channel SRM Counters"][mac][channel]["speed"] = speed
            elif re.match("^[0-9][0-9]\-", line):
                counter = line[0:25].strip().split("-")[1]
                rest_of_the_line = line[26:len(line)]
                for i, item in enumerate(rest_of_the_line.split()):
                    mac = mac_channel_list[i][0]
                    channel = mac_channel_list[i][1]
                    if ".." in item:
                        finalOutputDict["per Mac Channel SRM Counters"][mac][channel][counter] = "0"
                    else:
                        finalOutputDict["per Mac Channel SRM Counters"][mac][channel][counter] = item

    ######### parsing perSliceCnter #########
    if len(perSliceCnterList) != 0:
        finalOutputDict["per Slice Counters"] = {}
        """
            REG_NAME                 0                    1
            -------------------------------------------------------------------
            MAC_RX_TOTAL             859991975042         1168691105875
            MAC_RX_GOOD              859991974987         1168691105850
            PRX_IN                   154120896568         137955281103
            PRX_OUT                  154120896636         137955281109
            PRX_IN_BAD               ....                 ....
            FPX_IN                   3797045009           516328447
            FPX_OUT                  3797045038           516328453
            LU_PBX_IN                18446744073211629434 516328466
            PRX_PBX_IN               18446744073211629418 516328465
            PBX_OUT                  18446744073211629444 516328466
            LBX_IN                   1322352005029        1168747434318
            LBX_OUT                  1322352005029        1168747434318
            BAX_IN                   1395144979498        1230319729101
            BMX_ADMITTED             6                    6
            BMX_RWA                  1                    1
            RWX_IN                   943776952784         1676165296255
            RWX_OUT                  907932090208         1663878190130
            MAC_TX_TOTAL             541888348192         1540452519210
            MAC_TX_GOOD              541888348163         1540452519204
            
            
        """
        for line in perSliceCnterList:
            if "REG_NAME" in line:
                for i, item in enumerate(line.split()):
                    if i != 0:
                        slice = "slice"+ line.split()[i]
                        finalOutputDict["per Slice Counters"][slice] = {}
                continue
            if "_" in line:
                key = line.split()[0]
                for i, item in enumerate(line.split()):
                    if i !=0:
                        finalOutputDict["per Slice Counters"]["slice"+str(i-1)][key]=item

    ######### parsing perSlicePerPortCnter #########
        """
            GBL_C++: 1520554482.440091 s :  [MSG] PRINTING PER-PORT COUNTERS FOR SLICE :0   <<<< slice = slice0
            
            REG_NAME                 0  <<port0   1            2            3            4            5            6            7            8            9            10           11
            -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            SLICE0_MAC_RX_TOTAL      ....         ....         ....         ....         ....         ....         ....         ....         ....         ....         ....         ....
            SLICE0_MAC_RX_GOOD       ....         ....         ....         ....         ....         ....         ....         ....         ....         ....         ....         ....
            SLICE0_PRX_IN            ....         ....         ....         ....         ....         ....         ....         ....         ....         ....         ....         ....
            SLICE0_PRX_OUT           ....         ....         ....         ....         ....         ....         ....         ....         ....         ....         ....         ....
            SLICE0_BMX_OUT           1            1            1            1            1            1            1            1            1            1            1            1
            <snip>        
                    
            GBL_C++: 1520554482.442608 s :  [MSG] PRINTING PER-PORT COUNTERS FOR SLICE :1   <<<<< slice = slice1
            
            REG_NAME                 0            1            2            3            4            5            6            7            8            9            10           11
            -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            SLICE1_MAC_RX_TOTAL      326233346251 ....         ....         ....         ....         ....         ....         ....         ....         ....         ....         ....
            SLICE1_MAC_RX_GOOD       326233346251 ....         ....         ....         ....         ....         ....         ....         ....         ....         ....         ....
            <snip>
        """


    ######## parsing perSlicePerPortCnterList ########
    if len(perSlicePerPortCnterList) != 0:
        finalOutputDict["per Slice per Port Counters"] = {}
        slice = ""
        tmpPortList = []
        for line in perSlicePerPortCnterList:
            if "GBL_C++:" in line:    # expect to find slice# from this line
                sliceFoundRe = re.search('SLICE :([0-9]+)' , line)
                if sliceFoundRe:
                    slice = "slice" + str(sliceFoundRe.group(1))
                    finalOutputDict["per Slice per Port Counters"][slice] = {}
                else:
                    continue  # if slice is not found in this line, go to next line
                              # it should not happen, but just in case
            elif "REG_NAME" in line:
                tmpPortList = []
                for i, item in enumerate(line.split()):
                    if i != 0:
                        port = "port"+ line.split()[i]
                        tmpPortList.append(port)
                        finalOutputDict["per Slice per Port Counters"][slice][port] = {}
            elif re.search('^SLICE[0-9]+',line):
                key = line.split()[0]
                for i, item in  enumerate(line.split()):
                    if i !=0:
                        if ".." not in item:
                            finalOutputDict["per Slice per Port Counters"][slice][tmpPortList[i-1]][key] = item
                        else:
                            finalOutputDict["per Slice per Port Counters"][slice][tmpPortList[i-1]][key] = "0"



    ######### parsing perSlicePerOpcodeCnterList #########
    if len(perSlicePerOpcodeCnterList) != 0:
        """
        REG_NAME                            UC           L2MC         L3MC         RCPU         LCPU         SRVC         SPAN
        -------------------------------------------------------------------------------------------------------------------------------
        IN_SLICE0                           82363638114  ....         74676082002  ....         1905509770   ....         93001584858
        IN_SLICE1                           610589239416 ....         10315746454  ....         1428240247   ....         29775015387
        IN_RENQ                             ....         ....         ....         ....         ....         ....         18159215350
        OUT_SLICE0                          82363638198  ....         74676082016  ....         1905509767   ....         93001584866
        OUT_SLICE1                          610589239506 ....         10315746455  ....         1428240188   ....         29775015391
        OUT_RENQ                            ....         ....         ....         ....         ....         ....         18159215350
        IN_TOT                              692952877530 ....         84991828456  ....         3333750017   ....         140935815595
        OUT_TOT                             692952877704 ....         84991828471  ....         3333749955   ....         140935815607
        
        
        """
        finalOutputDict["per Slice Per Opcode Counters"] = {}
        opcodeList = []
        for line in perSlicePerOpcodeCnterList:

            if "REG_NAME" in line:
                for i, item in enumerate(line.split()):
                    if i != 0:
                        opcodeList.append(item)
            elif "_" in line:
                key = line.split()[0]
                finalOutputDict["per Slice Per Opcode Counters"][key] = {}
                for i, item in  enumerate(line.split()):
                    if i !=0:
                        if ".." not in item:
                            finalOutputDict["per Slice Per Opcode Counters"][key][opcodeList[i-1]] = item
                        else:
                            finalOutputDict["per Slice Per Opcode Counters"][key][opcodeList[i-1]]  = "0"


    ######### parsing perSliceIOCnterList #########
        """
            GBL_C++: 1520554482.447474 s :  [MSG]            Printing per slice in out stats
            GBL_C++: 1520554482.447537 s :  [MSG]            -------------------------------
            GBL_C++: 1520554482.447630 s :  [MSG] generic_reg_display: increased number width to 21 from 10
            REG_NAME                            IN_PKTS              OUT_PKTS             DROP_PKTS
            ---------------------------------------------------------------------------------------------------
            SLICE0                              175178259295         175178259301         18446744073709551610
            SLICE1                              622114073430         622114073457         18446744073709551589
            RENQ                                18159215350          18159215350          ....
            TOT                                 815451548075         815451548108         18446744073709551583
            
            GBL_C++: 1520554482.447748 s :  [MSG]    Total pkts received post opcode pruning = 797292332853
        
        """

    ######## parsing perSliceIOCnterList #########

        """
            GBL_C++: 1520554482.447474 s :  [MSG]            Printing per slice in out stats
            GBL_C++: 1520554482.447537 s :  [MSG]            -------------------------------
            GBL_C++: 1520554482.447630 s :  [MSG] generic_reg_display: increased number width to 21 from 10
            REG_NAME                            IN_PKTS              OUT_PKTS             DROP_PKTS
            ---------------------------------------------------------------------------------------------------
            SLICE0                              175178259295         175178259301         18446744073709551610
            SLICE1                              622114073430         622114073457         18446744073709551589
            RENQ                                18159215350          18159215350          ....
            TOT                                 815451548075         815451548108         18446744073709551583
            
            GBL_C++: 1520554482.447748 s :  [MSG]    Total pkts received post opcode pruning = 797292332853
        """

    if len(perSliceIOCnterList) != 0:
        finalOutputDict["per Slice IO Counters"] = {}
        counterTypes = []
        for line in perSliceIOCnterList:
            if "REG_NAME" in line:
                for i, item in enumerate(line.split()):
                    if i != 1:
                        counterTypes.append(item)
            if re.search('^(SLICE[0-9]+|RENQ|TOT)+\s+([0-9]+|\.\.\.\.)', line ):
                key = line.split()[0]
                finalOutputDict["per Slice IO Counters"][key] = {}
                for i, ct in enumerate(counterTypes):
                    value = line.split()[i+1]
                    if value == "....":
                        value = "0"
                    finalOutputDict["per Slice IO Counters"][key][ct] = value
            if "Total pkts received post opcode pruning" in line:
                valueFound = re.search('=\s*([0-9]+)',line)
                if valueFound :
                    finalOutputDict["per Slice IO Counters"]["Total pkts received post opcode pruning"] = valueFound.group(1)
                else:
                    finalOutputDict["per Slice IO Counters"]["Total pkts received post opcode pruning"] = "N/A"

    return finalOutputDict