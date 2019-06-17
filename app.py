from flask import Flask, render_template, request, redirect, url_for

import random
import pandas as pd
import requests

from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid, Range1d)
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
#from bokeh.models import TextInput, Button

# connect the app
app = Flask(__name__)

# the plotting function
def MakePlot(data):

    # set the Bokeh column data source
    source = ColumnDataSource(data)
    print(source.column_names)

    # set the tools
    TOOLS = "pan, wheel_zoom, box_zoom, reset, save"

    #p = figure(title='Pokémon',
    #    x_axis_label='Weight [kg]',
    #    y_axis_label='Height [m]',
    #    title_location='above',
    #    toolbar_location='right',
    #    tools=[hover], **PLOT_OPTS)

    # initialize the canvas for plotting
    p1 = figure(x_axis_type="datetime", title="Stock Prices 2016", tools=[TOOLS])
    p1.grid.grid_line_alpha = 0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'
    #p = figure(tools=[hover], **PLOT_OPTS)

    ticker = str(data['ticker'].unique())
    print(ticker)

    if('open' in data.columns): 
    	p1.line(data['date'], data['open'], color='#A6CEE3', legend=ticker+': open')
    if('close' in data.columns): 
    	p1.line(data['date'], data['close'], color='#B2DF8A', legend=ticker+': close')
    if('adj_open' in data.columns): 
    	p1.line(data['date'], data['adj_open'], color='#33A02C', legend=ticker+': adj_open')
    if('adj_close' in data.columns): 
    	p1.line(data['date'], data['adj_close'], color='#FB9A99', legend=ticker+': adj_close')
    
    p1.legend.location = 'top_left'

    # return the finalized plot
    return p1



# the homepage
@app.route('/', methods=['POST', 'GET'])
def homepage():

    # this block is only executed once the form is submitted
    if request.method == 'POST':

    	# load the dataset
		data = pd.read_csv('data/pokemon_complete.csv')
        print(data)



        # make the plot and extract its components for html rendering
        p = MakePlot(data)
        script, div = components(p)
        #print(script)
        #print(div)

        # render the html page with the plot embedded
        return render_template("chart.html", the_div=div, the_script=script)

    else:

        return render_template('login.html', ticker_symbol=ticker_symbol)









#if __name__ == "__main__":
#    app.run(debug=True)

if __name__ == '__main__':
 	app.run(port=33507)

