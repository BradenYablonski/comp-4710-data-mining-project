import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder

class WildfireDataProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None
        self.sub_dataset_cleaned = None
        self.cat_subdata = None

    def load_data(self):
        # Load Excel file
        self.data = pd.read_excel(self.filepath)
        print(f"Data loaded with shape: {self.data.shape}")
    
    def preprocess_data(self):
        # Select columns with interesting variables
        sub_dataset_columns = ['temperature', 'wind_speed', 'fire_position_on_slope', 'wind_direction', 
                               'relative_humidity', 'fire_type','weather_conditions_over_fire', 'current_size']
        sub_data = self.data[sub_dataset_columns]
        
        self.sub_dataset_cleaned = sub_data.dropna()
        
        self.sub_dataset_cleaned['wind_direction'] = self.sub_dataset_cleaned['wind_direction'].str.strip()
        self.sub_dataset_cleaned['fire_type'] = self.sub_dataset_cleaned['fire_type'].str.strip()
        
        # Prepare categorical subset
        cat_col = ['fire_position_on_slope', 'wind_direction', 'fire_type', 'weather_conditions_over_fire']
        self.cat_subdata = self.sub_dataset_cleaned[cat_col]

    def get_preprocess_data(self):
        return self.cat_subdata