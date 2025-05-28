from flask import Flask, render_template, request
import requests
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

# Replace with your own MarketStack access key
ACCESS_KEY = 'f026a623399236149938c9e08191527b'

@app.route('/', methods=['GET', 'POST'])
def index():
    chart_html = None
    if request.method == 'POST':
        symbol = request.form['symbol']
        date_from = request.form['date_from']
        date_to = request.form['date_to']

        url = 'http://api.marketstack.com/v2/eod'
        params = {
            'access_key': ACCESS_KEY,
            'symbols': symbol,
            'date_from': date_from,
            'date_to': date_to
        }

        response = requests.get(url, params=params)
        data = response.json()

        if 'data' in data and len(data['data']) > 0:
            eod_data = sorted(data['data'], key=lambda x: x['date'])  # sort by date
            dates = [entry['date'][:10] for entry in eod_data]
            opens = [entry['open'] for entry in eod_data]
            highs = [entry['high'] for entry in eod_data]
            lows = [entry['low'] for entry in eod_data]
            closes = [entry['close'] for entry in eod_data]

            fig = go.Figure(data=[go.Candlestick(
                x=dates,
                open=opens,
                high=highs,
                low=lows,
                close=closes
            )])

            fig.update_layout(title=f'{symbol} Candlestick Chart',
                              xaxis_title='Date',
                              yaxis_title='Price',
                              xaxis_rangeslider_visible=False)

            chart_html = pio.to_html(fig, full_html=False)

    return render_template('index1.html', chart=chart_html)

if __name__ == '__main__':
    app.run(debug=True)
