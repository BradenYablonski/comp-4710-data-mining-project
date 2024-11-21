import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

class KMeansProcessor:
    def __init__(self, sub_dfs):
        self.sub_dfs = sub_dfs
    
    def perform_clustering(self):
        k_result = {}
        kmeans = KMeans()

        for key in self.sub_dfs:
            print(f"{key}:")
            k_df_drop = self.sub_dfs[key].drop('current_size', axis=1)
            k_encoded = pd.get_dummies(k_df_drop, columns=['fire_position_on_slope', 'wind_direction', 'fire_type', 'weather_conditions_over_fire'])

            param_grid = {'n_clusters': [2, 3, 4, 5]}
            silhouette_best = -1
            best_k = param_grid['n_clusters'][0]
            
            for n in param_grid['n_clusters']:
                kmeans = KMeans(n_clusters=n, random_state=42)
                kmeans.fit(k_encoded)
                silhouette_avg = silhouette_score(k_encoded, kmeans.labels_)
                if silhouette_avg > silhouette_best:
                    silhouette_best = silhouette_avg
                    best_k = n

            kmeans = KMeans(n_clusters=best_k, random_state=42)
            kmeans.fit(k_encoded)
            labels = kmeans.labels_

            k_df = self.sub_dfs[key]
            k_df['label'] = labels
            k_df['current_size_avg'] = k_df.groupby('label')['current_size'].transform('mean')
            for col in ['temperature', 'wind_speed', 'relative_humidity']:
                k_df[f'{col}_max'] = k_df.groupby('label')[col].transform('max')
                k_df[f'{col}_min'] = k_df.groupby('label')[col].transform('min')
            
            result_by_label = {}

            for i in k_df['label'].unique():
                label_data = k_df[k_df['label'] == i]

                temperature_range = f"temperature Range: [{label_data['temperature_min'].iloc[0]}, {label_data['temperature_max'].iloc[0]}]"
                wind_speed_range = f"wind_speed Range: [{label_data['wind_speed_min'].iloc[0]}, {label_data['wind_speed_max'].iloc[0]}]"
                humidity_range = f"relative_humidity Range: [{label_data['relative_humidity_min'].iloc[0]}, {label_data['relative_humidity_max'].iloc[0]}]"
                current_size_avg = f"current_size: {label_data['current_size_avg'].iloc[0]}"
                matching_rows = f"Matching Rows: {len(label_data)}"

                key_split = key.split('_')[1:]
                key_join = ','.join(key_split)

                result_str = f"{key_join},{temperature_range}, {wind_speed_range}, {humidity_range} ==> {current_size_avg} | {matching_rows}"
                result_by_label[i] = result_str

                print(result_str)

            k_result[key] = result_by_label

        return k_result
