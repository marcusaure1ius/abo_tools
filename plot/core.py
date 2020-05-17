import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt # библиотека для построения простых графиков
import seaborn as sns # еще одна библиотека для построения более сложных графиков
from ..reports import funnel as funnel
from ..reports import flow as flow

def dist_plot(dataframe, column, title=None, kde_color = 'blue', hist_color = 'blue', **kwargs): # ГРАФИК РАСПРЕДЕЛЕНИЯ
    plt.figure(figsize=(16,6)) #figure size
    sns.set_style('whitegrid') #background style
    ax = sns.distplot(
        dataframe[column], # var
        kde_kws={'color': '{}'.format(kde_color), 'label': 'Line'}, #kde style
        hist_kws={'color':'{}'.format(hist_color),'label':'Histogram'} #hist style
    )
    if title is None:
        plt.title('Distplot of {}'.format(column))
    else:
        plt.title(title)
    plt.ylabel('Density')#y axis label
    plt.xlabel('{}'.format(column))# x axis label
    plt.show()

def count_plot(dataframe, column, title=None, hue_var=None, palette = 'Set3', xtick=None,legend=None, **kwargs): # ГРАФИК КОЛ-ВА ЗНАЧЕНИЙ
    plt.figure(figsize=(16,6)) #figure size
    sns.set_style('whitegrid') #background style
    if hue_var is None: #if hue is set
        ax = sns.countplot(x = dataframe[column], palette='{}'.format(palette))
    else:
        ax = sns.countplot(x = dataframe[column], palette='{}'.format(palette), hue = dataframe[hue_var])
    
    if title is None:
        plt.title('Countplot of {}'.format(column))
    else:
        plt.title(title)
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
        xaxis = {'title': '{}'.format(x_column)},
        yaxis = {'title': '{}'.format('Count')}
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

def pie_plot(df, column, labels=None, clr=None):
    colors = ['#721de2','#b5c3ff']
    if len(colors) > 2:
        colors = clr
        
    if labels is None:
        labels = df[column].unique()

    explode = df[column].value_counts()
    
    const = 0.05
    l = []
    for i in range(len(labels)):
        l.append(const)
        
    exp = l
    fig1, ax1 = plt.subplots()
    ax1.pie(explode, explode = exp, labels=labels, autopct='%1.1f%%',shadow=False, colors = colors, startangle=90, 
            textprops={'color':'#000000', 'fontsize':15})
    ax1.axis('equal')
    
    centre_circle = plt.Circle((0,0),0.60,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.show()

def bar_plot(x, y, title=None, palette = 'Set3', xtick=None,legend=None, **kwargs): # ГРАФИК КОЛ-ВА ЗНАЧЕНИЙ
    plt.figure(figsize=(16,6)) #figure size
    sns.set_style('darkgrid') #background style
    ax = sns.barplot(x=x, y=y, palette='{}'.format(palette))
    
    if title is None:
        plt.title('Countplot')
    else:
        plt.title(title)
    #plt.ylabel('Count')#y axis label
    #plt.xlabel('{}'.format(column))# x axis label
    if xtick is not None: #if xtick is set
        ax.set_xticklabels(xtick)
    if legend is not None:
        handles, _ = ax.get_legend_handles_labels()
        ax.legend(handles, legend)
    plt.show()

def funnel_plot(df, steps, col=None):
    """
    Функция для построения воронки с помощью plotly
    Parameters
    ---------
    df : pandas.DataFrame
        Объект pandas df.
    steps : list
        Список исследуемых событий. Список необходимо формировать в порядке воронки, от стартового события, до завершающего.
    col : str
        Фича, по которой будет разделение воронки. Например - OS, воронка будет разделена на iOS и Android.
    
    Returns
    -------
    fig : plotly.graph_objs._figure.Figure
        В качестве вывода будет объект Figure библиотеки plotly
    """
    data = []

    if col:
        dict_ = funnel.stacking_funnel(df, steps, col)
        title = 'Воронка заявки в разрезе {}'.format(col)
    else:
        funnel_df = funnel.create_funnel_df(df, steps)
        dict_ = {'Total': funnel_df}
        title = 'Воронка заявки'

    for t in dict_.keys():
        trace = go.Funnel(
            name=t,
            y=dict_[t].step.values,
            x=dict_[t].val.values,
            textinfo='value+percent previous'
        )
        data.append(trace)
    
    layout = go.Layout(margin={"l": 180, "r": 0, "t": 30, "b": 0, "pad": 0},
                       funnelmode="stack",
                       showlegend=True,
                       hovermode='closest',
                       title=title,
                       legend=dict(orientation="v",
                                   bgcolor='#E2E2E2',
                                   xanchor='left',
                                   font=dict(
                                       size=12)
                                   )
                       )
    fig = go.Figure(data, layout)
    return fig

def user_flow_plot(df, start_step, n_steps=5, events_per_step=5, title='User Flow'):
    """
    Функция для посроения графика путей клиентов по событиям
    Parameters
    ----------
    df : pandas.DataFrame
        Объект pandas df.\n
    start_step : str
        Название события, с которого начинается путь клиента\n
    n_steps : int
        Кол-во возвращаемых событий\n
    events_per_step : int
        Кол-во событий, показываемых на каждом из шагов. Минимально - должно быть не менее 5 событий\n
    title : str
        Название диаграммы    
    
    Returns
    -------
    fig : plotly.graph_objs._figure.Figure
        В качестве вывода будет объект Figure библиотеки plotly
    """
    # transform raw events dataframe into  source:target pairs including node ids and count of each combination
    label_list, colors_list, source_target_df = flow.get_flow_df(df, start_step, n_steps, events_per_step)

    # creating the sankey diagram
    data = dict(
        type='sankey',
        node=dict(
            pad=20,
            thickness=20,
            color=colors_list,
            line=dict(
                color="black",
                width=0.5
            ),
            label=label_list
        ),
        link=dict(
            source=source_target_df['source_id'].values.tolist(),
            target=source_target_df['target_id'].values.tolist(),
            value=source_target_df['count'].astype(int).values.tolist(),
            hoverlabel=dict(
                bgcolor='#C2C4C7')
        )
    )

    # set window width
    if n_steps < 5:
        width = None
    else:
        width = n_steps * 250

    layout = dict(
        height=600,
        width=width,
        margin=dict(t=30, l=0, r=0, b=30),
        #         autosize=True,
        title=title,
        font=dict(
            size=10
        )
    )

    fig = dict(data=[data], layout=layout)
    return fig