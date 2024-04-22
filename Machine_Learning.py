import numpy
import csv
import time
from itertools import product

def Read_Data(filename):
    with open(filename, newline='') as file:
        dict_reader = csv.DictReader(file, delimiter=';')
        data = list(dict_reader)

        new_data = []
        for dct in data:
            flat_list = []
            # Flatten the dictionary to a list maintaining the order of values
            for k, v in dct.items():
                if isinstance(v, list):
                    flat_list.extend(v)
                else:
                    flat_list.append(v)
            new_data.append(flat_list)
            
        # Convert the 2D list to a 2D numpy array
        
        return numpy.array(new_data).astype(float)


class Model():

    def __init__(self, ParameterLength):
          self.model = numpy.array([0]*ParameterLength)
          self.GUI = []

    def Predict(self, input, OverwriteModel):
            output = 0
            if all(OverwriteModel) == None:
                output = numpy.sum(numpy.multiply(self.model, input[:-1]))
            else:
                output = numpy.sum(numpy.multiply(OverwriteModel, input[:-1]))
            return output
    
    
        
    def Test(self, model, data):
        score = 0.0
        
        #for i in range(len(data)):
        for i in range(len(data)):
                score += abs(self.Predict(data[i], model)- float(data[i][len(data[i])-1]))
        return score


    def Select_Best(self, new_model, data, LastGeneration, depth):
        score_model = self.Test(self.model, data)
        score_new_model = self.Test(new_model, data)
        
        if score_model > score_new_model:
                self.model = new_model.copy()
                print(f'\033[32m Average Deviation: {score_new_model/2982} \033[39m / Model {self.model}')
            
                Last_generation = time.time()
                return True
        else:
                print(f'\033[31m Average Deviation: {score_new_model/2982} \033[39m / Model {self.model} / depth = {depth} / Last Generation: {round(abs(LastGeneration - time.time()))}')
                return False

    def Train(self, data, depth, LastChange, MaxWait, Precision, GUI, LastGeneration):
        
        if len(data[0])-1 != len(self.model):
            raise Exception("Could not train the model!\nPlease make sure the data has as many parameters as the model.")
        
        if LastChange != None:
                new_model = self.model.copy()
                
                # Apply changes
                for change_value in LastChange:
                        index = change_value - 10 if change_value > 10 else change_value
                        value = Precision if change_value <= 10 else -Precision
                        
                        if index < len(new_model):
                                new_model[index] += value
                                
                
                # Check if new model is better
                if self.Select_Best(new_model , data, LastGeneration, depth):
                        self.GUI.append(self.Test(self.model, data)/len(data))
                        LastGeneration = time.time()
                        self.Train(data, depth, LastChange, MaxWait, Precision, GUI, LastGeneration)
                        return
                        
                
        for changes in product(range(21), repeat=depth):
                new_model = self.model.copy()
                

                # Apply changes
                for change_value in changes:
                        index = change_value - 10 if change_value > 10 else change_value
                        value = Precision if change_value <= 10 else -Precision
                        
                        if index < len(new_model):
                                new_model[index] += value
                                
                                
                
                # Check if new model is better
                if self.Select_Best(new_model, data, LastGeneration, depth):
                        
                        if abs(LastGeneration - time.time()) < MaxWait:
                                self.GUI.append(self.Test(self.model, data)/len(data))
                                LastGeneration = time.time()
                                self.Train(data, depth, LastChange, MaxWait, Precision, GUI, LastGeneration)
                        
                        return
                
        
        if abs(LastGeneration - time.time()) < MaxWait:
                self.Train(data,depth+1, None, MaxWait, Precision, GUI, LastGeneration)
        return
    

mymodel = Model(4)
mymodel.Train(Read_Data("data.csv"), 1, None, 2, 100, None, time.time())

import matplotlib.pyplot as plt

plt.plot(mymodel.GUI)
plt.show()
plt.close()


data = Read_Data("data.csv")
ys = []
for i in range(len(data)):
      print(i)
      ys.append(mymodel.Predict(data[i], mymodel.model)/len(data))

plt.plot(ys)
plt.show()
plt.close()