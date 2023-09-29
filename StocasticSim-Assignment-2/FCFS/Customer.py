class Customer :

    def __init__(self, arr, lane):
        self.arrivalTime = arr
        self.lane = lane
        
    def __str__(self):
        return "Customer at " + str(self.arrivalTime)  + "in lane" + str(self.lane)
    
    def __lt__(self, other):
        return self.arrivalTime < other.arrivalTime
