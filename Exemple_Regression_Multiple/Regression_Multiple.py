# Ce programme est un exemple de régression Multi-Linéaire (sans évalution du modèle)

# Les Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression



# Importion des données de Advertising.csv
donnees = pd.read_csv('Advertising.csv', index_col=0)
print("")
print("Aperçu des données : ")
print(donnees.head())


# Création de y (variable reponse) et X (les covariables)
list_var = donnees.columns.drop("Sales") #Index de toutes les colones de data sauf 'Sales'
y = donnees.Sales
X = donnees[list_var]

# Création  d'un objet modeleReg pour recuperer les paramètres estimimer
modeleReg = LinearRegression()
# Régression (réalisation de l'interpolation)
modeleReg.fit(X,y)
# Récupération des coefs estimés et du score R2
a =  modeleReg.coef_  #En effet : a = [a1, a2, a3]
b =  modeleReg.intercept_
R2 = modeleReg.score(X,y)

# Prédiction
#y_fit = np.dot(X, a) + b #De manière analytique (à la main) ou ...
y_fit = modeleReg.predict(X) #Prédiction directement avec la method engendré par LinearRegression 

# Calcul du RMSE:
RMSE = np.sqrt(((y-y_fit)**2).sum()/len(y))



# Affichage des paramètres estimés dans le terminal
print("")
print("Le modèle est définie par : y = a1*TV + a2*Radio + a3*Newspaper + b")
print("Avec : b = ", b)
print("Et a = [a1, a2, a3] = ", a)
print("") 
print("Le coef de détermination de la régression vaut R² =", R2)
print("Le RMSE =", RMSE)


# Tracer des graphiques
plt.figure("y Préditent")
plt.plot(y, y_fit,'.')
plt.title('Valeurs préditent en fonction des reponses')
plt.xlabel('variables réponses (y)')
plt.ylabel('valeurs préditent (y_fit)')

plt.figure("Résidus modèle")
plt.plot(y_fit, y-y_fit,'.')
plt.title('Résidus du modèle en fonction des valeurs préditent')
plt.xlabel('valeurs préditent (y_fit)')
plt.ylabel('résidus (y-y_fit)')
plt.show()

