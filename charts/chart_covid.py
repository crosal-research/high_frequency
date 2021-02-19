#!/usr/local/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
import numpy as np
import requests
from io import StringIO

def fetch(series:list) -> pd.DataFrame:
    """
    takes a list of tickers, build the url and fetch the data into
    data frame, which is thus return
    """
    srs = "&".join([f"series={s}" for s in series])
    url = f"http://localhost:8080/api?{srs}"
    resp = requests.get(url)
    return  pd.read_csv(StringIO(resp.text)).set_index(["Data"])



td = (dt.datetime.today()).strftime(format="%d-%b-%Y")

#configurations
plt.style.use("ggplot")
fig= plt.figure(figsize=(8,9))
axs = fig.subplots(2, 2)
fig.suptitle(f"COVID-19 Update: {td}", fontsize=12)


def gen_chart(df, title, y_title, ax, date_ini=None):
    """"""
    df_final = df.copy()

    df_final.loc[:, ["ITALY + FR + GER + SPAIN"]].plot(ax=ax, 
                                                       color='black', linewidth=1.0, style="-", label="ITALY + FR + GER + SPAIN")
    df_final.loc[:, ["US"]].plot(ax=ax, color='blue', linewidth=1.0, style="-", label="US")
    # df_final.loc[:, ["Rest of the World"]].plot(ax=ax, color='green', linewidth=1.0,
    #                                             style="-", label="Rest of the World")
    df_final.loc[:, ["BRAZIL"]].plot(ax=ax, color='red', linewidth=1.0,
                                     style="-", label="Brazil")

    # markers
    df_final.loc[:, ["ITALY + FR + GER + SPAIN"]].dropna().tail(1).plot(ax=ax, color='black', linewidth=0,
                                                               style="-", marker=".")
    df_final.loc[:, ["US"]].dropna().tail(1).plot(ax=ax, color='blue', linewidth=0,
                                         style="-", marker=".")
    # df_final.loc[:, ["Rest of the World"]].dropna().tail(1).plot(ax=ax, color='green', linewidth=0,
    #                                                     style="-", marker=".")
    df_final.loc[:, ["BRAZIL"]].dropna().tail(1).plot(ax=ax, color='red', linewidth=0,
                                             style="-", marker=".")

    # labels labels
    for label in ax.xaxis.get_ticklabels():
        label.set_fontsize(9)
    for label in ax.yaxis.get_ticklabels():
        label.set_fontsize(9)

    #annotation
    value2 = np.round(df_final.loc[:, ["ITALY + FR + GER + SPAIN"]].dropna().values[-1][0],0)
    value3 = np.round(df_final.loc[:, ["US"]].dropna().values[-1][0], 0)
    # value4 = np.round(df_final.loc[:, ["Rest of the World"]].dropna().values[-1][0], 0)
    value5 = np.round(df_final.loc[:, ["BRAZIL"]].dropna().values[-1][0], 0)
    
    ax.annotate(value2, 
                xy=(df_final.loc[:, ["ITALY + FR + GER + SPAIN"]].dropna().index[-5], value2*(1.2)), 
                color="black", fontsize=10)
    ax.annotate(value3, 
                xy=(df_final.loc[:, ["US"]].dropna().index[-50], value3*(1.1)), 
                color="blue", fontsize=10)
    # ax.annotate(value4, 
    #             xy=(df_final.loc[:, ["Rest of the World"]].dropna().index[-1] + 1, value4*(1.0)), 
    #             color="green", fontsize=10)
    ax.annotate(value5, xy=(df_final.loc[:, ["BRAZIL"]].dropna().index[-1]
                        , value5*(0.4)),
                color="red", fontsize=10)

    #facecolor
    ax.set_facecolor('#dddddd')

    # title
    ax.set_title(title, fontsize=10)
    ax.title.set_position([.5,1.03])
    ax.set_xlabel('days', fontsize=8)
    ax.set_ylabel(y_title, fontsize=8)

    #margins
    ax.margins(0.0, 0.2)
    ax.set_xlim(ax.get_xlim()[0]-5, ax.get_xlim()[1]+ 5)

    #lengend
    ax.get_legend().remove()

    return fig



