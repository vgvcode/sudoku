from celllib import *
from sudokulib import *
from misc import *
from readpuzlib import *

allPuz = readPuzzles("onepuzzle.txt")
#p=0
#for puz in allPuz:
#    p = p+1
#    print "Puzzle: %d" % (p)
#    print puz

for puzObj in allPuz:
    print "Solving puzzle: %s" % (puzObj[0])
    nxn = puzObj[1]
    sxs = SudokuSquare()
    sxs.setVal(nxn)
    Globals.interactive = False
    Globals.explain = False
    
    sxs.solve(1,1,0,0)
    sxs.validate()

#for r in range(3,6):
#    for c in range(0,3):
#        print ("%d, %d: %s") % (r, c, sxs.cell(r,c).getOpt())

#for r in range(0,9):
#    print nxn[r]
#
#print        
#sxs.scanAll()
#options = sxs.sudokuSquareOptions()
#for r in range(0,9):
#    print options[r]


#print sxs.c(0,5).get()
#print sxs.c(0,8).count()
#print sxs.c(0,5).count()
#print sxs.rowVal(0)
#print sxs.colVal(5)
#print sxs.square(0,1)
#print sxs.squareVal(0,1)
#print sxs.c(3,3).square()

#r = 0
#for c in range(0,9):
#    print "Count @(%d, %d) = %d" % (r, c, sxs.cell(r,c).count())
#    
#sxs.scanRow(0,1)
#sxs.scanCol(0,1)
#sxs.scanSquare(0,1)
#
#r = 0
#for c in range(0,9):
#    print "Count @(%d, %d) = %d" % (r, c, sxs.cell(r,c).count())
