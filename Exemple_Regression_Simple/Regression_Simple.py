# Les Imports
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


# Les Fonctions
def predict(x_points):
    return a * x_points + b


# Le programme principale ------------------------------------6----------------

# Importation du DataSet
data = pd.read_csv('Data_Meteo_US.csv', delimiter=";")
print(data.head())
print("")
print("La taille du fichier est : ", len(data))
print("")

X =  data.actual_min_temp # selection de la première colonne de notre dataset
Y =  data.average_min_temp # selection de la deuxieme colonne de notre dataset

# Regression
a, b, r_value, p_value, std_err = stats.linregress(X, Y)
Y_Fit = a * X + b

# Tracer des graphiques
axes = plt.axes()
#axes.set_xlim([2, 25])
#axes.set_ylim([0, 30])
axes.grid()
plt.scatter(X,Y, label="Nuage (X, Y)")
plt.plot(X, Y_Fit,  c='r', label="Droite de Régression")
plt.text(10, 50, r"Le coeff R**2 = " + str(r_value**2))
plt.title('Exemple de Regression Lineaire Simple')
plt.xlabel('X --> Min temp actuel')
plt.ylabel('Y --> Moy des temp min')
plt.legend()  
plt.show()
#plt.savefig("D:/figure.png")


# Messages Console

# Coeff de determination
print("")
print("Le coeff R**2 = ", r_value**2)
print("")

# Prediction :
Val1 = 10.59
Val2 = 20.27
Val1_Predit = predict(Val1)
Val2_Predit = predict(Val2)

print("")
print("Le Y predit de ", Val1, " par le model lineaire est : ", Val1_Predit)
print("Le Y predit de ", Val2, " par le model lineaire est : ", Val2_Predit)
print("")
# -----------------------------------------------------------------------------