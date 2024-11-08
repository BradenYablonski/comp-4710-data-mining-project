from wildfire_data_processor import WildfireDataProcessor
from fp_growth_processor import FP_Growth_Processor

# Initialize WildfireDataProcessor
wildfire_processor = WildfireDataProcessor('fp-historical-wildfire-data-2006-2023.xlsx')
wildfire_processor.load_data()
wildfire_processor.preprocess_data()

# Initialize FPGrowthProcessor
fp_processor = FP_Growth_Processor(wildfire_processor, support_threshold=0.1)
fp_processor.generate_frequent_itemsets()
fp_processor.create_sub_dfs()

sub_dfs = fp_processor.get_sub_dfs()
print(sub_dfs['df_Surface_Flat'].head())
print(list(sub_dfs.keys()))
a = sub_dfs['df_Surface_Flat']
print(a['wind_speed'].head())