from PIL import Image
import numpy as np
from copy import deepcopy
import time
from math import *
import imageio
from random import *

print("WARNING /!\ ce script prend en entree une image toute noire, ou un labyrinthe incomplet, il doit y avoir au moins une case blanche ou grise au départ et si on veut restreindre le programme a un template, faut mettre des limites en bleu")
#Ce programme est capable de reprendre pour compléter une génération incomplète sans poser de questions.
#La sortie doit être placée manuellement.

SAVTEMPin=(input("Doit-on sauvegarder les étapes intermédiaires ? (True ou False)    "))
RETOURSin=(input("Doit-on recevoir des retours dans la console ? (True ou False)    "))
SAVTEMP=SAVTEMPin=="True"
RETOURS=RETOURSin=="True"
MAXSAVEDINTERETAP=int(input("Combien au maximum d'étapes intermédiaires souhaitez-vous sauvegarder en images ?   "))
NOMFINAL=str(input("Quel nom souhaitez-vous donner au fichier de sauvegarde du labyrinthe généré ?   "))
NAME=str(input("Nom du fichier du template à ouvrir (image de pixels noirs ([0,0,0]) avec des délimitations si voulues en bleu ([0,0,255]) et une entrée en gris ([100,100,100])) avec l'extension jpg ou png (pas testé sur autre chose) :"))
PROB=int(input("Probabilité qu'un mur soit converti en chemin : un chiffre plus grand implique un labyrinthe plus aléatoire et un temps de génération plus long (par exemple, un mur a une chance de se convertir de environ 1/nombre entré).   "))



t0=time.time()
im=Image.open(NAME)
tab=np.array(im)
locked={}
chemins={}
todel=[]
FOUND=False
#Recherche de l'entrée.
azert=0
for i in range(len(tab)):
    for j in range(len(tab[0])):
        if 50<tab[i][j][0]<200 and 50<tab[i][j][1]<200 and 50<tab[i][j][2]<200:
            azert=1
            Ie,Je=i,j
            FOUND=True
            break
    if azert==1:
        break


if FOUND:
    tab[Ie][Je]=[255,0,0]     #Marquage de l'entrée.

def ckoa(pix):     #Reconnaissance de mur/chemin/hypermur (ces derniers sont les limites du labyrinthe).
    if pix[0]==255 and pix[1]==0 and pix[2]==0:
        return "start"
    if pix[0]==0 and pix[1]==0 and pix[2]==255:
        return "hypermur"
    if 100>pix[0]:
        return "mur"
    return "chemin"

n=len(tab)
m=len(tab[0])

for i in range(len(tab)):
    for j in range(len(tab[0])):
        if ckoa(tab[i][j])=="chemin":
            chemins[(i,j)]=1


def converter(tab): #Création d'un graphe g sous forme de dictionnaire, où les clés représentent les coordonnées des points et les valeurs représentent les listes des chemins adjacents.
    g={}
    temp=[]
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            temp=[]
            if i>0 and (ckoa(tab[i-1][j])=="chemin" or ckoa(tab[i-1][j])=="start"):
                temp.append([i-1,j])
            if i<len(tab)-1 and (ckoa(tab[i+1][j])=="chemin" or ckoa(tab[i+1][j])=="start"):
                temp.append([i+1,j])
            if j>0 and (ckoa(tab[i][j-1])=="chemin" or ckoa(tab[i][j-1])=="start"):
                temp.append([i,j-1])
            if j<len(tab[0])-1 and (ckoa(tab[i][j+1])=="chemin" or ckoa(tab[i][j+1])=="start"):
                temp.append([i,j+1])
            if not (ckoa(tab[i][j])=="hypermur"):
                g[(i,j)]=temp
                temp=[]
    print("completion de la convertion en " +str(floor(time.time()-t0))+" secondes")
    return g



def cheminadkey():
    for c in g:
        if ckoa(tab[c])=="chemin":
            chemins[c]=1




