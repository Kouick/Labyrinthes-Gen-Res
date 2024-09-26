from PIL import Image
import numpy as np
import pickle



NAME=str(input("Nom du fichier du labyrinthe avec l'extension jpg ou png : "))
NAMENR=str(input("Nom du fichier contenant les informations relatives aux portails : "))
NameFin=str(input("Nom du fichier du graphe à sauvegarder : "))


def ckoa2(pix):     #Reconnaissance mur/chemin.
    if pix[0]==255 and pix[1]==0 and pix[2]==0:
        return "chemin"
    elif pix[0]==0 and pix[1]==255 and pix[2]==0:
        return "chemin"
    elif 100>pix[0]:
        return "mur"
    return "chemin"

def converter(g,tab): #Crée un graphe g sous forme de dictionnaire où les clés sont les coordonnées des points "chemin" et les valeurs sont leurs listes de points "chemin" adjacents.
    temp=[]
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            if ckoa2(tab[i][j])=="chemin":
                temp=[]
                if i>0 and ckoa2(tab[i-1][j])=="chemin":
                    temp.append((i-1,j))
                if i<len(tab)-1 and ckoa2(tab[i+1][j])=="chemin":
                    temp.append((i+1,j))
                if j>0 and ckoa2(tab[i][j-1])=="chemin":
                    temp.append((i,j-1))
                if j<len(tab[0])-1 and ckoa2(tab[i][j+1])=="chemin":
                    temp.append((i,j+1))
                g[(i,j)]=temp
                temp=[]
    return g

def enrichiG(g,NAMENR):          #Ajoute les données relatives aux portails dans le graphe.
    file = open(NAMENR, "rb")
    enr = pickle.load(file)
    for c in enr:
        for e in enr[c]:
            if not e in g[c]:
                g[c].append(e)
    file.close()
    return g

def saveG(g,NameFin):
    FinalFile = open(NameFin, "wb")
    pickle.dump(g,FinalFile)
    FinalFile.close()



g={}
if not NAME=="":
    im=Image.open(NAME)
    tab=np.array(im)
    im.close()
    g=converter(g,tab)
if not NAMENR=="":
    enrichiG(g,NAMENR)
saveG(g,NameFin)

















