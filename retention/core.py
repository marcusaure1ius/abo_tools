import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

class retention:
    def __init__(self, df):
        self.df = df
        
    def rete_prepare(self, by_percent=True):
        if by_percent:
            m = df.columns.tolist()
            del(m[1::2])
            df.drop(m,axis=1, inplace=True)
            
            df.drop(df.index[[0]], inplace=True)

            df.rename(columns={'Месяц 0 Retention, %':'Месяц 1',
            'Месяц 1 Retention, %':'Месяц 2',
            'Месяц 2 Retention, %':'Месяц 3',
            'Месяц 3 Retention, %':'Месяц 4',
            'Месяц 4 Retention, %':'Месяц 5',
            'Месяц 5 Retention, %':'Месяц 6',
            'Месяц 6 Retention, %':'Месяц 7',
            'Месяц 7 Retention, %':'Месяц 8',
            'Месяц 8 Retention, %':'Месяц 9',
            'Месяц 9 Retention, %':'Месяц 10',
            'Месяц 10 Retention, %':'Месяц 11',
            'Месяц 11 Retention, %':'Месяц 12'}, inplace=True) 
        else:
            l = []
            for i in range(1, len(df.columns), 2):
                l.append(i)
            df.drop(df.columns[[l]], axis='columns', inplace=True)
            
            df.drop(df.columns[[0]], axis='columns', inplace=True)
            df.drop(df.index[[0]], inplace=True)

            df.rename(columns={'Месяц 0 Число вернувшихся пользователей в день N':'Месяц 1',
            'Месяц 1 Число вернувшихся пользователей в день N':'Месяц 2',
            'Месяц 2 Число вернувшихся пользователей в день N':'Месяц 3',
            'Месяц 3 Число вернувшихся пользователей в день N':'Месяц 4',
            'Месяц 4 Число вернувшихся пользователей в день N':'Месяц 5',
            'Месяц 5 Число вернувшихся пользователей в день N':'Месяц 6',
            'Месяц 6 Число вернувшихся пользователей в день N':'Месяц 7',
            'Месяц 7 Число вернувшихся пользователей в день N':'Месяц 8',
            'Месяц 8 Число вернувшихся пользователей в день N':'Месяц 9',
            'Месяц 9 Число вернувшихся пользователей в день N':'Месяц 10',
            'Месяц 10 Число вернувшихся пользователей в день N':'Месяц 11',
            'Месяц 11 Число вернувшихся пользователей в день N':'Месяц 12'}, inplace=True)
        
    def get_heatmap(self, title=''):
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