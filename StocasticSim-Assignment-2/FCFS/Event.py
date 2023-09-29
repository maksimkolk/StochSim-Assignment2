class Event:

    ARRIVAL = 0
    DEPARTURE = 1
    
    def __init__(self, typ, time, lane, cust = None):  # type is a reserved word
        self.type = typ
        self.time = time
        self.customer = cust
        self.lane = lane
        
    def __lt__(self, other):
        return self.time < other.time

    def __str__(self):
        s = ('Arrival', 'Departure')
        return s[self.type] + " of customer " + str(self.customer)
        + ' at t = ' + str(self.time)
    
    
