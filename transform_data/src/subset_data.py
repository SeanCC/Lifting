'''
To facilitate quicker turnaround in the coding process, we subset the data. 
Inferences on the subsetted data should be treated as preliminary

'''
import argparse
import pandas as pd
import numpy as np

def main(
    lift_file,
    config_file,
    output_file
    ):
    lift_dat = pd.read_csv(lift_file)
    lift_dat['Lifter_ID'] = pd.factorize(lift_dat.Name + str(lift_dat.Country))[0]
    IDs = lift_dat['Lifter_ID'].unique()
    subset_IDs = np.random.choice(IDs, size=config_file['subset_size'])
    lift_subset = lift_dat[lift_dat['Lifter_ID'] in subset_IDs]
    lift_subset.to_csv(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lift_file", help="Path to lift file")
    parser.add_argument("--config_file", help="Path to config")
    parser.add_argument("--output_file", help="Path to output file")
    args = parser.parse_args()

