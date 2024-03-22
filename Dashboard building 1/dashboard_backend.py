
import glob
import os
import pathlib
import csv
import pandas as pd
import re
import time
import numpy as np
from datetime import date, datetime, timedelta
import logging
import codecs
import shutil
import pandas as pd
import re
import pandas as pd

# change the output file directory to the root directory, instead of subfolders

def clean_csv(file_path, date_today):
    # Read and clean a CSV file
    temp_df = pd.read_csv(file_path, sep=',', on_bad_lines='skip', engine='c', header=0)
    include_keywords = ['Temperature', 'Time Stamp', 'Power', 'Gradient']
    temp_df = temp_df[[col for col in temp_df.columns if any(keyword in col for keyword in include_keywords)]]
    temp_df = temp_df.replace(regex=['--\[', '\] --'], value='')
    temp_df.columns = [x.strip().replace(' ', '') for x in temp_df.columns]
    temp_df = temp_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    temp_df = temp_df.filter(regex='Temperature|TimeStamp|Power|Gradient', axis=1)
    temp_df['TimeStamp'] = pd.to_datetime(temp_df['TimeStamp'], dayfirst=True, errors='coerce')
    temp_df = temp_df.dropna()
    return temp_df[temp_df['TimeStamp'] <= date_today]

def process_subfolder(subfolder_path, subfolder_name):
    # print(f"Processing subfolder: {subfolder_name}")

    pmlogfiles_path = os.path.join(subfolder_path, "dashboard files")

    if os.path.exists(pmlogfiles_path):
        pcs_no = subfolder_name
        output_filename = os.path.join(root_directory, "Output", f'output_pcno.')
        date_today = datetime.now().strftime("%Y-%m-%d")
        total = 0

        df_list = []

        filenames = glob.glob(os.path.join(path, name*.csv'))

        # Load the list of processed files
        processed_files = set()
        processed_file_list_path = os.path.join(subfolder_path, 'processed_files.txt')
        if os.path.exists(processed_file_list_path):
            with open(processed_file_list_path, 'r') as file:
                processed_files = set(file.read().splitlines())
    df_list = []

    for filename in filenames:
        print('Processing file:', filename)

        try:
            time_temp = time.strptime(time.ctime(os.path.getmtime(filename)))
            time_val = time.strftime("%Y-%m-%d", time_temp)

            if time_val <= date_today:
                temp_df = clean_csv(filename, date_today)
                df_list.append(temp_df)
        except Exception as e:
            print(f"Error processing file: {filename}, Error: {str(e)}")
    
    

    if df_list:
        df = pd.concat(df_list)
        df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], dayfirst=True)
        df.set_index('TimeStamp', inplace=True)
        df = df.groupby(pd.Grouper(freq='5Min', origin='start')).agg({
            "ValuePPT_0": "max",
            "Temperature": "max",
            "Temperature": "max",
        })

        # Filter rows where all specified columns have values
        df = df.dropna(subset=["ValuePPT_0", "Temperature", "Temperature"], how="all")

        df.reset_index(inplace=True)
        df.index.name = 'cycle'
        df.index += 1

        df.to_csv(output_filename)

    # for filename in filenames:
    #     if filename in processed_files:
    #         continue  # Skip already processed files

    #     print('Processing file:', filename)

    #     try:
    #         time_temp = time.strptime(time.ctime(os.path.getmtime(filename)))
    #         time_val = time.strftime("%Y-%m-%d", time_temp)

    #         if time_val <= date_today:
    #             temp_df = clean_csv(filename, date_today)
    #             df_list.append(temp_df)

    #         # Add the filename to the list of processed files
    #         processed_files.add(filename)
    #     except Exception as e:
    #         print(f"Error processing file: {filename}, Error: {str(e)}")

    # if df_list:
    #     df = pd.concat(df_list)
    #     df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], dayfirst=True)
    #     df.set_index('TimeStamp', inplace=True)
    #     df = df.groupby(pd.Grouper(freq='5Min', origin='start')).agg({
    #         "GPU0PowerTGPPower": "max",
    #         "GPU0TemperatureHotspot": "max",
    #         "GPU0TemperatureGradientMaximumMaxToMin": "max",
    #     })

    #     # Filter rows where all specified columns have values
    #     df = df.dropna(subset=["Power", "Hotspot", "GradientMaximumMaxToMin"], how="all")

    #     df.reset_index(inplace=True)
    #     df.index.name = 'cyclecount'
    #     df.index += 1

        df.to_csv(output_filename)

    # Update the list of processed files
    with open(processed_file_list_path, 'w') as file:
        file.write('\n'.join(processed_files))

#this is the hostnames txt is being called, run script with hostnames as folder 
def process_all_subfolders(root_directory):
    hostnames_file = os.path.join(root_directory, "hostnames.csv")
    if not os.path.exists(hostnames_file):
        print("hostnames file not found.")
        return

    with open(hostnames_file, 'r') as file:
        subfolder_names = [line.strip() for line in file.readlines()]

    for subfolder_name in subfolder_names:
        subfolder_path = os.path.join(root_directory, subfolder_name)
        print("Checking path:", subfolder_path)
        if os.path.exists(subfolder_path):
            process_subfolder(subfolder_path, subfolder_name)
        else:
            print(f"Subfolder '{subfolder_name}' not found.")

#make sure to change root directory to server directory when running on server
if __name__ == "__main__":
    root_directory = r'root'
    # # # 
    # root_directory = r'root'
    process_all_subfolders(root_directory)


