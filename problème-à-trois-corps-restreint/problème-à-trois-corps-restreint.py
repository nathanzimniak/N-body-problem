import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation





## RÉSOLUTION DU PROBLÈME À TROIS CORPS RESTREINT PAR MÉTHODE RK4





## Choix du référentiel (tournant par défaut, galiléen si "G")

referentiel = "G"


## Constantes du système

m1, m2 = 2e30, 2e27     # Masse des corps du système (kg)
v = 0.01 #m2/(m1+m2)    # Paramètre de masse
w = 1                   # Vitesse de rotation

## Calcul de la position des deux corps les plus massifs

P1 = [-v, 0]
P2 = [1-v, 0]


## Calcul de la position des points de Lagrange

L1 = [(1-(v/3)**(1/3)), 0]
L2 = [(1+(v/3)**(1/3)), 0]
L3 = [(-1-5*v/12),0]
L4 = [(1/2-v), np.sqrt(3)/2]
L5 = [(1/2-v), -np.sqrt(3)/2]





## Fonction qui retourne un tableau avec les fonctions à intégrer

def TroisCorps(Y, t):
    # Attribution d'une colonne du tableau Y à chaque variable du système
    x, y, vx, vy = Y
    # Calcul des distances entre le troisième corps et les deux autres corps
    d1 = np.sqrt((x+v)**2 + y**2)
    d2 = np.sqrt((x+v-1)**2 + y**2)
    # Fonctions à intégrer
    dxdt = vx + w*y
    dydt = vy - w*x
    dvxdt = w*vy - (w**2)*((1-v)*(x+v)/d1**3 + v*(x+v-1)/d2**3)
    dvydt = -w*vx - (w**2)*((1-v)*(y)/d1**3 + v*(y)/d2**3)
    return np.array([dxdt, dydt, dvxdt, dvydt])





## Fonction qui définit la zone accessible par le système

def ZA(E):
    x = np.linspace(-1.5, 1.5, 50)
    y = np.linspace(-1.5, 1.5, 50)[:,np.newaxis]
    # Calcul des distances entre le troisième corps et les deux autres corps
    d1 = np.sqrt((x+v)**2 + y**2)
    d2 = np.sqrt((x+v-1)**2 + y**2)
    # Calcul de l'énergie cinétique du troisième corps
    T = E + 0.5*(x**2 + y**2) + ((1-v)/d1) + v/d2
    # Création des lignes de niveaux
    ldn = np.linspace(-200, 200, 3)
    plt.contourf(T, ldn, extent = (-1.5, 1.5, -1.5, 1.5), cmap = "cividis")
    #Affichage des corps et points de Lagrange
    plt.plot(P1[0], P1[1],'o', label = "Corps 1", markersize = 9, markerfacecolor = "#F0B200", markeredgecolor = "#FFEAAE")
    plt.plot(P2[0], P2[1],'o', label = "Corps 2", markersize = 9, markerfacecolor = "#EF6200", markeredgecolor = "#FFB581")
    plt.plot(L1[0], L1[1],'o', label = "Points de Lagrange", markersize = 3, markerfacecolor = "#FF0000", markeredgecolor = "#FF0000")
    plt.plot(L2[0], L2[1],'o', markersize = 3, markerfacecolor = "#FF0000", markeredgecolor = "#FF0000")
    plt.plot(L3[0], L3[1],'o', markersize = 3, markerfacecolor = "#FF0000", markeredgecolor = "#FF0000")
    plt.plot(L4[0], L4[1],'o', markersize = 3, markerfacecolor = "#FF0000", markeredgecolor = "#FF0000")
    plt.plot(L5[0], L5[1],'o', markersize = 3, markerfacecolor = "#FF0000", markeredgecolor = "#FF0000")
    plt.legend(bbox_to_anchor = (1, 1), loc = "upper left")
    # Paramètres du graphe
    plt.axis("square")
    plt.title(rf'$\nu$= {v}' + f"\n T = {E:4.2f} + V(x,y)")
    plt.xlabel('$x$')
    plt.ylabel('$y$')





