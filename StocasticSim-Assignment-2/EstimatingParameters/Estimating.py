import pandas as pd

def estimateParameters():
    df = pd.read_excel(r'C:\Users\20203453\Documents\GitHub\StocasticSim-Assignment-2\arrivals5.xlsx', header = None)
    df.columns = [0,1]
    lane0 = df[0].tolist()
    lane1 = df[1].tolist()
    B = 1
    alpha = []
    mu = []
    for i in range(2):
        lanes = [lane0, lane0]
        lane = lanes[i]
        proportion =[0,0]       #[greater then 1, less then 1]
        sumOfIntArr = []
        time1 = 0    # initialize value for the arrival time of the first car
        time2 = lane.pop(0)     # initialize value for the arrival time of the second car
        while len(lane) > 0:
            if time2 - time1 > B: # Check if the interarrival time is > or <= to B
                proportion[0] += 1
            else:
                proportion[1] += 1
            sumOfIntArr.append(time2 - time1)
            time1, time2 = time2, lane.pop(0) # Update the arrival times, such that we can look at the next interarrival time.
        a = proportion[0] / sum(proportion)
        mean = sum(sumOfIntArr) / len(sumOfIntArr)
        m = a / (mean-a*B)
        alpha.append(a)
        mu.append(m)
        print(f'alpha {i} = {a}')
        print(f'mean of interarrival time of lane {i} = {mean}')
        print(f'mu {i} = {a / (mean-a*B)} ')
    return alpha, mu

estimateParameters()
