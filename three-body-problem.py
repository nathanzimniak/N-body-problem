import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D





## RÉSOLUTION DU PROBLÈME À TROIS CORPS PAR MÉTHODE RK4





## Constantes dimensionnées du système

G = 6.674e-11                   # Constante gravitationelle (N.m.kg-2)
mA, mB, mC = 2e30, 2e30, 2e30   # Masse des corps du système (kg)

## Constantes adimensionnées du système

G = G * (6e24 * (365*24*60*60)**2) / (1.496e11)**3  # Constante gravitationelle
mA, mB, mC = mA/6e24, mB/6e24, mC/6e24              # Masse des corps du système





## Fonction qui retourne un tableau avec les fonctions à intégrer

def TroisCorps(Y, t):
    # Attribution d'une colonne du tableau Y à chaque variable du système
    xA, yA, zA, xB, yB, zB, xC, yC, zC, vxA, vyA, vzA, vxB, vyB, vzB, vxC, vyC, vzC = Y     # Attribution d'une colonne du tableau Y à chaque variable du système
    # Calcul des distances entre les corps
    rAB = np.sqrt((xA-xB)**2+(yA-yB)**2+(zA-zB)**2)                                         # Distances entre les corps
    rAC = np.sqrt((xA-xC)**2+(yA-yC)**2+(zA-zC)**2)
    rBC = np.sqrt((xB-xC)**2+(yB-yC)**2+(zB-zC)**2)
    # Fonctions à intégrer
    dxAdt = vxA
    dyAdt = vyA
    dzAdt = vzA
    dxBdt = vxB
    dyBdt = vyB
    dzBdt = vzB
    dxCdt = vxC
    dyCdt = vyC
    dzCdt = vzC
    dvxAdt = -G*mB*(xA-xB)/rAB**3-G*mC*(xA-xC)/rAC**3
    dvyAdt = -G*mB*(yA-yB)/rAB**3-G*mC*(yA-yC)/rAC**3
    dvzAdt = -G*mB*(zA-zB)/rAB**3-G*mC*(zA-zC)/rAC**3
    dvxBdt = -G*mA*(xB-xA)/rAB**3-G*mC*(xB-xC)/rBC**3
    dvyBdt = -G*mA*(yB-yA)/rAB**3-G*mC*(yB-yC)/rBC**3
    dvzBdt = -G*mA*(zB-zA)/rAB**3-G*mC*(zB-zC)/rBC**3
    dvxCdt = -G*mA*(xC-xA)/rAC**3-G*mB*(xC-xB)/rBC**3
    dvyCdt = -G*mA*(yC-yA)/rAC**3-G*mB*(yC-yB)/rBC**3
    dvzCdt = -G*mA*(zC-zA)/rAC**3-G*mB*(zC-zB)/rBC**3
    return np.array([dxAdt, dyAdt, dzAdt, dxBdt, dyBdt, dzBdt, dxCdt, dyCdt, dzCdt, dvxAdt, dvyAdt, dvzAdt, dvxBdt, dvyBdt, dvzBdt, dvxCdt, dvyCdt, dvzCdt])





## Conditions initiales

ti = 0          # Temps initial (années)
tf = 10         # Temps final (années)
n = 500         # Nombre de pas
dt = (tf-ti)/n  # Temps d'un pas
# Création de la liste des valeurs de temps
T = np.linspace(ti, tf, n)

xA0 = -4        # Positions initiales (UA)
yA0 = 0
zA0 = -4
xB0 = 0
yB0 = 4
zB0 = 4
xC0 = 0
yC0 = 0
zC0 = 0
vxA0 = 1        # Vitesses initiales (UA/ans)
vyA0 = -1
vzA0 = 1
vxB0 = 0
vyB0 = 2
vzB0 = -0.5
vxC0 = 0
vyC0 = 0.5
vzC0 = 0
# Création de la liste des positions et des vitesses initiales
Y0 = (xA0, yA0, zA0, xB0, yB0, zB0, xC0, yC0, zC0, vxA0, vyA0, vzA0, vxB0, vyB0, vzB0, vxC0, vyC0, vzC0)




