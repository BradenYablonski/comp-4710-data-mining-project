import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder

class FP_Growth_Processor:
    def __init__(self, wildfire_processor, support_threshold=0.1):
        self.wildfire_processor = wildfire_processor
        self.support_threshold = support_threshold
        self.interesting_itemsets = None
        self.sub_dfs = {}

    def generate_frequent_itemsets(self):
        # Transaction encoding
        cat_subdata = self.wildfire_processor.cat_subdata
        te = TransactionEncoder()
        te_ary = te.fit(cat_subdata.to_numpy()).transform(cat_subdata.to_numpy())
        cat_subdata_trans = pd.DataFrame(te_ary, columns=te.columns_)
        
        # Frequent itemset generation using FP-Growth
        frequent_itemsets = fpgrowth(cat_subdata_trans, min_support=self.support_threshold, use_colnames=True)
        frequent_itemsets['support'] = frequent_itemsets['support'].round(4)
        
        # Filter interesting itemsets with length >= 2
        self.interesting_itemsets = frequent_itemsets[frequent_itemsets['itemsets'].apply(lambda x: len(x) >= 2)]
        self.interesting_itemsets = self.interesting_itemsets['itemsets'].apply(list).reset_index(drop=True)
        
    def create_sub_dfs(self):
        sub_dataset_cleaned = self.wildfire_processor.sub_dataset_cleaned
        for i in range(len(self.interesting_itemsets)):
            pair = self.interesting_itemsets[i]
            sub_df_name = "df_" + "_".join(pair)
            sub_df = sub_dataset_cleaned[
                sub_dataset_cleaned.apply(lambda row: all(value in row.values for value in pair), axis=1)
            ]
            self.sub_dfs[sub_df_name] = sub_df.reset_index(drop = True)
    
    def get_sub_dfs(self):
        return self.sub_dfs
