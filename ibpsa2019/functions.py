# Set of functions needed for experiments completion
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math


"""
Constants for time period with maximum number of buildings measured simultaneously in the BDG dataset.
For more details, go to RawFeatures_BDG.ipynb
"""
BDG_STARTDATE = datetime.strptime('01/01/15 00:00', '%d/%m/%y %H:%M')
BDG_ENDDATE = datetime.strptime('30/11/15 23:00','%d/%m/%y %H:%M')


"""
Function to load datasets. Currently the following datasets are in the repo:
- Building Data Genome Dataset
- Washington D.C. dataset
"""
def loadDataset(name):
    # Building Data Genome dataset
    if name == 'BDG':
        df = pd.read_csv('data/temp_open_utc_complete.csv', parse_dates=True, infer_datetime_format=True, index_col=0)
    
    # Washington D.C. dataset
    elif name == 'DC':
        df = pd.read_csv('data/DGS_322_Buildings-15m-By_Building-DST-gap-filled-3-2-18-508pm.csv',
                            parse_dates=[['Building ID', 'Unnamed: 1']], infer_datetime_format=True)
        # get rid of temperature column
        del df['Unnamed: 2']

        # update column names to match the row of building names
        new_column_names = df.iloc[0,:]
        df.columns = new_column_names

        # get rid of rows with metadata and update index
        df = df.drop([0,1,2], axis=0)
        df = df.rename(columns = {'Building nan':'timestamp'})
        df.index = df['timestamp'].astype('datetime64[ns]')
        del df['timestamp']
        df = df.astype(float)
        
        # since the dataset is made from 15min interval readings, resample to 1 hr
        df = df.resample('1H').sum()

    else:
        print("Please choose a valid dataset")
        exit()

    return df


"""
Function to extract a given context from a dataframe. The resulting context is saved in a csv file.
Current contexts:
- Weekday
- Weekend
- Entire Week
"""
def getContext(context, dataframe, name):
    # truncate the dataframe based on a pre-calculated time period, if needed
    if name == 'BDG':
        startDate = BDG_STARTDATE
        endDate = BDG_ENDDATE
    else:
        startDate = dataframe.index[0]
        endDate = dataframe.index[len(dataframe) - 1]
    
    dataframe_truncated = dataframe[(dataframe.index >= startDate) & (dataframe.index <= endDate)]

    # resample based on context    
    if context == "weekday":
        df_context = dataframe_truncated[(dataframe_truncated.index.weekday != 5) & 
                                     (dataframe_truncated.index.weekday != 6)]
    elif context == "weekend":
        df_context = dataframe_truncated[(dataframe_truncated.index.weekday == 5) |
                                     (dataframe_truncated.index.weekday == 6)]
    elif context == "entireweek":
        df_context = dataframe_truncated.copy()
    else:
        print("Please choose a valid context")
        exit()
    
    # delete the dates with 0 values
    df_context = df_context[(df_context.T != 0).any()]
    # replace 0.0 with NaN to drop columns with NaN
    # df_context = df_context.replace(0.0, np.nan)
    # drop columns with all nan values
    df_context = df_context.dropna(axis=1, how='all') 
    # drop columns with more than 7 nan values (seems to be a sweet spot)
    df_context = df_context.dropna(thresh=len(df_context) - 7,axis=1)

    # save the file and return the dataframe
    df_context.to_csv("data/{}_{}Context.csv".format(name, context))
    return df_context


"""
Function that calculates a load profile curve, for each building on a dataframe, based on the specified function.
Currently the following functions are supported:
- Average
- Median
- Linear Regression

And the currently resampling:
- Daily
"""
def doAggregation(function, dataframe, resolution):
    df_load_curves = pd.DataFrame() # dataframe that will hold all load curves
    
    # resample based on parameter
    if (resolution == 'day'):
        availableSamples = (dataframe.resample('1D').asfreq()).index # get list of timestamps group by day
        delta = 23 # timedelta based on resample
    else:
        print("Please choose a valid resolution")
        exit()

    # iterate through all buildings (column)
    for column in range(len(dataframe.columns)):
        df_sampledReadings = pd.DataFrame() # dataframe to hold new samples for a column
        currentRow = pd.DataFrame(dataframe.iloc[:, column])
        
        # iterate through each day
        for timestamp in availableSamples:
            # update time limits to the current date
            start = timestamp
            end = timestamp + timedelta(hours=delta)
            # get meter data from only this resolution
            df_reading = currentRow[(currentRow.index >= start) & (currentRow.index <= end)]
            # ignore index since they are unique timestamps
            df_reading.reset_index(drop=True, inplace=True)         
            # append new sample as columns
            df_sampledReadings = pd.concat([df_sampledReadings, df_reading], axis=1)
            
        # make sure sure there are no columns with NaN values
        df_sampledReadings.dropna(axis=1, how='all', inplace=True)
        df_sampledReadings = df_sampledReadings.T # transpose it so it's easier to see and operate
        # up to this point, the matrix above has the shape nxm where is the number of instances and m is the number of readings

        # calculate load curve based on function
        if function == 'average':
            load_curve = np.mean(df_sampledReadings, axis = 0)

        elif function =='median':
            df_sampledReadings.fillna(value=0, inplace=True) # median will not work with NaN
            load_curve = np.median(df_sampledReadings, axis = 0)

        # elif function == 'linear':
            # TODO: perform linear regresion based on 2d matrix
        else:
            print("Please choose a valid context")
            exit()

        ####################################################################
        # # TODO: coding is for plotting purposes
        # print (df_sampledReadings)
        # plt.figure(figsize=(18,10))
        # x_axis = range(0, len(df_sampledReadings.columns))
        # for _, curve in df_sampledReadings.iterrows():
        #     plt.plot(x_axis, curve, "k-", alpha=.2)
        # plt.plot(x_axis, load_curve, "r-")
        # plt.title("Load Profiles and red representative curve based on {}".format(function))        
        # plt.show()
        ####################################################################

        # turn into one column dataframe for easier manipulation
        load_curve = pd.DataFrame(load_curve)
        # keep the instance name as column name
        instance_name = []
        instance_name.append(df_sampledReadings.index[0])
        load_curve.columns = instance_name
        # append current load curve to dataframe
        df_load_curves = pd.concat([df_load_curves, load_curve], axis=1)
        
        # end of for loop for one column

    df_load_curves = df_load_curves.T # rotate the final dataframe
    # save the file and return the dataframe
    df_load_curves.to_csv("data/loadCurves_{}_{}.csv".format(resolution, function))
    return df_load_curves

