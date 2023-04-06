from typing import Tuple
import numpy as np

def get_shift(point: Tuple[float, float]) -> str: # select wanted EL and AZ
    newData = np.loadtxt('lookangles.csv',delimiter=',' ,skiprows=1)
    phase = newData[np.nonzero(np.logical_and(newData[:,0]==point[0],newData[:,1]==point[1]))][0,2:]
    if phase.shape[0] > 0:
          shift  = bits(phase[0])
          shift += bits(phase[1])
          shift += bits(phase[2])
          shift += bits(phase[3])  
    return shift

def bits(angle: float) -> str:
    return bin(int(angle / 22.5) * 4)[2:].zfill(6)