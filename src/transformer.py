import pandas as pd

def transform_tribal_data(df):
    """
    Performs the specific column renaming and mapping for Tribal data.
    """

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
        "Omicron": "Synth"
    }
    
    sub_tribe_df = pd.DataFrame(df_transformed['Dim_Tribe'].unique(), columns=['Dim_Tribe'])
    sub_tribe_df['V_Category'] = sub_tribe_df['Dim_Tribe'].map(category_map)
    
    return df_transformed, sub_tribe_df