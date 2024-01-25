#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import os

def log_experiment(experiment_data, filename="experiment_results.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['experiment_id', 'Dataset_Name', 'Column_name', 'inputs', 
                      'description_keywords', 'example_pairs', 'output', 
                      'accuracy', 'total_number_of_token']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # Write the header if file doesn't exist

        writer.writerow(experiment_data)

