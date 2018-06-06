def cmd_breaker(lines):
    cmdDict = {}
    contentList = []
    key = ""
    for line in lines:
        if "# CMD: " in line:
            contentList = []
            key = line.replace("# CMD: " , "").replace('\n' , "")
        elif "##############################" in line:
            pass
        #elif
        else:
            contentList.append(line.replace('\n' , ""))
            cmdDict[key] = contentList
    return cmdDict