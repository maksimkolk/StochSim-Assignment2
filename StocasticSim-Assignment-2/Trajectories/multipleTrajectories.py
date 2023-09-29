from Trajectories.trajectory import Trajectory
import matplotlib.pyplot as plt
import pandas as pd

# The following imports are only necessary for plotting the trajectories of the simulations, not the plot_trajectories(...) function itself
from FCFS.Exhaustive_Simulation import EXHSimulation
from FCFS.BunchedExponential import BunchedExp


# Here we are going to plot all trajectories instead of just one.
def plot_trajectories(arrival_times_0: list, service_start_0: list, arrival_times_1: list, service_start_1: list):
    '''Show the trajectories of all vehicles, given a list of arrival times (initial
    arrival times/arrival at queue) and service start times (actual/scheduled
    arrival at the intersection/start of service) for each of the two lanes'''
    
    # First we prepare the figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    
    # Plot trajectories separately for both lanes
    for lane in [0,1]:
        if lane == 0:
            assert len(arrival_times_0) == len(service_start_0), "The number of cars arriving and leaving should be the same"
            nrCars = len(arrival_times_0)
            
            #first trajectory
            traj = Trajectory(arrival_times_0[0],service_start_0[0])
            times = traj.calculate_trajectory_times()
            traj.show_one_trajectory(times, lane=0, single_plot=False)
            t_full_y = times[4]
            t_f_y = times[5]
            
            #Save road_length for setting the axes:
            road_length = traj.road_length
            
            #all other trajectories
            for i in range(1,nrCars):
                traj = Trajectory(arrival_times_0[i],service_start_0[i],t_full_y=t_full_y,start_service_predecessor=t_f_y)
                times = traj.calculate_trajectory_times()
                traj.show_one_trajectory(times, lane=0, single_plot=False)
                t_full_y = times[4]
                t_f_y = times[5]
            
            #save the highest used value of t for setting the axes:
            max_t_0 = t_f_y
        elif lane == 1:
            assert len(arrival_times_1) == len(service_start_1), "The number of cars arriving and leaving should be the same"
            nrCars = len(arrival_times_1)
            
            #first trajectory
            traj1 = Trajectory(arrival_times_1[0],service_start_1[0])
            times = traj1.calculate_trajectory_times()
            traj1.show_one_trajectory(times, lane=1, single_plot=False)
            t_full_y = times[4]
            t_f_y = times[5]
            
            #all other trajectories
            for i in range(1,nrCars):
                traj1 = Trajectory(arrival_times_1[i],service_start_1[i],t_full_y,t_f_y)
                times = traj1.calculate_trajectory_times()
                traj1.show_one_trajectory(times, lane=1, single_plot=False)
                t_full_y = times[4]
                t_f_y = times[5]
                
            #save the highest used value of t for setting the axes:
            max_t_1 = t_f_y
    # Here comes the rest of plot preparation, including setting the axes
    max_t = max(max_t_0, max_t_1)
    plt.axis([0,max_t,-road_length,road_length])
    # fig.savefig("Trajectories from distribution.pdf") # uncomment if you want to save the plot
    plt.show()
    

### Here we make the plots that are asked in the assignment.

## First the case with data
df = pd.read_excel(r'C:\Users\20193986\OneDrive - TU Eindhoven\TUe\2022-2023\_Q3\2WB50 Stochastic simulation\Assignment 2\StocasticSim-Assignment-2\arrivals5.xlsx', header=None)

df.columns = [0,1]
lane0 = df[0].tolist()
lane1 = df[1].tolist()

arrDist = [lane0, lane1]

sim = EXHSimulation(arrDist, 2, True) # the simulation model
res = sim.simulate(300)  # perform simulation 


# now that the simulation is finished, we read the data and convert them in such a way that the function above can be used to depict the trajectories
df_output = pd.read_csv(r'C:\Users\20193986\OneDrive - TU Eindhoven\TUe\2022-2023\_Q3\2WB50 Stochastic simulation\Assignment 2\StocasticSim-Assignment-2\output_data.csv')

# prepare the lists
arrival_times_0 = []
service_start_0 = []
arrival_times_1 = []
service_start_1 = []

# fill the lists with the correct values
for car in range(100):
    if df_output.at[car,'Lane'] == 0:
        arrival_times_0.append(round(df_output.at[car, 'Arrival'],10)) 
        service_start_0.append(round(df_output.at[car, 'Service'],10))
    elif df_output.at[car,'Lane'] == 1: # the car is in lane 1
        arrival_times_1.append(round(df_output.at[car, 'Arrival'],10))
        service_start_1.append(round(df_output.at[car, 'Service'],10))

# The input for show_trajectories(...) is prepared, now we can run the function
plot_trajectories(arrival_times_0, service_start_0, arrival_times_1, service_start_1)


## Next, the case with randomly generated data

# alpha and mu were determined before, using the estimateParameters() function
alpha0, alpha1, mu0, mu1 = 0.5995995995995996, 0.5725725725725725, 0.21564291046984274, 0.3102950696782692

arrDist = [BunchedExp, BunchedExp] # interarrival time distr. for each lane
sim = EXHSimulation(arrDist, 2, False, [alpha0, alpha1], [mu0, mu1]) # the simulation model
res = sim.simulate(1000)  # perform simulation. We only need the first 100 cars so a sim length of 1000 should be enough
print(res)  # print the results

# now that the simulation is finished, we read the data and convert them in such a way that the function above can be used to depict the trajectories
df_output = pd.read_csv(r'C:\Users\20193986\OneDrive - TU Eindhoven\TUe\2022-2023\_Q3\2WB50 Stochastic simulation\Assignment 2\StocasticSim-Assignment-2\output.csv')

# prepare the lists
arrival_times_0 = []
service_start_0 = []
arrival_times_1 = []
service_start_1 = []

# fill the lists with the correct values
for car in range(100):
    if df_output.at[car,'Lane'] == 0:
        arrival_times_0.append(round(df_output.at[car, 'Arrival'],8)) # there are sometimes rounding errors in the output, which cause errors because a car is served 3e-12 seconds before it arrives
        service_start_0.append(round(df_output.at[car, 'Service'],8))
    elif df_output.at[car,'Lane'] == 1: # the car is in lane 1
        arrival_times_1.append(round(df_output.at[car, 'Arrival'],8))
        service_start_1.append(round(df_output.at[car, 'Service'],8))

# The input for show_trajectories(...) is prepared, now we can run the function
plot_trajectories(arrival_times_0, service_start_0, arrival_times_1, service_start_1)
