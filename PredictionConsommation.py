import random
import csv
import numpy
import matplotlib.pyplot as plt
import time

def Predict(genome, entres):
        consommation = 0
        #print(genome)
        #print(entres)
        consommation = numpy.sum(numpy.multiply(genome, entres[0:10])) * 100
        #print(f"consommation : {consommation}")
        return consommation

def Modify(genome, change, jump):
        genome = list(genome)
        
        for x in range(jump):
                i = random.randint(0,9)
                
                if bool(random.getrandbits(1)):
                        genome[i] += change
                else:
                        genome[i] -= change
                return genome

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
               for x in range(11):
                      new_array[y][x] = float(new_array[y][x]) + 5

        
        return new_array.astype(float)




def Test(genome, data):
        score = 0.0
        #for i in range(len(data)):
        for i in range(len(data)):
                score += abs(Predict(genome, data[i])- float(data[i][10]))
        return score



average_deviation_generations = []
data = Read_Data()
print(data)
model = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
time_since_evolution = 0
change = 1
jump = 1



for i in range (1000):

        if time_since_evolution > 50:
               time_since_evolution = 0
               change +=1
        
        if change > 1 and score_model > 5000:
                
                for x in range(10):
                       for y in range(10):
                              for z in range(10):
                                     for k in range(10):
                                        new_model[x] += change
                                        new_model[y] += change
                                        new_model[z] -= change
                                        new_model[k] -= change
        else:
               
                new_model = Modify(model, change, jump)
        #print(new_model)
        score_model = Test(model, data)
        score_new_model = Test(new_model, data)

        
        if score_model > score_new_model:
                model = new_model
                average_deviation_generations.append(score_new_model / 2982)
                print(f'Generation {i} / Average Deviation: {Test(model, data)/2982} / Model {model} / Change {change} / Jump {jump}')
                time_since_evolution = 0
                change = 1
                jump = 1
        else:
               print(f"Generation {i}, pas d'amélioration, {score_model/2982}, Time since evolution: {time_since_evolution} / change {change} / jump {jump}")
               time_since_evolution += 1
               

        
        


print(model)



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