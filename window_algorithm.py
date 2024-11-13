import numpy as np
import pandas as pd

class WindowAlgorithmProcessor:
    def __init__(self, sub_dfs, chosen_quantitative_column = 'temperature', fire_size_column = 'current_size', mindif = 0):
        self.sub_dfs = sub_dfs
        self.quantitative_column = chosen_quantitative_column
        self.fire_size_column = fire_size_column
        self.mindif = mindif
        
    def window_algorithm(self, array, average):
        #returns a tuple containint range, mean of range, and whether it passed the z-test
        rules = []
        quantitative_values = array[self.quantitative_column].values
        num_values = len(quantitative_values)
        window_average = average + self.mindif 
        
        # rearrange the quantitative values
        sorted_indices = np.argsort(quantitative_values)
        sorted_quantitative_values = quantitative_values[sorted_indices]
        
        #initializing window variables
        A_start = 0 # begining of region A and the array
        A_end = 0 # end of region A
        B_start = 0 # begining of region B
        B_end = 0 # end of region B
        
        while A_start < num_values:
            # set A_start to the first above-average value 
            while A_start < num_values and sorted_quantitative_values[A_start] < window_average:
                A_start += 1
                
            if A_start >= num_values:
                break
            
            # initializing the parameters for A and B regions
            A_end = A_start
            B_start = A_end + 1
            
            # checks to see if adding a new value to B keeps the combined region (AUB) above average
            while B_start < num_values:
                B_end = B_start
                avg_of_regions = np.mean(sorted_quantitative_values[A_start : B_end + 1])
                    
                # if its above average, join B to A
                if avg_of_regions > window_average:
                    A_end = B_end
                    B_start = A_end + 1 # empty/reset B

                # if not, consider A a potential rule
                else:
                    break
                
                B_start += 1
                
            if A_end - A_start + 1 >= 2:
                rule_mean = np.mean(sorted_quantitative_values[A_start : A_end + 1])
                significance = True

                # do z-test
                
                if significance:
                    rules.append(((float(sorted_quantitative_values[A_start]), float(sorted_quantitative_values[A_end])), float(rule_mean), significance))
                    sub_array = pd.DataFrame(sorted_quantitative_values[A_start : A_end + 1], columns = [self.quantitative_column])
                    sub_rules = self.window_algorithm(sub_array, rule_mean)
                    rules.extend(sub_rules)   
                     
            A_start = A_end + 1 # reinitialize A and continue
                        
        return rules
        
    
    def process_all_dfs(self):
        all_rules = {}
        fire_size_mean = 0
        
        for name, sub_df in self.sub_dfs.items():
            if self.quantitative_column in sub_df.columns and self.fire_size_column in sub_df.columns:
                print(f"Processing Dataframe: {name}")

                fire_size_mean = sub_df[self.fire_size_column].mean()                
                rules = self.window_algorithm(sub_df, fire_size_mean)
                
                if rules:
                    print("Rules found:")
                    for rule in rules:
                        print(f"{self.quantitative_column} => Range: {rule[0]}, Mean of Range: {rule[1]}, Passed the z-test: {rule[2]}")
                    
                    all_rules[name] = rules 
                else:
                    print("No Significant Rules Found.")                  
            else:
                print(f"Columns {self.quantitative_column} or {self.fire_size_column} could not be found in the data frame.")

        return all_rules
               