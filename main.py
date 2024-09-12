"""
Main
"""

import pandas as pd
import matplotlib.pyplot as plt


def read_csv_file(file_name):
    return pd.read_csv(file_name)


def stats_overview(df, col):
    stat_table = df[[col]].describe()  # Doesn't include median
    median = df[[col]].median()
    stat_table.loc["median"] = median  # Add median to stat_table
    return stat_table


def split_day_night(df):
    # Transform 'date_time to datetime'
    df["date_time"] = pd.to_datetime(df["date_time"])

    # Separate data into day and night
    df_day = df.copy()[(df["date_time"].dt.hour >= 7) & (df["date_time"].dt.hour < 19)]
    df_night = df.copy()[
        (df["date_time"].dt.hour >= 19) | (df["date_time"].dt.hour < 7)
    ]

    return df_day, df_night


def hist_day_night(df_day, df_night):
    plt.figure(figsize=(11, 4))

    plt.subplot(1, 2, 1)
    plt.hist(df_day["traffic_volume"])
    plt.xlim(-100, 7500)
    plt.ylim(0, 8000)
    plt.title("Traffic Volume: Day")
    plt.xlabel("Traffic Volume")
    plt.ylabel("Frequency")

    plt.subplot(1, 2, 2)
    plt.hist(df_night["traffic_volume"])
    plt.xlim(-100, 7500)
    plt.ylim(0, 8000)
    plt.title("Traffic Volume: Night")
    plt.xlabel("Traffic Volume")
    plt.ylabel("Frequency")

    # plt.savefig("Figure/Traffic.png")


if __name__ == "__main__":
    # Create DataFrame of I-94 Traffic
    i_94_df = read_csv_file("Metro_Interstate_Traffic_Volume.csv.gz")

    # Get statistics about traffic volume
    traffic_volume_summary = stats_overview(i_94_df, "traffic_volume")
    print("Traffic Volume Summary\n", traffic_volume_summary, "\n")

    # Traffic stats: Day vs Night
    day_df, night_df = split_day_night(i_94_df)
    day_traffic_volume = stats_overview(day_df, "traffic_volume")
    print("Day Traffic Volume Stats\n", day_traffic_volume, "\n")

    night_traffic_volume = stats_overview(night_df, "traffic_volume")
    print("Night Traffic Volume Stats\n", night_traffic_volume, "\n")

    # # Histogram of Traffic Volume: Day vs Night
    hist_day_night(day_df, night_df)
    plt.savefig("Figure/Traffic.png")
