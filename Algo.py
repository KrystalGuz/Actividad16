import math 

def distancia_euclidiana(x1, x2,y1, y2):
    xt = (x2-x1)*(x2-x1)
    yt = (y2-y1)*(y2-y1)
    return math.sqrt(xt + yt)
