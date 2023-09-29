import numpy as np
from numpy import random
import seaborn as sns
import pandas as pd

import matplotlib.pyplot as plt

def BunchedExp(alpha, mu, B=1):
    """Sample n times from the bunched exponential distribution"""
    rng = random.default_rng()
    U = rng.uniform(0,1)
    if U < (1-alpha):
        return B
    else:
        output = (np.log(alpha)-np.log(-U+1)) / mu + B
        return output 
        

# l = [BunchedExp(0.6,0.3) for _ in range(1000)]   # Check the function by plotting a density plot. 
# l= np.cumsum(l)

# sns.kdeplot(l, color = 'darkblue')
# plt.show()


# # df = pd.read_excel(r'C:\Users\20203453\Documents\GitHub\StocasticSim-Assignment-2\arrivals5.xlsx', header = None)
# df = pd.read_excel(r'C:\Users\massi\Desktop\StocasticSim-Assignment-2\arrivals5.xlsx', header=None)
# df.columns = [0,1]
# lane0 = df[0].tolist()
# lane1 = df[1].tolist()
# df

# sns.kdeplot(lane0, color = 'darkblue')
# plt.show()

# sns.kdeplot(lane1, color = 'darkblue')
# plt.show()

# sns.histplot(lane1, color = 'darkblue')
# plt.show()

