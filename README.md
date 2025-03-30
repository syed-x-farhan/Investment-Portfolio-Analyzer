# Investment Portfolio Analyzer

## Overview
The **Investment Portfolio Analyzer** is a Streamlit-based web application that provides users with an interactive and visual way to analyze their investment portfolio. It allows users to track their assets, view performance metrics, and visualize portfolio allocation with interactive charts.

## Features
- 📊 **Portfolio Analysis:** View key financial metrics like total value, gain/loss percentage, and diversification score.
- 📈 **Asset Performance Tracking:** Monitor individual asset performance with bar charts.
- 🎯 **Risk vs Return Analysis:** Analyze the relationship between risk and return.
- 🔍 **Historical Data Visualization:** Fetch and display historical price trends using Yahoo Finance.
- 🏗 **Custom Investment Data:** Users can upload or input their own investment data for analysis.

## Installation
To run this project, ensure you have **Python 3.8+** installed. Follow these steps:

### 1. Clone the repository
```sh
 git clone <repository-url>
 cd investment-portfolio-analyzer
```

### 2. Install Dependencies
Install the required packages using the provided `requirements.txt` file:
```sh
pip install -r requirements.txt
```

### 3. Run the Application
Launch the Streamlit app by running:
```sh
streamlit run invest.py
```

## Dependencies
The project requires the following Python libraries, listed in `requirements.txt`:
- `streamlit`
- `pandas`
- `numpy`
- `plotly`
- `yfinance`

## Usage
1. **Start the app:** Run the `invest.py` script with Streamlit.
2. **Analyze Portfolio:** View performance metrics, charts, and asset allocation.
3. **Customize Data:** Upload your own investment details or use sample data.
4. **Explore Insights:** Use interactive graphs to make informed investment decisions.

## File Structure
```
├── invest.py             # Main Streamlit application
├── requirements.txt      # List of dependencies
└── README.md             # Documentation
```

## License
This project is licensed under the MIT License.

## Author
Developed by [Your Name]
