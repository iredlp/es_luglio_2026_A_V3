from model.model import Model

mymdl=Model()
mymdl.creaGrafo("2017-01-01","2019-12-31")
print(mymdl.getGraphDetails())