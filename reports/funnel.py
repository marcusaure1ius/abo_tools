import pandas as pd
import numpy as np
def create_funnel_df(df, steps):
    """
    Function used to create a pandas DataFrame that can be used for generating funnel plot
    Parameters
    ---------
    df : pandas.DataFrame
        Объект pandas df.
    steps : list
        Список исследуемых событий. Список необходимо формировать в порядке воронки, от стартового события, до завершающего.
    
    Returns
    -------
    funnel_df : pandas.DataFrame
        В качестве вывода будет объект pandas df с посчитанным кол-вом клиентов на каждом из этапов воронки (исследуемых событий).
    """

    # Фильтруем датафрейм только нужными для нас атрибутами и проверяем, что события из фрейма соответствуют событиям из steps
    df = df[['id', 'event', 'event_dt']]

    df = df[df['event'].isin(steps)]

    values = [] # Список значений для каждого события 

    dfs = {} # Словарь для датафрейма каждого события

    # Для каждого из событий создаем отдельный датафрейм
    for i, step in enumerate(steps):
        if i == 0:
            # Фильтурем и дедублицируем наш датафрейм и соответствующее событие
            dfs[step] = df[df['event'] == step].sort_values(['id', 'event_dt'], ascending=True).drop_duplicates(subset=['id', 'event'], keep='first')

        else:
            # Фильтруем одно событие
            dfs[step] = df[df['event'] == step]
            
            # Мерджим предыдущее событие и текущее таким образом вычисляем, сколько клиентов перешло на следующий шаг
            merged = pd.merge(dfs[steps[i - 1]], dfs[step], on='id', how='left')
            # Удостоверяемся, что следующее событие действительное следующее, делаем мы это проверкой на то, что следующее событие по времени больше предыдущего
            merged = merged[merged['event_dt_y'] >= merged['event_dt_x']].sort_values('event_dt_y', ascending=True)
            # Удаляем дубликаты
            merged = merged.drop_duplicates(subset=['id', 'event_x', 'event_y'], keep='first')
            # Переименовываем события для следующего мерджа
            merged = merged[['id', 'event_y', 'event_dt_y']].rename({'event_y': 'event', 'event_dt_y':'event_dt'}, axis=1)

            dfs[step] = merged
        # Вычисляем кол-во клиентов
        values.append(len(dfs[step]))

    funnel_df = pd.DataFrame({'step':steps, 'val':values})

    return funnel_df

def stacking_funnel(df, steps, col):
    """
    Функция разделения воронки на подгруппы, например, воронка в разрезе ОС
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
    dict_ : dict
        В качестве вывода будет объект dict, содержащий застаканные датафреймы
    """
    dict_ = {}
    # Получаем все ИД клиентов, разделенные по col в виде словаря
    ids = dict(df.groupby([col])['id'].apply(set))
    # Создаем отдельный датафрейм для каждого из параметров разделения (сol) и для каждого из них получаем параметры построения воронки и записываем в словарь
    for entry in df[col].dropna().unique():
        ids_list = ids[entry]
        df = df[df['id'].isin(ids_list)].copy()
        if len(df[df['event'] == steps[0]]) > 0:
            dict_[entry] = create_funnel_df(df, steps)
    return dict_