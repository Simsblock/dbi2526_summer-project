import pandas as pd
import itertools

totalPop = 29269534             # Total Population 
totalEGPop = 1418974            # Total Endgame Population
EGpercent = 29269534 / 1418974  # Engame %ile Population

def unify_realms(df0,df1,df2,df3,egdf0,egdf1,egdf2,egdf3):
    data = [
        df0[['Category', 'All']], 
        df1[['Category', 'All']], 
        df2[['Category', 'All']], 
        df3[['Category', 'All']], 
    ]

    egdata = [
        egdf0[['Category', 'Active']], 
        egdf1[['Category', 'Active']], 
        egdf2[['Category', 'Active']],
        egdf3[['Category', 'Active']], 
    ]

    combined_total = pd.concat(data, ignore_index=True)
    combined_total = combined_total.rename(columns={
        'Category': 'Dim_Realms', 
        'All': 'Total_Pop'
    })

    combined_eg = pd.concat(egdata, ignore_index=True)
    combined_eg = combined_eg.rename(columns={
        'Category': 'Dim_Realms', 
        'Active': 'Endgame_Pop'
    })

    df_final = pd.merge(combined_total, combined_eg, on='Dim_Realms')

    return df_final

def caluclate_gc_percent(df):

    df = df.rename(columns={'Category': 'Dim_GrandCompany'})
    
    df['Percentile'] = df['# of Characters'] / totalPop
    
    return df[['Dim_GrandCompany', 'Percentile']]


def generate_fact(df_realms,df_companies):

    isEndgame = [True, False]
    realms = df_realms['Dim_Realms'].unique()
    grand_companies = df_companies['Dim_GrandCompany'].unique()

    gc_percentiles = dict(zip(df_companies['Dim_GrandCompany'], df_companies['Percentile']))

    combinations = list(itertools.product(isEndgame, realms, grand_companies))
    fact_df = pd.DataFrame(combinations, columns=['Dim_isEndgame', 'Dim_Realms', 'Dim_GrandCompany'])

    def calculate_players(row):
        realm_data = df_realms[df_realms['Dim_Realms'] == row['Dim_Realms']].iloc[0]

        if row['Dim_isEndgame']:
            base_pop = realm_data['Endgame_Pop']
        else:
            base_pop = realm_data['Total_Pop']

        percentile = gc_percentiles.get(row['Dim_GrandCompany'], 1)

        return round(base_pop * percentile)

    fact_df['Fact_PlayerCount'] = fact_df.apply(calculate_players, axis=1)

    return fact_df