#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 20:05:26 2024

@author: may
"""

import csv
import random
import names  
import pandas as pd 

# Function to generate random salaries with some values as null
def generate_salaries(num_entries, null_percentage):
    salaries = []
    for _ in range(num_entries):
        if random.uniform(0, 1) < null_percentage:
            salaries.append(None)
        else:
            salaries.append(random.randint(30000, 100000))
    return salaries

# Generate random full names
full_names = [names.get_full_name() for _ in range(20)]

# Generate salaries with some null values
salaries = generate_salaries(20, 0.2)

# Combine full names and salaries into a list of tuples
data = list(zip(full_names, salaries))

# Specify the CSV file name
csv_file_name = '/Users/may/Downloads/employee_data.csv'

# Write the data to a CSV file
with open(csv_file_name, 'w', newline='') as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)

    # Write the header
    csv_writer.writerow(['Full Name', 'Salary'])

    # Write the data
    csv_writer.writerows(data)

print(f"CSV file '{csv_file_name}' has been created.")

df = pd.read_csv(csv_file_name)
print(df.dtypes)

salary_avg = pd.read_csv(csv_file_name, usecols=['Salary']).mean()
salary_avg = int(salary_avg.iloc[0])

df.fillna(salary_avg,inplace=True)
df.to_csv('/Users/may/Downloads/employee_data.csv', index=False)
