import os
import pandas as pd
from collections import defaultdict
from transformer import transform_isEndgame
from transformer import transform_grandCompany 
from transformer import transform_realms 
from transformer import transform_regions
from transformer import transform_sex 
from transformer import transform_species
from transformer import transform_tribal_data 
from visualization import visualize_Normal,visualize_Ridiculous,visualize_Geo

from factgenerator import unify_realms 
from factgenerator import caluclate_gc_percent
from factgenerator import generate_fact 
from factgenerator import unify_species_pop
from factgenerator import generate_enriched_fact 
from factgenerator import generate_ridicilous_fact 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'data'))

RAW_DIR = os.path.join(DATA_ROOT, 'raw')
OUT_DIR = os.path.join(DATA_ROOT, 'transformed')
FACT_OUT_DIR = os.path.join(DATA_ROOT, 'fact')

def process_files():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # isEndgame

    dim_isEndgame_df = transform_isEndgame()
        
    dim_isEndgame_df.to_csv(os.path.join(OUT_DIR, 'Dim_isEndgame.csv'), index=False)

    # grandCompany

    dim_GrandCompany_df = transform_grandCompany()
        
    dim_GrandCompany_df.to_csv(os.path.join(OUT_DIR, 'Dim_GrandCompany.csv'), index=False)

    # realm
    target_file = 'American_Realms.csv'
    target_file1 = 'European_Realms.csv'
    target_file2 = 'Japanese_Realms.csv'
    target_file3 = 'Oceanian_Realms.csv'
    input_path = os.path.join(RAW_DIR, target_file)
    input_path1 = os.path.join(RAW_DIR, target_file1)
    input_path2 = os.path.join(RAW_DIR, target_file2)
    input_path3 = os.path.join(RAW_DIR, target_file3)
        
    if os.path.exists(input_path):
        df = pd.read_csv(input_path)
        df1 = pd.read_csv(input_path1)
        df2 = pd.read_csv(input_path2)
        df3 = pd.read_csv(input_path3)

        dim_Realm_df = transform_realms(df,df1,df2,df3)
        dim_Realm_df.to_csv(os.path.join(OUT_DIR, 'Dim_Realms.csv'), index=False)

        sub_Region_df = transform_regions(df,df1,df2,df3)
        sub_Region_df.to_csv(os.path.join(OUT_DIR, 'Sub_Regions.csv'), index=False)

    else:
        print(f"Error: Could not find raws for regions")

    # Species & Sex
    target_file = 'Species_Sex_Endgame.csv'
    input_path = os.path.join(RAW_DIR, target_file)
    
    if os.path.exists(input_path):
        df = pd.read_csv(input_path)
        
        dim_species_df = transform_species(df)
        sub_sex_df = transform_sex()

        dim_species_df.to_csv(os.path.join(OUT_DIR, 'Dim_Species.csv'), index=False)
        sub_sex_df.to_csv(os.path.join(OUT_DIR, 'Sub_Sex.csv'), index=False)
    else:
        print(f"Error: Could not find {target_file} in {RAW_DIR}")

    # Tribals Interactions
    target_file = 'Tribal_Interactions.csv'
    input_path = os.path.join(RAW_DIR, target_file)
    
    if os.path.exists(input_path):
        df = pd.read_csv(input_path)
        
        dim_tribes_df, sub_tribe_cat_df = transform_tribal_data(df)
        
        dim_tribes_df.to_csv(os.path.join(OUT_DIR, 'Dim_Tribes.csv'), index=False)
        sub_tribe_cat_df.to_csv(os.path.join(OUT_DIR, 'Sub_Tribe_Categories.csv'), index=False)
    else:
        print(f"Error: Could not find {target_file} in {RAW_DIR}")

def process_fact():
    #realms
    target_file = 'American_Realms.csv'
    target_file1 = 'European_Realms.csv'
    target_file2 = 'Japanese_Realms.csv'
    target_file3 = 'Oceanian_Realms.csv'
    input_path = os.path.join(RAW_DIR, target_file)
    input_path1 = os.path.join(RAW_DIR, target_file1)
    input_path2 = os.path.join(RAW_DIR, target_file2)
    input_path3 = os.path.join(RAW_DIR, target_file3)
    #ef realms
    target_file4 = 'American_Realms_Endgame.csv'
    target_file5 = 'European_Realms_Endgame.csv'
    target_file6 = 'Japanese_Realms_Endgame.csv'
    target_file7 = 'Oceanian_Realms_Endgame.csv'
    input_path4 = os.path.join(RAW_DIR, target_file4)
    input_path5 = os.path.join(RAW_DIR, target_file5)
    input_path6 = os.path.join(RAW_DIR, target_file6)
    input_path7 = os.path.join(RAW_DIR, target_file7)
    #gc
    target_file8 = 'GrandCompanies.csv'
    input_path8 = os.path.join(RAW_DIR, target_file8)

    df = pd.read_csv(input_path)
    df1 = pd.read_csv(input_path1)
    df2 = pd.read_csv(input_path2)
    df3 = pd.read_csv(input_path3)
    df4 = pd.read_csv(input_path4)
    df5 = pd.read_csv(input_path5)
    df6 = pd.read_csv(input_path6)
    df7 = pd.read_csv(input_path7)
    df8 = pd.read_csv(input_path8)

    df_fact = generate_fact(unify_realms(df,df1,df2,df3,df4,df5,df6,df7), caluclate_gc_percent(df8))

    df_fact.to_csv(os.path.join(FACT_OUT_DIR, 'Fact.csv'), index=False)

    


