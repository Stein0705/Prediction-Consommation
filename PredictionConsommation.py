import csv
import numpy
import matplotlib.pyplot as plt
import time

def Predict(model, entres):
        consommation = 0
        
        consommation = numpy.sum(numpy.multiply(model, entres[0:10])) * 100
        
        return consommation

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
        for y in range(len(new_array)):
               for x in range(10):
                      new_array[y][x] = float(new_array[y][x]) + 10

        
        return new_array.astype(float)

def Test(genome, data):
        score = 0.0
        #for i in range(len(data)):
        for i in range(len(data)):
                score += abs(Predict(genome, data[i])- float(data[i][10]))
        return score

def Select_Best(option1, option2, depth):
        global generation
        global Last_generation
        score_model = Test(option1, data)
        score_new_model = Test(option2, data)
        
        if score_model > score_new_model:
                average_deviation_generations.append(score_new_model / 2982)
                print(f'\033[32m Generation {generation + 1} \033[39m / Average Deviation: {score_new_model/2982} / Model {model} / depth = {depth}')
                Last_generation = time.time()
                return True
        else:
                print(f'\033[31m Generation {generation + 1} \033[39m / Average Deviation: {Test(model, data)/2982} / Model {model} / depth = {depth} / Last Generation: {round(abs(Last_generation - time.time()))}')
                return False

model = numpy.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
change = 1
generation = 0
Last_generation = time.time()

from itertools import product

def Scan(depth, lastchange):
        global model
        global change
        global generation
        global Last_generation
        generation += 1
        
        
        if lastchange != None:
                new_model = model.copy()

                # Apply changes
                for change_value in lastchange:
                        index = change_value - 10 if change_value > 10 else change_value
                        value = change if change_value <= 10 else -change
                        
                        if index < len(new_model):
                                new_model[index] += value
                                
                
                # Check if new model is better
                if Select_Best(model, new_model , depth):
                        model = new_model.copy()
                        if Last_generation - time.time() < 30:
                                Scan(depth, lastchange)
                        return
                
        for changes in product(range(21), repeat=depth):
                new_model = model.copy()

                # Apply changes
                for change_value in changes:
                        index = change_value - 10 if change_value > 10 else change_value
                        value = change if change_value <= 10 else -change
                        
                        if index < len(new_model):
                                new_model[index] += value
                
                
                # Check if new model is better
                if Select_Best(model, new_model , depth):
                        
                        model = new_model.copy()
                        
                        if abs(Last_generation - time.time()) < 30:
                                Scan(depth, changes)
                        
                        return
                
        
        if abs(Last_generation - time.time()) < 30:
                Scan(depth+1, None)
        return
    


average_deviation_generations = []
data = Read_Data()




print(model)
Scan(1, None)


plt.plot(average_deviation_generations, 'r')
plt.show()

plt.close()

#High score means bad performance
ys = []
for i in range(len(data)):
        ys.append(Predict(model, data[i]))



ys2 = []
for i in range(len(data)):
        ys2.append(float(data[i][10]))


plt.plot(ys2, 'r', ys, 'g')
plt.show()
plt.close()