## Calcul des positions et des vitesses par méthode RK4

def RK4(f, Y0, T):
    #Création du tableau contenant les positions et les vitesses
    Y = np.zeros([len(T),len(Y0)])
    #Initialisation des variables de position et de vitesse
    Y[0,:] = Y0
    #Calcul des nouvelles valeurs de positions et de vitesses à chaque temps
    for k in range(1, len(T)):
        # Calcul des fonctions de la méthode RK4
        k1 = dt * f(Y[k-1], T[k-1])
        k2 = dt * f(Y[k-1]+0.5*k1, T[k-1] + dt/2)
        k3 = dt * f(Y[k-1]+0.5*k2, T[k-1] + dt/2)
        k4 = dt * f(Y[k-1]+k3, T[k-1] + dt)
        # Ajout des nouvelles valeurs de positions et de vitesses à la liste
        Y[k,:] = Y[k-1] + (k1+2*k2+2*k3+k4)/6
    return Y

# Création du tableau des solutions
Y = RK4(TroisCorps, Y0, T)

# Attribution d'une ligne de la transposée du tableau Y à chaque variable du système pour la lecture des solutions
xA, yA, zA, xB, yB, zB, xC, yC, zC, vxA, vyA, vzA, vxB, vyB, vzB, vxC, vyC, vzC = Y.T





## Calcul de la position du centre de masse (optionnel)

xCM = (mA*xA + mB*xB + mC*xC) / (mA + mB + mC)
yCM = (mA*yA + mB*yB + mC*yC) / (mA + mB + mC)
zCM = (mA*zA + mB*zB + mC*zC) / (mA + mB + mC)



#### Plot 2D
##
##ax = plt.axes() 
##
##ax.plot(xA, yA, "o-", label = "Corps 1", color = "#FFEAAE", markersize = 15, markevery = 10000, markerfacecolor = "#F0B200", lw = 2)    # Plot des trajectoires
##ax.plot(xB, yB, "o-", label = "Corps 2", color = "#FFB581", markersize = 8, markevery = 10000, markerfacecolor = "#EF6200", lw = 2)
##ax.plot(xC, yC, "o-", label = "Corps 3", color = "#96D7FF", markersize = 6, markevery = 10000, markerfacecolor = "#0097F3", lw = 2)
##
##ax.axis('square')
##ax.set_xlim(-7, 7)
##ax.set_ylim(-7, 7)
##plt.xlabel("x (UA)")
##plt.ylabel("y (UA)")
##
##plt.legend()
##plt.grid()





## Plot 3D

fig = plt.figure()
ax = plt.axes(projection = '3d')

# Plot des trajectoires
ax.plot3D(xA, yA, zA, label = "Corps 1", color = "#F0B200")
ax.plot3D(xB, yB, zB, label = "Corps 2", color = "#EF6200")
ax.plot3D(xC, yC, zC, label = "Corps 3", color = "#0097F3")

# Plot des planètes en fin de trajectoire
ax.scatter(xA[-1], yA[-1], zA[-1], color = "#F0B200", marker = "o", s = 75)
ax.scatter(xB[-1], yB[-1], zB[-1], color = "#EF6200", marker = "o", s = 75)
ax.scatter(xC[-1], yC[-1], zC[-1], color = "#0097F3", marker = "o", s = 75)


# Paramètres du graphe
ax.set_xlim3d(-7, 7)
ax.set_ylim3d(-7, 7)
ax.set_zlim3d(-7, 7)
ax.set_xlabel("x (UA)")
ax.set_ylabel("y (UA)")
ax.set_zlabel("z (UA)")
plt.legend()





