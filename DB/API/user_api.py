# imports of packages
from bottle import Bottle, run, request

# apps imports
from DB.transactions import fetch_multi_series


app = Bottle()

@app.get('/')
def hello(name="Myself"):
    return "Hi, this API is for Brazil's  High Frequency economic data!"


@app.get('/api')
def fetch_data():
    srs = request.query.getall("series")
    fort = request.query.get("format")
    if fort is None:
        fort = "csv"
        
    if len(srs) == 0:
        return "Please, add a series to your request"
    else:
        try:
            df = fetch_multi_series(srs)
            return df.to_csv()
        except:
            return "not valid series"


run(app, host='localhost', port=8080, debbug=False)
