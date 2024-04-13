import random
import csv
import numpy

def Predict(genome, entres):
        consommation = 0
        #print(genome)
        #print(entres)
        consommation = numpy.sum(genome * entres[:-1]) * 50000
        #print(f"consommation : {consommation}")
        return consommation

def Modify(genome):
        genome = list(genome)
        
        genome[random.randint(0,9)] = float(random.randint(0,9))
        return genome

def Read_data():
    with open("data.csv", newline='') as file:
        dict_reader = csv.DictReader(file, delimiter=';')
        data = list(dict_reader)
        
        return numpy.array([[*(1 if i == dct["JourSemaine"] else 0 for i in range(7)), *list(dct.values())[1:]] for dct in data]).astype(float)
                                





def Test(genome, data):
        score = 0.0
        #for i in range(len(data)):
        for i in range(len(data)):
                score += abs(Predict(genome, data[i])- float(data[i][10]))
        
        return score



average_deviation_generations = []
Posan = []
Temp = []
data = Read_data()
print(data)
model = numpy.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,5.0,7.0])

for i in range (10000):
        new_model = Modify(model)
        #print(new_model)
        score_model = Test(model, data)
        score_new_model = Test(new_model, data)
        
        if score_model > score_new_model:
                model = new_model
                average_deviation_generations.append(score_new_model / 2982)
                #Posan.append(int(new_model[0:4]))
                #Temp.append(int(new_model[4:8]))
                print(f'Generation {i} / Average Deviation: {Test(model, data)/2982} _ Model {model}')
                
                
import matplotlib.pyplot as plt





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



ys3 = []

for i in range(len(data)):
        ys3.append(Predict(model, data[i]) - float(data[i][10]))


plt.plot(ys2, 'r', ys, 'g', ys3, 'y')
plt.show()
plt.close()

plt.plot(ys3, 'y')
plt.show()
plt.close()

plt.plot(Posan, 'y', Temp, 'r')
plt.show()
plt.close()