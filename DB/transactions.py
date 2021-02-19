from pony import orm
import DB.db as db
import datetime as dt
import pandas as pd
import numpy as np
from functools import reduce, wraps


def multi_dfs_wrapper(func):
    @wraps(func)
    def wrapper(*args, **dargs):
        return reduce(lambda x, y: x.merge(y, left_index=True, right_index=True, how="outer"), func(*args, **dargs))
    return wrapper


@orm.db_session
def add_source(name:str, description:str) -> None:
    Uname = name.upper()
    if (src:= db.Source.get(name=Uname)):
        src.description = description
        print(f"Source {Uname} already exists. Updated")
    else:
        db.Source(name=Uname.upper(), description=description)
        print(f"Source {Uname} added to the database")


@orm.db_session
def add_series(ticker:str, description:str, country:str, source: str) -> None:
    Uticker = ticker.upper()
    if (series:=db.Series.get(ticker=Uticker)):
        series.description = description
        series.country = country.upper()
        series.source = db.Source.get(name=source.upper())
        print(f"Series {Uticker} already exists. Updated")
    else:
        if (src:=db.Source.get(name=source.upper())):
            db.Series(ticker=Uticker, description=description, 
                      country=country.upper(), source=src)
            print(f"Series {ticker.upper()} added to the ")
        else:
            print(f"Series {source.upper()} not in the database")


@orm.db_session
def add_observation(ticker: str, dat:dt.datetime , value:float) -> None:
    if (series:=db.Series.get(ticker=ticker.upper())):
        obs = db.Observation.get(date=dat, series=series)
        if obs:
            obs.set(date=dat, obs=value)
        else:
            db.Observation(date=dat, obs=value, series=series)
    else:
        print(f"Ticker {ticker.upper()} not in the database")

@orm.db_session
def add_batch_observations(ticker:str, df:pd.DataFrame):
    """Adds data frame n x 1 into the database related to a ticker. The
    index should be a datetime.index and the observations of the data
    column should be float numbers
    """
    if df.shape[1] == 1:
        for ind in df.index:
            add_observation(ticker.upper(), ind, float(df.loc[ind].values))
    else:
        print("Data Frame with wrong dimension")


@orm.db_session        
def fetch_series_list() -> pd.DataFrame:
    """
    Fetch the list of series in the database
    """
    srs = orm.select((s.ticker, s.description, s.source.name) for s in db.Series)
    return pd.DataFrame(data=list(srs), columns=["Ticker", "Description", "Source"])

    

@orm.db_session
def fetch_series(ticker:str, ini:str=None, final:str=None) -> pd.DataFrame:
    """Fetches from database the observation of a single series. Return a
    data frame with the observations.
    missing: checking whether ini <= final
    """
    Uticker = ticker.upper()
    sr =  db.Series.get(ticker=Uticker)
    ini = dt.datetime.fromisoformat(ini) if ini is not None else None
    final = dt.datetime.fromisoformat(final) if final is not None else None
    if sr:
        if (ini is None) and (final is None):
            obs = orm.select((o.date, o.obs) for o in db.Observation 
                             if o.series.ticker == Uticker)
        elif (ini is not None) and (final is None):
            obs = orm.select((o.date, o.obs) for o in db.Observation 
                             if o.series.ticker == Uticker and o.date >= ini)
        elif ini is None and (final is not None):
            obs = orm.select((o.date, o.obs) for o in db.Observation 
                             if o.series.ticker == Uticker and o.date <= final)
        else:
            obs = orm.select((o.date, o.obs) for o in db.Observation 
                             if o.series.ticker == Uticker and o.date <= final
                             and o.date >= ini)
        return  pd.DataFrame(list(obs), columns=["Data", Uticker]).set_index("Data")
    else:
        print(f"Ticker {Uticker} in not in the database")


@multi_dfs_wrapper
def fetch_multi_series(srs: list, ini:str=None, final:str=None) -> [pd.DataFrame]:
    return  [fetch_series(sr, ini, final) for sr in srs]
    
        
        
            