def process_enriched_fact():
    #realms
    target_file = 'American_Realms.csv'
    target_file1 = 'European_Realms.csv'
    target_file2 = 'Japanese_Realms.csv'
    target_file3 = 'Oceanian_Realms.csv'
    input_path = os.path.join(RAW_DIR, target_file)
    input_path1 = os.path.join(RAW_DIR, target_file1)
    input_path2 = os.path.join(RAW_DIR, target_file2)
    input_path3 = os.path.join(RAW_DIR, target_file3)
    #ef realms
    target_file4 = 'American_Realms_Endgame.csv'
    target_file5 = 'European_Realms_Endgame.csv'
    target_file6 = 'Japanese_Realms_Endgame.csv'
    target_file7 = 'Oceanian_Realms_Endgame.csv'
    input_path4 = os.path.join(RAW_DIR, target_file4)
    input_path5 = os.path.join(RAW_DIR, target_file5)
    input_path6 = os.path.join(RAW_DIR, target_file6)
    input_path7 = os.path.join(RAW_DIR, target_file7)
    #gc
    target_file8 = 'GrandCompanies.csv'
    input_path8 = os.path.join(RAW_DIR, target_file8)
    #species
    target_file9 = 'Species_Sex.csv'
    input_path9 = os.path.join(RAW_DIR, target_file9)
    target_file10 = 'Species_Sex_Endgame.csv'
    input_path10 = os.path.join(RAW_DIR, target_file10)
    target_file11 = 'Dim_Tribes.csv'
    input_path11 = os.path.join(OUT_DIR, target_file11)

    df = pd.read_csv(input_path)
    df1 = pd.read_csv(input_path1)
    df2 = pd.read_csv(input_path2)
    df3 = pd.read_csv(input_path3)
    df4 = pd.read_csv(input_path4)
    df5 = pd.read_csv(input_path5)
    df6 = pd.read_csv(input_path6)
    df7 = pd.read_csv(input_path7)
    df8 = pd.read_csv(input_path8)
    df9 = pd.read_csv(input_path9)
    df10 = pd.read_csv(input_path10)
    df11 = pd.read_csv(input_path11)

    df_fact = generate_ridicilous_fact(
        unify_realms(df,df1,df2,df3,df4,df5,df6,df7), 
        caluclate_gc_percent(df8),
        unify_species_pop(df9,df10),
        df11
        )

    df_fact.to_csv(os.path.join(FACT_OUT_DIR, 'Ridicilous_Fact.csv'), index=False)

def visualize():
    df_fact=  pd.read_csv(os.path.join(FACT_OUT_DIR, 'Fact.csv'))
    df_tribe=  pd.read_csv(os.path.join(OUT_DIR, 'Dim_Tribes.csv'))
    df_subtribe=  pd.read_csv(os.path.join(OUT_DIR, 'Sub_Tribe_Categories.csv'))
    df_result = df_subtribe.merge(
    df_tribe[["Dim_Tribe", "V_Interactions"]],
    on="Dim_Tribe",
    how="left"   
    )
    df_realms=pd.read_csv(os.path.join(OUT_DIR, 'Sub_Regions.csv'))
    result = df_fact.groupby('Dim_Realms')['V_PlayerCount'].sum().reset_index()
    result=result.merge(df_realms, on='Dim_Realms', how='left')
    result = result.groupby('V_Region')['V_PlayerCount'].sum().reset_index()
    
    coords = {
        'Americas': (45, -105),
        'Europe':   (50,  15),
        'Japan':    (36, 138),
        'Oceania':  (-25, 135)
    }


    result['lat'] = result['V_Region'].map(lambda r: coords[r][0])
    result['lon'] = result['V_Region'].map(lambda r: coords[r][1])
    result['label'] = result['V_Region'] + '<br>' + result['V_PlayerCount'].astype(str)

    visualize_Normal(df_fact)
    visualize_Ridiculous(df_result)
    visualize_Geo(result)



   

if __name__ == "__main__":
    process_files()
    process_fact()
    process_enriched_fact()
    visualize()
