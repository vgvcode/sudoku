
def printRow(lov):
    print lov
    #nLov = []
    #for l in lov:
    #    if l == 0:
    #        nLov.append(".")
    #    else:
    #        nLov.append(l)
    #print ("%s%s%s %s%s%s %s%s%s") % (nLov[0], nLov[1], nLov[2], nLov[3], nLov[4], nLov[5], nLov[6], nLov[7], nLov[8])

class Node:
    def __init__(self, row, col, parent, value):
        self.r = row
        self.c = col
        self.p = parent
        self.v = value
        self.children = []

    def getVal(self):
        return self.v
    
    def getRow(self):
        return self.r
    
    def getCol(self):
        return self.c
    
    def assignCell(self, ssq):
        ssq.cell(self.r, self.c).setVal(self.v)            

class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class Cell:
    def __init__(self, row, col):
        self.r = row
        self.c = col
        self.v = 0
        self.o = [1,2,3,4,5,6,7,8,9]

    def setVal(self, value):
        #valid value, and value is in one of the options in the cell
        if (value >= 1 and value <= 9 and (value in self.o)):
            self.v = value
            self.o = []
            SudokuSquare.setCell = True
        elif value == 0:
            #do nothing
            pass
        else:
            raise ValueError('Cannot assign %d to Cell(%d, %d).  Options are: %s' % (value, self.r, self.c, self.o))
        
    def getVal(self):
        return self.v
    
    def getRow(self):
        return self.r
    
    def getCol(self):
        return self.c
    
    def getOpt(self):
        return self.o
        
    def removeOpt(self, x):
        if x in self.o:
            #print "Removing %d from %s" % (x, self.o)
            (self.o).remove(x)
        return self.o
            
    def addOpt(self, x):
        if not x in self.o:
            (self.o).add(x)
        return self.o
    
    def countOpt(self):
        return len(self.o)
    
    def subCellLoc(self):
        return [int(self.r/3), int(self.c/3)]
    
    def setSingleOpt(self):
        if (len(self.o) == 1):
            result = self.setVal(self.o[0])
            if (SudokuSquare.explain):
                print "Cell(%d,%d) = %d (single option)" % (self.r, self.c, self.v)
        else:
            result = False
            print "Error: Option set has %d elements" % (len(self.o))
        return result

