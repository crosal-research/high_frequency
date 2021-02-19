#!/usr/local/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import requests
from io import StringIO

# configurations
plt.style.use("ggplot")

def fetch(series:list) -> pd.DataFrame:
    """
    takes a list of tickers, build the url and fetch the data into
    data frame, which is then return
    """
    srs = "&".join([f"series={s}" for s in series])
    url = f"http://localhost:8080/api?{srs}"
    resp = requests.get(url)
    return  pd.read_csv(StringIO(resp.text)).set_index(["Data"])



# chart for fully vaccination per handred

def gen_lines(df, data_ini):
    global dfinal
    dfinal = df[df.index >= data_ini]
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for c in dfinal.columns:
        dfinal.loc[:, [c]].plot(ax=ax1, alpha=0.8, linewidth=2.0)
    # axis
    ax1.set_xlabel("")
    ax1.tick_params(axis='x', labelrotation=45)
    ax1.set_title(f"Daily Vaccination  per Million \n (Last: {df.index.values[-1]} - Weekly MA)")
    ax1.text(0.0, -100.0, "source: ONS", fontsize=9)
    return fig


# tipos de energia
energia = ["Carga", "total"]


tcks = []
for e in energia:
    tcks.append(f"ONS.{e}".upper())

dg = fetch(tcks).rolling(window=7).mean().dropna()
dg.columns = energia


# produce charts

fig = gen_lines(dg.loc[:, ["Carga"]], "2020-03-01")
plt.tight_layout()
plt.show()
# plt.savefig("./images/ons.png")
# print("Ons charts are all ready!")
# print("-----\n")
