import json
import os
import csv

import requests
import urllib3
from bs4 import BeautifulSoup
from dotenv import load_dotenv

import constants as consts

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

ito_resp = requests.post(
    consts.ITO_URL,
    allow_redirects=True,
    verify=False,
    data=os.environ['R_DATA'],
    headers={
        "Content-Type": os.environ['R_CONTENT_TYPE'],
        "User-Agent": os.environ['R_USER_AGENT'],
        "X-Requested-With": os.environ['R_X_REQUESTED_WITH'],
        "Cookie": os.environ['R_COOKIE'],
    },
)
ito_resp.raise_for_status()

soup = BeautifulSoup(ito_resp.text, "html.parser")

headers = ["domain", "ipv4", "ip_network","update_date", "due_date"]

rows = []
for tr in soup.find_all("tr")[1:]:
    rows.append([td.text for td in tr.find_all("td")])


data = [dict(zip(headers, row)) for row in rows]

sorted_items = sorted(data, key=lambda d: d['domain'])

data = sorted_items

# convert to json and save to file

# make sure directory exists
os.makedirs(os.path.dirname(consts.JSON_OUT_PATH), exist_ok=True)

with open(consts.JSON_OUT_PATH, "w", encoding="utf-8") as outfile:
    json.dump(data, outfile)


# convert to csv and save to file

# make sure directory exists
os.makedirs(os.path.dirname(consts.CSV_OUT_PATH), exist_ok=True)

# Open the CSV file for writing
with open(consts.CSV_OUT_PATH, "w", encoding="utf-8") as csvfile:
    # Create the DictWriter object
    writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())

    # Write the column names
    writer.writeheader()

    # Write the data rows
    writer.writerows(data)
