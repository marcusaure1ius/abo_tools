import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt # библиотека для построения простых графиков
import seaborn as sns # еще одна библиотека для построения более сложных графиков

def dist_plot(dataframe, column, title, kde_color = 'blue', hist_color = 'blue', **kwargs): # ГРАФИК РАСПРЕДЕЛЕНИЯ
    plt.figure(figsize=(16,6)) #figure size
    sns.set_style('whitegrid') #background style
    ax = sns.distplot(
        dataframe[column], # var
        kde_kws={'color': '{}'.format(kde_color), 'label': 'Line'}, #kde style
        hist_kws={'color':'{}'.format(hist_color),'label':'Histogram'} #hist style
    )
    plt.title('Distplot of {}'.format(title)) #plot title
    plt.ylabel('Density')#y axis label
    plt.xlabel('{}'.format(column))# x axis label
    plt.show()

def count_plot(dataframe, column, title, hue_var=None, palette = 'Set3', xtick=None,legend=None, **kwargs): # ГРАФИК КОЛ-ВА ЗНАЧЕНИЙ
    plt.figure(figsize=(16,6)) #figure size
    sns.set_style('whitegrid') #background style
    if hue_var is None: #if hue is set
        ax = sns.countplot(x = dataframe[column], palette='{}'.format(palette))
    else:
        ax = sns.countplot(x = dataframe[column], palette='{}'.format(palette), hue = dataframe[hue_var])
    plt.title('Countplot of {}'.format(title)) #plot title
    plt.ylabel('Count')#y axis label
    plt.xlabel('{}'.format(column))# x axis label
    if xtick is not None: #if xtick is set
        ax.set_xticklabels(xtick)
    if legend is not None:
        handles, _ = ax.get_legend_handles_labels()
        ax.legend(handles, legend)
    plt.show()

def inter_hist_plot(dataframe, x_column = None, y_column = None, xbins_size = None, title = None,
                    x_title = None, y_title = None, **kwargs):
    trace0 = go.Histogram(
        x = dataframe[x_column],
        xbins = {'size': xbins_size}
    )
    layout = go.Layout(
        title = title,
        xaxis = {'title': '{}'.format(x_title)},
        yaxis = {'title': '{}'.format(y_title)}
    )

    data = [trace0]

    fig = go.Figure(data = data, layout = layout)
    py.iplot(fig, show_link = False)

def get_int_heatmap(df, title=''):
    z = df.values
    x = df.columns.array
    y = df.index.array
    colorscale = [[0,'#FFFFFF'],[1, '#F1C40F']]
    z_text = np.around(z, decimals=2)
    fig = ff.create_annotated_heatmap(
        z,
        x,
        annotation_text=z_text,
        colorscale=colorscale, 
        hoverinfo='z',
        showscale=True,
    )

    fig.layout.update(
        go.Layout(
            title = title,
        )
    )

    py.iplot(fig, show_link=False)

def get_static_heatmap(df, title='', cbar_title='', **kwargs):
    plt.figure(figsize=(16,6))
    sns.set_style('whitegrid')
    sns.set(font_scale=1.0)
    plt.title('Heatmap of {}'.format(title))
    ax = sns.heatmap(
        df, 
        annot=True, 
        vmin=35, 
        vmax=100, 
        fmt=".0f", 
        cbar_kws={'label': cbar_title},
    )
    ax.set_ylim(12.0, 0.0)
    plt.show()