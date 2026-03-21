import pandas as pd

def transform_isEndgame():
    column = "Dim_isEndgame"
    data = {
        "true",
        "false"
    }

    df = pd.DataFrame(data, columns=[column])

    return df

def transform_GrandCompany():
    column = "Dim_GrandCompany"
    data = {
        "None",
        "Maelstrom",
        "Immortal Flames",
        "Order of the Twin Adder"
    }

    df = pd.DataFrame(data, columns=[column])

    return df

def transform_realms(df,df1,df2,df3):
    categories = [
        df['Category'], 
        df1['Category'], 
        df2['Category'], 
        df3['Category']
    ]

    combined = pd.concat(categories, ignore_index=True)
    
    df = pd.DataFrame(combined, columns=['Category']).rename(
        columns={'Category': 'Dim_Realms'}
    ).drop_duplicates().reset_index(drop=True)
    
    return df

def transform_tribal_data(df):
    df_transformed = df.rename(columns={
        'Category': 'Dim_Tribe',
        'Tribe': 'V_Interactions'
    })
    
    category_map = {
        "Amaljaa": "Scaley", 
        "Sylph": "Fey", 
        "Kobold": "Furry",
        "Sahagin": "Auquarian", 
        "Ixal": "Avian", 
        "Vanu Vanu": "Avian",
        "Vath": "Scaley", 
        "Moogle": "Fey", 
        "Kojin": "Scaley",
        "Ananta": "Scaley", 
        "Namazu": "Auquarian", 
        "Pixie": "Fey",
        "Dwarf": "Fey", 
        "Qitari": "Furry", 
        "Arkasodara": "Pachyderm",
        "Loporrit": "Furry", 
        "Omnicron": "Synth"
    }
    
    sub_tribe_df = pd.DataFrame(df_transformed['Dim_Tribe'].unique(), columns=['Dim_Tribe'])
    sub_tribe_df['V_Category'] = sub_tribe_df['Dim_Tribe'].map(category_map)
    
    return df_transformed, sub_tribe_df