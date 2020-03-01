import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
from ..utils import utils_core as utls
from ..plot import core as plot

def bool_type(df, col, drop=False, label=None, outlier=False, plot_type=None, *args, **kwargs):
    if drop:
        df.dropna(subset=[col], inplace=True)

    utls.categoriсal_dict(df, col)

    if label is not None:
        label = label
    else:
        label = df[col].unique()

    if outlier:
        utls.remove_outlier(df, col)

    for i in range(len(label)):
        print('{name} - {count}, {percent: .2f}%'.format(name=label[i], count=df[df[col] == i][col].count(),
            percent=(df[df[col] == i][col].count()/df[col].count())*100))
    
    #TODO: сделать словарь для визуализаций
    if plot_type == 'pie':
        pie_plot(df, col, labels=label)
    elif plot_type == 'count':
        count_plot(df, col)