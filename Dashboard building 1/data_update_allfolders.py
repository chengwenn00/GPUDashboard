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

def process_all_subfolders(root_directory):
    for root, dirs, files in os.walk(root_directory):
        for subfolder in dirs:
            subfolder_path = os.path.join(root, subfolder)
            if "PCS" in subfolder:
                print(f"Processing subfolder: {subfolder_path}")
                # os.chdir (r'C:\Users\yongyang\OneDrive - Advanced Micro Devices Inc\Documents\04program\navi')
                # change directory accordingly
                # Enter the "pmlogfiles" folder within the selected subfolder
                pmlogfiles_path = os.path.join(subfolder_path, "pmlogfiles")
                    
                if os.path.exists(pmlogfiles_path):
                    print(f"Processing pmlogfiles in: {pmlogfiles_path}")
                    PATH = pmlogfiles_path
                    pcs_no = subfolder  # Use the subfolder name as pcs_no
                    output_filename = f'OUTPUT_{pcs_no}.csv'  # Include subfolder name in the output filename
                    date_today=datetime.now().strftime("%Y-%m-%d") 
                    total=0
                    #----------------grab all files for total cycles count------------------------------    
                    df = pd.DataFrame()

                    filenames = glob.glob(PATH+r'/pm*.csv')
                    filenames = glob.glob(os.path.join(PATH, 'pm*.csv'))


                    files_to_move = []

                    for filename in filenames:
                        print('current filename:',filename)
                        filesize=os.path.getsize(filename)


                        time_temp=time.strptime(time.ctime(os.path.getmtime(filename)))
                        print(time_temp)
                        time_val=(time.strftime("%Y-%m-%d",time_temp))
                        if time_val<=date_today:
                            temp_df=pd.read_csv(filename,sep=',',on_bad_lines='skip',engine='c',header=0)
                        else:
                            continue
                        temp_df=pd.read_csv(filename,sep=',',on_bad_lines='skip',engine='c',header=0)
                        temp_df=temp_df.replace(regex=['--\[','\] --'], value='')
                        temp_df.columns=[x.strip().replace(' ','') for x in temp_df.columns]
                        temp_df.applymap(lambda x: x.strip() if type(x)==str else x)
                        temp_df = temp_df.filter(regex='Temperature|TimeStamp|Power|Gradient',axis=1)
                        temp_df['TimeStamp']=pd.to_datetime(temp_df['TimeStamp'],dayfirst=True,errors='coerce')
                        temp_df = temp_df.dropna()
                        global_row=temp_df.shape[0]
                        df = pd.concat([df,temp_df])


                    df['Time Stamp']=pd.to_datetime(df['TimeStamp'],dayfirst=True)
                    df.set_index("TimeStamp", inplace = True)
                    # print(df.head())
                    # df=df.resample("5T").max()
                    df = df.groupby(pd.Grouper(freq='5Min', origin='start')).agg({
                                                            "GPU0PowerTGPPower":  "max",
                                                            "GPU0TemperatureHotspot":  "max",
                                                            "GPU0TemperatureGradientMaximumMaxToMin": "max",})
                                                        #     "GPU0GDFLLFrequenciesDFLL0Post-DS": "max",
                                                        # })
                    df.reset_index(inplace=True)
                    df = df.rename(columns = {'index':'TimeStamp'})
                    df=df.dropna().reset_index(drop=True)
                    df.index.name='cyclecount'
                    df.index += 1 

                    output_filename = f'OUTPUT_{pcs_no}.csv'
                    df.to_csv(os.path.join(PATH,output_filename))

if __name__ == "__main__":
    # Specify the root directory that contains all subfolders to process
    root_directory = r'Z:\power_cycling'
    process_all_subfolders(root_directory)





            

# print('-----completed max *** archiving--------')

# # -----we need to clean df before plotting----

# print(12)

# def find_timestamp_above_threshold(df, variable_name, threshold_value):  
#     # Initialize a flag to track if the threshold has been crossed
#     threshold_crossed = False
    
#     # Iterate through rows in the DataFrame
#     for index, row in df.iterrows():
#         if row[variable_name] > threshold_value:
#             print(row)
#             return row['TimeStamp']



    #         if threshold_crossed:
    #             return row['TimeStamp']
    #         else:
    #             threshold_crossed = True
    #     else:
    #         threshold_crossed = False
    
    # return None

# # Define the variable name and threshold value
# variable_name = 'GPU0TemperatureHotspot'
# threshold_value = 100

# # Find the timestamp when "GPU0TemperatureHotspot" crosses 100 in the CSV file
# timestamp_above_threshold = find_timestamp_above_threshold(df, variable_name, threshold_value)

# if timestamp_above_threshold:
#     print(f"The timestamp when {variable_name} crosses {threshold_value} is {timestamp_above_threshold}.")
# else:
#     print(f"{variable_name} never crosses the threshold of {threshold_value} in the CSV file.")


# def remove_outliers(data,col):
#    q3=np.quantile(data[col],0.75)
#    q1=np.quantile(data[col],0.25)
#    iqr=q3-q1
#    print(iqr)
#    upfence=q3+1.5*iqr
#    lowfence=q1-1.5*iqr
#    data=data.drop(data[(data[col]>upfence) | (data[col]<lowfence)].index,inplace=True)
#    return data

# df.drop(df[df['GPU0TemperatureHotspot']<85].index,inplace=True)

