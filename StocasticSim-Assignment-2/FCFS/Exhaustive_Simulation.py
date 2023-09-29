from collections import deque
from Customer import Customer
from Event import Event
from FES import FES
from SimResults import SimResults
import numpy as np
import csv
from BunchedExponential import BunchedExp
import pandas as pd

class EXHSimulation :
    
    B = 1
    S = 2.4

    def __init__(self, arrDist, nrLanes, data: bool, alpha = None, mu = None): # arrDist should be a list of distributions for the various lanes / or a list of arrival times
        self.arrDist = arrDist
        self.nrLanes = nrLanes
        self.data = data
        self.alpha = alpha
        self.mu = mu

        # creating export file for exporting service times of all vehicles
        # export file for distribution
        with open('output.csv', 'w', newline='') as output_file:
            output_writer = csv.writer(output_file)
            output_writer.writerow(['Lane', 'Arrival', 'Service'])

        # export file for data
        with open('output_data.csv', 'w', newline='') as output_file_data:
            output_writer_data = csv.writer(output_file_data)
            output_writer_data.writerow(['Lane', 'Arrival', 'Service'])
    
    def export_servicetime(self, servicetime, customer): 
        if self.data:
            with open('output_data.csv', 'a', newline='') as output_file_data:
                    output_writer_data = csv.writer(output_file_data)
                    output_writer_data.writerow([customer.lane, customer.arrivalTime, servicetime])
        else:
            with open('output.csv', 'a', newline='') as output_file:
                output_writer = csv.writer(output_file)
                output_writer.writerow([customer.lane, customer.arrivalTime, servicetime])
        
    def simulate(self, T):
        fes = FES()                                     # future event set
        res = SimResults(self.nrLanes)                  # simulation results for all lanes
        queue = [deque() for _ in range(self.nrLanes)]  # generate queue for all lanes
        t = 0                                           # current time
        lastDepTime = 0                                   # last departure time
        lastDepLane = 'not assigned'                      # last lane we departed from
        if self.data: # first customers, for each lane.  We check whether we use data or distributions
            c = [Customer(self.arrDist[lane].pop(0), lane) for lane in range(self.nrLanes)] #data contains arrival times
        else:
            c = [Customer(t + self.arrDist[lane](self.alpha[lane], self.mu[lane]), lane) for lane in range(self.nrLanes)]  # arrDist contains interarrival times 
        firstEvents = [Event(Event.ARRIVAL, c[lane].arrivalTime, lane, c[lane]) for lane in range(self.nrLanes)]  #add arrival event for each lane
        for lane in range(self.nrLanes):
            fes.add(firstEvents[lane])                 # schedule first arrival event for all lanes
        
        first_customer = min(c) # The first customer is the one that arrives first
        lane_to_serve = first_customer.lane # The lane that we serve first, is the lane of the first customer.

        while t < T :                           # main loop
            e = fes.next()                      # jump to next event
            t = e.time                          # update the time
            c1 = e.customer                     # customer associated with this event
            lane = e.lane                       #lane associated with event
             
            res.registerQueueLength(t, len(queue[lane]), lane)  # register queue length

            if e.type == Event.ARRIVAL :        # handle an arrival event
                queue[lane].append(c1)          # add customer to the (correct lane) queue

                if sum([len(queue[lane]) for lane in range(self.nrLanes)]) <= 1 : #there was a free server
                    lane_to_serve = lane        # c1 is the only customer in the system so we switch to this lane.
                    res.registerWaitingTime(t - c1.arrivalTime, lane) 
                    if c1.lane != lastDepLane and lastDepLane != 'not assigned':
                        dep = Event(Event.DEPARTURE, max(t + EXHSimulation.B, lastDepTime + EXHSimulation.S) , c1.lane, c1)  
                        lastDepTime = max(t + EXHSimulation.B, lastDepTime + EXHSimulation.S)
                    else:
                        dep = Event(Event.DEPARTURE, t + EXHSimulation.B , c1.lane, c1)
                        lastDepTime = t + EXHSimulation.B
                    lastDepLane = lane
                    fes.add(dep)                # schedule departure of c1

                if self.data:
                    c2 = Customer(self.arrDist[lane].pop(0), lane)
                else:
                    c2 = Customer(t + self.arrDist[lane](self.alpha[lane], self.mu[lane]), lane) # create next arrival

                arr = Event(Event.ARRIVAL, c2.arrivalTime, c2.lane,  c2)
                fes.add(arr)                    # schedule the next arrival
            
            elif e.type == Event.DEPARTURE :    # handle a departure event
                self.export_servicetime(t-1, c1)# export service time
                queue[lane].remove(c1)          # remove the customer
                lane_to_serve = lane   
                if sum([len(queue[lane]) for lane in range(self.nrLanes)]) >= 1 : # someone was waiting (if any queue length is greater or equal to 1)
                    while len(queue[lane_to_serve]) == 0:   # Choose the lane that we need to serve.
                        lane_to_serve = (lane_to_serve + 1) % self.nrLanes # switch lanes, until we find a queue that is not empty.
                    
                    c2 = queue[lane_to_serve][0]# We select the first customer in the queue (from the lane that we are serving)
                    res.registerWaitingTime(t - c2.arrivalTime, c2.lane)
                    if c2.lane != lastDepLane and lastDepLane != 'not assigned': # depending on wheter or not we switched lanes we add the departure event.
                        dep = Event(Event.DEPARTURE, t + EXHSimulation.S, c2.lane, c2)
                        lastDepTime = t + EXHSimulation.S
                    else:
                        dep = Event(Event.DEPARTURE, t + EXHSimulation.B, c2.lane, c2)
                        lastDepTime = t + EXHSimulation.B
                    lastDepLane = c2.lane  
                    fes.add(dep)                # schedule this departure
        return res

    
