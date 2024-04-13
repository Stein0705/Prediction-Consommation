import csv
import numpy
import random
import matplotlib.pyplot as plt

model = numpy.array([1.1,1.1,1.1,1.1,1.0,1.0,1.0,1.0,1.0,1.0])

def Read_Data():
    with open("data.csv", newline='') as file:
        dict_reader = csv.DictReader(file, delimiter=';')
        data = list(dict_reader)

        new_data = []
        for dct in data:
            binary_list = [0]*7
            binary_list[int(dct["JourSemaine"])] = 1
            dct["JourSemaine"] = binary_list
            flat_list = []
            # Flatten the dictionary to a list maintaining the order of values
            for k, v in dct.items():
                if isinstance(v, list):
                    flat_list.extend(v)
                else:
                    flat_list.append(v)
            new_data.append(flat_list)
            
        # Convert the 2D list to a 2D numpy array
        new_array = numpy.array(new_data)


        
        return new_array.astype(float)

def Modify(model):
    i = random.randint(0, 9)
    temp_model = model
    if (random.randint(0,1) == 1):
        
        temp_model[i] += model[i] * 0.1
    else:
        temp_model[i] -= model[i] * 0.1
    
    #print(f"{model[5]} / {model[5] * 1.1}")
    
    
    return temp_model

def Predict(model, data):
    return numpy.sum(numpy.multiply(model, data[:-1])) * 1000

def Test(model, data):
    deviation = 0.0
    for i in range(len(data)):
        deviation += abs(Predict(model, data[i])- data[i][10])
    return deviation

data = Read_Data()
models = []

for i in range(1000):
    new_model = Modify(model)
    
    deviation_model = Test(model, data)
    models.append(deviation_model)
    print("Dev", deviation_model/2982)
    deviation_new_model = Test(new_model, data)
    
    if deviation_model > deviation_new_model:
        model = new_model
        print(f"Generation {i}: Model {model} / Avg Dev. {deviation_new_model}")

    else:
        print(f"Generation {i}")

plt.plot(models, "g")
plt.show()
plt.close()
models = []
for i in range(len(data)):
    models.append(Predict(model, data[i]))

conso = []
for i in range(len(data)):
    conso.append(data[i][10])


plt.plot(models, "r", conso, "g")
plt.show()
plt.plot()