## Conditions initiales du système

ti = 0                      # Temps initial (années)
tf = 10                     # Temps final (années)
n = 250                     # Nombre de pas
dt = (tf-ti)/n              # Temps d'un pas
T = np.linspace(ti, tf, n)  # Création de la liste des valeurs de temps

x0, y0 = 1/2-v, -0.75       # Positions initiales
vx0, vy0 = -y0, x0          # Vitesses initiales
Y0 = (x0, y0, vx0, vy0)     # Création de la liste des positions et des vitesses initiales




## Calcul des positions et des vitesses par méthode RK4

def RK4(f, Y0, T):
    # Création du tableau contenant les positions et les vitesses
    Y = np.zeros([len(T),len(Y0)])
    # Initialisation des variables de position et de vitesse
    Y[0,:] = Y0
    # Calcul des nouvelles valeurs de positions et de vitesses à chaque temps
    for k in range(1, len(T)):
        # Calcul des fonctions de la méthode RK4
        k1 = dt * f(Y[k-1], T[k-1])
        k2 = dt * f(Y[k-1]+0.5*k1, T[k-1] + dt/2)
        k3 = dt * f(Y[k-1]+0.5*k2, T[k-1] + dt/2)
        k4 = dt * f(Y[k-1]+k3, T[k-1] + dt)
        # Ajout des nouvelles valeurs de positions et de vitesses à la liste
        Y[k,:] = Y[k-1] + (k1+2*k2+2*k3+k4)/6
    return Y

Y = RK4(TroisCorps, Y0, T)  # Création du tableau des solutions
x, y, vx, vy = Y.T          # Attribution d'une ligne de la transposée du tableau Y à chaque variable du système pour la lecture des solutions





## Animation 2D

fig = plt.figure()
ax = plt.axes() 


# Fonction qui retourne la position à chaque frame

def Animation(i):
    t = "Temps = " + str(round(T[i],1)) + " années"
    temps.set_text(t)
    if referentiel == "G":
        # Position des corps
        ligne1.set_data(P1[0]*np.cos(T[i]), P1[0]*np.sin(T[i]))
        ligne2.set_data(P2[0]*np.cos(T[i]), P2[0]*np.sin(T[i]))
        ligne3.set_data(x[i]*np.cos(T[i]) - y[i]*np.sin(T[i]), x[i]*np.sin(T[i]) + y[i]*np.cos(T[i]))
        # Position des points de Lagrange
        ligneL1.set_data(L1[0]*np.cos(T[i]), L1[0]*np.sin(T[i]))
        ligneL2.set_data(L2[0]*np.cos(T[i]), L2[0]*np.sin(T[i]))
        ligneL3.set_data(L3[0]*np.cos(T[i]), L3[0]*np.sin(T[i]))
        ligneL4.set_data(L4[0]*np.cos(T[i]) - L4[1]*np.sin(T[i]), L4[0]*np.sin(T[i]) + L4[1]*np.cos(T[i]))
        ligneL5.set_data(L5[0]*np.cos(T[i]) - L5[1]*np.sin(T[i]), L5[0]*np.sin(T[i]) + L5[1]*np.cos(T[i]))
        return (ligne1, ligne2, ligne3, ligneL1, ligneL2, ligneL3, ligneL4, ligneL5)
    else:
        # Position du troisième corps
        ligne3.set_data(x[i], y[i])
        return ligne3


# Fonction qui retourne la zone accessible à chaque frame

def anim_ZA():
	E = np.arange(-3, 1, 0.03)  # Choix arbitraire d'une plage d'énergies
	for Energie in E:
		plt.clf()
		ZA(Energie)
		plt.pause(0.03)


# Plot la position

