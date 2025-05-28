from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from datetime import datetime, timedelta
import pandas as pd
import json

app = Flask(__name__)

# Create the PHI financial research agent
phi_agent = Agent(
    name="Financial Stock Insight Agent",
    model=Groq(id="llama3-70b-8192"),
    tools=[
        DuckDuckGo(),
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True
        )
    ],
    instructions=[
        "You are a highly skilled financial research assistant.",
        "Provide detailed analysis with insights on the stock performance.",
        "Summarize analyst recommendations (Buy/Hold/Sell).",
        "Include recent news articles with links and brief descriptions.",
        "Mention potential risks and opportunities based on news and trends.",
        "Use markdown formatting for clarity and structure.",
    ],
    show_tool_calls=False,
    markdown=True,
)

# List of popular stocks with name and ticker
POPULAR_STOCKS = [
    {"name": "Apple Inc.", "ticker": "AAPL", "sector": "Technology"},
    {"name": "Microsoft Corporation", "ticker": "MSFT", "sector": "Technology"},
    {"name": "Amazon.com Inc.", "ticker": "AMZN", "sector": "Consumer Cyclical"},
    {"name": "Alphabet Inc. (Google)", "ticker": "GOOGL", "sector": "Communication Services"},
    {"name": "Tesla, Inc.", "ticker": "TSLA", "sector": "Automotive"},
    {"name": "Meta Platforms, Inc.", "ticker": "META", "sector": "Technology"},
    {"name": "NVIDIA Corporation", "ticker": "NVDA", "sector": "Technology"},
    {"name": "Berkshire Hathaway Inc.", "ticker": "BRK-B", "sector": "Financial Services"},
    {"name": "JPMorgan Chase & Co.", "ticker": "JPM", "sector": "Financial Services"},
    {"name": "Johnson & Johnson", "ticker": "JNJ", "sector": "Healthcare"},
    {"name": "Walmart Inc.", "ticker": "WMT", "sector": "Consumer Defensive"},
    {"name": "Visa Inc.", "ticker": "V", "sector": "Financial Services"},
    {"name": "Procter & Gamble Co.", "ticker": "PG", "sector": "Consumer Defensive"},
    {"name": "UnitedHealth Group Inc.", "ticker": "UNH", "sector": "Healthcare"},
    {"name": "Home Depot Inc.", "ticker": "HD", "sector": "Consumer Cyclical"},
    {"name": "Mastercard Inc.", "ticker": "MA", "sector": "Financial Services"},
    {"name": "Bank of America Corp.", "ticker": "BAC", "sector": "Financial Services"},
    {"name": "Exxon Mobil Corp.", "ticker": "XOM", "sector": "Energy"},
    {"name": "Walt Disney Co.", "ticker": "DIS", "sector": "Communication Services"},
    {"name": "Netflix Inc.", "ticker": "NFLX", "sector": "Communication Services"},
    # Indian stocks
    {"name": "Reliance Industries Ltd.", "ticker": "RELIANCE.NS", "sector": "Energy"},
    {"name": "Tata Consultancy Services Ltd.", "ticker": "TCS.NS", "sector": "Technology"},
    {"name": "HDFC Bank Ltd.", "ticker": "HDFCBANK.NS", "sector": "Financial Services"},
    {"name": "Infosys Ltd.", "ticker": "INFY.NS", "sector": "Technology"},
    {"name": "ICICI Bank Ltd.", "ticker": "ICICIBANK.NS", "sector": "Financial Services"}
]


# Group stocks by sector
def get_stocks_by_sector():
    stocks_by_sector = {}
    for stock in POPULAR_STOCKS:
        sector = stock["sector"]
        if sector not in stocks_by_sector:
            stocks_by_sector[sector] = []
        stocks_by_sector[sector].append(stock)
    return stocks_by_sector


def format_ticker(ticker):
    """Format ticker symbols correctly for different markets"""
    # For Indian stocks, add .NS or .BO suffix if not already present
    if "HDFC" in ticker or "RELIANCE" in ticker or "TCS" in ticker:
        if not (ticker.endswith(".NS") or ticker.endswith(".BO")):
            return f"{ticker}.NS"  # National Stock Exchange of India
    return ticker


