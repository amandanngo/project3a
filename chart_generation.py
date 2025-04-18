import pygal


##Generate a graph and open in the user’s default browser.
## bar graph
def generate_chart(labels,open,high,low,close, chart_type, symbol, start_date, end_date):
    
    if chart_type == '1':
        bar_chart = pygal.Bar(x_label_rotation=20, height=500)
        bar_chart.title = f"Stock Data for {symbol}: {start_date} to {end_date} "
        bar_chart.x_labels = labels
        bar_chart.add("Open", open)
        bar_chart.add("High", high)
        bar_chart.add("Low", low)
        bar_chart.add("Close", close)
        return bar_chart.render_data_uri()
    
    if chart_type == '2':
        line_chart = pygal.Line(x_label_rotation=20, height=500)
        line_chart.title = f"Stock Data for {symbol}: {start_date} to {end_date} "
        line_chart.x_labels = labels
        line_chart.add("Open", open)
        line_chart.add("High", high)
        line_chart.add("Low", low)
        line_chart.add("Close", close)
        return line_chart.render_data_uri()






