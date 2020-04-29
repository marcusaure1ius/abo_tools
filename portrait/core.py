import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
from ..utils import utils_core as utils
from ..plot import core as plot

def bool_type(df, col, label=None, use_drop=False, use_cat_dict=False, use_outlier=False, use_nan_dict=False, *args, **kwargs):
    if use_drop:
        df.dropna(subset=[col], inplace=True)

    if use_cat_dict:
        utils.categoriсal_dict(df, col)

    if label is not None:
        label = label
    else:
        label = df[col].unique()

    if use_outlier:
        utils.remove_outlier(df, col)

    if use_nan_dict:
        df[col] = df[col].map(utils.nan_dict)

    for i in range(len(label)):
        print('{name} - {count}, {percent: .2f}%'.format(name=label[i], count=df[df[col] == i][col].count(),
            percent=(df[df[col] == i][col].count()/df[col].count())*100))