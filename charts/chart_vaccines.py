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
def gen_bar(df):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    (df.T).plot.barh(ax=ax, align="center", alpha=0.5, 
                     color=["blue", "blue","blue", "black", "blue", "blue"])
    # axis
    ax.set_xlabel("%")
    ax.tick_params(axis='x', labelrotation=45)

    ax.set_title(f"Fully Vaccinated Inhabitants per Hundred \n ({df.index.values[-1]})")
    
    ax.get_legend().remove()
    ax.text(-0.2, -1.7, "source: Our World in Data, Univ. of Oxford", fontsize=9)
    return fig


def gen_lines(df):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for c in df.columns:
        df.loc[:, [c]].plot(ax=ax1, alpha=0.8, linewidth=2.0)
    # axis
    ax1.set_xlabel("")
    ax1.tick_params(axis='x', labelrotation=45)
    ax1.set_title(f"Daily Vaccination  per Million \n (Last: {df.index.values[-1]} - Weekly MA)")
#    ax1.text(0.0, -100.0, "source: Our World in Data, Univ. of Oxford", fontsize=9)
    return fig


# fully vaccination per 100 inhabitants
countries = ["World", "Brazil", "United_States", "Germany",
             "United_Kingdom", "Argentina"]


# chart on vaccination per hundred
tcks = []
for c in countries:
    var = "people_fully_vaccinated_per_hundred"
    tcks.append(f"OWID.{c}_{var}".upper())

df = fetch(tcks).fillna(method="ffill")
df_final = pd.DataFrame(data=[[x if x >0 else 0 for x in df.tail(1).values[0]]], 
                        columns = [c.replace("_", " ") for c in countries], 
                        index = [df.tail(1).index[0]]).sort_values(by=[df.tail(1).index.values[0]],axis=1)


# daily vaccination per millions
tcks = []
for c in countries:
    var = "daily_vaccinations_per_million"
    tcks.append(f"OWID.{c}_{var}".upper())

dg = fetch(tcks).rolling(window=7).mean()
dg.columns = [c.replace("_", " ") for c in countries]
dg_final = dg

# produce charts
fig = gen_bar(df_final)
plt.tight_layout()
plt.savefig("./images/vaccine_per_h.png")

fig = gen_lines(dg_final)
plt.tight_layout()
plt.savefig("./images/vaccine_per_mn.png")
print("Vaccine charts are all ready!")
print("-----\n")
