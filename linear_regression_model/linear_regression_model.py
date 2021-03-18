import os
import datetime
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
#import seaborn as sns

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
timestamp = datetime.datetime.now()

data = os.path.join(DATA_DIR, 'data_file.csv')
#pandas
df = pd.read_csv(data)
print("Dataframe Info:")
print(df.info())
df.dropna(axis=0, how='any') # To drop rows with any empty cells
df.drop_duplicates()
#Summary information with descriptive statistics like count, mean, stdev, and the five number summary.
print("Descriptive Statistics Summary:")
print(df.describe())
print("Data example (10 first rows):")
print(df.head(10))

print('Generating linear regression models statistics...')
"""
Simple Linear Regression Model (with one numeric variable) - Using statsmodels module.
"""
#Using data columns 0 and 1 as the targeted and predictor variables (change formula if needed)
lrm = smf.ols(formula="{} ~ {}".format(df.columns[0], df.columns[1]), data= df).fit()
#print(lrm.summary()) # these are the results
#print(lrm.params) #numpy array

#figure with scatterplot
lrm_plot = plt
lrm_plot.style.use('ggplot')
lrm_plot.figure(figsize=(10,6))
lrm_plot.scatter(df.iloc[:, 1], df.iloc[:, 0], c = 'g')
lrm_plot.plot(df.iloc[:, 1], lrm.params[0] + lrm.params[1] * df.iloc[:, 1])
lrm_plot.xlabel("{}".format(df.columns[1]).replace("_", " ").title())
lrm_plot.ylabel("{}".format(df.columns[0]).replace("_", " ").title())
lrm_plot.title("{} vs. {}".format(df.columns[1].replace("_", " ").title(), df.columns[0].replace("_", " ").title()))
lrm_plot.savefig(os.path.join(FIGURES_DIR, "simple-linear-regre-plot__predictor_{}__{}.png".format(df.columns[1], timestamp.strftime("%Y-%m-%d"))))
#lrm_plot.show()
lrm_plot.clf()
lrm_plot.close()

#figure with results summary
lrm_fig = plt
lrm_fig.figure(figsize=(8,5))
lrm_fig.text(0.01, 0.05, str(lrm.summary()), {'fontsize': 10}, fontproperties = 'monospace')
lrm_fig.axis('off')
lrm_fig.tight_layout()
lrm_fig.savefig(os.path.join(FIGURES_DIR, "simple-linear-regr-results__predictor_{}__{}.png".format(df.columns[1], timestamp.strftime("%Y-%m-%d"))))
#lrm_fig.show()
lrm_fig.clf()
lrm_fig.close()
print('Simple linear regression model done')


"""
Multiple Linear Regression Model (with several numeric variables) - Using statsmodels module.
More predictor variables can be added in the formula if a linear relationship 
between the target variable and a potential predictor variable is significant (P-value <= 0.05).

To do: 
Check first correlation of each predictor variable with the target variable to add it or not to the formula.
"""
#Using data columns 0, 1, 2, as the targeted and predictor variables correspondingly (change formula if needed)
predictor_vars = "{} + {}".format(df.columns[1], df.columns[2])
lrm_multiple = smf.ols(formula=df.columns[0] + "~" + predictor_vars, data= df).fit()
#print(lrm_multiple.summary()) # these are the results
#print(lrm_multiple.params)

#figure with results summary
mul_lrm_fig = plt
mul_lrm_fig.figure(figsize=(9,6))
mul_lrm_fig.text(0.01, 0.05, str(lrm_multiple.summary()), {'fontsize': 10}, fontproperties = 'monospace')
mul_lrm_fig.axis('off')
mul_lrm_fig.tight_layout()
fname_mul = "multiple-linear-regr-results__{}.png".format(timestamp.strftime("%Y-%m-%d"))
to_save_mul = os.path.join(FIGURES_DIR, fname_mul)
mul_lrm_fig.savefig(to_save_mul)
#mul_lrm_fig.show()
mul_lrm_fig.clf()
mul_lrm_fig.close()
print('Multiple linear regression model done')


"""
Multiple Linear Regression Model (including one categorical variable) - Using statsmodels module.
Statsmodel automatically does one-hot encoding of the categorical variables (creating dummy variables with 0/1 values )
"""
#Using data column 0 as target var; 1 and 2, as numerical predictor vars; and 3 as categorical predictor var
#C() operator treats explicitly a variable as categorical (e.g. if it had been numeric)
predictor_vars = "{} + {} + C({})".format(df.columns[1], df.columns[2], df.columns[3])
lrm_mult_with_cate = smf.ols(formula=df.columns[0] + "~" + predictor_vars, data= df).fit()
#print(lrm_multiple_with_cat.summary()) # these are the results
#print(lrm_multiple_with_cat.params) #regression params

#figure with results summary
mc_lrm_fig = plt
mc_lrm_fig.figure(figsize=(9,6))
mc_lrm_fig.text(0.01, 0.05, str(lrm_mult_with_cate.summary()), {'fontsize': 10}, fontproperties = 'monospace')
mc_lrm_fig.axis('off')
mc_lrm_fig.tight_layout()
fname_mc = "multiple-linear-regr-w-categorical-results__{}.png".format(timestamp.strftime("%Y-%m-%d"))
to_save_mc = os.path.join(FIGURES_DIR, fname_mc)
mc_lrm_fig.savefig(to_save_mc)
#mul_lrm_fig.show()
mc_lrm_fig.clf()
mc_lrm_fig.close()
print('Multiple linear regression model with categorical vars done')

print('Models results correctly saved in the figures folder')
