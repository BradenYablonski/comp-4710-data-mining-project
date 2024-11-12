import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

class KMeansProcessor:
    def __init__(self, sub_dfs):
        self.sub_dfs = sub_dfs
    
    def perform_clustering(self):
        k_result = {}
        kmeans = KMeans()

        for i, k_df in enumerate(self.sub_dfs.values()):
            k_df_drop = k_df.drop('current_size', axis=1)
            k_encoded = pd.get_dummies(k_df_drop, columns=['fire_position_on_slope', 'wind_direction', 'fire_type', 'weather_conditions_over_fire'])

            param_grid = {'n_clusters': [2, 3, 4, 5, 6]}
            silhouette_best = -1
            best_k = param_grid['n_clusters'][0]
            
            for n in param_grid['n_clusters']:
                kmeans = KMeans(n_clusters=n, random_state=42)
                kmeans.fit(k_encoded)
                silhouette_avg = silhouette_score(k_encoded, kmeans.labels_)
                print(f"Group :{i}  n_clusters: {n}, silhouette_score: {silhouette_avg}")
                if silhouette_avg > silhouette_best:
                    silhouette_best = silhouette_avg
                    best_k = n

            kmeans = KMeans(n_clusters=best_k, random_state=42)
            kmeans.fit(k_encoded)
            labels = kmeans.labels_
            
            k_df['label'] = labels
            k_df['current_size_avg'] = k_df.groupby('label')['current_size'].transform('mean')
            for col in ['temperature', 'wind_speed', 'relative_humidity', 'current_size']:
                k_df[f'{col}_max'] = k_df.groupby('label')[col].transform('max')
                k_df[f'{col}_min'] = k_df.groupby('label')[col].transform('min')
            
            k_df.to_csv(f"kmean_result_{i}.csv", index=False)
            k_result[i] = k_df

        return k_result
