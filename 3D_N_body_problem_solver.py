#!/usr/bin/env python3
# coding: utf-8

'''
Programme pour résoudre le problème à N corps
'''

__author__ = 'Nathan Zimniak'


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.integrate import odeint
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import time
start_time = time.time()




#Initialisation des constantes
N = 20                                                          #Nombre de corps
ti = 0                                                          #Temps initial
tf = 10                                                         #Temps final
n = 500                                                         #Nombre d'itérations temporelles
dt = (tf-ti)/n                                                  #Pas temporel
T = np.linspace(ti, tf, n)                                      #Liste des temps
G = 6.674e-11 * (6e24 * (365*24*60*60)**2) / (1.496e11)**3      #Constante gravitationnelle
M = np.random.uniform(low=6e24, high=2e30, size=N) / 6e24       #Masses


#Création du tableau des solutions
R0 = np.random.uniform(low=-7, high=7, size=3*N)
V0 = np.random.uniform(low=-5, high=5, size=3*N)
Y0 = np.append(R0,V0)                               #Conditions initiales



def NCorps(Yk, t):
    ''' Calcule la liste contenant les fonctions à intégrer (vitesses et accélérations)
        ----------
        :param Yk: liste, liste des fonctions à intégrer à la k-ième itération
        :param t: liste, liste des temps
        :return Sk: liste, liste des fonctions à intégrer
        ----------
    '''
    #Place les positions dans un tableau 2D pour plus de praticité
    Rk = np.zeros((3,N))
    a = 0
    b = 0
    c = 0
    for i in range(0,3*N):
        if i%3 == 0:
            Rk[0,a] = Yk[i]
            a = a+1
        if i%3 == 1:
            Rk[1,b] = Yk[i]
            b = b+1
        if i%3 == 2:
            Rk[2,c] = Yk[i]
            c = c+1
    #Création de la liste contenant les fonctions à intégrer
    Sk = []
    for i in range(3*N, 6*N):
            Sk.append(Yk[i])
    for i in range(0, N):
        axk = 0
        ayk = 0
        azk = 0
        for j in range(0, N):
            if j != i:
                axk = axk - G*M[j]*(Rk[0,i]-Rk[0,j])/(((Rk[0,i]-Rk[0,j])**2+(Rk[1,i]-Rk[1,j])**2+(Rk[2,i]-Rk[2,j])**2)**(3/2)+1e-1)
                ayk = ayk - G*M[j]*(Rk[1,i]-Rk[1,j])/(((Rk[0,i]-Rk[0,j])**2+(Rk[1,i]-Rk[1,j])**2+(Rk[2,i]-Rk[2,j])**2)**(3/2)+1e-1)
                azk = azk - G*M[j]*(Rk[2,i]-Rk[2,j])/(((Rk[0,i]-Rk[0,j])**2+(Rk[1,i]-Rk[1,j])**2+(Rk[2,i]-Rk[2,j])**2)**(3/2)+1e-1)
        Sk.append(axk)
        Sk.append(ayk)
        Sk.append(azk)
    return Sk



Y = odeint(NCorps, Y0, T)





## Animation 2D

plt.style.use('dark_background')
fig = plt.figure()
ax = plt.axes()
ax.axis('square')
ax.set_xlim(np.min(R0)-10, np.max(R0)+10)
ax.set_ylim(np.min(R0)-10, np.max(R0)+10)
plt.xlabel("x (UA)")
plt.ylabel("y (UA)")

trail = 50

def Animate2D(k):
    for i, ligne in enumerate(lignes, 0):
        ligne.set_data(Y[k:max(1, k - trail):-1, 3*i], Y[k:max(1, k - trail):-1, 3*i+1])
    plt.title("Problème à " + str(N) + " corps à t = " + str(round(T[k],1)) + " ans")
    return lignes

lignes = [ax.plot([], [], "o-", markersize = 3, markevery = 10000, lw = 1)[0] for _ in range(N)]

anim2D = animation.FuncAnimation(fig, Animate2D, frames = len(T), interval = 30, blit = False)

writergif = animation.PillowWriter(fps=30)
anim2D.save("2D_N_Body_Problem.gif", writer=writergif)



## Animation 3D

plt.style.use('dark_background')
fig = plt.figure()
ax = plt.axes(projection = '3d')
ax.zaxis.set_rotate_label(False)
ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
ax.grid(False)
ax.set_xlim3d(np.min(R0)-10, np.max(R0)+10)
ax.set_ylim3d(np.min(R0)-10, np.max(R0)+10)
ax.set_zlim3d(np.min(R0)-10, np.max(R0)+10)
ax.set_xlabel("x (UA)")
ax.set_ylabel("y (UA)")
ax.set_zlabel("z (UA)")

trail = 20

def Animate3D(k):
    for i, ligne in enumerate(lignes, 0):
        ligne.set_data(Y[k:max(1, k - trail):-1, 3*i], Y[k:max(1, k - trail):-1, 3*i+1])
        ligne.set_3d_properties(Y[k:max(1, k - trail):-1, 3*i+2])
    ax.view_init(azim=k/2)
    plt.title("Problème à " + str(N) + " corps à t = " + str(round(T[k],1)) + " ans")
    return lignes

lignes = [ax.plot([], [], "o-", markersize = 3, markevery = 10000, lw = 1)[0] for _ in range(N)]

anim3D = animation.FuncAnimation(fig, Animate3D, frames = n, interval = 30, blit = False, repeat = True)

writergif = animation.PillowWriter(fps=30)
anim3D.save("3D_N_Body_Problem.gif", writer=writergif)

print("%s secondes" % (time.time() - start_time))
plt.show()