def df_harvest(df:pd.DataFrame):
    '''
    Consumer a pandas data frame of and indexes (through a common index) them
    in count for the number of passing dates where the occurance takes place.
    Input:
    - df: DataFrame
    Output:
    - DataFrame
    '''
    dhf = pd.DataFrame()
    for c in df.columns:
        dh = df.loc[df.loc[:, c] > 0 , [c]]
        dhf = dhf.merge(pd.DataFrame(data=dh.values, index=range(0, len(dh)), 
                                     columns=[c]), 
                        left_index=True, right_index=True, how = "outer")
    return dhf



# initial date
date_ini = "2020-01-21"

# Regions
EU = ["ITALY", "GERMANY", "FRANCE", "SPAIN"]

### Fatal Cases

df = fetch(["JHU.Italy_fatalities", "JHU.FRANCE_fatalities", "JHU.Spain_fatalities", 
            "JHU.Germany_fatalities", "JHU.US_fatalities", "JHU.China_fatalities", 
            "JHU.Brazil_fatalities"])


    
df.columns = [(c.split("."))[1].split("_")[0] for c in df.columns]
df["ITALY + FR + GER + SPAIN"] = df.loc[:, EU].sum(axis=1)
# df["Rest of the World"] = df.drop(columns=["ITALY", "GERMANY",
#                                            "FRANCE", "SPAIN",
#                                            "US",
#                                            "ITALY + FR + GER + SPAIN",
#                                            "BRAZIL"]).sum(axis=1)

# harvest of fatal case
dhf = df_harvest(df)
gen_chart(dhf, "Harvests by Regions - Fatal Cases", "Units", axs[0, 0])


# Harvest New fatal cases
#dff = (df - df.shift(1)).dropna()
dff = (df - df.shift(1))
dhff = df_harvest(dff).rolling(window=7).mean()
gen_chart(dhff, "Harvests by Regions - New Daily Fatal Cases \n (7-days ma)", "Units", axs[0, 1], date_ini=date_ini)


### Reported Cases
dc = fetch(["JHU.Italy_cases", "JHU.FRANCE_cases", "JHU.Spain_cases", "JHU.Germany_cases", "JHU.US_cases", "JHU.China_cases", "JHU.Brazil_cases"])
dc.columns = [(c.split("."))[1].split("_")[0] for c in dc.columns]

dc["ITALY + FR + GER + SPAIN"] = dc.loc[:, EU].sum(axis=1)
# dc["Rest of the World"] = dc.drop(columns=["ITALY", "GERMANY", 
#                                            "FRANCE", "SPAIN",
#                                            "US",
#                                            "ITALY + FR + GER + SPAIN",
#                                            "BRAZIL"]).sum(axis=1)

#New Reported Cases
dn = (dc - dc.shift(1))
#dn = (dc - dc.shift(1)).dropna()
dn = (dc - dc.shift(1))
dnc = df_harvest(dn).rolling(window=7).mean()
gen_chart(dnc, "Harvests by Region - New Daily confirmed Cases \n (7-days ma)", "Units", axs[1, 1], date_ini=date_ini)

# harvest of cases
dhc = df_harvest(dc)    
gen_chart(dhc, "Harvests by Region - Confirmed Cases", "Units", axs[1, 0])


# legends
axs[0][0].legend(['Italy + FR + \n GER + Spain',
                  'US', 'Brazil'], 
                 loc='upper left', fontsize=9)


#Add Source
plt.text(0.9, -0.3, "Source: John Hopkins CSSE", 
         transform=axs[1,0].transAxes, fontsize=10)

# Save figure
plt.savefig("./images/coronavirus.png")

print("Covid charts are all ready!")
print("-----------\n")
