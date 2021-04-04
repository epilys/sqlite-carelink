#!python3
import csv
import argparse
import sys
import sqlite3
import re

parser = argparse.ArgumentParser(description='Import sensor readings')
parser.add_argument('--db', help="The sqlite3 database path", type=str, required=True)
parser.add_argument('csv', nargs='?', help="The csv exported from Carelink", type=argparse.FileType('r'), default=sys.stdin)
args = parser.parse_args()

# Read entire CSV file to string
f = args.csv.read()

# CSV file will contain multiple tables, we want the one that contains the Sensor values
skip_until_re=r'-------,[^,]*,Sensor,[^,]*,------- \n'
s = re.split(skip_until_re, f)[1]

# Detect CSV format dialect
dialect = csv.Sniffer().sniff(s)
reader = csv.DictReader(s.strip().split('\n'), dialect=dialect)

con = sqlite3.connect(args.db)
cur = con.cursor()
values = []
for row in reader:
    if len(row["Sensor Glucose (mg/dL)"]) >0:
        values.append((None, row['Date'].replace('/', '-')+' '+row['Time'], row["Sensor Glucose (mg/dL)"], row["ISIG Value"]))

print("Inserted", cur.executemany('INSERT OR IGNORE INTO sensor_glucose VALUES (?,?,?,?)', values).rowcount, "readings")
con.commit()
con.close()
