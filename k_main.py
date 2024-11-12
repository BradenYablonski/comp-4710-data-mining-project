from wildfire_data_processor import WildfireDataProcessor
from fp_growth_processor import FP_Growth_Processor


from sklearn.cluster import KMeans
import pandas as pd
from sklearn.metrics import silhouette_score

# Initialize WildfireDataProcessor
wildfire_processor = WildfireDataProcessor('fp-historical-wildfire-data-2006-2023.xlsx')
wildfire_processor.load_data()
wildfire_processor.preprocess_data()

# Initialize FPGrowthProcessor
fp_processor = FP_Growth_Processor(wildfire_processor, support_threshold=0.1)
fp_processor.generate_frequent_itemsets()
fp_processor.create_sub_dfs()

sub_dfs = fp_processor.get_sub_dfs()
# print(sub_dfs['df_Surface_Flat'].head())
print(list(sub_dfs.keys()))






k_result = {}

for i, k_df in enumerate (fp_processor.sub_dfs.values()):
    k_df_drop = k_df.drop('current_size',axis = 1)
    k_encoded = pd.get_dummies(k_df_drop, columns = ['fire_position_on_slope', 'wind_direction', 'fire_type', 'weather_conditions_over_fire'])
    kmeans = KMeans()

    param_grid = {'n_clusters': [2, 3, 4, 5, 6]}
    silhouette_best = -1
    best_k = param_grid['n_clusters'][0]
    
    for n in param_grid['n_clusters']:    
        kmeans = KMeans(n_clusters = n, random_state = 42)
        kmeans.fit(k_encoded)
        silhouette_avg = silhouette_score(k_encoded, kmeans.labels_)
        print(f"Group :{i}  n_clusters: {n}, silhouette_score: {silhouette_avg}")
        if silhouette_avg > silhouette_best:
            silhouette_best = silhouette_avg
            best_k = n

    kmeans = KMeans(n_clusters = best_k, random_state = 42)
    kmeans.fit(k_encoded)
    labels = kmeans.labels_
    
    k_df['label']=labels
    k_df['current_size_avg'] = k_df.groupby('label')['current_size'].transform('mean')
    for col in ['temperature', 'wind_speed', 'relative_humidity', 'current_size']:
        k_df[f'{col}_max'] = k_df.groupby('label')[col].transform('max')
        k_df[f'{col}_min'] = k_df.groupby('label')[col].transform('min')
        k_df.to_csv(f"kmean_result_{i}.csv", index=False)
    k_result[i] = k_df
