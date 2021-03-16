import os
import datetime
#import math
import pandas as pd
import numpy as np
#import itertools
#from itertools import chain, combinations
import statsmodels.formula.api as smf
#import scipy.stats as scipystats
import statsmodels.api as sm
import statsmodels.stats.stattools as stools
import statsmodels.stats as stats 
from statsmodels.graphics.regressionplots import *
import matplotlib.pyplot as plt
#import seaborn as sns

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
timestamp = datetime.datetime.now()

data = os.path.join(DATA_DIR, 'data_file.csv')
df = pd.read_csv(data)
#print(df.describe())
#print(df.iloc[:, 0])
#print(df.head(n=10))

'''
Simple Linear Regression Model (with numeric variables) - using statsmodels module.
'''
lrm = sm.OLS.from_formula(formula= "{} ~ {}".format(df.columns[0], df.columns[1]), data= df).fit()
#print(lrm.summary()) # these are the results

#figure with scatterplot
lrm_plot = plt
lrm_plot.rcParams['figure.figsize'] = (10, 6)
lrm_plot.scatter(df.iloc[:, 1], df.iloc[:, 0], c = 'g')
lrm_plot.plot(df.iloc[:, 1], lrm.params[0] + lrm.params[1] * df.iloc[:, 1])
lrm_plot.xlabel("{}".format(df.columns[1]).replace("_", " ").title())
lrm_plot.ylabel("{}".format(df.columns[0]).replace("_", " ").title())
lrm_plot.title("Simple Linear Regression Plot")
lrm_plot.savefig(os.path.join(FIGURES_DIR, "simple-plot_predictor_{}__{}.png".format(df.columns[1], timestamp.strftime("%Y-%m-%d"))))
#lrm_plot.show()
lrm_plot.close()

#figure with results summary
lrm_fig = plt
lrm_fig.rcParams['figure.figsize'] = (8, 5)
lrm_fig.text(0.01, 0.05, str(lrm.summary()), {'fontsize': 10}, fontproperties = 'monospace')
lrm_fig.axis('off')
lrm_fig.tight_layout()
lrm_fig.savefig(os.path.join(FIGURES_DIR, "simple-results_predictor_{}__{}.png".format(df.columns[1], timestamp.strftime("%Y-%m-%d"))))
#lrm_fig.show()
lrm_fig.close()


'''
Multiple Linear Regression Model (with numeric variables) - using statsmodels module.
More predictor variables are added in the next formula, if a linear relationship 
between the targeted variable and a potential predictor variable is significant (P-value <= 0.05)
'''
lrm_multiple = sm.OLS.from_formula(formula= "{} ~ {} + {}".format(df.columns[0], df.columns[1], df.columns[2]), data= df).fit()
#print(lrm_multiple.summary()) # these are the results

#figure with results summary
mul_lrm_fig = plt
mul_lrm_fig.rcParams['figure.figsize'] = (8, 5)
mul_lrm_fig.text(0.01, 0.05, str(lrm_multiple.summary()), {'fontsize': 10}, fontproperties = 'monospace')
mul_lrm_fig.axis('off')
mul_lrm_fig.tight_layout()
fname_mul = "multiple-linear-reg-results__{}.png".format(timestamp.strftime("%Y-%m-%d"))
to_save_mul = os.path.join(FIGURES_DIR, fname_mul)
lrm_fig.savefig(to_save_mul)
#lrm_fig.show()
mul_lrm_fig.close()