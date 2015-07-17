
def printRow(lov):
    print lov
    #nLov = []
    #for l in lov:
    #    if l == 0:
    #        nLov.append(".")
    #    else:
    #        nLov.append(l)
    #print ("%s%s%s %s%s%s %s%s%s") % (nLov[0], nLov[1], nLov[2], nLov[3], nLov[4], nLov[5], nLov[6], nLov[7], nLov[8])

class Cell:
    def __init__(self, row, col):
        self.r = row
        self.c = col
        self.v = 0
        self.o = [1,2,3,4,5,6,7,8,9]

    def set(self, value):
        if (value >= 1 and value <= 9):
            self.v = value
            self.o = []
        
    def getVal(self):
        return self.v
    
    def getRow(self):
        return self.r
    
    def getCol(self):
        return self.c
    
    def getOpt(self):
        return self.o
        
    def remove(self, x):
        if x in self.o:
            #print "Removing %d from %s" % (x, self.o)
            (self.o).remove(x)
        return self.o
            
    def add(self, x):
        if not x in self.o:
            (self.o).add(x)
        return self.o
    
    def count(self):
        return len(self.o)
    
    def subCellLoc(self):
        return [int(self.r/3), int(self.c/3)]
    
    def setSingleOption(self):
        if (len(self.o) == 1):
            self.set(self.o[0])
            if (SudokuSquare.explain):
                print "Cell(%d,%d) = %d (single option)" % (self.r, self.c, self.v)
        else:
            print "Error: Option set has %d elements" % (len(self.o))

class SudokuSquare:
    
    explain = False
    
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
 
    def set(self, sq):
        for r in range(0, 9):
            for c in range(0, 9):
                self.nxn[r][c].set(sq[r][c])
        
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
    
    def rowOptionsVal(self, r):
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

    def colOptionsVal(self, c):
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
    
    def subCellOptionsVal(self, x, y):
        lov = []
        for r in range(x*3, (x+1)*3):
            row = []
            for c in range(y*3, (y+1)*3):
                row.append(self.nxn[r][c].getOpt())
            lov.append(row)
        #print "subCellOptionsVal(%d %d): %s" % (x, y, lov)
        return lov
    
    def rowFindUniqueOption(self, r):
        #within a row, find cells which have a unique option - i.e an option which no other cell
        #in the row has (this means that subject cell is the only cell that can have that option)
        rowOptVal = self.rowOptionsVal(r)
        for n in range(1,10):
            count = 0
            foundR = r
            foundC = 0
            for c in range(0,9):
                if n in rowOptVal[c]:
                        count = count + 1
                        foundC = c
                if (count > 1):
                    #this number is already present in 2 option buckets
                    break
            if (count == 1):
                self.cell(foundR, foundC).set(n)
                if (SudokuSquare.explain):
                    print "Cell(%d,%d) = %d (unique option)" % (foundR, foundC, n)
                #eliminate degrees of freedom for all cells in the row, col and subcell of this subject cell
                self.scanRow(foundR, foundC)
                self.scanCol(foundR, foundC)
                self.scanSubCell(foundR, foundC)
                    
    def colFindUniqueOption(self, c):
        #within a row, find cells which have a unique option - i.e an option which no other cell
        #in the row has (this means that subject cell is the only cell that can have that option)
        colOptVal = self.colOptionsVal(c)
        for n in range(1,10):
            count = 0
            foundR = 0
            foundC = c
            for r in range(0,9):
                if n in colOptVal[r]:
                        count = count + 1
                        foundR = r
                if (count > 1):
                    #this number is already present in 2 option buckets
                    break
            if (count == 1):
                self.cell(foundR, foundC).set(n)
                if (SudokuSquare.explain):
                    print "Cell(%d,%d) = %d (unique option)" % (foundR, foundC, n)
                #eliminate degrees of freedom for all cells in the row, col and subcell of this subject cell
                self.scanRow(foundR, foundC)
                self.scanCol(foundR, foundC)
                self.scanSubCell(foundR, foundC)

    def subCellFindUniqueOption(self, x, y):
        #within a subcell (3x3 subCell) find cells which have a unique option - i.e an option which no other cell
        #in the subCell has (this means that subject cell is the only cell that can have that option)
        sqOptVal = self.subCellOptionsVal(x, y)
        for n in range(1,10):
            count = 0
            foundR = 0
            foundC = 0
            for r in range(0,3):
                for c in range(0,3):
                    if n in sqOptVal[r][c]:
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
                self.cell(sudokuRow, sudokuCol).set(n)
                if (SudokuSquare.explain):
                    print "Cell(%d,%d) = %d (unique option)" % (sudokuRow, sudokuCol, n)
                #eliminate degrees of freedom for all cells in the row, col and subcell of this subject cell
                self.scanRow(sudokuRow, sudokuCol)
                self.scanCol(sudokuRow, sudokuCol)
                self.scanSubCell(sudokuRow, sudokuCol)
    
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
                row.append(self.nxn[r][c].count())
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
                if self.nxn[r][c].count() == 1:
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
                self.nxn[myRow][col].remove(cellVal)
                
    def scanCol(self, myRow, myCol):
        cellVal = self.nxn[myRow][myCol].getVal()
        for row in range(0,9):
            if row != myRow:
                self.nxn[row][myCol].remove(cellVal)
                
    def scanSubCell(self, myRow, myCol):
        cellVal = self.nxn[myRow][myCol].getVal()
        mySubCellLoc = self.nxn[myRow][myCol].subCellLoc()
        msr = mySubCellLoc[0]
        msc = mySubCellLoc[1]
        #print "Cellval: %d, msr: %d, msc:%d" %(cellVal, msr, msc)

        for r in range(msr*3, (msr+1)*3):
            for c in range(msc*3, (msc+1)*3):
                if not (r == myRow and c == myCol):
                        self.nxn[r][c].remove(cellVal)
                        
    def scanAllCells(self):
        #go through every cell in sudoku and eliminate degrees of freedom in row, col and square of subject cell
        for r in range(0,9):
            for c in range(0,9):
                    self.scanRow(r, c)
                    self.scanCol(r, c)
                    self.scanSubCell(r, c)
                    
    
    def findUniqueAllRows(self):
        for r in range(0,9):
            self.rowFindUniqueOption(r)
    
    def findUniqueAllCols(self):
        for c in range(0,9):
            self.colFindUniqueOption(c)
    
    def findUniqueAllSubCells(self):
        for x in range(0,3):
            for y in range(0,3):
                self.subCellFindUniqueOption(x, y)
                    
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
        while(not solved and not stopped):
            if (self.isSolved()):
                solved = True
            else:
                iter = iter + 1                
                print "Iterations: %d" % (iter)
                self.printSudokuSquare()
                print
                print "Degrees of freedom:"
                self.printSudokuSquareOptions()
                response = raw_input("Continue (Y/N) ?:")
                if (iter > 100):
                    response = "n"
                    
                if (response[0].lower() == "n"):
                    stopped = True
                else:
                    self.scanAllCells()
                    lov = self.getOneOptionCells()
                    for cell in lov:
                        cell.setSingleOption()
                        r = cell.getRow()
                        c = cell.getCol()
                        self.scanRow(r, c)
                        self.scanCol(r, c)
                        self.scanSubCell(r, c)
                    self.findUniqueAllRows()
                    self.findUniqueAllCols()
                    self.findUniqueAllSubCells()
                        
            if (solved):
                self.printSudokuSquare()
                print "Solved!"
            
