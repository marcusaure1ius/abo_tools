import pandas as pd
import numpy as np

def get_start_step(x, start_step, n_steps):
    """
    Функция, возвращающая первые n_steps шагов для каждого клиента, начиная с start_step
    Parameters
    ----------
    x : pd.Series
        Серия пандас с событиями\n
    start_step : str
        Название события, с которого начинается путь клиента\n
    n_steps : int
        Кол-во возвращаемых событий

    Returns
    -------
    x : list
        Список событий
    """
    start_step_index = x.index(start_step)

    return x[start_step_index: start_step_index + n_steps]

def get_user_flow(df, start_step, n_steps=5, events_per_step=5):
    """
    Функция возвращающая уникальную последовательность событий для каждого из клиентов
    Parameters
    ----------
    df : pandas.DataFrame
        Объект pandas df.\n
    start_step : str
        Название события, с которого начинается путь клиента\n
    n_steps : int
        Кол-во возвращаемых событий\n
    events_per_step : int
        Кол-во событий, показываемых на каждом из шагов. Минимально - должно быть не менее 5 событий
    
    Returns
    -------
    flow : pandas.DataFrame
        Объект pandas df.\n
    """
    events = df.sort_values(['id', 'event_dt'])
    # find the users that have performed the starting_step
    valid_ids = events[events['event'] == start_step]['id'].unique()

    # plan out the journey per user, with each step in a separate column
    flow = events[(events['id'].isin(valid_ids))] \
        .groupby('id') \
        .event.agg(list) \
        .to_frame()['event'] \
        .apply(lambda x: get_start_step(x, start_step=start_step, n_steps=n_steps)) \
        .to_frame() \
        ['event'].apply(pd.Series)

    # fill NaNs with "End" to denote no further step by user; this will be filtered out later
    flow = flow.fillna('End')

    # add the step number as prefix to each step
    for i, col in enumerate(flow.columns):
        flow[col] = '{}: '.format(i + 1) + flow[col].astype(str)

    # replace events not in the top "events_per_step" most frequent list with the name "Other"
    # this is done to avoid having too many nodes in the sankey diagram
    for col in flow.columns:
        all_events = flow[col].value_counts().index.tolist()
        all_events = [e for e in all_events if e != (str(col + 1) + ': End')]
        top_events = all_events[:events_per_step]
        to_replace = list(set(all_events) - set(top_events))
        flow[col].replace(to_replace, [str(col + 1) + ': Other'] * len(to_replace), inplace=True)

    # count the number of identical journeys up the max step defined
    flow = flow.groupby(list(range(n_steps))) \
        .size() \
        .to_frame() \
        .rename({0: 'count'}, axis=1) \
        .reset_index()

    return flow

def get_flow_df(df, start_step, n_steps=5, events_per_step=5):
    """
    Функция для генерация датафрейма для дальнейшей визуализации
    Parameters
    ----------
    df : pandas.DataFrame
        Объект pandas df.\n
    start_step : str
        Название события, с которого начинается путь клиента\n
    n_steps : int
        Кол-во возвращаемых событий\n
    events_per_step : int
        Кол-во событий, показываемых на каждом из шагов. Минимально - должно быть не менее 5 событий
    
    Returns
    -------
    label_list : list
        Список значений\n
    colors_list : list
        Список цветов\n
    source_target_df : pandas.DataFrame
        Объект pandas df.
    """
    # generate the user user flow dataframe
    flow = get_user_flow(df, start_step, n_steps, events_per_step)

    # create the nodes labels list
    label_list = []
    cat_cols = flow.columns[:-1].values.tolist()
    for cat_col in cat_cols:
        label_list_temp = list(set(flow[cat_col].values))
        label_list = label_list + label_list_temp

    # create a list of colours for the nodes
    # assign 'blue' to any node and 'grey' to "Other" nodes
    colors_list = ['blue' if i.find('Other') < 0 else 'grey' for i in label_list]

    # transform flow df into a source-target pair
    for i in range(len(cat_cols) - 1):
        if i == 0:
            source_target_df = flow[[cat_cols[i], cat_cols[i + 1], 'count']]
            source_target_df.columns = ['source', 'target', 'count']
        else:
            temp_df = flow[[cat_cols[i], cat_cols[i + 1], 'count']]
            temp_df.columns = ['source', 'target', 'count']
            source_target_df = pd.concat([source_target_df, temp_df])
        source_target_df = source_target_df.groupby(['source', 'target']).agg({'count': 'sum'}).reset_index()

    # add index for source-target pair
    source_target_df['source_id'] = source_target_df['source'].apply(lambda x: label_list.index(x))
    source_target_df['target_id'] = source_target_df['target'].apply(lambda x: label_list.index(x))

    # filter out the end step
    source_target_df = source_target_df[(~source_target_df['source'].str.contains('End')) &
                                        (~source_target_df['target'].str.contains('End'))]

    return label_list, colors_list, source_target_df