def ps(inputDict):
    cmdContentLns = inputDict
    finalOutputDict = {}
    port = ""
    unit = ""
    for line in cmdContentLns:
        """
        unit is 0
        """

        if "unit is" in line:
            unit = 'unit'+line.split()[2]
            finalOutputDict[unit] = {}
        if "xe" in line or "hg" in line:
            lineBrkDwn = line.split()
            port = lineBrkDwn[0]
            finalOutputDict[unit][port] = {}
            ena_link = lineBrkDwn[1]
            speed = lineBrkDwn[2]
            dplx = lineBrkDwn[3]
            link_scan = lineBrkDwn[4]
            auto_nego_q = lineBrkDwn[5]
            stp_state = lineBrkDwn[6]
            """
               xe0  up     40G  FD   HW  No   Forward          None   FA  XGMII  9022
                ^                                ^               ^                ^
                #0                               #6             #7               #10  <<we use this to check how 
                                                                                        many fields were skipped/added
               xe1  !ena    1G  FD   HW  Yes  Disable  TX RX   None   FA   GMII  9022
                ^                                ^               ^                ^
                #0                               #6             #9               #12               
               xe2  !ena    1G  FD   HW  Yes  Disable  TX      None   FA   GMII  9022
                ^                                ^               ^                ^
                #0                               #6             #8               #11                  
            """
            pause = ""
            nextKey = 0
            if unicode(lineBrkDwn[10], 'utf-8').isnumeric():  #pause field skipped
                nextKey = 7
                pass
            elif unicode(lineBrkDwn[11], 'utf-8').isnumeric(): #one pause filed
                pause = lineBrkDwn[7]
                nextKey = 8
            elif unicode(lineBrkDwn[12], 'utf-8').isnumeric(): #two pause fields
                pause = lineBrkDwn[7]+"|"+lineBrkDwn[8]
                nextKey = 9
            discard = lineBrkDwn[nextKey]
            nextKey+=1
            lrn_ops = lineBrkDwn[nextKey]
            nextKey += 1
            interface = lineBrkDwn[nextKey]
            nextKey += 1
            max_frame = lineBrkDwn[nextKey]
            nextKey += 1
            loopback = ""
            try:
                loopback = lineBrkDwn[nextKey]
            except IndexError:
                pass
            if unit != "":

                finalOutputDict[unit][port]["ena_link"] = ena_link
                finalOutputDict[unit][port]["speed"] = speed
                finalOutputDict[unit][port]["dplx"] = dplx
                finalOutputDict[unit][port]["link_scan"] = link_scan
                finalOutputDict[unit][port]["auto_nego_q"] = auto_nego_q
                finalOutputDict[unit][port]["stp_state"] = stp_state
                finalOutputDict[unit][port]["pause"] = pause
                finalOutputDict[unit][port]["discard"] = discard
                finalOutputDict[unit][port]["lrn_ops"] = lrn_ops
                finalOutputDict[unit][port]["interface"] = interface
                finalOutputDict[unit][port]["max_frame"] = max_frame
                finalOutputDict[unit][port]["loopback"] = loopback
    return finalOutputDict
def show_c_all(inputDict):
    cmdContentLns = inputDict
    finalOutputDict = {}
    unit = ""
    for line in cmdContentLns:
        """
        unit is 0
        """

        if "unit is" in line:
            unit = 'unit'+line.split()[2]
            finalOutputDict[unit] = {}
        elif ":" in line:
            """
                RIPD4.cpu0                  :                     0                  +0
                RIPC4.cpu0                  :           306,211,942          +4,146,780              24/s
                RIPHE4.cpu0                 :                     0                  +0
                IMRP4.cpu0                  :                     0                  +0
                RIPD6.cpu0                  :                     0                  +0
                <snip>
                RQ_DROP_BYTE(0)             :                     0                  +0
                RQ_DROP_BYTE(1)             :                     0                  +0
                RQ_DROP_BYTE(2)             :                     0                  +0
                RQ_DROP_BYTE(3)             :                     0                  +0
            """

            cntrName = line.split(":")[0].replace("\t","").strip()
            pkts = line.split(":")[1].split()[0].strip()
            deltaPkt = line.split(":")[1].split()[1].strip()
            try:
                rate = line.split(":")[1].split()[2].strip()
            except IndexError:
                rate = ""
            if "." in cntrName:
                finalOutputDict[unit]
                port = cntrName.split(".")[1].strip()
                cntr = cntrName.split(".")[0].replace("\t","").strip()
                if port not in finalOutputDict[unit]:
                    finalOutputDict[unit][port] = {}
                finalOutputDict[unit][port][cntr] = {}
                finalOutputDict[unit][port][cntr]['pkts'] = pkts
                finalOutputDict[unit][port][cntr]['deltaPkt'] = deltaPkt
                finalOutputDict[unit][port][cntr]['rate'] = rate
            else:
                finalOutputDict[unit][cntrName] = {}
                finalOutputDict[unit][cntrName]['pkts'] = pkts
                finalOutputDict[unit][cntrName]['deltaPkt'] = deltaPkt
                finalOutputDict[unit][port][cntr]['rate'] = rate
    return finalOutputDict