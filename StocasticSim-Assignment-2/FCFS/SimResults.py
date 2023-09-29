from collections import deque

from numpy.ma.core import zeros, sqrt

import matplotlib.pyplot as plt


class SimResults:
    
    MAX_QL = 10000  # maximum queue length that will be recorded
    
    def __init__(self, nrLanes):
        self.nrLanes = nrLanes
        self.sumQL = zeros(nrLanes)
        self.sumQL2 = zeros(nrLanes)
        self.nQ = zeros(nrLanes)
        self.oldTime = zeros(nrLanes)
        self.queueLengthHistogram = [zeros(self.MAX_QL + 1) for _ in range(nrLanes)] 
        self.sumW = zeros(nrLanes)
        self.sumW2 = zeros(nrLanes)
        self.nW = zeros(nrLanes)
        self.waitingTimes = [deque() for _ in range(nrLanes)] # not adjusted
        
    def registerQueueLength(self, time, ql, lane):
        self.sumQL[lane] += ql * (time - self.oldTime[lane])
        self.sumQL2[lane] += ql * ql * (time - self.oldTime[lane])
        self.queueLengthHistogram[lane][min(ql, self.MAX_QL)] += (time - self.oldTime[lane])
        self.oldTime[lane] = time
        self.nQ[lane] +=1
        
    def registerWaitingTime(self, w, lane):
        self.waitingTimes[lane].append(w)
        self.nW[lane] += 1
        self.sumW[lane] += w
        self.sumW2[lane] += w * w
        
    def getMeanQueueLength(self, lane): 
        return self.sumQL[lane] / self.oldTime[lane]
    
    def getVarianceQueueLength(self, lane): 
        return self.sumQL2[lane] / self.oldTime[lane] - self.getMeanQueueLength(lane)**2
    
    def getMeanWaitingTime(self, lane):
        return self.sumW[lane] / self.nW[lane]
        
    def getVarianceWaitingTime(self, lane):
        return self.sumW2[lane] / self.nW[lane] - self.getMeanWaitingTime(lane)**2

    def getQueueLengthHistogram(self, lane) :
        return [x/self.oldTime[lane] for x in self.queueLengthHistogram[lane]]
    
    def getWaitingTimes(self, lane):
        return self.waitingTimes[lane]
    
    def __str__(self):
        s = 'Mean queue length: '+str([self.getMeanQueueLength(lane) for lane in range(self.nrLanes)]) + '\n'
        s += 'Standard deviation queue length: '+str([sqrt(self.getVarianceQueueLength(lane)) for lane in range(self.nrLanes)]) + '\n'
        s += 'Mean waiting time: '+str([self.getMeanWaitingTime(lane) for lane in range(self.nrLanes)]) + '\n'
        s += 'Standard deviation waiting time: '+str([sqrt(self.getVarianceWaitingTime(lane)) for lane in range(self.nrLanes)]) + '\n'
        return s
    
    def histQueueLength(self, maxq=50):
        plt.figure()
        transparency=1 + 0.5 / self.nrLanes
        for lane in range(self.nrLanes):
            transparency -= 0.5/self.nrLanes
            ql = self.getQueueLengthHistogram(lane)
            maxx = maxq + 1
            plt.bar(range(0, maxx), ql[0:maxx], alpha=transparency)
        plt.ylabel('P(Q = k)')
        plt.xlabel('k')
        plt.legend([f'lane{i}' for i in range(self.nrLanes)])
        plt.show()
        
    def histWaitingTimes(self, nrBins=100):
        plt.figure()
        
        for lane in range(self.nrLanes):
            plt.hist(self.waitingTimes[lane], bins=nrBins, rwidth=0.8, density=True)
        plt.ylabel('P(W = k)')
        plt.xlabel('k')
        plt.legend([f'lane{i}' for i in range(self.nrLanes)])
        plt.show()
    
    def getConfidenceQLmean(self, lane):
        return f'{self.getMeanQueueLength(lane)} +- {1.96*sqrt(self.getVarianceQueueLength(lane))/self.nQ[lane]}'
    
    def getConfidenceWmean(self, lane):
        return f'{self.getMeanWaitingTime(lane)} +- {1.96*sqrt(self.getVarianceWaitingTime(lane))/self.nQ[lane]}'