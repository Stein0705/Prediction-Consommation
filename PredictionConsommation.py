import random
import csv
import time

def Predict(genome, entres):
        consommation = 0
        if int(genome[44:45]) < 5: 
                consommation += int(genome[0:4])/5000 * float(entres["Posan"])
        else:
                consommation -= int(genome[0:4])/5000 * float(entres["Posan"])
        if int(genome[45:46]) < 5: 
                consommation += int(genome[4:8])/5000 * ((float(entres["Temperature"])+10)/30)
        else:
                consommation -= int(genome[4:8])/5000 * ((float(entres["Temperature"])+10)/30)
        if int(genome[46:47]) < 5:
                consommation += int(genome[8:16])/5000 * float(entres["JourFerie"])
        else:
                consommation -= int(genome[8:16])/5000 * float(entres["JourFerie"])
        if int(genome[47:48]) < 5:
                if entres["JourSemaine"] == 0:
                        consommation += int(genome[16:20])/10000
        else:
                if entres["JourSemaine"] == 0:
                        consommation -= int(genome[16:20])/10000
        if int(genome[48:49]) < 5:
                if entres["JourSemaine"] == 1:
                        consommation += int(genome[20:24])/10000
        else:
                if entres["JourSemaine"] == 1:
                        consommation -= int(genome[20:24])/10000
        if int(genome[49:50]) < 5:
                if entres["JourSemaine"] == 2:
                        consommation +=  int(genome[24:28])/10000
        else:
                if entres["JourSemaine"] == 2:
                        consommation -=  int(genome[24:28])/10000
        if int(genome[50:51]) < 5:
                if entres["JourSemaine"] == 3:
                        consommation += int(genome[28:32])/10000
        else: 
                if entres["JourSemaine"] == 3:
                        consommation -= int(genome[28:32])/10000
        if int(genome[51:52]) < 5:
                if entres["JourSemaine"] == 4:
                        consommation += int(genome[32:36])/10000
        else:
                if entres["JourSemaine"] == 4:
                        consommation -= int(genome[32:36])/10000
        if int(genome[52:53]) < 5:
                if entres["JourSemaine"] == 5:
                        consommation += int(genome[36:40])/10000
        else:
                if entres["JourSemaine"] == 5:
                        consommation -= int(genome[36:40])/10000
        if int(genome[53:54]) < 5:
                if entres["JourSemaine"] == 6:
                        consommation += int(genome[40:44])/10000
        else:
                if entres["JourSemaine"] == 6:
                        consommation -= int(genome[40:44])/10000

        return consommation * 50000

def Modify(genome):
        genome = list(genome)
        genome[random.randint(0,54)] = str(random.randint(0,9))
        return "".join(genome)

def Read_data():
    with open("data.csv", newline='') as file:
        dict_reader = csv.DictReader(file, delimiter=';')
        data = list(dict_reader)
    return data

def Test(genome, data):
        score = 0.0
        #for i in range(len(data)):
        for i in range(len(data)):
                score += abs(Predict(genome, data[i])- float(data[i]["CONSOMMATION"]))
        
        return score



average_deviation_generations = []
Posan = []
Temp = []
data = Read_data()

model = "0000000000000000000000000000000000000000000000000000000"

for i in range (5000):
        new_model = Modify(model)
        score_model = Test(model, data)
        score_new_model = Test(new_model, data)
        
        if score_model > score_new_model:
                model = new_model
                average_deviation_generations.append(score_new_model / 2982)
                Posan.append(int(new_model[0:4]))
                Temp.append(int(new_model[4:8]))
                print(f'Generation {i} / Model: {model} / Average Deviation: {Test(model, data)/2982}')
                
                
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
        ys2.append(float(data[i]["CONSOMMATION"]))



ys3 = []

for i in range(len(data)):
        ys3.append(Predict(model, data[i]) - float(data[i]["CONSOMMATION"]))


plt.plot(ys2, 'r', ys, 'g', ys3, 'y')
plt.show()
plt.close()

plt.plot(ys3, 'y')
plt.show()
plt.close()

plt.plot(Posan, 'y', Temp, 'r')
plt.show()
plt.close()