import os
import datetime
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import scipy.stats as scipystats
import statsmodels.api as sm
import statsmodels.stats.stattools as stools
import statsmodels.stats as stats 
from statsmodels.graphics.regressionplots import *
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
#timestamp = datetime.datetime.now()

data = os.path.join(DATA_DIR, 'data_file.csv')
#pandas
df = pd.read_csv(data)
#Summary information with describe like how many non-missing values there, mean, stdev, and the five number summary.
print(df.describe())

'''
Visualizing a single variable with a histogram and density plots
'''
#print(df.iloc[:,0]) 
plt.style.use('ggplot')
plt.hist(df.iloc[:,0], bins=10, density=1, color = 'g', alpha = 0.4, edgecolor = 'black')
#sns.distplot(df.iloc[:,0], hist=True, kde=True, bins=int(10), color = 'green', hist_kws={'edgecolor':'black'})
plt.title("Density Plot and Histogram of {}".format(df.columns[0]).replace("_", " ").title())
plt.xlabel("{}".format(df.columns[0]).replace("_", " ").title())
plt.ylabel("Density")

# add density plot
density = scipystats.gaussian_kde(df.iloc[:,0])
x_vals = np.linspace(0, 100, 50)
density.covariance_factor = lambda : .2 #bandwith
density._compute_covariance()
plt.plot(x_vals, density(x_vals), color = "b")
#plt.show()
#plt.close()

#Box Plot
plt.boxplot(df.iloc[:,0], 0)
#plt.show()
#plt.close()

'''
Correlation of the data among variables (visualazing multiple plots)
'''
# check correlation between each variable and the targeted/dependent variable (saved at the first column)
corrMatrix = df.corr()
print(corrMatrix)
sns.heatmap(corrMatrix, annot=True)
plt.title("Correlation Matrix of {}".format(os.path.basename(data)))
plt.show()
plt.close()

sns.pairplot(df.dropna(how = 'any', axis = 0))
plt.show()
plt.close()