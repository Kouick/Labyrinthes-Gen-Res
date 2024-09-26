from PIL import Image
import numpy as np
from copy import deepcopy
import time
from math import *
import imageio
import threading
print("WARNING /!\ ce script détecte également les cycles, il n'est utilisable que sur des labyrinthes du type 'lab.jpg', la sortie et l'entrée peuvent cependant être changé de place, ce programme donne toute les solutions possibles")

t0=time.time()

def ckoa(pix):     #Reconnaissance de mur/chemin/fin/début.
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
    print("completion de la convertion en " +str(floor(time.time()-t0))+" secondes")
    return g




def solv(g,RETOURS,SAVTEMP,MAXSAVEDINTERETAP,INRVALCAP,tab):
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
        if RETOURS:
            print("étape "+str(a)+" complétée en "+str(floor(time.time()-t0))+" seconde")
        if SAVTEMP and b<MAXSAVEDINTERETAP and a%INRVALCAP==0:
            b+=1
            sav(g,str(a),tab)
##            thread=threading.Thread(target=sav, args=(deepcopy(g),str(a)))
##            thread.start()
    print("completion du labyrinth en "+str(floor(time.time()-t0))+" secondes")







def sav(g,nom,tab):
    ta=deepcopy(tab)
    for c in g:
        i,j=c
        ta[i][j]=[0,0,255]
    ta[Ie][Je]=[255,0,0]
    ta[Is][Js]=[0,255,0]
    imageio.imwrite(nom+".png", ta)
    print("fichier suvegardé apres " +str(floor(time.time()-t0))+" secondes")


Ie,Je=0,0
Is,Js=99,99
def solvm(i):
    im=Image.open(str(i)+'.png')
    tab=np.array(im)
    g=converter(tab)
    solv(g,False,False,1,1,tab)
    sav(g,str(i)+' Soluce',tab)

for i in range(1000):
    thread = threading.Thread(target=solvm, args=(i,))
    thread.start()
