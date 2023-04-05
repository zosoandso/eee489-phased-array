import pandas as pd
import numpy as np
from scipy import io, integrate, linalg, signal
from scipy.sparse.linalg import cg, eigs

def Find_LookAngle_Point(Az,El,Dir):
    #Dir defines the direction to search for the next point given a scope and a
    #tolerance value. 
    #Dir is defined as 1=+AZ, 2=-AZ, 3=+EL, 4=-EL
    data = pd.read_csv('lookangles.csv')
    newData = data.to_numpy()
    tolerance=5
    scope = 15
    
    match Dir:
        case 1:
            #need a catch for when increasing AZ may exceed 360
            Look = newData[np.nonzero(np.logical_and(np.logical_and(newData[:,0] < (Az+scope),newData[:,0] > Az), abs(newData[:,1]-El) < tolerance))]
            I = np.argsort(Look[:,0])
            #need an error catch and re-iterate for when there are no datapoints found with >tolerance or >scope
            Look_sort = Look[I,:]   
            print(Look_sort[0])
            
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case _:
            print("Invalid direction command")
    
    
    
    
