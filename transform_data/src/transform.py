import argparse
import pandas as pd
import yaml
import logging
import logging.info

def main(
    data_file,
    file_date,
    output_file,
    config
    ):
    lift_dat = pd.read_csv(data_file)






    #lifters['Active'] = (lifters)

def generate_lift_info(lift_dat):
    # Generating unique lifter and event IDs
    lift_dat['Lifter_ID'] = pd.factorize(lift_dat.Name + str(lift_dat.Country))[0]
    lift_dat['Date'] = pd.to_datetime(lift_dat['Date'], format='%Y-%m-%d', errors='coerce')
    lift_dat['Event_ID'] = pd.factorize(lift_dat['MeetName'] + lift_date['Date'].strftime('%Y-%m-%d') + lift_date['Federation'])
    # Sort values by lifter and date to make outcome generation quicker and easier
    lift_dat.sort_values(by=['Lifter_ID', 'Date'], inplace=True)
    # Generate date diffs and identify first event for feature and outcome generation
    lift_dat['Date_Diff'] = lift_dat['Date'].diff()
    lift_dat['First_Event'] = ~(lift_dat['Lifter_ID'].eq(lift_dat['Lifter_ID'].shift()))
    lift_dat.loc[lift_dat['First_Event'] == True, 'Date_Diff'] = -1
    lift_dat['Date_Diff'] = pd.to_timedelta(lift_dat['Date_Diff'])

    return(lift_dat)

def generate_lifters(lift_dat):
    lifters = pd.DataFrame(lift_dat['Lifter_ID'].unique())
    min_groupby = lift_dat.groupby(['Lifter_ID']).min().reset_index()
    max_groupby = lift_dat.groupby(['Lifter_ID']).max().reset_index()
    lifters['Start_Age'] = min_groupby['Age']
    lifters['Last_Age'] = max_groupby['Age']
    lifters['Lowest_Weight'] = min_groupby['BodyweightKg']
    lifters['Highest_Weight'] = max_groupby['BodyweightKg']
    lifters['First_Event_Date'] = max_groupby['Date'] 
    lift_dat['First_Event'] = lifters.loc[lifters['Lifter_ID'] == lift_dat['Lifter_ID'], 'First_Event_ID']

def generate_cutoff(lift_dat):
    def is_post(row):
        subset = lift_dat[(lift_dat['Lifter_ID'] == row['Lifter_ID']) & (lift_dat['Date'] <= row['Date'])]
        if subset['Greater_Than_Cutoff'].max() == True:
            return True
        else:
            return False
    # Flag rows that occur after the lifter has been gone for longer than the cutoff period
    lift_dat['Greater_Than_Cutoff'] = (lift_dat['Date_Diff'] > pd.Timedelta(365,'d'))
    lift_dat['Post_Removal'] = lift_dat.apply(is_post, axis=1)
    return(lift_dat)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_file", help="Path to powerlifting data")
    parser.add_argument("--file_date", help="Date when data was pulled")
    parser.add_argumnet("--config_file", help="Path to config file")
    parser.add_argument("--output_file", help="Path to output file")
    args = parser.parse()

    main(
        data_file = args.data_file,
        file_date = args.file_date,
        output_file = args.output_file
    )