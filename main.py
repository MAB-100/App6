from flask import Flask , render_template
import pandas as pd 

app = Flask(__name__)



@app.route("/")
def home():
    filename = "data_small\stations.txt"
    station = pd.read_csv(filename, skiprows=17)
    station= station[["STAID","STANAME                                 "]]
    return render_template("home.html" , data = station.to_html())

@app.route("/api/v1/<station>/<date>")
def api(station,date):
    filename = "data_small\TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    return {"station": station,"date":date,
            "temperature":temperature}

@app.route("/api/v1/yearly/<station>/<year>")
def yearly_data(station,year):
    filename = "data_small\TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result
    

@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data_small\TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result




if __name__ == "__main__":
    app.run(debug=True)