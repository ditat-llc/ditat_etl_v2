import pandas as pd


def filter_companies(
        df: pd.DataFrame,
        mapping: dict,
        index_column: str='id'
    ):

    '''
    Filters dataframe according to different mapping using
    column names(s) as candidates where the label/tags mmight be present.

    Args:
        - df (pd.DataFrame)i
        - mappping (dict): The structure is the folling

        "
            {
                'industry': {
                    'filters: []
                    'columns': []
                } 
            }
        "
    '''

    # Not affecting the original dataframe
    df = df.copy()

    df_fitered = None
    
    # Also return a summary of the terms matched according to column and term name
    all_vcs = pd.DataFrame(columns=['index'])

    for key, value in mapping.items():
        is_range  = value.get('is_range')

        temp_vcs = pd.DataFrame(columns=['index'])
        temp_dfs = []

        columns = value['columns']
        filters = value['filters']

        if is_range:
            lower_range = filters[0]
            upper_range = filters[1]
    
            for col in columns:
                filtered_df = df.loc[(df[col] >= lower_range) & (df[col] <= upper_range), :]
    
        else:
            filters = [col.lower() for col in filters]

            for col in columns:
                filtered_df = df[df[col].str.lower().str.contains('|'.join(filters), na=False)]
                vc = filtered_df[col].value_counts().reset_index()
                temp_vcs = pd.merge(temp_vcs, vc, on='index', how='outer')

        temp_dfs.append(filtered_df)
        temp_df = pd.concat(temp_dfs, axis=0)
        temp_df.drop_duplicates(inplace=True, subset=[index_column])

        print(f"{key} | {temp_df.shape}")

        if df_fitered is None:
            df_fitered = temp_df
        else:
            df_fitered = df_fitered.loc[df_fitered[index_column].isin(temp_df[index_column]), :]

        temp_vcs = temp_vcs.add_suffix(f'__{key}')
        temp_vcs.rename(columns={f'index__{key}': 'index'}, inplace=True)

        temp_vcs.fillna(0, inplace=True)

        all_vcs = pd.merge(all_vcs, temp_vcs, on='index', how='outer')

    all_vcs_total = all_vcs.drop('index', axis=1).sum(axis=1)
    all_vcs.insert(1, 'vc_total', all_vcs_total)
    all_vcs.sort_values('vc_total', ascending=False, inplace=True)
    all_vcs.fillna(0, inplace=True)
    return df_fitered, all_vcs                                  
