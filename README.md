# comp-4710-data-mining: Wildfire Data Mining Project

This project analyzes wildfire data using data mining techniques, including frequent pattern mining, clustering, and statistical testing. The goal is to uncover trends and patterns in the data and derive meaningful insights.

---

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Files and Directories](#files-and-directories)
5. [Contributors](#contributors)

---

## Overview

The project uses wildfire data ([link](https://open.canada.ca/data/en/dataset/a221e7a0-4f46-4be7-9c5a-e29de9a3447e/resource/27e03b8f-8855-4b9e-8d1e-542297750fc9)) from 2006 to 2023 to find association rules from multiple categorical and quantitative data simultaneously. 
The dataset can also be downloaded from the GitHub repo: ([https://github.com/BradenYablonski/comp-4710-data-mining-project](https://github.com/BradenYablonski/comp-4710-data-mining-project)). The dataset is located in the file named fp-historical-wildfire-data-2006-2023.xlsx.
Our new algorithm combines FP Growth to deal with categorical data and k-means clustering to create clusters for quantitative data. 
Rule pruning is performed by applying z-test.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BradenYablonski/comp-4710-data-mining-project.git
   cd comp-4710-data-mining-project

2. Install dependencies:
This project requires the following Python libraries:

pandas

numpy

scipy

scikit-learn

mlxtend

You can install all dependencies using the requirements.txt file:
   ```bash
   pip install -r requirements.txt
   ```
   
---

## Usage:

To run the code

- Preprocess the wildfire data:
   ```bash
   python wildfire_data_processor.py
  
- Apply frequent pattern mining:
   ```bash
   python fp_growth_processor.py
   
- Perform k-means clustering:
bash
python kmeans_processor.py

- Run statistical tests:
   ```bash
   python z_test_processor.py

- Run window algorithm:
  ```bash
  python window_algorithm.py
   
- For a full pipeline execution to get the rules from new algorithm and existing window algorithm:
   ```bash
   python main.py

---

## Files and Directories

project_figures_and_tables: Figures and Tables used within the report. Also contains tables and figures generated using output from the code.
fp-historical-wildfire-data-2006-2023.xlsx: Main dataset file.
wildfire_data_processor.py: Preprocessing script for the wildfire dataset.
fp_growth_processor.py: Script for frequent pattern mining.
kmeans_processor.py: Clustering script using k-means.
z_test_processor.py: Script for performing statistical tests.
main.py: Orchestrates the entire pipeline.
requirements.txt: All libraries required to run this project.
window_algorithm.py: Script for window algorithm.

---

## Contributors
- Braden Yablonski
- Chineze Obi
- Han Sun
- Mai Nguyen
