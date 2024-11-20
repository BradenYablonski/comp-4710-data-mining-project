import scipy.stats as stats
import numpy as np

class Z_Test_Processor:
    def __init__(self, wildfire_cleaned_df, rules, alpha=0.25):
        self.cleaned_df = wildfire_cleaned_df
        self.all_rules = rules
        self.alpha = alpha
        self.sub_dfs = {}
    
    def z_test(self):
        rules_pass = {}
        mu = self.cleaned_df.current_size.mean()
        sigma = self.cleaned_df.current_size.std()
        if bool(self.all_rules):
            for keys in self.all_rules:
                rules_pass[keys] = []
                for val in self.all_rules[keys]:
                    X_bar = float(val.split(" | ")[0].split(" ")[-1])
                    n = float(val.split(" | ")[1].split(" ")[-1])
                    Z = (X_bar - mu) / (sigma / np.sqrt(n))
                    p_value = 2 * (1 - stats.norm.cdf(abs(Z)))
                    if p_value < self.alpha:
                        rules_pass[keys].append(val)
        else: print("No interesting rule")
        return(rules_pass)