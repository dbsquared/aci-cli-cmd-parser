def show_plat_int_counters_port_detail(inputDict):
    cmdContentLns = inputDict
    finalOutputDict = {}
    intf = ""
    for line in cmdContentLns:

        """
        eth-1/1      1  Total        273894506945  187360931345619     184382270490   147644168627361
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
                       Unicast   273892613590  187360026471121     163545304291   146101883979759
                       Multicast   341970    21886080            0            0
                       Flood            0           0
                       UnknownUC        0           0
                       Unclass     325889   128684088
                    Total Drops       135                        0
                    Storm Drops(Bytes)         0       
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
            finalOutputDict[intf]["floodInputPkts"] = floodInputPkts
            finalOutputDict[intf]["floodInputBytes"] = floodInputBytes
        elif "                   UnknownUC" in line:
            uucInputPkts = line.split()[1]
            uucInputBytes = line.split()[2]
            finalOutputDict[intf]["uucInputPkts"] = uucInputPkts
            finalOutputDict[intf]["uucInputBytes"] = uucInputBytes
        elif "                   Unclass" in line:
            unclassInputPkts = line.split()[1]
            unclassInputBytes = line.split()[2]
            finalOutputDict[intf]["unclassInputPkts"] = unclassInputPkts
            finalOutputDict[intf]["unclassInputBytes"] = unclassInputBytes
        elif "                Total Drop" in line:
            totalInputPktDrop = line.split()[1]
            totalOutputPktDrop = line.split()[2]
            finalOutputDict[intf]["totalInputPktDrop"] = totalInputPktDrop
            finalOutputDict[intf]["totalOutputPktDrop"] = totalOutputPktDrop
        elif "                Storm Drops(Bytes)" in line:
            stormDropBytes = line.split()[1]
            finalOutputDict[intf]["stormDropBytes"] = stormDropBytes

            """
                               PERQ Stats
                    Class 0
                     UC NO OOBFC                      162778271008   145844180563273
                     UC OOBFC                             2110     221548
                     MC                                      0          0
                    Class 1
                     UC NO OOBFC                             0          0
                     UC OOBFC                                0          0
                     MC                                      0          0
                    Class 2
                     UC NO OOBFC                             0          0
                     UC OOBFC                                0          0
                     MC                                      0          0
                    Class 3
                     UC NO OOBFC                           473      86848
                     UC OOBFC                                0          0
                     MC                                      0          0
                    Class SPAN
                     UC                                      0          0
                     MC                                      0          0
                    Class SUP
                     UC                               21603234719   1799562823493
                     MC                                      0          0
                    Class 0 Drops
                     UC NO OOBFC                             0          0
                     UC OOBFC                                0          0
                     MC                                      0          0
                    Class 1 Drops
                     UC NO OOBFC                             0          0
                     UC OOBFC                                0          0
                     MC                                      0          0
                    Class 2 Drops
                     UC NO OOBFC                             0          0
                     UC OOBFC                                0          0
                     MC                                      0          0
                    Class 3 Drops
                     UC NO OOBFC                             0          0
                     UC OOBFC                                0          0
                     MC                                      0          0
                    Class SPAN Drops
                     UC                                      0          0
                     MC                                      0          0
                    Class SUP Drops
                     UC                                     31       3168
                     MC                                      0          0

                     
                     ########## Logic ########
                     - first hit Class x <Drops>
                     - set the dictionary key, cls, to the class name
                     - the next line must be one of these:
                        - UC NO OOBFC
                        - UC OOBFC
                        - MC
                        - UC
                     - the logic is relying on the lines coming in sequential order
                     - debug might be needed if the input dictionary 
                       comes in wrong order.
                     #########################
            """
        elif line == "                    Class 0":
            cls = "class0"
            finalOutputDict[intf][cls] = {}
        elif line == "                    Class 1":
            cls = "class1"
            finalOutputDict[intf][cls] = {}
        elif line == "                    Class 2":
            cls = "class2"
            finalOutputDict[intf][cls] = {}
        elif line == "                    Class 3":
            cls = "class3"
            finalOutputDict[intf][cls] = {}
        elif line == "                    Class SPAN":
            cls = "classSpan"
            finalOutputDict[intf][cls] = {}
        elif line == "                    Class SUP":
            cls = "classSUP"
            finalOutputDict[intf][cls] = {}
        elif line == "                    Class 0 Drops":
            cls = "class0Drop"
            finalOutputDict[intf][cls] = {}
        elif line == "                    Class 1 Drops":
            cls = "class1Drops"
            finalOutputDict[intf][cls] = {}
        elif line == "                    Class 2 Drops":
            cls = "class2Drops"
            finalOutputDict[intf][cls] = {}
        elif line == "                    Class 3 Drops":
            cls = "class3Drops"
            finalOutputDict[intf][cls] = {}
        elif line == "                    Class SPAN Drops":
            cls = "classSpanDrops"
            finalOutputDict[intf][cls] = {}
        elif line == "                    Class SUP Drops":
            cls = "classSUPDrops"
            finalOutputDict[intf][cls] = {}
        elif "                     UC NO OOBFC" in line:  #re-used in class0-3<Drop>/UC NO OOBFC
            ucNoOobfcPkts = line.split()[3]
            ucNoOobfcBytes = line.split()[4]
            finalOutputDict[intf][cls]["ucNoOobfcPkts"] = ucNoOobfcPkts
            finalOutputDict[intf][cls]["ucNoOobfcBytes"] = ucNoOobfcBytes
        elif "                     UC OOBFC" in line:     #re-used in class0-3<Drop>/UC OOBFC
            ucOobfcPkts = line.split()[2]
            ucOobfcBytes = line.split()[3]
            finalOutputDict[intf][cls]["ucOobfcPkts"] = ucOobfcPkts
            finalOutputDict[intf][cls]["ucOobfcBytes"] = ucOobfcBytes
        elif "                     MC" in line:         #re-used in class0-3,SPAN,SUP<Drop>/MC
            mcPkts = line.split()[1]
            mcBytes = line.split()[2]
            finalOutputDict[intf][cls]["ucOobfcPkts"] = ucOobfcPkts
            finalOutputDict[intf][cls]["ucOobfcBytes"] = ucOobfcBytes
        elif "                     UC          " in line:   #additional space appended to differentiate from "UC NO OOBFC"
            ucPkts = line.split()[1]                        #only used in classSUP,SPAN<Drop>/UC
            ucBytes = line.split()[2]
            finalOutputDict[intf][cls]["ucPkts"] = ucPkts
            finalOutputDict[intf][cls]["ucBytes"] = ucBytes

            """
                       Mac RMON
                        snmpIfInOctets                         187360931345619
                        snmpIfInUcastPkts                      273893839201
                        snmpIfInNUcastPkts                       667744
                        snmpIfInDiscards                            135
                        snmpIfInErrors                                0
                        snmpIfInUnknownProtos                         0
                        snmpIfOutOctets                        147644168627361
                        snmpIfOutUcastPkts                     184357201243
                        snmpIfOutNUcastPkts                    25069247
                        snmpIfOutDiscards                             0
                        snmpIfOutErrors                               0
                        snmpIfOutQLen                                 0
                        snmpIpInReceives                              0
                        snmpIpInHdrErrors                             0
                        snmpIpForwDatagrams                    163546051724
                        <snip>
            """
        elif "snmpIfInOctets" in line:
            snmpIfInOctets = line.split()[1]
            finalOutputDict[intf]["snmpIfInOctets"] = snmpIfInOctets
        elif "snmpIfInUcastPkts" in line:
            snmpIfInUcastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIfInUcastPkts"] = snmpIfInUcastPkts
        elif "snmpIfInNUcastPkts" in line:
            snmpIfInNUcastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIfInNUcastPkts"] = snmpIfInNUcastPkts
        elif "snmpIfInDiscards" in line:
            snmpIfInDiscards = line.split()[1]
            finalOutputDict[intf]["snmpIfInDiscards"] = snmpIfInDiscards
        elif "snmpIfInErrors" in line:
            snmpIfInErrors = line.split()[1]
            finalOutputDict[intf]["snmpIfInErrors"] = snmpIfInErrors
        elif "snmpIfInUnknownProtos" in line:
            snmpIfInUnknownProtos = line.split()[1]
            finalOutputDict[intf]["snmpIfInUnknownProtos"] = snmpIfInUnknownProtos
        elif "snmpIfOutOctets" in line:
            snmpIfOutOctets = line.split()[1]
            finalOutputDict[intf]["snmpIfOutOctets"] = snmpIfOutOctets
        elif "snmpIfOutUcastPkts" in line:
            snmpIfOutUcastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIfOutUcastPkts"] = snmpIfOutUcastPkts
        elif "snmpIfOutNUcastPkts" in line:
            snmpIfOutNUcastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIfOutNUcastPkts"] = snmpIfOutNUcastPkts
        elif "snmpIfOutDiscards" in line:
            snmpIfOutDiscards = line.split()[1]
            finalOutputDict[intf]["snmpIfOutDiscards"] = snmpIfOutDiscards
        elif "snmpIfOutErrors" in line:
            snmpIfOutErrors = line.split()[1]
            finalOutputDict[intf]["snmpIfOutErrors"] = snmpIfOutErrors
        elif "snmpIfOutQLen" in line:
            snmpIfOutQLen = line.split()[1]
            finalOutputDict[intf]["snmpIfOutQLen"] = snmpIfOutQLen
        elif "snmpIpInReceives" in line:
            snmpIpInReceives = line.split()[1]
            finalOutputDict[intf]["snmpIpInReceives"] = snmpIpInReceives
        elif "snmpIpInHdrErrors" in line:
            snmpIpInHdrErrors = line.split()[1]
            finalOutputDict[intf]["snmpIpInHdrErrors"] = snmpIpInHdrErrors
        elif "snmpIpForwDatagrams" in line:
            snmpIpForwDatagrams = line.split()[1]
            finalOutputDict[intf]["snmpIpForwDatagrams"] = snmpIpForwDatagrams
        elif "snmpIpInDiscards" in line:
            snmpIpInDiscards = line.split()[1]
            finalOutputDict[intf]["snmpIpInDiscards"] = snmpIpInDiscards
        elif "snmpDot1dBasePortDelayExceededDiscards" in line:
            snmpDot1dBasePortDelayExceededDiscards = line.split()[1]
            finalOutputDict[intf]["snmpDot1dBasePortDelayExceededDiscards"] = snmpDot1dBasePortDelayExceededDiscards
        elif "snmpDot1dBasePortMtuExceededDiscards" in line:
            snmpDot1dBasePortMtuExceededDiscards = line.split()[1]
            finalOutputDict[intf]["snmpDot1dBasePortMtuExceededDiscards"] = snmpDot1dBasePortMtuExceededDiscards
        elif "snmpDot1dTpPortInFrames" in line:
            snmpDot1dTpPortInFrames = line.split()[1]
            finalOutputDict[intf]["snmpDot1dTpPortInFrames"] = snmpDot1dTpPortInFrames
        elif "snmpDot1dTpPortOutFrames" in line:
            snmpDot1dTpPortOutFrames = line.split()[1]
            finalOutputDict[intf]["snmpDot1dTpPortOutFrames"] = snmpDot1dTpPortOutFrames
        elif "snmpDot1dPortInDiscards" in line:
            snmpDot1dPortInDiscards = line.split()[1]
            finalOutputDict[intf]["snmpDot1dPortInDiscards"] = snmpDot1dPortInDiscards
        elif "snmpEtherStatsDropEvents" in line:
            snmpEtherStatsDropEvents = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsDropEvents"] = snmpEtherStatsDropEvents
        elif "snmpEtherStatsMulticastPkts" in line:
            snmpEtherStatsMulticastPkts = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsMulticastPkts"] = snmpEtherStatsMulticastPkts
        elif "snmpEtherStatsBroadcastPkts" in line:
            snmpEtherStatsBroadcastPkts = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsBroadcastPkts"] = snmpEtherStatsBroadcastPkts
        elif "snmpEtherStatsUndersizePkts" in line:
            snmpEtherStatsUndersizePkts = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsUndersizePkts"] = snmpEtherStatsUndersizePkts
        elif "snmpEtherStatsFragments" in line:
            snmpEtherStatsFragments = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsFragments"] = snmpEtherStatsFragments
        elif "snmpEtherStatsPkts64Octets" in line:
            snmpEtherStatsPkts64Octets = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsPkts64Octets"] = snmpEtherStatsPkts64Octets
        elif "snmpEtherStatsPkts65to127Octets" in line:
            snmpEtherStatsPkts65to127Octets = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsPkts65to127Octets"] = snmpEtherStatsPkts65to127Octets
        elif "snmpEtherStatsPkts128to255Octets" in line:
            snmpEtherStatsPkts128to255Octets = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsPkts128to255Octets"] = snmpEtherStatsPkts128to255Octets
        elif "snmpEtherStatsPkts256to511Octets" in line:
            snmpEtherStatsPkts256to511Octets = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsPkts256to511Octets"] = snmpEtherStatsPkts256to511Octets
        elif "snmpEtherStatsPkts512to1023Octets" in line:
            snmpEtherStatsPkts512to1023Octets = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsPkts512to1023Octets"] = snmpEtherStatsPkts512to1023Octets
        elif "snmpEtherStatsPkts1024to1518Octets" in line:
            snmpEtherStatsPkts1024to1518Octets = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsPkts1024to1518Octets"] = snmpEtherStatsPkts1024to1518Octets
        elif "snmpEtherStatsOversizePkts" in line:
            snmpEtherStatsOversizePkts = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsOversizePkts"] = snmpEtherStatsOversizePkts
        elif "snmpEtherRxOversizePkts" in line:
            snmpEtherRxOversizePkts = line.split()[1]
            finalOutputDict[intf]["snmpEtherRxOversizePkts"] = snmpEtherRxOversizePkts
        elif "snmpEtherTxOversizePkts" in line:
            snmpEtherTxOversizePkts = line.split()[1]
            finalOutputDict[intf]["snmpEtherTxOversizePkts"] = snmpEtherTxOversizePkts
        elif "snmpEtherStatsJabbers" in line:
            snmpEtherStatsJabbers = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsJabbers"] = snmpEtherStatsJabbers
        elif "snmpEtherStatsOctets" in line:
            snmpEtherStatsOctets = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsOctets"] = snmpEtherStatsOctets
        elif "snmpEtherStatsPkts" in line:
            snmpEtherStatsPkts = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsPkts"] = snmpEtherStatsPkts
        elif "snmpEtherStatsCollisions" in line:
            snmpEtherStatsCollisions = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsCollisions"] = snmpEtherStatsCollisions
        elif "snmpEtherStatsCRCAlignErrors" in line:
            snmpEtherStatsCRCAlignErrors = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsCRCAlignErrors"] = snmpEtherStatsCRCAlignErrors
        elif "snmpEtherStatsTXNoErrors" in line:
            snmpEtherStatsTXNoErrors = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsTXNoErrors"] = snmpEtherStatsTXNoErrors
        elif "snmpEtherStatsRXNoErrors" in line:
            snmpEtherStatsRXNoErrors = line.split()[1]
            finalOutputDict[intf]["snmpEtherStatsRXNoErrors"] = snmpEtherStatsRXNoErrors
        elif "snmpDot3StatsAlignmentErrors" in line:
            snmpDot3StatsAlignmentErrors = line.split()[1]
            finalOutputDict[intf]["snmpDot3StatsAlignmentErrors"] = snmpDot3StatsAlignmentErrors
        elif "snmpDot3StatsFCSErrors" in line:
            snmpDot3StatsFCSErrors = line.split()[1]
            finalOutputDict[intf]["snmpDot3StatsFCSErrors"] = snmpDot3StatsFCSErrors
        elif "snmpDot3StatsSingleCollisionFrames" in line:
            snmpDot3StatsSingleCollisionFrames = line.split()[1]
            finalOutputDict[intf]["snmpDot3StatsSingleCollisionFrames"] = snmpDot3StatsSingleCollisionFrames
        elif "snmpDot3StatsMultipleCollisionFrames" in line:
            snmpDot3StatsMultipleCollisionFrames = line.split()[1]
            finalOutputDict[intf]["snmpDot3StatsMultipleCollisionFrames"] = snmpDot3StatsMultipleCollisionFrames
        elif "snmpDot3StatsSQETTestErrors" in line:
            snmpDot3StatsSQETTestErrors = line.split()[1]
            finalOutputDict[intf]["snmpDot3StatsSQETTestErrors"] = snmpDot3StatsSQETTestErrors
        elif "snmpDot3StatsDeferredTransmissions" in line:
            snmpDot3StatsDeferredTransmissions = line.split()[1]
            finalOutputDict[intf]["snmpDot3StatsDeferredTransmissions"] = snmpDot3StatsDeferredTransmissions
        elif "snmpDot3StatsLateCollisions" in line:
            snmpDot3StatsLateCollisions = line.split()[1]
            finalOutputDict[intf]["snmpDot3StatsLateCollisions"] = snmpDot3StatsLateCollisions
        elif "snmpDot3StatsExcessiveCollisions" in line:
            snmpDot3StatsExcessiveCollisions = line.split()[1]
            finalOutputDict[intf]["snmpDot3StatsExcessiveCollisions"] = snmpDot3StatsExcessiveCollisions
        elif "snmpDot3StatsInternalMacTransmitErrors" in line:
            snmpDot3StatsInternalMacTransmitErrors = line.split()[1]
            finalOutputDict[intf]["snmpDot3StatsInternalMacTransmitErrors"] = snmpDot3StatsInternalMacTransmitErrors
        elif "snmpDot3StatsCarrierSenseErrors" in line:
            snmpDot3StatsCarrierSenseErrors = line.split()[1]
            finalOutputDict[intf]["snmpDot3StatsCarrierSenseErrors"] = snmpDot3StatsCarrierSenseErrors
        elif "snmpDot3StatsFrameTooLongs" in line:
            snmpDot3StatsFrameTooLongs = line.split()[1]
            finalOutputDict[intf]["snmpDot3StatsFrameTooLongs"] = snmpDot3StatsFrameTooLongs
        elif "snmpDot3StatsInternalMacReceiveErrors" in line:
            snmpDot3StatsInternalMacReceiveErrors = line.split()[1]
            finalOutputDict[intf]["snmpDot3StatsInternalMacReceiveErrors"] = snmpDot3StatsInternalMacReceiveErrors
        elif "snmpDot3StatsSymbolErrors" in line:
            snmpDot3StatsSymbolErrors = line.split()[1]
            finalOutputDict[intf]["snmpDot3StatsSymbolErrors"] = snmpDot3StatsSymbolErrors
        elif "snmpDot3ControlInUnknownOpcodes" in line:
            snmpDot3ControlInUnknownOpcodes = line.split()[1]
            finalOutputDict[intf]["snmpDot3ControlInUnknownOpcodes"] = snmpDot3ControlInUnknownOpcodes
        elif "snmpDot3InPauseFrames" in line:
            snmpDot3InPauseFrames = line.split()[1]
            finalOutputDict[intf]["snmpDot3InPauseFrames"] = snmpDot3InPauseFrames
        elif "snmpDot3OutPauseFrames" in line:
            snmpDot3OutPauseFrames = line.split()[1]
            finalOutputDict[intf]["snmpDot3OutPauseFrames"] = snmpDot3OutPauseFrames
        elif "snmpIfHCInOctets" in line:
            snmpIfHCInOctets = line.split()[1]
            finalOutputDict[intf]["snmpIfHCInOctets"] = snmpIfHCInOctets
        elif "snmpIfHCInUcastPkts" in line:
            snmpIfHCInUcastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIfHCInUcastPkts"] = snmpIfHCInUcastPkts
        elif "snmpIfHCInMulticastPkts" in line:
            snmpIfHCInMulticastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIfHCInMulticastPkts"] = snmpIfHCInMulticastPkts
        elif "snmpIfHCInBroadcastPkts" in line:
            snmpIfHCInBroadcastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIfHCInBroadcastPkts"] = snmpIfHCInBroadcastPkts
        elif "snmpIfHCOutOctets" in line:
            snmpIfHCOutOctets = line.split()[1]
            finalOutputDict[intf]["snmpIfHCOutOctets"] = snmpIfHCOutOctets
        elif "snmpIfHCOutUcastPkts" in line:
            snmpIfHCOutUcastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIfHCOutUcastPkts"] = snmpIfHCOutUcastPkts
        elif "snmpIfHCOutMulticastPkts" in line:
            snmpIfHCOutMulticastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIfHCOutMulticastPkts"] = snmpIfHCOutMulticastPkts
        elif "snmpIfHCOutBroadcastPckts" in line:
            snmpIfHCOutBroadcastPckts = line.split()[1]
            finalOutputDict[intf]["snmpIfHCOutBroadcastPckts"] = snmpIfHCOutBroadcastPckts
        elif "snmpIpv6IfStatsInReceives" in line:
            snmpIpv6IfStatsInReceives = line.split()[1]
            finalOutputDict[intf]["snmpIpv6IfStatsInReceives"] = snmpIpv6IfStatsInReceives
        elif "snmpIpv6IfStatsInHdrErrors" in line:
            snmpIpv6IfStatsInHdrErrors = line.split()[1]
            finalOutputDict[intf]["snmpIpv6IfStatsInHdrErrors"] = snmpIpv6IfStatsInHdrErrors
        elif "snmpIpv6IfStatsInAddrErrors" in line:
            snmpIpv6IfStatsInAddrErrors = line.split()[1]
            finalOutputDict[intf]["snmpIpv6IfStatsInAddrErrors"] = snmpIpv6IfStatsInAddrErrors
        elif "snmpIpv6IfStatsInDiscards" in line:
            snmpIpv6IfStatsInDiscards = line.split()[1]
            finalOutputDict[intf]["snmpIpv6IfStatsInDiscards"] = snmpIpv6IfStatsInDiscards
        elif "snmpIpv6IfStatsOutForwDatagrams" in line:
            snmpIpv6IfStatsOutForwDatagrams = line.split()[1]
            finalOutputDict[intf]["snmpIpv6IfStatsOutForwDatagrams"] = snmpIpv6IfStatsOutForwDatagrams
        elif "snmpIpv6IfStatsOutDiscards" in line:
            snmpIpv6IfStatsOutDiscards = line.split()[1]
            finalOutputDict[intf]["snmpIpv6IfStatsOutDiscards"] = snmpIpv6IfStatsOutDiscards
        elif "snmpIpv6IfStatsInMcastPkts" in line:
            snmpIpv6IfStatsInMcastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIpv6IfStatsInMcastPkts"] = snmpIpv6IfStatsInMcastPkts
        elif "snmpIpv6IfStatsOutMcastPkts" in line:
            snmpIpv6IfStatsOutMcastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIpv6IfStatsOutMcastPkts"] = snmpIpv6IfStatsOutMcastPkts
        elif "snmpIfInBroadcastPkts" in line:
            snmpIfInBroadcastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIfInBroadcastPkts"] = snmpIfInBroadcastPkts
        elif "snmpIfInMulticastPkts" in line:
            snmpIfInMulticastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIfInMulticastPkts"] = snmpIfInMulticastPkts
        elif "snmpIfOutBroadcastPkts" in line:
            snmpIfOutBroadcastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIfOutBroadcastPkts"] = snmpIfOutBroadcastPkts
        elif "snmpIfOutMulticastPkts" in line:
            snmpIfOutMulticastPkts = line.split()[1]
            finalOutputDict[intf]["snmpIfOutMulticastPkts"] = snmpIfOutMulticastPkts

    return finalOutputDict


def show_plat_int_ns_counters_mac_asic_0_detail(inputDict):
    cmdContentLns = inputDict
    finalOutputDict = {}
    port = ""
    for line in cmdContentLns:

        """
        Port  0 (MACN  4): RX =      26137935250 [    667641526+ @        7226/s ] TX =      66027373524 [   2090127101+ @       22621/s ]
        """

        if "Port" in line:
            port = "port" + line.split()[1]
            finalOutputDict[port] = {}
            macn = line.split()[3].replace( "):" , "" )
            rx =  line.split()[6]
            rxDelta = line.split()[8]
            rxRate = line.split()[10]
            tx =  line.split()[14]
            txDelta =  line.split()[16]
            txRate = line.split()[18]
            finalOutputDict[port]["macn"] = macn
            finalOutputDict[port]["rx"] = rx
            finalOutputDict[port]["rxDelta"] = rxDelta
            finalOutputDict[port]["rxRate"] = rxRate
            finalOutputDict[port]["tx"] = tx
            finalOutputDict[port]["txDelta"] = txDelta
            finalOutputDict[port]["txRate"] = txRate
            """
            MIB:
            
            GBL_C++:  [MSG] ***** MIBs for MM_PORT2 *****
            GBL_C++:  [MSG] TX_PKT_SIZE_LT_64           = 0
            GBL_C++:  [MSG] TX_PKT_SIZE_IS_64           = 85
            GBL_C++:  [MSG] TX_PKT_SIZE_IS_65_TO_127    = 6958700602
            GBL_C++:  [MSG] TX_PKT_SIZE_IS_128_TO_255   = 3939254519
            GBL_C++:  [MSG] TX_PKT_SIZE_IS_256_TO_511   = 2897638837
            """
        elif "GBL_C++:  [MSG] *****" in line:
            continue

        elif "GBL_C++:  [MSG]" in line:
            key = line.split()[2]
            value = line.split()[4]
            finalOutputDict[port][key] = value

            """
                PCS Errors:
                
                REG_NAME                      4
                ----------------------------------------
                FRAMING_ERR_0                 ....
                FRAMING_ERR_1                 ....
                FRAMING_ERR_2                 ....
                FRAMING_ERR_3                 ....
                MF_LEN_ERR_0                  ....
                MF_LEN_ERR_1                  ....
            """
        elif "FRAMING_ERR_0" in line:
            FRAMING_ERR_0 = line.split()[1]
            finalOutputDict[port]["FRAMING_ERR_0"] = FRAMING_ERR_0
        elif "FRAMING_ERR_1" in line:
            FRAMING_ERR_1 = line.split()[1]
            finalOutputDict[port]["FRAMING_ERR_1"] = FRAMING_ERR_1
        elif "FRAMING_ERR_2" in line:
            FRAMING_ERR_2 = line.split()[1]
            finalOutputDict[port]["FRAMING_ERR_2"] = FRAMING_ERR_2
        elif "FRAMING_ERR_3" in line:
            FRAMING_ERR_3 = line.split()[1]
            finalOutputDict[port]["FRAMING_ERR_3"] = FRAMING_ERR_3
        elif "MF_LEN_ERR_0" in line:
            MF_LEN_ERR_0 = line.split()[1]
            finalOutputDict[port]["MF_LEN_ERR_0"] = MF_LEN_ERR_0
        elif "MF_LEN_ERR_1" in line:
            MF_LEN_ERR_1 = line.split()[1]
            finalOutputDict[port]["MF_LEN_ERR_1"] = MF_LEN_ERR_1
        elif "MF_LEN_ERR_2" in line:
            MF_LEN_ERR_2 = line.split()[1]
            finalOutputDict[port]["MF_LEN_ERR_2"] = MF_LEN_ERR_2
        elif "MF_LEN_ERR_3" in line:
            MF_LEN_ERR_3 = line.split()[1]
            finalOutputDict[port]["MF_LEN_ERR_3"] = MF_LEN_ERR_3
        elif "MF_REPEAT_ERR_0" in line:
            MF_REPEAT_ERR_0 = line.split()[1]
            finalOutputDict[port]["MF_REPEAT_ERR_0"] = MF_REPEAT_ERR_0
        elif "MF_REPEAT_ERR_1" in line:
            MF_REPEAT_ERR_1 = line.split()[1]
            finalOutputDict[port]["MF_REPEAT_ERR_1"] = MF_REPEAT_ERR_1
        elif "MF_REPEAT_ERR_2" in line:
            MF_REPEAT_ERR_2 = line.split()[1]
            finalOutputDict[port]["MF_REPEAT_ERR_2"] = MF_REPEAT_ERR_2
        elif "MF_REPEAT_ERR_3" in line:
            MF_REPEAT_ERR_3 = line.split()[1]
            finalOutputDict[port]["MF_REPEAT_ERR_3"] = MF_REPEAT_ERR_3
        elif "MF_ERR_0" in line:
            MF_ERR_0 = line.split()[1]
            finalOutputDict[port]["MF_ERR_0"] = MF_ERR_0
        elif "MF_ERR_1" in line:
            MF_ERR_1 = line.split()[1]
            finalOutputDict[port]["MF_ERR_1"] = MF_ERR_1
        elif "MF_ERR_2" in line:
            MF_ERR_2 = line.split()[1]
            finalOutputDict[port]["MF_ERR_2"] = MF_ERR_2
        elif "MF_ERR_3" in line:
            MF_ERR_3 = line.split()[1]
            finalOutputDict[port]["MF_ERR_3"] = MF_ERR_3
        elif "BIP_ERR_0" in line:
            BIP_ERR_0 = line.split()[1]
            finalOutputDict[port]["BIP_ERR_0"] = BIP_ERR_0
        elif "BIP_ERR_1" in line:
            BIP_ERR_1 = line.split()[1]
            finalOutputDict[port]["BIP_ERR_1"] = BIP_ERR_1
        elif "BIP_ERR_2" in line:
            BIP_ERR_2 = line.split()[1]
            finalOutputDict[port]["BIP_ERR_2"] = BIP_ERR_2
        elif "BIP_ERR_3" in line:
            BIP_ERR_3 = line.split()[1]
            finalOutputDict[port]["BIP_ERR_3"] = BIP_ERR_3
        elif "MISALIGNED" in line:
            MISALIGNED = line.split()[1]
            finalOutputDict[port]["MISALIGNED"] = MISALIGNED
        elif "BAD_PREAMBLE" in line:
            BAD_PREAMBLE = line.split()[1]
            finalOutputDict[port]["BAD_PREAMBLE"] = BAD_PREAMBLE
        elif "BAD_CODE" in line:
            BAD_CODE = line.split()[1]
            finalOutputDict[port]["BAD_CODE"] = BAD_CODE
        elif "BAD_SFD" in line:
            BAD_SFD = line.split()[1]
            finalOutputDict[port]["BAD_SFD"] = BAD_SFD
    return finalOutputDict