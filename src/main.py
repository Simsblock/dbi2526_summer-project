import os
import pandas as pd
from transformer import transform_isEndgame
from transformer import transform_grandCompany 
from transformer import transform_realms 
from transformer import transform_regions
from transformer import transform_sex 
from transformer import transform_species
from transformer import transform_tribal_data 


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'data'))

RAW_DIR = os.path.join(DATA_ROOT, 'raw')
OUT_DIR = os.path.join(DATA_ROOT, 'transformed')

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


if __name__ == "__main__":
    process_files()