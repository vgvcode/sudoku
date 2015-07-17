
def printRow(lov):
    print lov
    #nLov = []
    #for l in lov:
    #    if l == 0:
    #        nLov.append(".")
    #    else:
    #        nLov.append(l)
    #print ("%s%s%s %s%s%s %s%s%s") % (nLov[0], nLov[1], nLov[2], nLov[3], nLov[4], nLov[5], nLov[6], nLov[7], nLov[8])

class MyError:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class Globals:
    cellSolved = False
    explain = False
    interactive = False
