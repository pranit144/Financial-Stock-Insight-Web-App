
# Financial Stock Insight Web App

## Overview

The **Financial Stock Insight Web App** is a Flask-based application designed to provide users with comprehensive and detailed financial analysis of popular global and Indian stocks. It combines real-time stock data fetched from Yahoo Finance with AI-powered financial research using the PHI framework and the Groq large language model.

Users can explore historical stock price trends, key financial metrics, analyst recommendations, recent news, and potential risks and opportunities — all presented in a clean, intuitive web interface.

---

## Features

- **Stock Selection by Sector:** Browse and select from a curated list of popular stocks grouped by industry sector, including Technology, Financial Services, Healthcare, Energy, Consumer Cyclical, and more.
- **Detailed Stock Analysis:** Get AI-generated in-depth insights covering stock performance, financial ratios, analyst recommendations (Buy/Hold/Sell), recent news summaries with links, and potential risks or opportunities.
- **Historical Trend Visualization:** Interactive charts showing stock closing prices and trading volumes over the last 5 months.
- **Comparison Tool:** Compare multiple stocks side-by-side with historical data visualizations.
- **User-Friendly Interface:** Responsive and easy to navigate pages for home, analysis, comparison, and about sections.

---

## Technologies Used

- **Backend:**
  - Python 3.x
  - Flask (Web Framework)
  - yfinance (Yahoo Finance API for stock data)
  - PHI Agent with Groq model (AI-based financial insights)
  - Pandas (Data processing)

- **Frontend:**
  - Jinja2 (Template rendering)
  - JavaScript (for interactive charts and UI)

---

## Installation and Setup

### Prerequisites

- Python 3.7 or above installed on your system
- Internet connection for fetching stock data and AI analysis

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/financial-stock-insight.git
   cd financial-stock-insight
   ```

2. **(Optional) Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. **Install required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application:**

   ```bash
   python app.py
   ```

5. **Access the app in your web browser:**

   ```
   http://127.0.0.1:5001
   ```
6. ** Download the  zip  for the  frontend  of the  page :**
   ```
   https://drive.google.com/file/d/17lKsp-PavXpO9A2YH-gFAebuCZfFA9Ot/view?usp=sharing
   ```
---

## Usage Instructions

- **Home Page:** Select a stock by sector or use the search box to enter a ticker symbol.
- **Stock Analysis:** After selection, view detailed AI-generated financial insights, key metrics, and recent trends.
- **Compare Stocks:** Use the comparison page to analyze multiple stocks simultaneously.
- **About:** Learn more about the purpose and functionality of the app.

---

## Project Structure

```
financial-stock-insight/
│
├── app.py                 # Main Flask app code
├── templates/             # HTML templates for rendering pages
│   ├── home.html
│   ├── analysis.html
│   ├── compare.html
│   └── about.html
├── static/                # Static files: CSS, JS, images
├── requirements.txt       # Python dependencies list
└── README.md              # This documentation file
```

---

## Dependencies

Below are the key Python packages used in this project (also listed in `requirements.txt`):

- Flask
- yfinance
- pandas
- phi (PHI framework and related packages)
- datetime (standard library)
- json (standard library)

*Note:* Ensure you have access to the PHI framework and the Groq model. Installation instructions for PHI can be found in their official documentation.

---

## Contribution

Contributions, issues, and feature requests are welcome! Feel free to:

- Fork the repository
- Create your feature branch (`git checkout -b feature-name`)
- Commit your changes (`git commit -m 'Add new feature'`)
- Push to the branch (`git push origin feature-name`)
- Open a Pull Request

Please ensure your code follows best practices and includes proper documentation/comments.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Yahoo Finance for providing stock data via `yfinance`
- The PHI AI framework and Groq LLM for enabling advanced financial insights
- Flask community for the web framework
- OpenAI for inspiration and support

---

## Contact

For questions or support, please contact:

- Your Name / Your Email
- GitHub: [yourusername](https://github.com/yourusername)

---

**Enjoy exploring stocks with AI-powered insights! 📈🚀**
