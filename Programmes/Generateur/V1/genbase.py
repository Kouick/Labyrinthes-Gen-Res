from PIL import Image
import numpy as np
import imageio





def genbase(p,q,NOMFINAL):
    tab=np.full((p, q, 3), [0, 0, 0], dtype=np.uint8)
    tab[0][0]=[100,100,100]
    np.array(imageio.imwrite(NOMFINAL+".png", tab))
    
genbase(10,10,"machin")