# remove_outliers(df,'GPU0PowerTGPPower')
# remove_outliers(df,'GPU0TemperatureHotspot')
# remove_outliers(df,'GPU0TemperatureGradientMaximumMaxToMin')
# # remove_outliers(df,'GPU0GDFLLFrequenciesDFLL0Post-DS')

# # ----- resets cycle count back to continous after dropping anomalies -----
# df.reset_index(drop=True,names='cyclecount',inplace=True)
# df.index.name='cyclecount'
# df.index += 1   
# df.to_csv(os.path.join(PATH,'OUTPUT_clean.csv')) 

# # Initialising graphs    (Change the title and x and y axis title accordingly)
# # Initialise more graphs if you need to plot more
# graph1 = figure(title = "Maximum Socket Power",
#                x_axis_label = "Cycle Numbers",
#                y_axis_label = "Socket Power(W)",
#                width = 1000)

# graph2 = figure(title = "Maximum Temperature Hotspot",
#                x_axis_label = "Cycle Numbers",
#                y_axis_label = "Temperature Hotspot(deg)",
#                width = 1000)

# graph3 = figure(title = "Maximum Temperature Gradient(deg)",
#                x_axis_label = "Cycle Numbers",
#                y_axis_label = "Temperature Gradient",
#                width = 1000)

# # graph4 = figure(title = "Maximum FGX Frequency (HZ)",
# #                x_axis_label = "Cycle Numbers",
# #                y_axis_label = "Frequency (HZ)",
# #                width = 1000)



# source = ColumnDataSource(df)


# graph1.line(x='cyclecount', y='GPU0PowerTGPPower',
#          source=source)
# graph1.y_range.start = 0
# graph1.xaxis.formatter=BasicTickFormatter(use_scientific=False)
# graph1.title.text_font_size = "20pt"
# graph1.axis.axis_label_text_font_size = "20pt"
# graph1.axis.major_label_text_font_size = "20pt"

# graph2.line(x='cyclecount', y='GPU0TemperatureHotspot',
#          source=source)
# graph2.y_range.start = 0
# graph2.xaxis.formatter=BasicTickFormatter(use_scientific=False)
# graph2.title.text_font_size = "20pt"
# graph2.axis.axis_label_text_font_size = "20pt"
# graph2.axis.major_label_text_font_size = "20pt"

# graph3.line(x='cyclecount', y='GPU0TemperatureGradientMaximumMaxToMin',
#          source=source)
# graph3.y_range.start = 0
# graph3.xaxis.formatter=BasicTickFormatter(use_scientific=False)
# graph3.title.text_font_size = "20pt"
# graph3.axis.axis_label_text_font_size = "20pt"
# graph3.axis.major_label_text_font_size = "20pt"

# # graph4.line(x='cyclecount', y='GPU0GDFLLFrequenciesDFLL0Post-DS',
# #          source=source)
# # graph4.y_range.start = 0
# # graph4.xaxis.formatter=BasicTickFormatter(use_scientific=False)
# # graph3.line(cycleCount, grad_gpu1,color='blue',legend='GPU1 max gradient temp')
# # graph4.title.text_font_size = "20pt"
# # graph4.axis.axis_label_text_font_size = "20pt"
# # graph4.axis.major_label_text_font_size = "20pt"

# graph1.add_tools(HoverTool(
#     tooltips=[
#     ('Cycle','@cyclecount{o}'),
#     ('Cycle Max Socket Power(W)','@GPU0PowerTGPPower')],
# ))

# graph2.add_tools(HoverTool(
#     tooltips=[
#     ('Cycle','@cyclecount{o}'),
#     ('Temperature Hotspot(deg)','@GPU0TemperatureHotspot')],
#     mode='vline'
# ))

# graph3.add_tools(HoverTool(
#     tooltips=[
#     ('Cycle','@cyclecount{o}'),
#     ('Temperature Gradient','@GPU0TemperatureGradientMaximumMaxToMin')],
#     mode='vline'
# ))

# # graph4.add_tools(HoverTool(
# #     tooltips=[
# #     ('Cycle','@cyclecount{o}'),
# #     ('Frequency(Hz)','@{GPU0GDFLLFrequenciesDFLL0Post-DS}')],
# #     mode='vline'
# # ))

# output_file(os.path.join(PATH, 'NV21_PC plotting'+ date_today + '.html'), title="Power Cycling Plot")

# graph_list = [graph1, graph2, graph3]#, graph4]             # if you added or removed graphs, change the list accordingly

# # show(graph1)
# print('complete')
# show(gridplot(graph_list, ncols=1, width=1000))

# # cheng wen debugged this part further. code has to run through the list before placing into folder
# print(df)
# for filename in filenames:
#     if not os.path.exists(filename):
#         print(filename)
#         print(PATH)
#         print('1')
#         continue
#     temp_df = pd.read_csv(filename,sep=',', on_bad_lines='skip', engine='c', header=0)

#     psn_value = temp_df['GPU0 Master PSN'][0]
#     if(psn_value==None):
#         psn_value = temp_df['GPU0 Master PSN'][1]
#     print(psn_value)
#     target_folder = os.path.join(PATH, psn_value)
#     if not os.path.exists(target_folder):
#         os.mkdir(target_folder)
#     shutil.move(filename, os.path.join(target_folder, os.path.basename(filename)))


# Move the print statement here, outside of the loop
# print("CSV files classified into respective PSN folders.")