if referentiel == "G":
    titre = "Référentiel Galiléen"
    # Position des corps
    ligne1, = ax.plot([], [], "o", label = "Corps 1", color = "#FFEAAE", markersize = 10, markevery = 10000, markerfacecolor = "#F0B200", zorder = 3)
    ligne2, = ax.plot([], [], "o", label = "Corps 2", color = "#FFB581", markersize = 8, markevery = 10000, markerfacecolor = "#EF6200", zorder = 3)
    ligne3, = ax.plot([], [], "o", label = "Corps 3", color = "#96D7FF", markersize = 5, markevery = 10000, markerfacecolor = "#0097F3", zorder = 3)
    # Position des points de Lagrange
    ligneL1, = ax.plot([], [], "o", label = "Pts de L", color = "#FF0000", markersize = 3, markevery = 10000, markerfacecolor = "#FF0000", zorder = 2)
    ligneL2, = ax.plot([], [], "o", color = "#FF0000", markersize = 3, markevery = 10000, markerfacecolor = "#FF0000", zorder = 2)
    ligneL3, = ax.plot([], [], "o", color = "#FF0000", markersize = 3, markevery = 10000, markerfacecolor = "#FF0000", zorder = 2)
    ligneL4, = ax.plot([], [], "o", color = "#FF0000", markersize = 3, markevery = 10000, markerfacecolor = "#FF0000", zorder = 2)
    ligneL5, = ax.plot([], [], "o", color = "#FF0000", markersize = 3, markevery = 10000, markerfacecolor = "#FF0000", zorder = 2)
else:
    titre = "Référentiel tournant"
    # Position des corps
    ax.plot(P1[0], 0, "o", label = "Corps 1", markersize = 9, markerfacecolor = "#F0B200", markeredgecolor = "#FFEAAE", zorder = 3)
    ax.plot(P2[0], 0, "o", label = "Corps 2", markersize = 9, markerfacecolor = "#EF6200", markeredgecolor = "#FFB581", zorder = 3)
    ligne3, = ax.plot([], [], "o", label = "Corps 3", color = "#96D7FF", markersize = 5, markevery = 10000, markerfacecolor = "#0097F3", zorder = 3)
    # Position des points de Lagrange
    ax.plot(L1[0], 0, "o", label = "Pts de L", markersize = 3, markerfacecolor = "#FF0000", markeredgecolor = "#FF0000", zorder = 2)
    ax.plot(L2[0], 0, "o", markersize = 3, markerfacecolor = "#FF0000", markeredgecolor = "#FF0000", zorder = 2)
    ax.plot(L3[0], 0, "o", markersize = 3, markerfacecolor = "#FF0000", markeredgecolor = "#FF0000", zorder = 2)
    ax.plot(L4[0], L4[1], "o", markersize = 3, markerfacecolor = "#FF0000", markeredgecolor = "#FF0000", zorder = 2)
    ax.plot(L5[0], L5[1], "o", markersize = 3, markerfacecolor = "#FF0000", markeredgecolor = "#FF0000", zorder = 2)


# Plot le temps passé

temps = ax.text(0, 1.8, "", horizontalalignment = "center", verticalalignment = "center")


# Fonction d'animation

anim = animation.FuncAnimation(fig, Animation, frames = len(T), interval = 30, blit = False)

# Paramètre du graphe

ax.axis("square")
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
plt.xlabel("x")
plt.ylabel("y")

plt.title(titre)
plt.legend(bbox_to_anchor = (1, 1), loc = "upper left")
plt.grid()

plt.show()

# Enregistrement de l'animation ?
choix = input("Voulez vous transformer l'animation en GIF?(Oui ou Non) : ")

if (choix.lower() == "oui"):                                                                # Transformation de l'input en minuscules
	anim.save(f"nu_{v}_{referentiel}.gif", writer = animation.PillowWriter(fps = 30))   # Sauvegarde de l'animation et conversion en GIF


#Dessin de la zone accessible
anim_ZA()
