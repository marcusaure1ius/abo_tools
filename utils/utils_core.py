import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns

"""
List of help function. If you need some help, call various method from this module and be HAPPY!
"""

def categoriсal_dict(df, col):
    categoryValue = df[col].unique()
    categoryValueCount = len(categoryValue)
    category_dict = {}
    for i in range(0, categoryValueCount):
        category_dict[categoryValue[i]] = i
    df[col] = df[col].map(category_dict).astype(int)

def remove_outlier(df, col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    fence_low = q1 - 1.5*iqr
    fence_high = q3 + 1.5*iqr
    df.drop(df[(df[col] < fence_low) | (df[col] > fence_high)].index, inplace=True)

def nan_dict(map_var):
    if map_var is np.nan:
        return 0
    else:
        return 1