#### Animation 2D
##
##fig = plt.figure()
##ax = plt.axes() 
##
##corpsA_trail = 50  # Longueur de trainée
##corpsB_trail = 50
##corpsC_trail = 10
##
##def Init2D():         # Plot le fond de chaque frame
##    ligne2DA.set_data([], [])
##    ligne2DB.set_data([], [])
##    ligne2DC.set_data([], [])
##    temps2D.set_text("")
##    return (ligne2DA, ligne2DB, ligne2DC, temps2D)
##
##def Animate2D(i):     # Plot la position à chaque frame
##    ligne2DA.set_data(xA[i:max(1,i-corpsA_trail):-1], yA[i:max(1,i-corpsA_trail):-1])
##    ligne2DB.set_data(xB[i:max(1,i-corpsB_trail):-1], yB[i:max(1,i-corpsB_trail):-1])
##    ligne2DC.set_data(xC[i:max(1,i-corpsC_trail):-1], yC[i:max(1,i-corpsC_trail):-1])
##    t = "Temps = " + str(round(T[i],1)) + " années"
##    temps2D.set_text(t)
##    return (ligne2DA, ligne2DB, ligne2DC)
##
##ligne2DA, = ax.plot([], [], "o-", label = "Corps 1", color = "#FFEAAE", markersize = 10, markevery = 10000, markerfacecolor = "#F0B200", lw = 2)
##ligne2DB, = ax.plot([], [], "o-", label = "Corps 2", color = "#FFB581", markersize = 10, markevery = 10000, markerfacecolor = "#EF6200", lw = 2)
##ligne2DC, = ax.plot([], [], "o-", label = "Corps 3", color = "#96D7FF", markersize = 10, markevery = 10000, markerfacecolor = "#0097F3", lw = 2)
##
##ax.axis('square')
##ax.set_xlim(-7, 7)
##ax.set_ylim(-7, 7)
##plt.xlabel("x (UA)")
##plt.ylabel("y (UA)")
##
##temps2D = ax.text(0, 7.5, "", horizontalalignment = "center", verticalalignment = "center")
##
##anim2D = animation.FuncAnimation(fig, Animate2D, init_func = Init2D, frames = len(T), interval = 30, blit = False)
##
##plt.legend(bbox_to_anchor=(1, 1), loc = 'upper left')
##plt.grid()





## Animation 3D

fig = plt.figure()
ax = plt.axes(projection = '3d')

corpsA_trail = 50  # Longueur de trainée
corpsB_trail = 50
corpsC_trail = 50

# Plot la position à chaque frame
def Animate3D(i):
    ligne3DA.set_data(xA[i:max(1,i-corpsA_trail):-1], yA[i:max(1,i-corpsA_trail):-1])
    ligne3DA.set_3d_properties(zA[i:max(1,i-corpsA_trail):-1])
    ligne3DB.set_data(xB[i:max(1,i-corpsB_trail):-1], yB[i:max(1,i-corpsB_trail):-1])
    ligne3DB.set_3d_properties(zB[i:max(1,i-corpsB_trail):-1])
    ligne3DC.set_data(xC[i:max(1,i-corpsC_trail):-1], yC[i:max(1,i-corpsC_trail):-1])
    ligne3DC.set_3d_properties(zC[i:max(1,i-corpsC_trail):-1])
    t = "Temps = " + str(round(T[i],1)) + " années"
    temps3D.set_text(t)
    return (ligne3DA, ligne3DB, ligne3DC)

ligne3DA, = ax.plot([], [], "o-", label = "Corps 1", color = "#F0B200", markersize = 10, markevery = 10000, markerfacecolor = "#F0B200", lw = 2)
ligne3DB, = ax.plot([], [], "o-", label = "Corps 2", color = "#EF6200", markersize = 10, markevery = 10000, markerfacecolor = "#EF6200", lw = 2)
ligne3DC, = ax.plot([], [], "o-", label = "Corps 3", color = "#0097F3", markersize = 10, markevery = 10000, markerfacecolor = "#0097F3", lw = 2)

anim3D = animation.FuncAnimation(fig, Animate3D, frames = len(T), interval = 30, blit = False)

# Affiche le temps passé
temps3D = ax.text(0, 9, 9, "", horizontalalignment = "center", verticalalignment = "center")

# Paramètres du graphe
ax.set_xlim3d(-7, 7)
ax.set_ylim3d(-7, 7)
ax.set_zlim3d(-7, 7)
ax.set_xlabel("x (UA)")
ax.set_ylabel("y (UA)")
ax.set_zlabel("z (UA)")
plt.legend(bbox_to_anchor=(1, 1), loc = 'upper left')





# Affiche les graphes
plt.show()
