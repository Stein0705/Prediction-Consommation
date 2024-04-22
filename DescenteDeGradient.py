import numpy
import csv
import math
#model = numpy.array([85.0, 36.0, 42.0, 0.0, 0.0, 0.0, -40.0, -32.0, -6.0, -11.0])
model = numpy.array([0.0]*10)
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
        #for i in range(len(data)):
        
        for i in range(len(data)):    
            score += data[i][index] * abs(Predict(model, data[i][:-1])- float(data[i][10]))
            #print(data[i][10] * abs(Predict(model, data[i][:-1])- float(data[i][10])))
        #print("score moyenne", score/len(data))
        return score/len(data)


Err = []
def Train(model, data, precision):
    Error = 0.0
    DirectionalVector = numpy.array([0.0]*10)
    for i in range(5000):
        
        for index in range(len(model)):
            Error = 0.0
            DirectionalVector = numpy.array([0.0]*10)
            Error = Test(model, data, index)
            DirectionalVector[index] = precision * Error
        #print(DirectionalVector)
        #print(DirectionalVector)
        print(f"Generation {i}: Error: {Level(model, data)}")
        model = numpy.add(model, DirectionalVector)
        Err.append(Error)
    return model




model = Train(model, Read_Data(), 0.0001)

import matplotlib.pyplot as plt

plt.plot(Err, "r")
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

