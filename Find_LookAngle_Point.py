from typing import Tuple
import pandas as pd
import numpy as np
from scipy import io, integrate, linalg, signal
from scipy.sparse.linalg import cg, eigs

def Find_LookAngle_Point(point: Tuple[float, float],Dir):
    #Dir defines the direction to search for the next point given a scope and a
    #tolerance value. 
    #Dir is defined as 1=+AZ, 2=-AZ, 3=+EL, 4=-EL
    Az = point[0]
    El = point[1]
    found=False
    data = pd.read_csv('lookangles.csv')
    newData = data.to_numpy()
    tolerance=5
    scope = 15
    
    match Dir:
        case 1:
            if El == 90:
                Look = newData[147-1] #147th data point [270,82.8]
                I = 0
                found = True
                
            while found == False:
                if Az+scope < 360:
                    Look = newData[np.nonzero(np.logical_and(np.logical_and(newData[:,0] < (Az+scope),newData[:,0] > Az), abs(newData[:,1]-El) < tolerance))]
                    I = np.argsort(Look[:,0])
                elif Az+scope>=360:
                    Look = newData[
                        np.nonzero(
                            np.logical_and(
                                np.logical_or(
                                    np.logical_and(
                                        newData[:,0] < (Az+scope),
                                        newData[:,0] > Az
                                        ),
                                    np.logical_and(
                                        newData[:,0] < (scope-(360-Az)),
                                        newData[:,0] >= 0
                                        )
                                    ),
                                abs(newData[:,1]-El) < tolerance
                                )
                            )
                        ]
                    if (np.any(Look[:,0] >= Az)):
                        I = np.argsort(Look[:,0])[::-1]
                    else:
                        I = np.argsort(Look[:,0])    
                        
                Look_sort = Look[I,:]   
                if Look_sort.shape[0] > 0:
                    found=True
                else:
                    scope+=1
                    
            return Look_sort[0]
            
        case 2:
            if El == 90:
                Look = newData[51-1] #51st data point [90,83]
                I = 0
                found = True
                
            while found == False:
                if Az-scope >= 0:
                    Look = newData[np.nonzero(np.logical_and(np.logical_and(newData[:,0] > (Az-scope),newData[:,0] < Az), abs(newData[:,1]-El) < tolerance))]
                    I = np.argsort(Look[:,0])[::-1]
                elif Az-scope < 0:
                    Look = newData[
                        np.nonzero(
                            np.logical_and(
                                np.logical_or(
                                    np.logical_and(
                                        newData[:,0] > (Az-scope),
                                        newData[:,0] < Az
                                        ),
                                    np.logical_and(
                                        newData[:,0] > (360+(Az-scope)),
                                        newData[:,0] < 360
                                        )
                                    ),
                                abs(newData[:,1]-El) < tolerance
                                )
                            )
                        ]
                    if (np.any(Look[:,0] <= Az)):
                        I = np.argsort(Look[:,0])
                    else:
                        I = np.argsort(Look[:,0])[::-1]        
                    
                
                Look_sort = Look[I,:]
                if Look_sort.shape[0] > 0:
                    found=True
                else:
                    scope+=1
                    
            return Look_sort[0]
        
        case 3:
            if El == 90:
                Look = newData[9-1] #ninth data point [0,82.8]
                I = 0
                found = True
            
            while found == False:
                if abs(90-(El+scope)) <= 5:
                    Look = newData[0:1]
                    I=[0]
                elif El+scope < 85:
                    Look = newData[np.nonzero(np.logical_and(np.logical_and(newData[:,1] < (El+scope),newData[:,1] > El), abs(newData[:,0] - Az) < tolerance))]
                    I = np.argsort(Look[:,1])
                elif El+scope>95:
                    if Az+180 >= 360:
                        newAz = Az - 180
                    else:
                        newAz = Az + 180
                        
                    Look = newData[
                        np.nonzero(
                            np.logical_or(
                                np.logical_and(
                                    np.logical_and(
                                        newData[:,1] <= 90,
                                        newData[:,1] > El
                                        ),
                                    abs(newData[:,0] - Az) < tolerance
                                    ),
                                np.logical_and(
                                    np.logical_and(
                                        newData[:,1] < 90,
                                        newData[:,1] > (90-(scope-(90-El))) #90 minus the remainder of the scope
                                        ),
                                    abs(newData[:,0] - newAz) < tolerance 
                                    )
                                )
                            )
                        ]
                    if (np.any(Look[:,0] >= El)):
                        I = np.argsort(Look[:,0])[::-1]
                    else:
                        I = np.argsort(Look[:,0])    
                        
                Look_sort = Look[I,:]   
                if Look_sort.shape[0] > 0:
                    found=True
                else:
                    tolerance+=1
                    
            return Look_sort[0]
        
        case 4:
            if El == 90:
                Look = newData[99-1] #99th data point [90,82.8]
                I = 0
                found = True
                
            while found == False:
                if El < 12.4:
                    El=El+scope+1
                if El-scope > 0:
                    Look = newData[np.nonzero(np.logical_and(np.logical_and(newData[:,1] > (El-scope),newData[:,1] < El), abs(newData[:,0] - Az) < tolerance))]
                    I = np.argsort(Look[:,1])[::-1]
                elif El-scope <=0: #infinite loops if El < 10, shouldn't happen as the lowest points are 12.X
                    Look = newData[np.nonzero(np.logical_and(np.logical_and(newData[:,1] > 0,newData[:,1] < El), abs(newData[:,0] - Az) < tolerance))]
                    I = np.argsort(Look[:,1])[::-1]
                        
                Look_sort = Look[I,:]   
                if Look_sort.shape[0] > 0:
                    found=True
                else:
                    tolerance+=1
                    
            return Look_sort[0]
        
        case _:
            print("Invalid direction command")
    
    
    
    