def gen(g):
    a=0
    at=time.time()
    z = True
    while z:                    #Tant qu'il peut se passer des choses.
        z = False
        for c in g:             #Les murs avec un chemin adjacent peuvent devenir des chemins avec une probabilité de 1/PROB.
            if len(g[c]) > 1:
                locked[c]=1
                todel.append(c)
            if not c in locked and len(g[c]) ==1:
                if not c in chemins:
                    z = True
                    if randint(0,PROB)==1:
                        i, j = c
                        x = [i, j]
                        chemins[c]=1
                        if i>0 and not (ckoa(tab[i-1][j])=="hypermur") and not ((i-1,j) in locked) and not (i-1,j) in chemins:
                            g[i-1,j].append(x)
                        if i<len(tab)-1 and  not (ckoa(tab[i+1][j])=="hypermur") and not ((i+1,j) in locked) and not (i+1,j) in chemins:
                            g[i+1,j].append(x)
                        if j>0 and  not (ckoa(tab[i][j-1])=="hypermur") and not ((i,j-1) in locked) and not (i,j-1) in chemins:
                            g[i,j-1].append(x)
                        if j<len(tab[0])-1 and not (ckoa(tab[i][j+1])=="hypermur") and not ((i,j+1) in locked) and not (i,j+1) in chemins:
                            g[i,j+1].append(x)
                        g[c].append([0,0])
                        todel.append(c)
        for c in todel:
            if c in g:
                del g[c]
        a+=1
        if RETOURS:
            print("completion de l'étape " +str(a)+" en " +str(floor(time.time()-t0))+" secondes")
            at=time.time()
        if SAVTEMP:
            at=time.time()
            savetap(g,a)
    print("genere en " +str(floor(time.time()-t0))+" secondes")
    return g


def savetap(g,a):                       #Cette version du programme a été abandonnée avant la réalisation des tests de cette fonction.
    ta=deepcopy(tab)
    for c in g:
        if len(g[c])==0:
            i,j=c
            ta[i][j]=[0,0,0]
    for c in chemins:
            i,j=c
            ta[i][j]=[255,255,255]
    if FOUND:
        tab[Ie][Je]=[255,0,0]
    if a<MAXSAVEDINTERETAP:
        imageio.imwrite("etape_"+str(a)+".png", ta)
    else:
        imageio.imwrite("etape_"+str(MAXSAVEDINTERETAP)+".png", ta)
    print("étape "+str(a)+" rendue en " +str(floor(time.time()-t0))+" secondes")



def end(g):       #Génère le tableau de l'image du labyrinthe stocké dans le graphe et le dictionnaire des chemins.
    ta=deepcopy(tab)
    for c in g:
        if len(g[c])==0:
            i,j=c
            ta[i][j]=[0,0,0]
    for c in chemins:
            i,j=c
            ta[i][j]=[255,255,255]
    for c in locked:
            i,j=c
            ta[i][j]=[0,0,0]
    if FOUND:
        tab[Ie][Je]=[255,0,0]
    print("labyrinthe finale rendue en " +str(floor(time.time()-t0))+" secondes")
    return ta



def finitions():
    for i in range(len(ta)):
        for j in range(len(ta[0])):
            if ckoa(ta[i,j])=="hypermur":
                ta[i,j]=[0,0,0]
    if FOUND:
        ta[Ie][Je]=[100,100,100]
    imageio.imwrite(NOMFINAL+".png", ta)         #Artefact du moment où je n'étais pas au courant que PIL peut enregistrer en PNG : sauvegarde et affichage de l'image.
    (Image.fromarray(ta)).show()




g=converter(tab)  #Lancement de la génération.
gen(g)
cheminadkey()
ta=end(g)
finitions()


print("C'est moche, mais c'est un labyrinthe parfait (reconnu par l'autre script), mais il n'y a pas encore de sortie à placer manuellement. La sortie est un pixel [100,100,100].")

