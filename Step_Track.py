from typing import Tuple
import antenna_driver as an
import numpy as np
import time

#current=[Az,El,RSSI]
# Threshold may need to get changed to a global variable that is configured by the 
# antenna baseline, determined by tracking the lowest power reading during intital 
# search scan
def Step_Track(current: Tuple[float,float,float],Threshold):
    Peaked=False
    Tracking=True
    Allowed_variance=2 #variance range is doubled as it is treated as a +/- value
    
    
    
    while Peaked == False:
        Step_table = np.zeros((5,3))
        Step_table[0,:]=np.array([current[0],current[1],current[2]])
        for i in range(1,5):
            #Step_info return from Step_Position
            #Step_info [Az,El,RSSI]
            #Steps the antenna in the four directions
            Step_info=Step_Position((current[0],current[1]),i)
            #Records the positions and RSSI of the four step directions
            Step_table[i,:]=[Step_info[0],Step_info[1],Step_info[3]]
            
        #test for whether all directions are equal with an allowed variance range
        test=Step_table[np.nonzero(abs(Step_table[:,2]-Step_table[0,2]) <= Allowed_variance)]
        
        #If shape of test is =5 then all four directions has the same power as the current direction
        if test.shape[0] < 5:
            #finds the highest signal strength of the five datapoints
            I = np.argsort(Step_table[:,2])[::-1]
            best=Step_table[I,:][0]
            #assigns best lookangle and RSSI to current
            current=[best[0],best[1],best[2]]
            an.do_shift([current[0],current[1]])

        else:
            Peaked == True
            #if all power values are equal and below threshold, we are not longer tracking, 
            #set tracking variable to false and send it back to calling function. Likely need
            #to call SearchAp at that point
            if Step_table[0,2] < Threshold:
                Tracking=False
    #returns Az, El, RSSI of the best step directions as well as the tracking state
    return [current[0],current[1],current[2],Tracking]

#current=[Az,El], Dir=[1-4]
#Dir is defined as 1=+AZ, 2=-AZ, 3=+EL, 4=-EL
def Step_Position(current: Tuple[float,float], Dir):
    #find look angle point from database in desired direction
    new = Find_LookAngle_Point(current,Dir)
    
    #shift the antenna in desired direction based up on found lookangle point
    an.do_shift([new[0],new[1]])
        
    #wait 20ms (testing may need to alter this up or down)
    time.sleep(0.02)
    
    #obtain power value of AP
    new_power = an.get_rssi()
    
    #set antenna back to current position (may not be necessary but avoids any 
    #potential that if routines are jumped, antenna is left in original configuration
    #and not in last movement of the steptrack)
    an.do_shift(current)
    
    #returns Az, El and RSSI of lookangle point in the desired direction
    return [new[0],new[1],new_power]

