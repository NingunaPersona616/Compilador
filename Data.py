class CMnemonic:
    instruction = ' '
    modDirection = ' '
    longInstruction = ' '
    codOperation = ' '

    def setInstruction(self,i):
        self.instruction = i

    def setModDirection(self,md):
        self.modDirection = md

    def setLongInstruction(self,li):
        self.longInstruction = li

    def setCodOperation(self,co):
        self.codOperation=co[0:len(co)]

    def getInstruction(self):
        return self.instruction

    def getModDirection(self):
        return self.modDirection

    def getLongInstruction(self):
        return self.longInstruction

    def getCodOperation(self):
        return self.codOperation

    def saludar(self):

        print("Hola, soy un objeto")

class CInstruction:
    mnemonico = ' '
    direction = ' '
    label = ' '

    def setMnemonico(self,m):
        self.mnemonico = m

    def setDirection(self,d):
        self.direction = d[0:len(d)]

    def setLabel(self, l):
        self.label=l

    def getMnemonico(self):
        return self.mnemonico

    def getDirection(self):
        return self.direction

    def getLabel(self):
        return self.label

    def printObj(self):
        print("Hola,soy CInstruction")
