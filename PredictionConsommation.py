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


def Select_Best(option1, option2):
        score_model = Test(option1, data)
        score_new_model = Test(option2, data)
        
        if score_model > score_new_model:
                print(score_model / 2982 , score_new_model/ 2982, option2)
                average_deviation_generations.append(score_new_model / 2982)
                print(f'Generation  / Average Deviation: {Test(model, data)/2982} / Model {model}')
                return True
        else:
                print(f"Generation {score_model/2982}, model {option1}")
                return False

model = numpy.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
def Scan(change, model, generation):
        generation += 1
        print("generation: ", generation)
        for i in range(10):
                new_model = model.copy()
                new_model[i] += change
                if Select_Best(model, new_model) == True:
                        print("+", new_model)
                        model = new_model.copy()
                        print("+", model)
                        if generation < 1000:
                                Scan(change, model, generation)
                new_model = model.copy()
                new_model[i] -= change
                if Select_Best(model, new_model) == True:
                        print("-", new_model)
                        model = new_model.copy()
                        print("-", model)
                        if generation < 1000:
                                Scan(change, model, generation)
        
                        
average_deviation_generations = []
data = Read_Data()
model = numpy.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
change = 1
generation = 0

Scan(change, model, generation)
for i in range (1000):
        pass
        
        

        
        


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