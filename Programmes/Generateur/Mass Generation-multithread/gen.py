from PIL import Image
import numpy as np
from copy import deepcopy
import time
from math import *
import imageio
from random import *
import threading
import os
import sys
print("WARNING /!\ Ce script génère automatiquement un grand nombre de labyrinthes, chacun sur un thread différent.")

PROB=2


t0=time.time()



def ckoa(pix):     #Reconnaissance de mur/chemin/fin/départ.
    if pix[0]==0 and pix[1]==0 and pix[2]==255:
        return "hypermur"
    if 100>pix[0]:
        return "mur"
    return "chemin"

def merge(g1,g2):
    for c in g2:
        g1[c]=g2[c]
    return g1


def adj(g,i,j):
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

def possible(g,i,j,p,q):
    return i>=0 and j>=0 and i<p and j<q and not ((i,j) in g) and adj(g,i,j)==1




"""On fait "pousser" deux arbres de chemins différents que l'on rejoint en un unique point de leur frontière."""
def gen(p,q,Ie,Je,Is,Js):     #Génère à partir d'une entrée et d'une sortie.
    g={}
    cu1,nxt1=[],[]
    cu2,nxt2=[],[]      #"cu" et "nxt" contiennent les chemins possibles respectivement à l'instant courant et à l'instant suivant.
    g1={}
    g1[Ie,Je]=1
    g2={}
    g2[Is,Js]=1
    g[Ie,Je]=1
    g[Is,Js]=1
    if possible(g,Ie,Je+1,p,q):         #On indexe les murs adjacents à l'entrée et à la sortie qui sont susceptibles de se transformer en chemin.
        nxt1.append((Ie,Je+1))
    if possible(g,Ie,Je-1,p,q):
        nxt1.append((Ie,Je-1))
    if possible(g,Ie+1,Je,p,q):
        nxt1.append((Ie+1,Je))
    if possible(g,Ie-1,Je,p,q):
       nxt1.append(Ie-1,Je)
    if possible(g,Is,Js+1,p,q):
        nxt2.append((Is,Js+1))
    if possible(g,Is,Js-1,p,q):
        nxt2.append((Is,Js-1))
    if possible(g,Is+1,Js,p,q):
        nxt2.append((Is+1,Js))
    if possible(g,Is-1,Js,p,q):
        nxt2.append((Is-1,Js))
    while not (nxt1==[] and nxt2==[]):
        cu1,nxt1=nxt1,[]
        cu2,nxt2=nxt2,[]
        for k in cu1:                    #On fait "pousser" "l'arbre" de l'entrée.                
            i,j=k
            if possible(g,i,j,p,q) and randint(0,PROB)==1:
                g[k]=1
                g1[k]=1
                if possible(g,i,j+1,p,q):
                    nxt1.append((i,j+1))
                if possible(g,i,j-1,p,q):
                   nxt1.append((i,j-1))
                if possible(g,i+1,j,p,q):
                    nxt1.append((i+1,j))
                if possible(g,i-1,j,p,q):
                    nxt1.append((i-1,j))
            else:
                if possible(g,i,j,p,q):
                    nxt1.append((i,j))
        for k in cu2:                    #On fait "pousser" "l'arbre" de la sortie. 
            i,j=k
            if possible(g,i,j,p,q) and randint(0,PROB)==1:
                g[k]=1
                g2[k]=1
                if possible(g,i,j+1,p,q):
                    nxt2.append((i,j+1))
                if possible(g,i,j-1,p,q):
                   nxt2.append((i,j-1))
                if possible(g,i+1,j,p,q):
                    nxt2.append((i+1,j))
                if possible(g,i-1,j,p,q):
                    nxt2.append((i-1,j))
            else:
                if possible(g,i,j,p,q):
                    nxt2.append((i,j))
    l=[]
    for i in range(p):                    #On fusionne les deux "arbres" sur un point unique.
        for j in range(q):
            nb=0
            b1=False
            b2=False
            if (i-1,j) in g:
                nb+=1
            if (i-1,j) in g1:
                b1=True
            if (i-1,j) in g2:
                b2=True
            if (i+1,j) in g:
                nb+=1
            if (i+1,j) in g1:
                b1=True
            if (i+1,j) in g2:
                b2=True
            if (i,j+1) in g:
                nb+=1
            if (i,j+1) in g1:
                b1=True
            if (i,j+1) in g2:
                b2=True
            if (i,j-1) in g:
                nb+=1
            if (i,j-1) in g1:
                b1=True
            if (i,j-1) in g2:
                b2=True
            if b1 and b2 and nb==2:
                l.append((i,j))
    if len(l)>0:
        n=randint(0,len(l)-1)
        g[l[n]]=1
    else:
        gen(p,q,Ie,Je,Is,Js)
    return g





def genere(nom,p,q,Ie,Je,Is,Js):
    ta=np.full((p, q, 3), [0, 0, 0], dtype=np.uint8)
    g=gen(p,q,Ie,Je,Is,Js)
    for c in g:
        i,j=c
        ta[i][j]=[255,255,255]
    ta[Ie][Je]=[255,0,0]
    ta[Is][Js]=[0,255,0]
    imageio.imwrite(nom+".png", ta)

print(time.time()-t0)

for i in range(10):
    tread=threading.Thread(target=genere, args=((str(i),100,100,0,0,99,99)))
    tread.start()
print("launched")