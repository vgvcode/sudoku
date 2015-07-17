from celllib import *
from misc import *
import copy
import sys
import os

class SudokuSquare:
    
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
        for n in range(1,10):
            rov = self.rowOptVal(r)
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
                if (Globals.explain):
                    print "Cell(%d,%d) = %d (unique option @ row scan)" % (foundR, foundC, n)
                #eliminate degrees of freedom for all cells in the row, col and subcell of this subject cell
                self.scanRow(foundR, foundC)
                self.scanCol(foundR, foundC)
                self.scanSubCell(foundR, foundC)
                    
    def colFindUniqueOpt(self, c):
        #within a row, find cells which have a unique option - i.e an option which no other cell
        #in the row has (this means that subject cell is the only cell that can have that option)
        for n in range(1,10):
            cov = self.colOptVal(c)
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
                if (Globals.explain):
                    print "Cell(%d,%d) = %d (unique option @ col scan)" % (foundR, foundC, n)
                #eliminate degrees of freedom for all cells in the row, col and subcell of this subject cell
                self.scanRow(foundR, foundC)
                self.scanCol(foundR, foundC)
                self.scanSubCell(foundR, foundC)

    def subCellFindUniqueOpt(self, x, y):
        #within a subcell (3x3 subCell) find cells which have a unique option - i.e an option which no other cell
        #in the subCell has (this means that subject cell is the only cell that can have that option)
        for n in range(1,10):
            sqov = self.subCellOptVal(x, y)
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
                if (Globals.explain):
                    print "Cell(%d,%d) = %d (unique option @ subcell scan)" % (sudokuRow, sudokuCol, n)
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
                
    def findUniqueAllCells(self):
        self.findUniqueAllRows()
        self.findUniqueAllCols()
        self.findUniqueAllSubCells()
                    
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
            if (Globals.explain):
                print "findDoubletonRow: %d %s" % (r, lodb)
            for db in lodb:
                n1 = db[0]
                n2 = db[1]
                for c in range(0,9):
                    optVal = self.cell(r, c).getOpt()
                    #do not remove the numbers from the doubleton. Remove the numbers only from other options
                    if (len(optVal) == 0) or (db == optVal):
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
            if (Globals.explain):
                print "findDoubletonCol: %d %s" % (c, lodb)
            for db in lodb:
                n1 = db[0]
                n2 = db[1]
                for r in range(0,9):
                    optVal = self.cell(r, c).getOpt()
                    #do not remove the numbers from the doubleton. Remove the numbers only from other options
                    if (len(optVal) == 0) or (db == optVal):
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
            if (Globals.explain):
                print "findDoubletonSubCell: subcell(%d %d) %s" % (x, y, lodb)
            for db in lodb:
                n1 = db[0]
                n2 = db[1]
                for x1 in range(x*3, (x+1)*3):
                    for y1 in range(y*3, (y+1)*3):
                        optVal = self.cell(x1, y1).getOpt()
                        #do not remove the numbers from the doubleton. Remove the numbers only from other options
                        if (len(optVal) == 0) or (db == optVal):
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
            
    def solveOneOptionCells(self):
        #solve all cells with only one degree of freedom (i.e. that cell is solved)
        for r in range(0,9):
            for c in range(0,9):
                if self.nxn[r][c].countOpt() == 1:
                    self.nxn[r][c].setSingleOpt()
                    #scan row, col, subcell again after solving to reduce more d-o-f in other cells
                    self.scanRow(r, c)
                    self.scanCol(r, c)
                    self.scanSubCell(r, c)
   
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
                        
    def solve(self, level, iter, startRow, startCol):
        solved = False
        stopped = False
        response = "y"
        noProgress = 0
        try:
            if (iter > 100):
                print "Too many iterations %d. Stopped" % (iter)
                raise MyError("Too many iterations %d. Stopped" % (iter))
            else:
                subIter = 0
                while(not solved and not stopped):
                    if (self.isSolved()):
                        print
                        self.printSudokuSquare()
                        print "Solved!"
                        solved = True
                    else:
                        subIter = subIter + 1                
                        print "Iterations: %d-%d" % (iter, subIter)
                        if (Globals.explain):
                            self.printSudokuSquare()
                            print
                            print "Degrees of freedom:"
                            self.printSudokuSquareOptions()
                        if (Globals.interactive):
                            response = ""
                            while not response[0].lower() in ["y", "n", "a"]:
                                response = raw_input("Continue (Y/N) or A(Abort) or Cell Options [dd]?:")
                                if response.isdigit():
                                    r = int(response[0])
                                    c = int(response[1])
                                    print "Options for (%d, %d): %s" % (r, c, self.cell(r, c).getOpt())
                        else:
                            response = "y"
    
                        if (response[0].lower() == "a"):
                            exit()
                        # Response is y or n at this point
                        elif (response[0].lower() == "n"):
                            stopped = True
                        else:
                            Globals.cellSolved = False
                            self.scanAllCells()
                            # Solve the cells which have only one degree of freedom
                            self.solveOneOptionCells()
                            self.findUniqueAllCells()
                            # Again, solve the cells which have only one degree of freedom
                            self.solveOneOptionCells()
                            if (Globals.cellSolved == False):
                                noProgress = noProgress + 1
                                if (noProgress < 3):
                                    print "No luck with simple moves. Try doubleton"
                                    self.findDoubletonAll()
                                    # Again, solve the cells which have only one degree of freedom
                                    self.solveOneOptionCells()
                                else:
                                    print "Exhausted all strategies. Proceeding to guess..."
                                    solved,stopped = self.guessASolution(level, iter, startRow, startCol)
                                    if (not solved and not stopped):
                                        #guess was wrong, it resulted in no possible solution
                                        stopped = True
                                
        except MyError as e:
            print "Exception occurred: %s" % (e.value)
            stopped = True
            solved = False
        except SystemExit:
            print "Terminated"
            os.abort()
        except:
            print "Unexpected error %s" % (sys.exc_info()[0])
            stopped = True
            solved = False                        
        finally:
            return (solved, stopped)
        
    def deepCopy(self):
        return copy.deepcopy(self)
            
    def guessASolution(self, level, count, startRow, startCol):
        solved = False
        stopped = False
        nextLevel = level + 1
        nextCount = count
        
        if (nextLevel == 2):
            #first find out how many combinations exist
            num = 1
            for r in range(startRow,9):
                for c in range(startCol,9):
                    optCount = self.cell(r, c).countOpt()
                    if (optCount > 0):
                        num = num * optCount
            print "%d combinations to explore" % (num)
                        
        for r in range(0,9):
            for c in range(0,9):
                optVal = self.cell(r,c).getOpt()
                print "Row %d Col %d" % (r,c)
                if len(optVal) > 1:
                    for o in optVal:
                        print "OptVal: %s" % (optVal)
                        nextCount = nextCount + 1
                        #make a deep copy of original
                        mySsq = self.deepCopy()
                        mySsq.cell(r,c).setVal(o)
                        #scan the row, col, subcell to remove degrees of freedom
                        mySsq.scanRow(r, c)
                        mySsq.scanCol(r, c)
                        mySsq.scanSubCell(r, c)
                        print "Set cell(%d, %d) = %d" % (r, c, o)
                        if (Globals.interactive):
                            response = raw_input("Proceed to solve: Y/N?")
                        else:
                            response = "y"
                        if (response[0].lower() == "y"):
                            if (startCol < 8):
                                nextCol = startCol + 1
                                nextRow = startRow
                            else:
                                startCol = 0
                                nextRow = nextRow + 1

                            print "Next Level: %d Next Count: %d Next Row: %d Next Col: %d" % (nextLevel, nextCount, nextRow, nextCol)
                            solved,stopped = mySsq.solve(nextLevel, nextCount, nextRow, nextCol)
                            print "Solved: %s Stopped: %s" % (solved, stopped)
                        else:
                            stopped = True
                        if solved or stopped:
                            break
                if solved or stopped:
                    break
            if solved or stopped:
                break
        print "Solved: %s Stopped: %s Next Level: %d Next Count: %d" % (solved, stopped, nextLevel, nextCount)
        return (solved, stopped)
                        
