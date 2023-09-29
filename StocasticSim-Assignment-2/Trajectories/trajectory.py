from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
B = 1
linewidth = 0.7

class Trajectory:
    ''' An object of this class describes the trajectory of one car. Input for
    initialization is the original arrival time, the scheduled arrival time
    i.e. start of service, t_full_y (the time the predecessor reaches full
    speed), start of service (i.e. scheduled arrival time) of the predecessor,
    and the road length which is initialized at 300 as given in the assignment.'''
    
    def __init__(self, arrival: float, start_service: float, t_full_y = -100, start_service_predecessor = -100, road_length=300, v_m=13, a_m=3):
        self.road_length = road_length
        self.t_full_y = t_full_y # time that pred(ecessor) reaches full speed
        self.start_service_pred = start_service_predecessor # start of service time of pred
        
        self.start_service = start_service # the time this car gets served is assigned in the simulation
        self.arrival = arrival #time the car would arrive at the intersection if driving the whole way at full speed, so arrival at queue
        
        self.v_m = v_m
        self.a_m = a_m
    
    def calculate_trajectory_times(self):
        ''' Calculates the starting times of each segment of the trajectory and
        returns them in a list in the order [start of segment, t_decelerate, t_stop,
        t_accelerate, t_full, start_service]'''
        
        assert self.start_service > self.start_service_pred, "A car cannot arrive earlier than its predecessor"
        if self.start_service - self.start_service_pred == B: # if the car has a predecessor in the same platoon
            t_full = self.t_full_y # t_full is the same as that of the predecessor
        else:
            t_full = self.start_service #if no predecessor, car reaches full speed at start of service
        
        t_start = self.arrival - self.road_length/self.v_m
        # does the car have to make a full stop?
        # if the difference between original arrival and scheduled arrival is large enough to stop and start again then yes
        if self.v_m * (self.start_service - t_start - self.v_m/self.a_m) >= self.road_length:
            full_stop = True
        else:
            full_stop = False
        
        # next we calculate all the times and return them
        if full_stop: # if the car makes a full stop
            # the next three formulas are taken from the article of Timmerman and Boon, algorithm 4
            t_accelerate = t_full - self.v_m/self.a_m
            t_stop = t_accelerate - (self.start_service - t_start - self.v_m/self.a_m - self.road_length/self.v_m)
            t_decelerate = t_stop - self.v_m/self.a_m
            return [t_start, t_decelerate, t_stop, t_accelerate, t_full, self.start_service]
        else: # the car makes no full stop
            # the next four formulas are taken from the article of Timmerman and Boon, algorithm 4
            deceleration_time = sqrt(((self.start_service-t_start)*self.v_m - self.road_length)/self.a_m) # this is the amount of time the car decelerates for
            t_accelerate = t_full - deceleration_time # the car decelerates and accelerates for the same amount of time
            t_stop = t_accelerate # the car makes no full stop so we set this
            t_decelerate = t_accelerate - deceleration_time
            return [t_start, t_decelerate, t_stop, t_accelerate, t_full, self.start_service]
        
    def show_one_trajectory(self, trajectory_times:list, v_m=13, a_m=3, lane=0, single_plot=True):
        ''' Plot a single trajectory, given the starting times of each segment
        in the order [start of segment, t_decelerate, t_stop,
        t_accelerate, t_full, start_service], speed v_m in m/s, acceleration a_m
        in m/s^2 and the lane.'''
        assert lane <= 3, "Lane number is above 3"
        road_length = -self.road_length
        colors = ['b', 'r', 'g', 'c'] # this can handle systems with up to 4 lanes. Since we only need 2, that is enough
        direction = (-1)**lane # positive for even lane number, negative for odd lane number
        arrival_cr = trajectory_times[0]
        
        # we check again whether the car makes a full stop or not
        if self.v_m * (self.start_service - trajectory_times[0] - self.v_m/self.a_m) >= self.road_length:
            full_stop = True
        else:
            full_stop = False
        
        # if there is only one plot, we need to prepare it. Else that is done outside of this function
        if single_plot == True:
            # setting the axes at the centre
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')

        # plot the functions
        if full_stop: # the car makes a full stop
            # but first some local variables so that we don't compute them several times
            shift = (trajectory_times[4]-trajectory_times[5])*self.v_m - self.v_m**2/(2*self.a_m)
            
            # segments 1, 3, 5 are straight lines so we only need to name their start and endpoints
            plt.plot(trajectory_times[0:2],[direction*road_length,direction*(road_length+self.v_m*(trajectory_times[1]-arrival_cr))], colors[lane],linewidth=linewidth)
            plt.plot(trajectory_times[2:4],[direction*shift,direction*shift], colors[lane],linewidth=linewidth)
            plt.plot(trajectory_times[4:],[direction*(shift+self.v_m**2/(2*self.a_m)),0], colors[lane],linewidth=linewidth)
    
            # the other two segments are quadratic functions
            t_deceleration = np.linspace(trajectory_times[1], trajectory_times[2],20)
            t_acceleration = np.linspace(trajectory_times[3], trajectory_times[4],20)
    
            x_decelerate = direction*(shift - (self.a_m/2)*(t_deceleration - trajectory_times[2])**2)
            x_accelerate = direction*(shift + (self.a_m/2)*(t_acceleration - trajectory_times[3])**2)
    
            plt.plot(t_deceleration,x_decelerate, colors[lane],linewidth=linewidth)
            plt.plot(t_acceleration,x_accelerate, colors[lane],linewidth=linewidth)
        
        elif not full_stop: # the car makes no full stop
            #segments 1 and 4 (out of 4) are straight lines so we only need their start and endpoints
            plt.plot(trajectory_times[0:2],[direction*road_length,direction*(road_length+self.v_m*(trajectory_times[1]-arrival_cr))], colors[lane],linewidth=linewidth)
            plt.plot(trajectory_times[4:],[-direction*(trajectory_times[5]-trajectory_times[4])*self.v_m,0], colors[lane],linewidth=linewidth)
            
            # the other two segments are quadratic functions
            t_deceleration = np.linspace(trajectory_times[1], trajectory_times[2],20)
            t_acceleration = np.linspace(trajectory_times[3], trajectory_times[4],20)
            
            x_decelerate = direction*(road_length + self.v_m * (t_deceleration-arrival_cr) - (self.a_m/2)*(t_deceleration - trajectory_times[1])**2)
            x_accelerate = direction*((t_acceleration - trajectory_times[5])*self.v_m + (self.a_m/2)*(t_acceleration - trajectory_times[4])**2)
            
            plt.plot(t_deceleration,x_decelerate, colors[lane],linewidth=linewidth)
            plt.plot(t_acceleration,x_accelerate, colors[lane],linewidth=linewidth)
        else:
            pass

        if single_plot:
            # show the plot
            plt.show()
