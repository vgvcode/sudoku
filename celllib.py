from misc import *

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
            Globals.cellSolved = True
        elif value == 0:
            #do nothing
            pass
        else:
            raise MyError('Cannot assign %d to Cell(%d, %d).  Options are: %s' % (value, self.r, self.c, self.o))
        
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
            if (Globals.explain):
                print "Cell(%d,%d) = %d (single option)" % (self.r, self.c, self.v)
