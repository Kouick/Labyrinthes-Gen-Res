from PIL import Image
import numpy as np
from copy import deepcopy
import time
from math import *
import imageio
from random import *

print("WARNING /!\ Ce script génère un labyrinthe parfait où un pixel blanc est un chemin et un pixel noir est un mur.")

SAVTEMPin=(input("Doit-on sauvegarder les étapes intermédiaires ? (True ou False)    "))
RETOURSin=(input("Doit-on recevoir des retours dans la console ? (True ou False)    "))
SAVTEMP=SAVTEMPin=="True"
RETOURS=RETOURSin=="True"
MAXSAVEDINTERETAP=int(input("Combien au maximum d'étapes intermédiaires souhaitez-vous sauvegarder en images ?   "))
NOMFINAL=str(input("Quel nom souhaitez-vous donner au fichier de sauvegarde du labyrinthe généré ?   "))
SIZEP=int(input("Taille (abscisse) en pixels du labyrinthe généré :   "))
SIZEQ=int(input("Taille (ordonnée) en pixels du labyrinthe généré :   "))
PROB=int(input("Probabilité qu'un mur soit converti en chemin : un chiffre plus grand implique un labyrinthe plus aléatoire et un temps de génération plus long (par exemple, un mur a une chance de se convertir de environ 1/nombre entré).   "))


g={}




def fus(ta,p,q):
    for i in range(ta):
        for j in range(ta[0]):
            tab[i+p][j+q]=ta[i][j]

def ckoa(pix):     #Reconnaissance de mur/chemin.
    if pix[0]==0 and pix[1]==0 and pix[2]==255:
        return "hypermur"
    if 100>pix[0]:
        return "mur"
    return "chemin"




tab=[[(0,0,0)*SIZEP] for _ in range(SIZEQ)]

def adj(i,j):
    a=0
    if (i-1,j) in g:
        a+=1
    if (i+1,j) in g:
        a+=1
    if (i,j-1) in g:
        a+=1
    if (i,j+1) in g:
        a+=1
    return a

def possible(i,j,p,q):
    return i>0 and j>0 and i<p and j<q and not ((i,j) in g) and adj(i,j)==1

sta=0,0
def gen(p,q,Ie,Je):     #Propage l'arbre du labyrinthe à partir d'un seul point.
    cu,nxt=[],[]
    g={}
    if possible(Ie,Je+1,p,q):
        nxt.append(Ie,Je+1)
    if possible(Ie,Je-1,p,q):
        nxt.append(Ie,Je-1)
    if possible(Ie+1,Je,p,q):
        nxt.append(Ie+1,Je)
    if possible(Ie-1,Je,p,q):
        nxt.append(Ie-1,Je)
    g[Ie,Je]=1
    while not nxt==[]:
        cu,nxt=nxt,[]
        for k in cu:
            i,j=k
            if possible(i,j,p,q) and randint(0,PROB)==1:
                g[k]=1
                if possible(i,j+1,p,q):
                    nxt.append(i,j+1)
                if possible(i,j-1,p,q):
                   nxt.append(i,j-1)
                if possible(i+1,j,p,q):
                    nxt.append(i+1,j)
                if possible(i-1,j,p,q):
                    nxt.append(i-1,j)
    return g