def get_stock_trend_data(ticker):
    try:
        # Format ticker appropriately
        formatted_ticker = format_ticker(ticker)

        # Calculate date 5 months ago
        end_date = datetime.now()
        start_date = end_date - timedelta(days=150)

        # Get historical data
        stock = yf.Ticker(formatted_ticker)
        hist = stock.history(start=start_date, end=end_date)

        # Check if we got valid data
        if hist.empty:
            print(f"No historical data found for {formatted_ticker}")
            return None

        # Convert to dictionary for JSON serialization
        dates = hist.index.strftime('%Y-%m-%d').tolist()
        close_prices = hist['Close'].tolist()
        volumes = hist['Volume'].tolist()

        # Initialize metrics with default values
        metrics = {
            'high_52week': 'N/A',
            'low_52week': 'N/A',
            'avg_volume': 'N/A',
            'market_cap': 'N/A',
            'pe_ratio': 'N/A',
            'dividend_yield': 'N/A'
        }

        # Try to get additional metrics
        try:
            info = stock.info
            if info:
                if 'fiftyTwoWeekHigh' in info:
                    metrics['high_52week'] = f"${info['fiftyTwoWeekHigh']:.2f}"

                if 'fiftyTwoWeekLow' in info:
                    metrics['low_52week'] = f"${info['fiftyTwoWeekLow']:.2f}"

                if 'averageVolume' in info:
                    avg_vol = info['averageVolume']
                    if avg_vol > 1000000:
                        metrics['avg_volume'] = f"{avg_vol / 1000000:.2f}M"
                    else:
                        metrics['avg_volume'] = f"{avg_vol / 1000:.2f}K"

                if 'marketCap' in info:
                    market_cap = info['marketCap']
                    if market_cap > 1000000000:
                        metrics['market_cap'] = f"${market_cap / 1000000000:.2f}B"
                    else:
                        metrics['market_cap'] = f"${market_cap / 1000000:.2f}M"

                if 'trailingPE' in info:
                    metrics['pe_ratio'] = f"{info['trailingPE']:.2f}"

                if 'dividendYield' in info and info['dividendYield'] is not None:
                    metrics['dividend_yield'] = f"{info['dividendYield'] * 100:.2f}%"
        except Exception as e:
            print(f"Error getting additional metrics: {e}")
            # Continue with default values if there's an error

        return {
            'dates': dates,
            'prices': close_prices,
            'volumes': volumes,
            'metrics': metrics
        }
    except Exception as e:
        print(f"Error fetching trend data: {e}")
        return None


@app.route('/', methods=['GET'])
def home():
    """Display the home page with stock selection options"""
    stocks_by_sector = get_stocks_by_sector()
    return render_template('home.html', stocks_by_sector=stocks_by_sector)


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Analyze a specific stock"""
    result = None
    stock_symbol = ""
    trend_data = None
    error_message = None

    if request.method == 'POST':
        stock_symbol = request.form['stock'].upper().strip()
    elif request.method == 'GET' and 'ticker' in request.args:
        stock_symbol = request.args.get('ticker').upper().strip()

    if stock_symbol:
        # Get trend data for charts
        trend_data = get_stock_trend_data(stock_symbol)

        if trend_data:
            # Only run the agent if we have valid trend data
            try:
                prompt = f"Provide comprehensive financial analysis for {stock_symbol}. Include performance metrics, analyst recommendations, key financial ratios explanation, and latest news with their potential impact on the stock price."
                result = phi_agent.run(prompt).content
            except Exception as e:
                print(f"Error running agent: {e}")
                error_message = f"Could not generate analysis for {stock_symbol}. Please try another ticker."
        else:
            error_message = f"Could not retrieve trend data for {stock_symbol}. Please verify the ticker symbol and try again."

    # Get stock name if it exists in our list
    stock_name = None
    for stock in POPULAR_STOCKS:
        if stock["ticker"] == stock_symbol:
            stock_name = stock["name"]
            break

    # Get current date and time for the "Last Updated" field
    now = datetime.now().strftime("%B %d, %Y %H:%M")

    return render_template('analysis.html',
                           result=result,
                           stock=stock_symbol,
                           stock_name=stock_name,
                           trend_data=json.dumps(trend_data) if trend_data else None,
                           error_message=error_message,
                           now=now)


@app.route('/compare', methods=['GET'])
def compare():
    """Compare multiple stocks"""
    # Get stocks to compare from query parameters
    tickers = request.args.getlist('tickers')
    if not tickers:
        # Default to comparing some tech stocks
        tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']

    # Get data for each stock
    comparison_data = {}
    for ticker in tickers:
        trend_data = get_stock_trend_data(ticker)
        if trend_data:
            comparison_data[ticker] = trend_data

    return render_template('compare.html',
                           comparison_data=json.dumps(comparison_data),
                           tickers=tickers,
                           all_stocks=POPULAR_STOCKS)


@app.route('/about')
def about():
    """About page with information about the application"""
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True,port=5001)