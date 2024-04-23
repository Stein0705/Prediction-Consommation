import numpy
import csv
import math
#model = numpy.array([893.59107926,  952.79062748,  960.02668559,  961.91353912,  959.19135035, 955.43143291,  910.90470165,  913.66189201,  937.96857275, -225.55975275])
model = numpy.array([0.0]*10)
#for i in range(7):
#    model[i] = 1000
#model[9] = -1000
Precision = 1

def Read_Data():
    with open("data.csv", newline='') as file:
        dict_reader = csv.DictReader(file, delimiter=';')
        data = list(dict_reader)

        new_data = []
        for dct in data:
            binary_list = [0.0]*7
            binary_list[int(dct["JourSemaine"])] = 1.0
            dct["JourSemaine"] = binary_list
            flat_list = []
            # Flatten the dictionary to a list maintaining the order of values
            for key, value in dct.items():
                if isinstance(value, list):
                    flat_list.extend(value)
                else:
                    flat_list.append(value)
            new_data.append(flat_list)
            
        # Convert the 2D list to a 2D numpy array
        new_array = numpy.array(new_data)
        for y in range(len(new_array)):
            for x in range(len(new_array[y])):
                new_array[y][x] = float(new_array[y][x]) + 10
                if x == 9:
                    new_array[y][x] = float(new_array[y][x])
        return new_array.astype(float)
    

data = Read_Data()

def Predict(model, input):
    return numpy.sum(numpy.multiply(model, input))

def Level(model, data):
    score = 0.0
    for i in range(len(data)):
        score += abs(Predict(model, data[i][:-1])- float(data[i][10]))
    return score / len(data)

def Test(model, data, index):
        score = 0.0
        
        
        for i in range(len(data)):    
            score += data[i][index] *   (Predict(model, data[i][:-1])- float(data[i][10]))
            
        return -score/len(data)

Last = 0.0
OutputData = {"Level": [], "DerLevel": []}
ModelThing = []
def Train(model, data, precision):
    DirectionalVector = numpy.array([0.0]*10)
    
    for i in range(int(input("Amount of Generations >>>"))):
        for i in range (200):
            for index in range(len(model)):
                DirectionalVector[index] = precision * Test(model, data, index)
            Last = Level(model, data)
            model = numpy.add(model, DirectionalVector)

            print(f"Generation {i}: Level: {Level(model, data)} / Better: {Last - Level(model, data)} / Model : ", model)

            OutputData["Level"].append(Level(model, data))
            OutputData["DerLevel"].append(-Last + Level(model, data))
            ModelThing.append(numpy.sum(model))
            
        
    return model




model = Train(model, Read_Data(), 0.0005)

import matplotlib.pyplot as plt

plt.plot(OutputData["Level"], "r")
plt.show()
plt.close()

plt.plot(OutputData["DerLevel"], "r")
plt.show()
plt.close()

plt.plot(ModelThing, "r")
plt.show()
plt.close()

pred = []
real = []
print(model)

for i in range(len(data)):
    pred.append(Predict(model, data[i][:-1]))
    real.append(data[i][10])


plt.plot(pred, "r", real, "g")
plt.show()
plt.close()

