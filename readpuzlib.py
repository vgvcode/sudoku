def readPuzzles(fn):
    file = open(fn, 'r')
    
    allpuz = []
    for line in file:
        line=line.strip(' \t\n')
        if (line.isspace() or len(line) == 0):
            #skip blank lines
            continue
        elif line[0] == '#':
            #begin next puzzle
            count = 0
            newpuzobj = [line]
            puz = []
        else:
            count = count + 1
            #convert this to a list of numbers
            lov = []
            for s in line.split(','):
                lov.append(int(s))
            puz.append(lov)
            if (count == 9):
                #end of puzzle
                newpuzobj.append(puz)
                allpuz.append(newpuzobj)
    
    return allpuz