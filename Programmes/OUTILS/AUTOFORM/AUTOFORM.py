from PIL import Image
import numpy as np
from copy import deepcopy
import time
from math import *
import imageio
from random import *
import os
import sys
import threading

PROB=2


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



def gen(g,p,q,Ie,Je,Is,Js):
    cu1,nxt1=[],[]
    cu2,nxt2=[],[]
    g1={}
    g1[Ie,Je]=1
    g2={}
    g2[Is,Js]=1
    g[Ie,Je]=1
    g[Is,Js]=1
    if possible(g,Ie,Je+1,p,q):
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
        for k in cu1:
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
        for k in cu2:
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
    for i in range(p):
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
        gen({},p,q,Ie,Je,Is,Js)
    return g











def ckoa(pix):
    if pix[0]==255 and pix[1]==0 and pix[2]==0:
        return "start"
    if pix[0]==0 and pix[1]==255 and pix[2]==0:
        return "end"
    if 100>pix[0]:
        return "mur"
    return "chemin"

def converter(tab):
    g={}
    temp=[]
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            temp=[]
            if i>0 and (ckoa(tab[i-1][j])=="chemin" or ckoa(tab[i-1][j])=="end" or ckoa(tab[i-1][j])=="start"):
                temp.append((i-1,j))
            if i<len(tab)-1 and (ckoa(tab[i+1][j])=="chemin" or ckoa(tab[i+1][j])=="end" or ckoa(tab[i+1][j])=="start"):
                temp.append((i+1,j))
            if j>0 and (ckoa(tab[i][j-1])=="chemin" or ckoa(tab[i][j-1])=="end" or ckoa(tab[i][j-1])=="start"):
                temp.append((i,j-1))
            if j<len(tab[0])-1 and (ckoa(tab[i][j+1])=="chemin" or ckoa(tab[i][j+1])=="end" or ckoa(tab[i][j+1])=="start"):
                temp.append((i,j+1))
            if (ckoa(tab[i][j])=="chemin" or ckoa(tab[i][j])=="end" or ckoa(tab[i][j])=="start"):
                g[(i,j)]=temp
                temp=[]
    return g




def solv(g,RETOURS,SAVTEMP,MAXSAVEDINTERETAP,INRVALCAP,tab,Ie,Je,Is,Js):
    a=0
    b=0
    cur,nxt=[],[]
    for i in g:
        if len(g[i])<2 and not (i == (Ie, Je) or i == (Is, Js)):
            nxt.append(i)
    while not nxt==[]:
        cur,nxt=nxt,[]
        for i in cur:
            if i in g:
                t=g[i]
                for j in t:
                    l=g[j]
                    l.remove(i)
                    g[j]=l
                    if len(l)<2 and not (i == (Ie, Je) or i == (Is, Js)):
                        nxt.append(j)
                del g[i]
        a+=1







def sav(g,nom,tab,Ie,Je,Is,Js):
    ta=deepcopy(tab)
    for c in g:
        i,j=c
        ta[i][j]=[0,0,255]
    ta[Ie][Je]=[255,0,0]
    ta[Is][Js]=[0,255,0]
    imageio.imwrite(nom+".png", ta)




def genere(nom,p,q,Ie,Je,Is,Js):
    ta=np.full((p, q, 3), [0, 0, 0], dtype=np.uint8)
    g=gen({},p,q,Ie,Je,Is,Js)
    for c in g:
        i,j=c
        ta[i][j]=[255,255,255]
    ta[Ie][Je]=[255,0,0]
    ta[Is][Js]=[0,255,0]
    imageio.imwrite(nom+".png", ta)





def AUTOFORM1(nom,p,q,Ie,Je,Is,Js):
    genere(nom,p,q,Ie,Je,Is,Js)
    im=Image.open(nom+".png")
    tab=np.array(im)
    g=converter(tab)
    solv(g,False,False,1,1,tab,Ie,Je,Is,Js)
    sav(g,nom+" solution",tab,Ie,Je,Is,Js)


def agrandis(Name,multi,multj):
    im=Image.open(Name)
    tab=np.array(im)
    ta=np.full((len(tab)*multi, len(tab[0])*multj, 3), [0, 0, 0], dtype=np.uint8)
    for i in range(len(ta)):
        for j in range(len(ta[0])):
            ta[i][j]=tab[i//multi][j//multj]
    imageio.imwrite(Name, ta)


def Auto1(nom,p,q,multi,multj):
    AUTOFORM1(str(nom),p,q,0,0,p-1,q-1)
    agrandis(str(nom)+".png",multi,multj)
    agrandis(str(nom)+" solution"+".png",multi,multj)

def AUTOFOMULT(NOMLIST,p,q,multi,multj):
    for nom in NOMLIST:
        Auto1(nom,p,q,multi,multj)


        #thread = threading.Thread(target=Auto1, args=(nom,p,q,multi,multj,))
        #thread.start()



Auto1("40 par 40",40,40,1,1)



##AUTOFOMULT(["Diapo "+str(i) for i in range(1,2)],441,784,5,5)







