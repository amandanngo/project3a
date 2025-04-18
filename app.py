from flask import Flask, render_template, request, flash
import csv

from chart_generation import generate_chart
from api_handling import fetch_stock_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


def get_symbols():

    symbols = []

    with open('stocks.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        next(csvFile)
        for lines in csvFile: 
                symbols.append(lines[0])

    return symbols

def filter_data_by_date(time_series_data, start_date, end_date):
    """
    Filter the stock data based on the provided date range.
    """
    filtered = {}

    for x in time_series_data:
        if(x >= start_date and x <=  end_date):
            filtered[x] = time_series_data[x]

    return filtered

def get_chart(symbol,chart_type,time_series,start_date,end_date):
    print(symbol,chart_type,time_series,start_date,end_date)

    function = "TIME_SERIES_"

    #convert chart type
    if(time_series == '1'):
        function += "INTRADAY"
    elif(time_series == '2'):
        function += "DAILY"
    elif(time_series == '3'):
        function += "WEEKLY"
    elif(time_series == '4'):
        function += "MONTHLY"

    data = fetch_stock_data(symbol, function)
    print("Data keys from API:", list(data.keys()))

    if data is None:
        print("Failed to fetch stock data. Please try again later.")
        return
    
    print("Successfully fetched stock data.\n")

    
    #manually input the key
    
    if function == "TIME_SERIES_INTRADAY":
        time_series_key = "Time Series (60min)"
    elif function == "TIME_SERIES_DAILY":
        time_series_key = "Time Series (Daily)"
    elif function == "TIME_SERIES_WEEKLY":
        time_series_key = "Weekly Time Series"
    elif function == "TIME_SERIES_MONTHLY":
        time_series_key = "Monthly Time Series"
    else:
        print("Invalid function type.")
        return

    time_series_data = data.get(time_series_key, {})

    if not time_series_data:
        print("No stock data available for the selected time series.")
        return
    
    filtered_data = filter_data_by_date(time_series_data, start_date, end_date)

    if not filtered_data:
        print("No stock data available for the selected date range. Try a different date.")
        return
    
    labels = sorted(filtered_data.keys())
    open = [float(filtered_data[date]["1. open"]) for date in labels]
    high = [float(filtered_data[date]["2. high"]) for date in labels]
    low = [float(filtered_data[date]["3. low"]) for date in labels]
    close = [float(filtered_data[date]["4. close"]) for date in labels]

    return generate_chart(labels, open, high, low, close, chart_type, symbol, start_date,end_date)


#Create application views/routes
@app.route('/', methods=['GET'])
def index():
    symbol_list = get_symbols()

    return render_template('index.html',symbol_list=symbol_list)

@app.route('/',methods=['POST'])
def stocks_post():
    #get form data
    symbol = request.form['symbol']
    chart_type = request.form['chart_type']
    time_series = request.form['time_series']
    start_date = request.form['start_date']
    end_date = request.form['end_date']


    #validate form data
    if(symbol == ""):
        flash("Symbol is required.")
    if(chart_type == ""):
        flash("Chart type is required.")
    if(time_series == ""):
        flash("Time series is required.")
    if(start_date == ""):
        flash("Start date is required.")
    if(end_date == ""):
        flash("End date is required.")

    
    #if no errors
    #send chart to stocks page
    symbol_list = get_symbols()
    chart = get_chart(symbol,chart_type,time_series,start_date,end_date)
    # chart = get_chart()
    if(chart):
        print("Chart generated.")
    return render_template('index.html',symbol_list=symbol_list, chart=chart)


if __name__ == '__main__':
    app.run(host="0.0.0.0")