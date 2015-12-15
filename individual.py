__author__ = 'max'
class individual(object):
    def __init__(self,p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13):
        self.parameters =[]
        self.values = []
        self.parameters.append(''+str(p0)+'')
        self.parameters.append(""+str(p1)+"")
        self.parameters.append(""+str(p2)+"")
        self.parameters.append(""+str(p3)+"")
        self.parameters.append(""+str(p4)+"")
        self.parameters.append(""+str(p5)+"")
        self.parameters.append(""+str(p6)+"")
        self.parameters.append(""+str(p7)+"")
        self.parameters.append(""+str(p8)+"")
        self.parameters.append(""+str(p9)+"")
        self.parameters.append(""+str(p10)+"")
        self.parameters.append(""+str(p11)+"")
        self.parameters.append(""+str(p12)+"")
        self.parameters.append(""+str(p13)+"")
        self.values.append(p0)
        self.values.append(p1)
        self.values.append(p2)
        self.values.append(p3)
        self.values.append(p4)
        self.values.append(p5)
        self.values.append(p6)
        self.values.append(p7)
        self.values.append(p8)
        self.values.append(p9)
        self.values.append(p10)
        self.values.append(p11)
        self.values.append(p12)
        self.values.append(p13)
    def getParameters(self):
        return self.parameters
    def express(self):
         self.phenotype =  self.values