#point=[Az,El]
#Dir defines the direction to search for the next point given a scope and a
#tolerance value. 
#Dir is defined as 1=+AZ, 2=-AZ, 3=+EL, 4=-EL
def Find_LookAngle_Point(point: Tuple[float, float],Dir):
    Az = point[0]
    El = point[1]
    found=False
    data = an.data 
    newData = data.to_numpy()
    tolerance=5
    scope = 15
    
    match Dir:
        case 1:       
            #+AZ
            while found == False:
                #If EL = 90, special case, move to a specific lookangle position based upon 
                #direction called
                if El == 90:
                    Look = newData[146-1:146] #146th data point [270,82.8]
                    I = [0]
                    found = True
                #if Az=scope is less than 360, no wraparound issues, 
                elif Az+scope < 360:
                    #find data points in increasing AZ inside a swath of EL range 
                    #of tolerance
                    Look = newData[np.nonzero(np.logical_and(np.logical_and(newData[:,0] < (Az+scope),newData[:,0] > Az), abs(newData[:,1]-El) < tolerance))]
                    #sorts by AZ in ascending order
                    I = np.argsort(Look[:,0])
                # if AZ+scope is equal to or greater than 360, wrap around situation
                elif Az+scope>=360:
                    #find all data points between current AZ and 360 and from 0 to 
                    #remainder of scope after taking the difference between AZ current 
                    #and 360
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
                    #if any of the found AZ points are greater than current AZ
                    if (np.any(Look[:,0] >= Az)):
                        #sort descending to get the highest data point 
                        #this may have the undesireable effect of grabbing a point 
                        #further than the neareest AZ within a range, however it is 
                        #expected that it would have minor effect
                        I = np.argsort(Look[:,0])[::-1]
                    #else found datapoints must be 0 or greater
                    else:
                        #sort datapoints ascending to obtain closest datapoint to 
                        #current AZ
                        I = np.argsort(Look[:,0])    
                
                #actual sorting of datapoints, I is array of indices
                Look_sort = Look[I,:]   
                #Is first dimension of Look_sort array greater than zero?
                #Determines if there is actual data
                if Look_sort.shape[0] > 0:
                    found=True
                #else Look_sort is empty
                else:
                    #increase scope to widen range of AZ searched for nearest datapoint
                    scope+=1
                    
            return Look_sort[0]
            
        case 2:    
            #-AZ            
            while found == False:
                #If EL = 90, special case, move to a specific lookangle position based upon 
                #direction called
                if El == 90:
                    Look = newData[50-1:50] #50th data point [90,83]
                    I = [0]
                    found = True
                #if az-scope greater than 0, than typical situation, no wraparound
                elif Az-scope >= 0:
                    #find all datapoints less than current AZ that are within 
                    #a swath of EL sized tolerance
                    Look = newData[np.nonzero(np.logical_and(np.logical_and(newData[:,0] > (Az-scope),newData[:,0] < Az), abs(newData[:,1]-El) < tolerance))]
                    I = np.argsort(Look[:,0])[::-1]
                #if az-scope is less than zero, wrap around situation
                elif Az-scope < 0:
                    #logic that works but don't want to try and explain. lots of conditionals
                    #to handle the many different situations that can occur during this event
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
                    #if any of the found AZ points are less than current AZ
                    if (np.any(Look[:,0] <= Az)):
                        #sort ascending to get lowest data point. This may have 
                        #the added effect of skipping a datapoint that was closer
                        #but the effect should be minor
                        I = np.argsort(Look[:,0])
                    #else found datapoints must be 360 or less
                    else:
                        #sort descending to find datapoint on the other side of the 
                        #the median
                        I = np.argsort(Look[:,0])[::-1]        
                    
                #actual sorting of datapoints, I is array of indices
                Look_sort = Look[I,:]
                #Is first dimension of Look_sort array greater than zero?
                #Determines if there is actual data
                if Look_sort.shape[0] > 0:
                    found=True
                 #else Look_sort is empty    
                else:
                    #increase scope to widen range of AZ searched for nearest datapoint
                    scope+=1
                    
            return Look_sort[0]
        
        case 3:   
            #+EL
            while found == False:
                #If EL = 90, special case, move to a specific lookangle position based upon 
                #direction called
                if El == 90:
                    Look = newData[8-1:8] #eigth data point [0,82.8]
                    I = [0]
                    found = True
                #if within El+scope is within 8 degrees of 90, go to EL90 position
                #subsequent steptrack will execute special movement for EL90 position
                elif abs(90-(El+scope)) <= 8:
                    Look = newData[0:1]
                    I=[0]
                #Normal, not 90 degree, not keyhole
                elif El+scope < 85:
                    Look = newData[np.nonzero(np.logical_and(np.logical_and(newData[:,1] < (El+scope),newData[:,1] > El), abs(newData[:,0] - Az) < tolerance))]
                    I = np.argsort(Look[:,1])
                elif El+scope>95:
                    #handles keyhole event logic as crossing 90 flips the AZ 180 degrees
                    if Az+180 >= 360:
                        newAz = Az - 180
                    else:
                        newAz = Az + 180
                    #logic that works but don't want to try and explain. lots of conditionals
                    #to handle the many different situations that can occur during this event
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
                    #tolerance used on El as increase in scope like AZ could cause massive 
                    #changes in direction
                    tolerance+=1
                    
            return Look_sort[0]
        
        case 4:    
            #-EL            
            while found == False:
                #if EL is too low can cause an infinite loop, adjusting El up scope+1
                #ensures that it comes back to its original position for -EL. Effectively nulls
                #-EL movement. 
                if El < 12.4:
                    El=El+scope+1
                #If EL = 90, special case, move to a specific lookangle position based upon 
                #direction called
                if El == 90:
                    Look = newData[98-1:98] #98th data point [90,82.8]
                    I = [0]
                    found = True
                #if El-scope is greater than zero, then shoudl function. Error 
                #catch will have corrected if El was less than 12.4 degrees
                elif El-scope > 0:
                    #searches for data points that are lower in elevation than current 
                    #and within a range of AZ
                    Look = newData[np.nonzero(np.logical_and(np.logical_and(newData[:,1] > (El-scope),newData[:,1] < El), abs(newData[:,0] - Az) < tolerance))]
                    I = np.argsort(Look[:,1])[::-1]
                elif El-scope <=0: #infinite loops if El < 10, shouldn't happen as the lowest points are 12.X, catch at beginning of while loop corrects 
                    #searches for all data points that are lower in elevation but greater than 0
                    Look = newData[np.nonzero(np.logical_and(np.logical_and(newData[:,1] > 0,newData[:,1] < El), abs(newData[:,0] - Az) < tolerance))]
                    I = np.argsort(Look[:,1])[::-1]
                        
                Look_sort = Look[I,:]   
                if Look_sort.shape[0] > 0:
                    found=True
                else:
                    #tolerance used on El as increase in scope like AZ could cause massive 
                    #changes in direction
                    tolerance+=1
                    
            return Look_sort[0]
        
        case _:
            print("Invalid direction command")
    
    
    
    


