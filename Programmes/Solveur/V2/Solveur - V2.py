from PIL import Image
import numpy as np
from copy import deepcopy
import time
from math import *
import imageio
import threading
import pickle
print("WARNING /!\ ce script détecte également les cycles, il n'est utilisable que sur des labyrinthes du type 'lab.jpg', la sortie et l'entrée peuvent cependant être changé de place, ce programme donne toute les solutions possibles")


SAVTEMPin=(input("Doit-on sauvegarder les étapes intermédiaires ? (True ou False)"))
RETOURSin=(input("Doit-on recevoir des retours dans la console ? (True ou False)"))
SAVTEMP=SAVTEMPin=="True"
RETOURS=RETOURSin=="True"
MAXSAVEDINTERETAP=int(input("Maximum d'étapes intermédiaires sauvegardées en images : "))
INRVALCAP=int(input("Intervalle d'étape entre chaque image intermédiaire : "))
NOMFINAL=str(input("Nom du fichier de sauvegarde du labyrinthe résolu : "))
NAME=str(input("Nom du fichier du labyrinthe avec l'extension jpg ou png : "))
NAMENR=str(input("Nom du fichier contenant les informations relatives aux portails : "))


t0=time.time()
im=Image.open(NAME)
tab=np.array(im)
print("chargé")
#Recherche de l'entrée et de la sortie.

#On recherche deux façons de couvrir les deux modèles d'enregistrement.
azert=0
for i in range(len(tab)):
    for j in range(len(tab[0])):
        if 50<tab[i][j][0]<200 and 50<tab[i][j][1]<200 and 50<tab[i][j][2]<200:
            if azert>0:
                azert=2
                Is,Js=i,j
                break
            else:
                azert=1
                Ie,Je=i,j
    if azert==2:
        break

for i in range(len(tab)):
    for j in range(len(tab[0])):
        if tab[i][j][0]==255 and tab[i][j][1]==0 and tab[i][j][2]==0:
            Ie,Je=i,j
        if tab[i][j][0]==0 and tab[i][j][1]==255 and tab[i][j][2]==0:
            Is,Js=i,j

tab[Ie][Je]=[255,0,0]     #Marquage de l'entrée et de la sortie.
tab[Is][Js]=[0,255,0]
print('entree-sortie trouvee')
def ckoa(pix):     #Reconnaissance de mur/chemin/entrée/sortie.
    if pix[0]==255 and pix[1]==0 and pix[2]==0:
        return "start"
    if pix[0]==0 and pix[1]==255 and pix[2]==0:
        return "end"
    if 100>pix[0]:
        return "mur"
    return "chemin"


def converter(tab): #Crée un graphe g sous forme de dictionnaire, où les clés sont les coordonnées des points et les valeurs sont les listes des sommets adjacents.
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
    if not NAMENR=="":
        file = open(NAMENR, "rb")
        enr = pickle.load(file)
        for dep in enr: #enrichissement de g par les portailes
            for dest in enr[dep]:
                g[dep].append(dest)
    print("completion de la convertion en " +str(floor(time.time()-t0))+" secondes")
    return g




#L'algorithme utilisé est le suivant : "Si tu es un cul-de-sac, alors tu es un mur". On applique cette transformation à chaque point du labyrinthe jusqu'à ce que le labyrinthe soit résolu.
#lLes chemins ne menant nulle part régresseront et disparaîtront jusqu'à ce qu'il ne reste que le bon chemin.

def solv(g,RETOURS,SAVTEMP,MAXSAVEDINTERETAP,INRVALCAP,tab):
    a=0
    b=0
    cur,nxt=[],[]     #cur[ent] et n[e]xt contiennent les chemins à supprimer respectivement à l'instant courant et à l'instant suivant.
    for i in g:
        if len(g[i])<2 and not (i == (Ie, Je) or i == (Is, Js)):  #Création de l'état initial des éléments à détruire.
            nxt.append(i)
    while not nxt==[]:      #Tant qu'il reste des éléments à détruire.
        cur,nxt=nxt,[]       #On inverse les listes de sorte que le suivant devienne le courant et on vide le suivant.
        for i in cur:
            if i in g:
                t=g[i]
                for j in t:        #On indexe les sommets adjacents qui deviennent "à détruire" dans la liste "suivant" si on retire le sommet i.
                    l=g[j]
                    l.remove(i)
                    g[j]=l
                    if len(l)<2 and not (i == (Ie, Je) or i == (Is, Js)):
                        nxt.append(j)
                del g[i]           # Puis, on supprime le sommet i.
        a+=1
        if RETOURS:
            print("étape "+str(a)+" complétée en "+str(floor(time.time()-t0))+" seconde")
        if SAVTEMP and b<MAXSAVEDINTERETAP and a%INRVALCAP==0:
            b+=1
            sav(g,str(a),tab)
##            thread=threading.Thread(target=sav, args=(deepcopy(g),str(a)))
##            thread.start()
    print("completion du labyrinthe en "+str(floor(time.time()-t0))+" secondes")







def sav(g,nom,tab):
    ta=deepcopy(tab)
    for c in g:
        i,j=c
        ta[i][j]=[0,0,255]
    ta[Ie][Je]=[255,0,0]
    ta[Is][Js]=[0,255,0]
    imageio.imwrite(nom+".png", ta)
    print("fichier suvegardé après " +str(floor(time.time()-t0))+" secondes")

g=converter(tab)
solv(g,RETOURS,SAVTEMP,MAXSAVEDINTERETAP,INRVALCAP,tab)
sav(g,NOMFINAL,tab)


