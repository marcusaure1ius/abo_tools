import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

def rete_prepare(df, by_percent=True, slice_num=7):
    if by_percent:
        m = df.columns.tolist()
        del(m[1::2])
        df.drop(m,axis=1, inplace=True)

        df.drop(df.index[[0]], inplace=True)

        templist = df.columns.tolist()
        sec_templist = []
        for element in templist:
            sec_templist.append(element[0:slice_num])
        
        df = df.set_axis(sec_templist, axis=1, inplace=True)


    else:
        m = df.columns.tolist()
        del(m[1::2])
        df.drop(m,axis=1, inplace=True)

        df.drop(df.columns[[0]], axis='columns', inplace=True)
        df.drop(df.index[[0]], inplace=True)

        templist = df.columns.tolist()
        sec_templist = []
        for element in templist:
            sec_templist.append(element[0:slice_num])
        
        df = df.set_axis(sec_templist, axis=1, inplace=True)