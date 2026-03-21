import os
import pandas as pd
from transformer import transform_tribal_data  # Direct import since they are in the same folder


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'data'))

RAW_DIR = os.path.join(DATA_ROOT, 'raw')
OUT_DIR = os.path.join(DATA_ROOT, 'transformed')

def process_files():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    target_file = 'Tribal_Interactions.csv'
    input_path = os.path.join(RAW_DIR, target_file)
    
    if os.path.exists(input_path):
        print(f"Reading: {input_path}")
        df = pd.read_csv(input_path)
        
        dim_tribes_df, sub_tribe_cat_df = transform_tribal_data(df)
        
        dim_tribes_df.to_csv(os.path.join(OUT_DIR, 'Dim_Tribes.csv'), index=False)
        sub_tribe_cat_df.to_csv(os.path.join(OUT_DIR, 'Sub_Tribe_Categories.csv'), index=False)
        
        print(f"Success! Files saved to: {OUT_DIR}")
    else:
        print(f"Error: Could not find {target_file} in {RAW_DIR}")

if __name__ == "__main__":
    process_files()