import pandas as pd
import pyarrow
import argparse
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

def main(
    lifters_file,
    output_file,
    config
    ):
    lifters = pd.read_csv(lifters_file)
    KM_fit = KaplanMeierFitter()
    Times = lifters['active_duration']
    Quit = lifters['inactive']
    KM_fit.fit(Times, event_observed=Quit)
    KM_fit.plot()
    plt.title("General survival curve for powerlifters")


    return()

if __name__ == "__main__":
