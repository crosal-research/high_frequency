#!/usr/local/bin/python3


#import from packages
import requests
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt

def fetch(series:list) -> pd.DataFrame:
    """
    takes a list of tickers, build the url and fetch the data into
    data frame, which is thus return
    """
    srs = "&".join([f"series={s}" for s in series])
    url = f"http://localhost:8080/api?{srs}"
    resp = requests.get(url)
    return  pd.read_csv(StringIO(resp.text)).set_index(["Data"])

df = fetch(["apple.brazil", "apple.germany", "apple.italy",
            "apple.united_kingdom", "apple.united_states", 
            "apple.spain", "apple.france"])
dp = (df.divide(df.iloc[0,:])-1)*100
dp.index = pd.to_datetime(dp.index)
dtoday = dt.strftime(dt.today(),"%d-%m-%Y")

# chart
plt.style.use("ggplot")

def gen_fig(df):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    dp.loc[:, ["APPLE.BRAZIL"]].plot(ax=ax, linewidth=0.0, color="red", label="_")
    dp.loc[:, ["APPLE.BRAZIL"]].rolling(window=7).mean().plot(ax=ax, linewidth=1.5, color="red")
    dp.loc[:, ["APPLE.UNITED_STATES"]].plot(ax=ax, linewidth=0.0, color="blue")
    dp.loc[:, ["APPLE.UNITED_STATES"]].rolling(window=7).mean().plot(ax=ax, linewidth=1.5, color="blue")
    dp.loc[:, ["APPLE.GERMANY"]].plot(ax=ax, linewidth=0.0, color="green")
    dp.loc[:, ["APPLE.GERMANY"]].rolling(window=7).mean().plot(ax=ax, linewidth=1.5, color="green")
    # dp.loc[:, ["APPLE.SPAIN"]].plot(ax=ax, linewidth=0.0, color="orange")
    # dp.loc[:, ["APPLE.SPAIN"]].rolling(window=7).mean().plot(ax=ax, linewidth=1.5, color="orange")
    dp.loc[:, ["APPLE.UNITED_KINGDOM"]].plot(ax=ax, linewidth=0.0, color="black")
    dp.loc[:, ["APPLE.UNITED_KINGDOM"]].rolling(window=7).mean().plot(ax=ax, linewidth=1.5, color="black")
    dp.loc[:, ["APPLE.FRANCE"]].plot(ax=ax, linewidth=0.0, color="purple")
    dp.loc[:, ["APPLE.FRANCE"]].rolling(window=7).mean().plot(ax=ax, linewidth=1.5, color="purple")

    # axis
    ax.set_xlabel("")
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_ylabel("%")
    ax.set_title(f"Mobility Tracker \n Date:{dtoday} \n (with weekly ma)")

    #margins
    ax.margins(0.05, 0.05)
    ax.set_xlim(ax.get_xlim()[0]-1, ax.get_xlim()[1]+ 1)

    #legend
#    global handles, labels
    handles, labels = ax.get_legend_handles_labels()
    labels = [l.split(".")[1] for l in labels]
    hs = [l[1] for  l in enumerate(handles) if l[0]%2==1]
    ls = [l[1] for  l in enumerate(labels) if l[0]%2==1]
    leg = ax.legend(hs, ls, loc="lower left")
    leg.get_frame().set_linewidth(0.0)
    return fig

fig = gen_fig(dp)


#Add Sourc
plt.tight_layout()
plt.text(0.55, 0, "source: Apple Inc", fontsize=10)

plt.savefig("./images/mobility.png")
print("Mobility Charts Done!")
print("-----\n")
