#!python3
import sys
import argparse
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime, time, timedelta

sns.set_theme(style="whitegrid")
pd.plotting.register_matplotlib_converters()

parser = argparse.ArgumentParser(description='Plot average day glucose chart')
parser.add_argument('--db', help="The sqlite3 database path", type=str, required=True)
parser.add_argument('--high-limit', help="Default: 180", default=180)
parser.add_argument('--low-limit', help="Default: 70", default=70)

args = parser.parse_args()
high_limit = args.high_limit
low_limit = args.low_limit

con = sqlite3.connect(args.db, detect_types=sqlite3.PARSE_COLNAMES)
df = pd.read_sql_query("select datetime, value from sensor_glucose;", con)
def transform_datetime(d):
    t = datetime.fromisoformat(d).time()
    t = t.replace(minute=(t.minute // 5)*5, second=0)
    return t

# Calculate earliest and latest day of data
min_date = datetime.fromisoformat(df["datetime"].min()).date()
max_date = datetime.fromisoformat(df["datetime"].max()).date()
# Calculate how many days of data in the interval (note: not distinct days)
days = (max_date-min_date).days

# Discard date information and keep only time
df["datetime"] = df["datetime"].apply(transform_datetime)

g = sns.relplot(x="datetime", y="value", kind="line", ci="sd", data=df, aspect=20.7/8.27)

g.set(ylabel="BG (mg/dL)", xlabel=f"Interval from {min_date} to {max_date}, total {days} days")

sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})

# Set x axis labels

xticks = [time(hour=hour, minute=min) for hour in range(0, 24) for min in range(0, 60, 30)]
xlabels = [t.strftime("%H:%M") for t in xticks]

# Set time labels every 30 minutes
g.set(xticks=xticks, xticklabels=xlabels)
# Show time labels rotated
g.set_xticklabels(rotation=90)

# Don't show empty space left and right of the chart
plt.ylim(0, df["value"].max())
plt.xlim(xticks[0], xticks[47])

# Draw goal range

g.ax.fill_between([df["datetime"].min(),df["datetime"].max()], low_limit, high_limit, color='tab:green', alpha=0.1)

plt.tight_layout()

plt.show()
con.close()
