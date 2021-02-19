import pandas as pd
from DB.transactions import add_series

energia = ["Total", "Carga"]

def load_series(energia) -> None:
    """
    takes energy type  and insert into the database 
    """
    tck = f"ONS.{energia}".upper()
    try:
        if energia.upper() == "CARGA":
            desc = "Carga despachada pelo sistema"
        else:
            desc = "Energia total produzida pelo o sistema"
        add_series(tck, desc , "BRASiL", "ONS")
    except:
        print(f"Series {tck} failed to be added!")



for e in energia:
    load_series(e)