class SudokuSquare:
    
    explain = False
    interactive = False
    setCell = False
    
    def __init__(self):       
        self.nxn = [ \
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        ]
        
        for r in range(0,9):
            for c in range(0,9):
                self.nxn[r][c] = Cell(r,c)
 
    def setVal(self, sq):
        for r in range(0, 9):
            for c in range(0, 9):
                self.nxn[r][c].setVal(sq[r][c])
        
        return self.nxn
 
    def get(self):
        return self.nxn
    
    def cell(self, r, c):
        return self.nxn[r][c]
    
    def row(self, r):
        return self.nxn[r]
    
    def rowVal(self, r):
        lov = []
        for cell in self.nxn[r]:
            lov.append(cell.getVal())
        return lov
    
    def rowOptVal(self, r):
        lov = []
        for cell in self.nxn[r]:
            lov.append(cell.getOpt())
        return lov

    def col(self, c):
        return [
            self.nxn[0][c], self.nxn[1][c], self.nxn[2][c], self.nxn[3][c], self.nxn[4][c], self.nxn[5][c], self.nxn[6][c], self.nxn[7][c], self.nxn[8][c]
            ]
        
    def colVal(self, c):
        return [
            self.nxn[0][c].getVal(), self.nxn[1][c].getVal(), self.nxn[2][c].getVal(), self.nxn[3][c].getVal(), self.nxn[4][c].getVal(), self.nxn[5][c].getVal(), self.nxn[6][c].getVal(), self.nxn[7][c].getVal(), self.nxn[8][c].getVal()
            ]

    def colOptVal(self, c):
        return [
            self.nxn[0][c].getOpt(), self.nxn[1][c].getOpt(), self.nxn[2][c].getOpt(), self.nxn[3][c].getOpt(), self.nxn[4][c].getOpt(), self.nxn[5][c].getOpt(), self.nxn[6][c].getOpt(), self.nxn[7][c].getOpt(), self.nxn[8][c].getOpt()
            ]
           
    def subCell(self, x, y):
        lov = []
        for r in range(x*3, (x+1)*3):
            row = []
            for c in range(y*3, (y+1)*3):
                row.append(self.nxn[r][c])
            lov.append(row)
        return lov

    def subCellVal(self, x, y):
        lov = []
        for r in range(x*3, (x+1)*3):
            row = []
            for c in range(y*3, (y+1)*3):
                row.append(self.nxn[r][c].getVal())
            lov.append(row)
        return lov
    
    def subCellOptVal(self, x, y):
        lov = []
        for r in range(x*3, (x+1)*3):
            row = []
            for c in range(y*3, (y+1)*3):
                row.append(self.nxn[r][c].getOpt())
            lov.append(row)
        #print "subCellOptionsVal(%d %d): %s" % (x, y, lov)
        return lov
    
    def rowFindUniqueOpt(self, r):
        #within a row, find cells which have a unique option - i.e an option which no other cell
        #in the row has (this means that subject cell is the only cell that can have that option)
        rov = self.rowOptVal(r)
        for n in range(1,10):
            count = 0
            foundR = r
            foundC = 0
            for c in range(0,9):
                if n in rov[c]:
                        count = count + 1
                        foundC = c
                if (count > 1):
                    #this number is already present in 2 option buckets
                    break
            if (count == 1):
                self.cell(foundR, foundC).setVal(n)
                if (SudokuSquare.explain):
                    print "Cell(%d,%d) = %d (unique option)" % (foundR, foundC, n)
                #eliminate degrees of freedom for all cells in the row, col and subcell of this subject cell
                self.scanRow(foundR, foundC)
                self.scanCol(foundR, foundC)
                self.scanSubCell(foundR, foundC)
                    
    def colFindUniqueOpt(self, c):
        #within a row, find cells which have a unique option - i.e an option which no other cell
        #in the row has (this means that subject cell is the only cell that can have that option)
        cov = self.colOptVal(c)
        for n in range(1,10):
            count = 0
            foundR = 0
            foundC = c
            for r in range(0,9):
                if n in cov[r]:
                        count = count + 1
                        foundR = r
                if (count > 1):
                    #this number is already present in 2 option buckets
                    break
            if (count == 1):
                self.cell(foundR, foundC).setVal(n)
                if (SudokuSquare.explain):
                    print "Cell(%d,%d) = %d (unique option)" % (foundR, foundC, n)
                #eliminate degrees of freedom for all cells in the row, col and subcell of this subject cell
                self.scanRow(foundR, foundC)
                self.scanCol(foundR, foundC)
                self.scanSubCell(foundR, foundC)

    def subCellFindUniqueOpt(self, x, y):
        #within a subcell (3x3 subCell) find cells which have a unique option - i.e an option which no other cell
        #in the subCell has (this means that subject cell is the only cell that can have that option)
        sqov = self.subCellOptVal(x, y)
        for n in range(1,10):
            count = 0
            foundR = 0
            foundC = 0
            for r in range(0,3):
                for c in range(0,3):
                    if n in sqov[r][c]:
                        count = count + 1
                        foundR = r
                        foundC = c
                    if (count > 1):
                        #this number is already present in 2 option buckets
                        break
                if (count > 1):
                    break
            if (count == 1):
                #print ("Square (%d, %d) Cell (%d, %d) has unique option %d") % (x,y,foundR,foundC,n)
                #assign the unique option to the cell
                sudokuRow = x * 3 + foundR
                sudokuCol = y * 3 + foundC
                self.cell(sudokuRow, sudokuCol).setVal(n)
                if (SudokuSquare.explain):
                    print "Cell(%d,%d) = %d (unique option)" % (sudokuRow, sudokuCol, n)
                #eliminate degrees of freedom for all cells in the row, col and subcell of this subject cell
                self.scanRow(sudokuRow, sudokuCol)
                self.scanCol(sudokuRow, sudokuCol)
                self.scanSubCell(sudokuRow, sudokuCol)
   
    def findUniqueAllRows(self):
        for r in range(0,9):
            self.rowFindUniqueOpt(r)
    
    def findUniqueAllCols(self):
        for c in range(0,9):
            self.colFindUniqueOpt(c)
    
    def findUniqueAllSubCells(self):
        for x in range(0,3):
            for y in range(0,3):
                self.subCellFindUniqueOpt(x, y)
                     
    def findDoubletonRow(self, r):
        lodb = []
        for c1 in range(0,9):
            optVal1 = self.cell(r, c1).getOpt()
            if len(optVal1) != 2:
                continue
            for c2 in range(0,9):
                if c1 == c2:
                    continue
                optVal2 = self.cell(r, c2).getOpt()
                if len(optVal2) != 2:
                    continue
                if (optVal1 == optVal2):
                    if not optVal1 in lodb:
                        lodb.append(optVal1)
        
        #at this point, you have a list of doubletons in lodb
        #remove these doubleton numbers from the other option values
        if len(lodb) > 0:
            print "findDoubletonRow: %s" % (lodb)
            for db in lodb:
                print "findDoubletonRow: %s" % (db)
                n1 = db[0]
                n2 = db[1]
                print "findDoubletonRow: %d %d" % (n1, n2)
                for c in range(0,9):
                    optVal = self.cell(r, c).getOpt()
                    #do not remove the numbers from the doubleton. Remove the numbers only from other options
                    if (db == optVal):
                        continue
                    self.cell(r, c).removeOpt(n1)
                    self.cell(r, c).removeOpt(n2)
                
    def findDoubletonAllRows(self):
        for r in range(0,9):
            self.findDoubletonRow(r)
                
    def findDoubletonCol(self, c):
        lodb = []
        for r1 in range(0,9):
            optVal1 = self.cell(r1, c).getOpt()
            if len(optVal1) != 2:
                continue
            for r2 in range(0,9):
                if r1 == r2:
                    continue
                optVal2 = self.cell(r2, c).getOpt()
                if len(optVal2) != 2:
                    continue
                if (optVal1 == optVal2):
                    if not optVal1 in lodb:
                        lodb.append(optVal1)
        
        #at this point, you have a list of doubletons in lodb
        #remove these doubleton numbers from the other option values

        if len(lodb) > 0:        
            for db in lodb:
                n1 = db[0]
                n2 = db[1]
                for r in range(0,9):
                    optVal = self.cell(r, c).getOpt()
                    #do not remove the numbers from the doubleton. Remove the numbers only from other options
                    if (db == optVal):
                        continue
                    self.cell(r, c).removeOpt(n1)
                    self.cell(r, c).removeOpt(n2)
    
    def findDoubletonAllCols(self):
        for c in range(0,9):
            self.findDoubletonCol(c)
            
    def findDoubletonSubCell(self, x, y):
        lodb = []
        for x1 in range(x*3, (x+1)*3):
            for y1 in range(y*3, (y+1)*3):
                optVal1 = self.cell(x1, y1).getOpt()
                if len(optVal1) != 2:
                    continue
                for x2 in range(x*3, (x+1)*3):
                    for y2 in range(y*3, (y+1)*3):
                        if [x1,y1] == [x2,y2]:
                            continue
                        optVal2 = self.cell(x2, y2).getOpt()
                        if len(optVal2) != 2:
                            continue
                        if (optVal1 == optVal2):
                            if not optVal1 in lodb:
                                lodb.append(optVal1)
                            
        #at this point, you have a list of doubletons in lodb
        #remove these doubleton numbers from the other option values
        
        if len(lodb) > 0:
            print "findDoubletonSubCell: %s" % (lodb)
            for db in lodb:
                print "findDoubletonSubCell: %s" % (db)
                n1 = db[0]
                n2 = db[1]
                print "findDoubletonSubCell: %d %d" % (n1, n2)
                for x1 in range(x*3, (x+1)*3):
                    for y1 in range(y*3, (y+1)*3):
                        optVal = self.cell(x1, y1).getOpt()
                        #do not remove the numbers from the doubleton. Remove the numbers only from other options
                        if (db == optVal):
                            continue
                        self.cell(x1, y1).removeOpt(n1)
                        self.cell(x2, y2).removeOpt(n2)
    
    
    def findDoubletonAllSubCells(self):
        for x in range(0,3):
            for y in range(0,3):
                self.findDoubletonSubCell(x, y)
    
    def findDoubletonAll(self):
        self.findDoubletonAllRows()
        self.findDoubletonAllCols()
        self.findDoubletonAllSubCells()
    
    def sudokuSquareVal(self):
        lov = []
        for r in range(0,9):
            row = []
            for c in range(0,9):
                row.append(self.nxn[r][c].getVal())
            lov.append(row)
        return lov
    
    def printSudokuSquare(self):
        sq = self.sudokuSquareVal()
        for r in range(0,9):
            printRow(sq[r])
            #if ((r+1) % 3 == 0):
            #    print
    
    def sudokuSquareOptionsCount(self):
        lov = []
        for r in range(0, 9):
            row = []
            for c in range(0, 9):
                row.append(self.nxn[r][c].countOpt())
            lov.append(row)
        return lov
    
    def printSudokuSquareOptions(self):
        sqo = self.sudokuSquareOptionsCount()
        for r in range(0,9):
            printRow(sqo[r])
            #if ((r+1) % 3 == 0):
            #    print
            
    def getOneOptionCells(self):
        #return a list of cells with only one degree of freedom (i.e. that cell is solved)
        lov = []
        for r in range(0,9):
            for c in range(0,9):
                if self.nxn[r][c].countOpt() == 1:
                    lov.append(self.nxn[r][c])
        return lov
    
    def isSolved(self):
        solved = True
        for r in range(0,9):
            for c in range(0,9):
                if (self.cell(r,c).getVal() == 0):
                    solved = False
                    break
            if (solved == False):
                break
        return solved
    
    def scanRow(self, myRow, myCol):
        cellVal = self.nxn[myRow][myCol].getVal()
        for col in range(0,9):
            if col != myCol:
                self.nxn[myRow][col].removeOpt(cellVal)
                
    def scanCol(self, myRow, myCol):
        cellVal = self.nxn[myRow][myCol].getVal()
        for row in range(0,9):
            if row != myRow:
                self.nxn[row][myCol].removeOpt(cellVal)
                
    def scanSubCell(self, myRow, myCol):
        cellVal = self.nxn[myRow][myCol].getVal()
        mySubCellLoc = self.nxn[myRow][myCol].subCellLoc()
        msr = mySubCellLoc[0]
        msc = mySubCellLoc[1]
        #print "Cellval: %d, msr: %d, msc:%d" %(cellVal, msr, msc)

        for r in range(msr*3, (msr+1)*3):
            for c in range(msc*3, (msc+1)*3):
                if not (r == myRow and c == myCol):
                        self.nxn[r][c].removeOpt(cellVal)
                        
    def scanAllCells(self):
        #go through every cell in sudoku and eliminate degrees of freedom in row, col and square of subject cell
        for r in range(0,9):
            for c in range(0,9):
                    self.scanRow(r, c)
                    self.scanCol(r, c)
                    self.scanSubCell(r, c)
                    
    def validateRow(self, r):
        validate = True
        lov = self.rowVal(r)
        for n in (1,10):
            if lov.count(n) > 1:
                valiate=False
                print "Row %d has more than one %d" % (r, n)
        return validate
    
    def validateCol(self, c):
        validate = True
        lov = self.colVal(c)
        for n in (1,10):
            if lov.count(n) > 1:
                valiate=False
                print "Col %d has more than one %d" % (c, n)
        return validate
    
    def validateSubCell(self, x, y):
        validate = True
        lov = self.subCellVal(x, y)
        for n in (1,10):
            if lov.count(n) > 1:
                valiate=False
                print "Subcell (%d,%d) has more than one %d" % (x, y, n)
        return validate

    def validate(self):
        validate = True
        for r in range(0,9):
            validate = self.validateRow(r)
            if validate == False:
                break
        
        if (validate == False):
            return False
        
        for c in range(0,9):
            validate = self.validateCol(c)
            if validate == False:
                break
        
        if (validate == False):
            return False
        
        for x in range(0,3):
            for y in range(0,3):
                validate = self.validateSubCell(x, y)
                if validate == False:
                    break

        return validate
                        
    def solve(self):
        solved = False
        stopped = False
        iter = 0
        response = "y"
        try:
            while(not solved and not stopped and iter < 100):
                if (self.isSolved()):
                    solved = True
                else:
                    iter = iter + 1                
                    print "Iterations: %d" % (iter)
                    self.printSudokuSquare()
                    print
                    print "Degrees of freedom:"
                    self.printSudokuSquareOptions()
                    if (SudokuSquare.interactive):
                        response = "i"
                        while not response[0].lower() in ["y", "n"]:
                            response = raw_input("Continue (Y/N) or I(input) or (B)?:")
                            if response.isdigit():
                                r = int(response[0])
                                c = int(response[1])
                                print "Options for (%d, %d): %s" % (r, c, self.cell(r, c).getOpt())
                            if (response[0].lower() == "b"):
                                self.buildNOptionsTree()
    
                    # Response is y or n at this point
                    if (response[0].lower() == "n"):
                        stopped = True
                    else:
                        SudokuSquare.setCell = False
                        self.scanAllCells()
                        lov = self.getOneOptionCells()
                        for cell in lov:
                            cell.setSingleOpt()
                            r = cell.getRow()
                            c = cell.getCol()
                            self.scanRow(r, c)
                            self.scanCol(r, c)
                            self.scanSubCell(r, c)
                        self.findUniqueAllRows()
                        self.findUniqueAllCols()
                        self.findUniqueAllSubCells()
                        if (SudokuSquare.setCell == False):
                            print "No luck with simple moves. Try doubleton"
                            self.findDoubletonAll()
                            #if (SudokuSquare.setCell == False):
                            #    print "Help. I'm stuck!"
                            #    stopped = True

            except                             
                        
            if (solved):
                self.printSudokuSquare()
                print "Solved!"
            
    def buildNOptionsTree(self):
        print "Building options tree"
        root = Node(0, 0, 0, 0)
        lastLevel = [root]
        num = 1
        for r in range(0,9):
            for c in range(0,9):
                optVal = self.cell(r,c).getOpt()
                if len(optVal) > 1:
                    num = num * len(optVal)
        print "Num options: %d" % (num)                
                #optVal = self.cell(r,c).getOpt()
                #print ("Options at Cell(%d, %d): %s" % (r, c, optVal))
                #if len(optVal) > 1:
                #    print "@Beginning: Nodes at current level: %d" % (len(lastLevel))
                #    #for leaf in lastLevel:
                #    #    print "At last level: (%d, %d) = %d" % (leaf.getRow(), leaf.getCol(), leaf.getVal())
                #    nextLevel = []
                #    for leaf in lastLevel:
                #        for o in optVal:
                #            n = Node(r, c, leaf, o)
                #            leaf.children.append(n)
                #            nextLevel.append(n)
                #    lastLevel = nextLevel
                #    print "@End: Nodes at last level: %d" % (len(lastLevel))
                #    #for leaf in lastLevel:
                #    #    print "At last level: %s" % (leaf.getVal())
                #    response = raw_input("Proceed?")
                #    if (response[0].lower() == "n"):
                #        return