### WITH DISTRIBUTIONS
print('with distribution')
alpha0, alpha1, mu0, mu1 = 0.5995995995995996, 0.5725725725725725, 0.21564291046984274, 0.3102950696782692

arrDist = [BunchedExp, BunchedExp] # interarrival time distr. for each lane
sim = EXHSimulation(arrDist, 2, False, [alpha0, alpha1], [mu0, mu1]) # the simulation model
res = sim.simulate(10000)  # perform simulation 
print(res)  # print the results

res.histQueueLength()  # plot of the queue length 
res.histWaitingTimes()  # histogram of waiting times 

# with data
print('with data')
df = pd.read_excel(r'C:\Users\20203453\Documents\GitHub\StocasticSim-Assignment-2\arrivals5.xlsx', header=None)

df.columns = [0,1]
lane0 = df[0].tolist()
lane1 = df[1].tolist()

arrDist = [lane0, lane1]

sim = EXHSimulation(arrDist, 2, True)   # the simulation model

# confidence intervals for the mean waiting times of the lanes

# number of simulation runs
n=500

sample_means_1 = []
sample_means_2 = []

for a in range(n):
    res = sim.simulate(10000)  # perform simulation 
    single_sample_mean_1 = res.getMeanWaitingTime(0)
    single_sample_mean_2 = res.getMeanWaitingTime(1)
    sample_means_1.append(single_sample_mean_1)
    sample_means_2.append(single_sample_mean_2)

# lane1
mean_mean_waiting_time1 = np.mean(sample_means_1)
lower1 = np.percentile(sample_means_1,2.5)
upper1 = np.percentile(sample_means_1,97.5)

# lane2
mean_mean_waiting_time2 = np.mean(sample_means_2)
lower2 = np.percentile(sample_means_2,2.5)
upper2 = np.percentile(sample_means_2,97.5)

print(f"lane 1 {lower1}-{mean_mean_waiting_time1}-{upper1}")
print(f"lane 2 {lower2}-{mean_mean_waiting_time2}-{upper2}")

 
print(res)                              # print the results

res.histQueueLength()  # plot of the queue length 
res.histWaitingTimes()  # histogram of waiting times 
