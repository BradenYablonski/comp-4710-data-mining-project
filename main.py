from wildfire_data_processor import WildfireDataProcessor
from fp_growth_processor import FP_Growth_Processor
from window_algorithm import WindowAlgorithmProcessor
from kmeans_processor import KMeansProcessor
from z_test_processor import Z_Test_Processor

import warnings
warnings.simplefilter(action='ignore')

# Initialize WildfireDataProcessor
wildfire_processor = WildfireDataProcessor('fp-historical-wildfire-data-2006-2023.xlsx')
wildfire_processor.load_data()
wildfire_processor.preprocess_data()

# Initialize FPGrowthProcessor
fp_processor = FP_Growth_Processor(wildfire_processor, support_threshold=0.1)
fp_processor.generate_frequent_itemsets()
fp_processor.create_sub_dfs()

sub_dfs = fp_processor.get_sub_dfs()
sub_dfs_list = list(sub_dfs.keys())

# Get the sub dataset (eg: the first sub dataset with index 0)
#print(sub_dfs[sub_dfs_list[0]])
#a = sub_dfs[sub_dfs_list[-2]]
#print(a['temperature'].head())
#print(list(sub_dfs.keys())) #list of sub dataset names

# Perform window algorithm to get interesting rules
quantitative_column = ['temperature', 'wind_speed', 'relative_humidity']
all_rules = {}
for quan_col in quantitative_column:
    window_processor = WindowAlgorithmProcessor(sub_dfs, chosen_quantitative_column=quan_col)
    all_rules.update(window_processor.process_all_dfs())

# prints only the interesting rules
# print("\n\nAll the found rules:")
# for name, rules in all_rules.items():
#     print(f"\n{name}:")
#     for rule in all_rules[name]:
#         print(rule)
 
                    
#kmeans
kmeans_processor = KMeansProcessor(sub_dfs)
kmeans_result = kmeans_processor.perform_clustering()


# z-test
print("Window Algorithm result")
z_test_window = Z_Test_Processor(wildfire_processor.sub_dataset_cleaned, all_rules)
print(z_test_window.z_test())

print("New Algorithm result")
z_test_kmeans = Z_Test_Processor(wildfire_processor.sub_dataset_cleaned, kmeans_result)
print(z_test_kmeans.z_test())