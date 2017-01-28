from django.shortcuts import render
from django.http import HttpResponse
import requests
import simplejson as json
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components


def bokeh(request):
    return render(request, 'nces/index.html')

def graph(request):
    form_dict = {}
    if request.method == 'POST':
        # Extract form info and handle errors
        ticker = request.POST['ticker']
        if not ticker:
            return HttpResponse('<h1>Please go back and enter a stock ticker</h1>')
        features = request.POST.getlist('features')
        if not features:
            return HttpResponse('<h1>Please go back and select some features to show</h1>')

        # Call the Quandl API
        api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json?api_key=bhDkb5WTxo-gXcFN5mgq' % ticker
        response = requests.get(api_url)
        json_response = json.loads(response.content)

        # Put the data in a Pandas dataframe
        data = pd.DataFrame(json_response['data'], columns=json_response['column_names'])
        data['Date'] = pd.to_datetime(data['Date'])

        # Send the data to the Bokeh plot
        p = figure(x_axis_type="datetime", width=800, height=600)
        line_color = ['red', 'green', 'blue', 'brown']
        for index, feature in enumerate(features):
            p.line(data['Date'], data[feature], legend=feature, line_color=line_color[index])
        script, div = components(p)
        form_dict['script'] = script
        form_dict['div'] = div
        form_dict['company'] = ticker.upper()

        return render(request, 'nces/graph.html', context = form_dict)