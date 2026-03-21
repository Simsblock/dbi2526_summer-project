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

def unify_species_pop(df_total, df_endgame):
    df_total = df_total[df_total['Category'] != '----'].copy()

    df_total['Total_Pop'] = df_total['Female'].fillna(0) + df_total['Male'].fillna(0)
    df_endgame['Endgame_Pop'] = df_endgame['Female'].fillna(0) + df_endgame['Male'].fillna(0)

    df_total = df_total[['Category', 'Total_Pop']].rename(columns={'Category': 'Dim_Species'})
    df_endgame = df_endgame[['Category', 'Endgame_Pop']].rename(columns={'Category': 'Dim_Species'})

    df_final = pd.merge(df_total, df_endgame, on='Dim_Species', how='outer').fillna(0)

    return df_final


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

    fact_df['V_PlayerCount'] = fact_df.apply(calculate_players, axis=1)

    return fact_df

def generate_enriched_fact(df_realms,df_companies,df_species):

    isEndgame = [True, False]
    realms = df_realms['Dim_Realms'].unique()
    grand_companies = df_companies['Dim_GrandCompany'].unique()
    species_list = df_species['Dim_Species'].unique()

    gc_percentiles = dict(zip(df_companies['Dim_GrandCompany'], df_companies['Percentile']))
    species_eg_percent = dict(zip(df_species['Dim_Species'], df_species['Endgame_Pop'] / totalPop))
    species_total_percent = dict(zip(df_species['Dim_Species'], df_species['Total_Pop'] / totalEGPop))

    combinations = list(itertools.product(isEndgame, realms, grand_companies, species_list))
    fact_df = pd.DataFrame(combinations, columns=['Dim_isEndgame', 'Dim_Realms', 'Dim_GrandCompany', 'Dim_Species'])


    def calculate_players(row):
        realm_data = df_realms[df_realms['Dim_Realms'] == row['Dim_Realms']].iloc[0]

        if row['Dim_isEndgame']:
            realm_base = realm_data['Endgame_Pop']
            species_share = species_eg_percent.get(row['Dim_Species'], 0)
        else:
            realm_base = realm_data['Total_Pop'] - realm_data['Endgame_Pop']
            species_share = species_total_percent.get(row['Dim_Species'], 0)

        gc_share = gc_percentiles.get(row['Dim_GrandCompany'], 0)

        return round(realm_base * gc_share * species_share)

    fact_df['V_PlayerCount'] = fact_df.apply(calculate_players, axis=1)

    return fact_df

def generate_ridicilous_fact(df_realms,df_companies,df_species,df_tribes):

    isEndgame = [True, False]
    realms = df_realms['Dim_Realms'].unique()
    grand_companies = df_companies['Dim_GrandCompany'].unique()
    species_list = df_species['Dim_Species'].unique()
    tribe_list = df_tribes['Dim_Tribe'].unique()

    gc_percentiles = dict(zip(df_companies['Dim_GrandCompany'], df_companies['Percentile']))
    species_eg_percent = dict(zip(df_species['Dim_Species'], df_species['Endgame_Pop'] / totalPop))
    species_total_percent = dict(zip(df_species['Dim_Species'], df_species['Total_Pop'] / totalEGPop))
    tribe_rates = dict(zip(df_tribes['Dim_Tribe'], df_tribes['V_Interactions'] / totalPop))

    combinations = list(itertools.product(isEndgame, realms, grand_companies, species_list, tribe_list))
    fact_df = pd.DataFrame(combinations, columns=['Dim_isEndgame', 'Dim_Realms', 'Dim_GrandCompany', 'Dim_Species', 'Dim_Tribe'])


    def calculate_players(row):
        realm_data = df_realms[df_realms['Dim_Realms'] == row['Dim_Realms']].iloc[0]

        if row['Dim_isEndgame']:
            realm_base = realm_data['Endgame_Pop']
            species_share = species_eg_percent.get(row['Dim_Species'], 0)
        else:
            realm_base = realm_data['Total_Pop'] - realm_data['Endgame_Pop']
            species_share = species_total_percent.get(row['Dim_Species'], 0)

        gc_share = gc_percentiles.get(row['Dim_GrandCompany'], 0)
        tribe_share = tribe_rates.get(row['Dim_Tribe'], 0)

        player_count = realm_base * gc_share * species_share
        tribe_completions = player_count * tribe_share

        return pd.Series([round(player_count), round(tribe_completions)])

    fact_df[['V_PlayerCount', 'V_TribeCompletions']] = fact_df.apply(calculate_players, axis=1)
    return fact_df