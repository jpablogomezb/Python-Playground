import os
import datetime, random, string
import pandas as pd
import numpy as np
import statsmodels.api as sm
#import statsmodels.formula.api as smf
import scipy.stats as scipystats
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
timestamp = datetime.datetime.now()

data_file = os.path.join(DATA_DIR, 'data_file.csv')
#pandas
df = pd.read_csv(data_file)
print("Dataframe Info:")
print(df.info())
#Summary information with descriptive statistics like count, mean, stdev, and the five number summary.
#print(df.describe)

def descriptive_stats_to_img(df, dir_to_save=None, df_fname=None):    
    """Create an image file with descriptive statistics summary from a dataframe.

    Parameters
    ----------
    df: pandas DataFrame
    dir_to_save: str or path object 
            directory to save the image
    df_fname: str
            Name to save the image (optional)
    """
    if dir_to_save == None:
        raise Exception("Please provide a str, path object for the directory to save the image")
    figures_dir = dir_to_save
    if df_fname != None:
        f_name = df_fname 
    else:
        try:
            fstr = os.path.basename(data_file)
        except:
            fstr  = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
        f_name = "{}__descriptive-statistics__{}.png".format(fstr, timestamp.strftime("%Y-%m-%d"))
    try:
        desc_img = plt
        #desc_img.rcParams['figure.figsize'] = (6,2)
        desc_img.figure(figsize=(6,2))
        desc_img.text(0.01, 0.05, str(df.describe()), {'fontsize': 10}, fontproperties = 'monospace')
        desc_img.axis('off')
        desc_img.tight_layout()
        desc_img.savefig(os.path.join(figures_dir, f_name)) 
        #desc_img.show()
        desc_img.clf()
        desc_img.close()
        saved = True
        print("Descriptive statitics of {}...".format(os.path.basename(data_file)))
    except:
        saved = False
    return saved

descriptive_stats_to_img(df, FIGURES_DIR)

def explore_numeric_vars_to_img(df, dir_to_save=None):
    """ Using each numeric variable in data:
    Create image files for visualizing univariate histogram and density plots, and box plots.
    Create a correlation matrix image among variables
    Create a plot pairwise relationship using scatterplots for each pairing of the variables.
    
    Parameters
    ----------
    df: pandas DataFrame
    dir_to_save: str or path object 
            directory to save the image
    """

    if dir_to_save == None:
        raise Exception("Please provide a str, path object for the directory to save the figures")
    figures_dir = dir_to_save
    try:
        for i in range(df.select_dtypes(exclude=['object', 'bool']).shape[1]):
            try:
                print("Histogram / density plot for variable: {}...".format(df.columns[i]))
                var_data = df.iloc[:,i]
                #print(var_data)
                plt.style.use('ggplot')
                plt.figure(figsize=(8,6))
                plt.hist(var_data, density=True, color = 'g',  label='Histogram from values', alpha = 0.4, edgecolor = 'black')
                #sns.distplot(df.iloc[:,i], hist=True, kde=True, bins=int(10), color = 'green', hist_kws={'edgecolor':'black'})
                plt.title("Density Plot and Histogram for {}".format(df.columns[i].replace("_", " ").title()))
                plt.xlabel("{}".format(df.columns[i]).replace("_", " ").title())
                plt.ylabel("Density")

                # add density plot
                density = scipystats.gaussian_kde(var_data)
                x_vals = np.linspace(var_data.min(), var_data.max())
                density.covariance_factor = lambda : .2 #bandwith
                density._compute_covariance()
                plt.plot(x_vals, density(x_vals), color = "b")
                plt.savefig(os.path.join(figures_dir, "{}__histogram-density-plot__{}.png".format(df.columns[i], timestamp.strftime("%Y-%m-%d"))))
                #plt.show()
                plt.clf()
                plt.close()

                #Box Plot
                print("Box plot for variable: {}...".format(df.columns[i]))
                plt.style.use('ggplot')
                plt.title("Box Plot for {}".format(df.columns[i].replace("_", " ").title()))
                plt.boxplot(var_data)
                plt.savefig(os.path.join(figures_dir, "{}__box-plot__{}.png".format(df.columns[i], timestamp.strftime("%Y-%m-%d"))))
                #plt.show()
                plt.clf()
                plt.close()
            except Exception as e:
                print(e)
                print("There was a problem generating the plots for variable: {}".format(df.columns[i]))

        #check correlation among variables
        print("Correlation Matrix of {}...".format(os.path.basename(data_file)))
        corrMatrix = df.corr()
        #print(corrMatrix)
        plt.style.use('ggplot')
        plt.figure(figsize=(8,6))
        sns.heatmap(corrMatrix, annot=True)
        plt.title("Correlation Matrix of {}".format(os.path.basename(data_file)))
        plt.savefig(os.path.join(figures_dir, "{}__correlation-matrix__{}.png".format(os.path.basename(data_file), timestamp.strftime("%Y-%m-%d"))))
        #plt.show()
        plt.clf()
        plt.close()

        print("Plot pairwise relationships of {}...".format(os.path.basename(data_file)))
        plt.style.use('ggplot')
        sns.pairplot(df.dropna(how='any', axis=0), corner=True, height=3.5)
        plt.ylabel("Plot pairwise relationships of {}".format(os.path.basename(data_file)))
        plt.savefig(os.path.join(figures_dir, "{}__plot-pairwise-relationships__{}.png".format(os.path.basename(data_file), timestamp.strftime("%Y-%m-%d"))))
        #plt.show()
        plt.clf()
        plt.close()

        return True

    except Exception as e:
        print(e)
        return False

explore_numeric_vars_to_img(df, FIGURES_DIR)