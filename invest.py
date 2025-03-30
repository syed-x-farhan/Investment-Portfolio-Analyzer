import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf

# Set page configuration
st.set_page_config(
    page_title="Investment Portfolio Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 2rem;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin-top: 3rem;
        margin-bottom: 2rem;
    }
    .card {
        border-radius: 10px;
        padding: 2rem;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        text-align: center;
        transition: transform 0.2s;
        height: 100%;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .metric-label {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
        margin-top: 0.5rem;
        line-height: 1.2;
    }
    .gain {
        color: #4CAF50;
    }
    .loss {
        color: #F44336;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: background-color 0.2s;
        width: 100%;
        margin: 0.5rem 0;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
    .main-content {
        padding: 2rem;
    }
    .section-divider {
        height: 2px;
        background-color: #e0e0e0;
        margin: 3rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E88E5;
        color: white;
    }
    .metrics-container {
        margin-bottom: 3rem;
    }
    .chart-container {
        margin-bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def calculate_portfolio_metrics(df):
    """Calculate key portfolio metrics"""
    total_value = df['Current Value'].sum()
    total_cost = df['Cost Basis'].sum()
    total_gain_loss = total_value - total_cost
    total_gain_loss_pct = (total_gain_loss / total_cost) * 100 if total_cost > 0 else 0
    
    # Calculate weighted return
    df['Weight'] = df['Current Value'] / total_value
    weighted_return = (df['Weight'] * df['Return %']).sum()
    
    # Calculate volatility (standard deviation of returns)
    volatility = df['Return %'].std()
    
    # Calculate diversification score (simple version: 100 - highest allocation %)
    category_allocation = df.groupby('Category')['Weight'].sum() * 100
    max_allocation = category_allocation.max() if len(category_allocation) > 0 else 100
    diversification_score = 100 - max_allocation
    
    return {
        'total_value': total_value,
        'total_cost': total_cost,
        'total_gain_loss': total_gain_loss,
        'total_gain_loss_pct': total_gain_loss_pct,
        'weighted_return': weighted_return,
        'volatility': volatility,
        'diversification_score': diversification_score,
        'category_allocation': category_allocation
    }

def get_historical_data(ticker, period="1y"):
    """Get historical price data for a ticker"""
    try:
        data = yf.Ticker(ticker).history(period=period)
        return data['Close']
    except:
        return pd.Series()

def create_sample_data():
    """Create sample portfolio data"""
    return pd.DataFrame({
        'Asset': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'VTI', 'AGG', 'BTC-USD', 'ETH-USD', 'Real Estate'],
        'Category': ['Stocks', 'Stocks', 'Stocks', 'Stocks', 'Stocks', 'ETFs', 'Bonds', 'Crypto', 'Crypto', 'Real Estate'],
        'Quantity': [10, 5, 2, 3, 8, 15, 20, 0.5, 2, 1],
        'Purchase Price': [150, 300, 2800, 3300, 800, 220, 100, 35000, 2500, 200000],
        'Current Price': [180, 350, 2900, 3400, 750, 240, 102, 40000, 3000, 210000],
    })

def process_data(df):
    """Process the dataframe to add calculated columns"""
    df['Cost Basis'] = df['Quantity'] * df['Purchase Price']
    df['Current Value'] = df['Quantity'] * df['Current Price']
    df['Gain/Loss'] = df['Current Value'] - df['Cost Basis']
    df['Return %'] = (df['Gain/Loss'] / df['Cost Basis']) * 100
    return df

def create_allocation_chart(df, metrics):
    """Create asset allocation pie chart"""
    fig = px.pie(
        df, 
        values='Current Value', 
        names='Category',
        title='Portfolio Allocation by Asset Category',
        color_discrete_sequence=px.colors.qualitative.Plotly,
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(t=50, l=20, r=20, b=20),
        height=400
    )
    return fig

def create_asset_performance_chart(df):
    """Create asset performance bar chart"""
    df_sorted = df.sort_values('Return %')
    colors = ['#F44336' if x < 0 else '#4CAF50' for x in df_sorted['Return %']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_sorted['Asset'],
        y=df_sorted['Return %'],
        marker_color=colors
    ))
    fig.update_layout(
        title='Individual Asset Performance',
        xaxis_title='Asset',
        yaxis_title='Return (%)',
        height=400,
        margin=dict(t=50, l=20, r=20, b=50)
    )
    return fig

def create_risk_return_chart(df):
    """Create risk vs return scatter plot"""
    # For demonstration, we'll use standard deviation of each asset as a risk proxy
    # In a real app, this would be calculated from historical data
    
    # Create sample risk data (in a real app, calculate this from historical returns)
    risk_values = np.abs(df['Return %'] / 10) + np.random.uniform(1, 5, size=len(df))
    
    fig = px.scatter(
        x=risk_values,
        y=df['Return %'],
        text=df['Asset'],
        size=df['Current Value'],
        color=df['Category'],
        title='Risk vs. Return Analysis',
        labels={'x': 'Risk (Volatility)', 'y': 'Return (%)'},
        height=500
    )
    fig.update_traces(textposition='top center', marker=dict(sizemin=10))
    fig.update_layout(margin=dict(t=50, l=20, r=20, b=20))
    return fig

def create_historical_chart(selected_assets, portfolio_df, period="1y"):
    """Create historical price chart for selected assets"""
    end_date = datetime.now()
    
    fig = go.Figure()
    valid_assets = []
    
    for asset in selected_assets:
        # Check if the asset is likely a tradable security (not real estate, etc.)
        if asset in portfolio_df['Asset'].values and "-" in asset or asset.isupper():
            historical_data = get_historical_data(asset, period)
            if not historical_data.empty:
                # Normalize to percentage change from start
                normalized_data = (historical_data / historical_data.iloc[0] - 1) * 100
                fig.add_trace(go.Scatter(
                    x=normalized_data.index,
                    y=normalized_data.values,
                    mode='lines',
                    name=asset
                ))
                valid_assets.append(asset)
    
    if not valid_assets:
        return None
    
    fig.update_layout(
        title=f'Historical Performance Comparison ({period})',
        xaxis_title='Date',
        yaxis_title='Price Change (%)',
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        height=500,
        margin=dict(t=50, l=20, r=20, b=50)
    )
    return fig

def format_currency(value):
    """Format value as currency"""
    return f"${value:,.2f}"

def format_percent(value):
    """Format value as percentage"""
    return f"{value:.2f}%"

# Main App
def main():
    # Initialize session state variables
    if 'portfolio_data' not in st.session_state:
        st.session_state.portfolio_data = process_data(create_sample_data())
    if 'show_sample_data' not in st.session_state:
        st.session_state.show_sample_data = True
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Portfolio Analysis"
    
    # Header
    st.markdown('<div class="main-header">📊 Investment Portfolio Analyzer</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        Analyze your investment portfolio with advanced metrics and visualizations.
        Upload your data or add investments manually to get started.
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["📈 Portfolio Analysis", "➕ Add Investments", "📊 Advanced Analytics"])
    
    with tab1:
        if st.session_state.portfolio_data is not None and not st.session_state.portfolio_data.empty:
            portfolio_df = st.session_state.portfolio_data
            metrics = calculate_portfolio_metrics(portfolio_df)
            
            # Portfolio Overview Section
            st.markdown('<div class="sub-header">Portfolio Overview</div>', unsafe_allow_html=True)
            
            # Filter options
            category_filter = st.multiselect(
                "Filter by Asset Category:",
                options=sorted(portfolio_df['Category'].unique()),
                default=sorted(portfolio_df['Category'].unique())
            )
            
            filtered_df = portfolio_df[portfolio_df['Category'].isin(category_filter)]
            if filtered_df.empty:
                st.warning("No data available with the selected filters. Please adjust your selection.")
                return
            
            filtered_metrics = calculate_portfolio_metrics(filtered_df)
            
            # Key Metrics in Cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f'''
                <div class="card">
                    <div class="metric-label">Total Portfolio Value</div>
                    <div class="metric-value">{format_currency(filtered_metrics["total_value"])}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                gain_loss_class = "gain" if filtered_metrics["total_gain_loss"] >= 0 else "loss"
                st.markdown(f'''
                <div class="card">
                    <div class="metric-label">Total Gain/Loss</div>
                    <div class="metric-value {gain_loss_class}">{format_currency(filtered_metrics["total_gain_loss"])}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col3:
                gain_loss_pct_class = "gain" if filtered_metrics["total_gain_loss_pct"] >= 0 else "loss"
                st.markdown(f'''
                <div class="card">
                    <div class="metric-label">Total Return</div>
                    <div class="metric-value {gain_loss_pct_class}">{format_percent(filtered_metrics["total_gain_loss_pct"])}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col4:
                st.markdown(f'''
                <div class="card">
                    <div class="metric-label">Weighted Return</div>
                    <div class="metric-value">{format_percent(filtered_metrics["weighted_return"])}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Risk Metrics in Cards
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'''
                <div class="card">
                    <div class="metric-label">Portfolio Volatility</div>
                    <div class="metric-value">{format_percent(filtered_metrics["volatility"])}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'''
                <div class="card">
                    <div class="metric-label">Diversification Score</div>
                    <div class="metric-value">{format_percent(filtered_metrics["diversification_score"])}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Portfolio Allocation Chart
            st.markdown('<div class="sub-header">Portfolio Allocation</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            allocation_chart = create_allocation_chart(filtered_df, filtered_metrics)
            st.plotly_chart(allocation_chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Asset Performance Chart
            st.markdown('<div class="sub-header">Asset Performance</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            performance_chart = create_asset_performance_chart(filtered_df)
            st.plotly_chart(performance_chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Portfolio Table
            st.markdown('<div class="sub-header">Portfolio Details</div>', unsafe_allow_html=True)
            st.dataframe(
                filtered_df[[
                    'Asset', 'Category', 'Quantity', 'Purchase Price', 'Current Price', 
                    'Cost Basis', 'Current Value', 'Gain/Loss', 'Return %'
                ]].sort_values('Current Value', ascending=False),
                use_container_width=True,
                hide_index=True
            )
            
            # Sample data notice
            if st.session_state.show_sample_data:
                st.info("**Note:** You're currently viewing sample data. Add your own investments or upload a CSV file to analyze your portfolio.")
        else:
            st.info("No portfolio data available. Please add investments or upload a portfolio file.")
    
    with tab2:
        st.markdown('<div class="sub-header">Add Your Investment Data</div>', unsafe_allow_html=True)
        
        input_method = st.radio("Choose input method:", ["Manual Entry", "CSV Upload", "Use Sample Data"])
        
        if input_method == "Manual Entry":
            st.markdown("### Add Individual Investment")
            
            # Form for manual entry
            with st.form("add_investment_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    asset = st.text_input("Asset Name/Ticker")
                    category = st.selectbox(
                        "Asset Category",
                        ["Stocks", "ETFs", "Bonds", "Crypto", "Real Estate", "Commodities", "Cash", "Other"]
                    )
                    quantity = st.number_input("Quantity", min_value=0.0, step=0.01)
                
                with col2:
                    purchase_price = st.number_input("Purchase Price ($)", min_value=0.0, step=0.01)
                    current_price = st.number_input("Current Price ($)", min_value=0.0, step=0.01)
                
                submit_button = st.form_submit_button("Add Investment")
                
                if submit_button:
                    if not asset or quantity <= 0 or purchase_price <= 0 or current_price <= 0:
                        st.error("Please fill all fields with valid values")
                    else:
                        new_investment = pd.DataFrame({
                            'Asset': [asset],
                            'Category': [category],
                            'Quantity': [quantity],
                            'Purchase Price': [purchase_price],
                            'Current Price': [current_price]
                        })
                        
                        new_investment = process_data(new_investment)
                        
                        if st.session_state.portfolio_data is not None and not st.session_state.portfolio_data.empty:
                            st.session_state.portfolio_data = pd.concat([st.session_state.portfolio_data, new_investment], ignore_index=True)
                        else:
                            st.session_state.portfolio_data = new_investment
                        
                        st.success(f"Added {asset} to your portfolio!")
                        st.session_state.show_sample_data = False
            
            # Clear portfolio button
            if st.button("Clear Portfolio"):
                st.session_state.portfolio_data = pd.DataFrame()
                st.success("Portfolio cleared!")
        
        elif input_method == "CSV Upload":
            st.markdown("### Upload Portfolio CSV File")
            st.markdown("""
            Upload a CSV file with your portfolio data. The file should have the following columns:
            - Asset (name/ticker)
            - Category (asset type)
            - Quantity
            - Purchase Price
            - Current Price
            """)
            
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    required_columns = ['Asset', 'Category', 'Quantity', 'Purchase Price', 'Current Price']
                    
                    # Check if all required columns exist
                    if all(col in df.columns for col in required_columns):
                        df = process_data(df)
                        st.session_state.portfolio_data = df
                        st.success("Portfolio data loaded successfully!")
                        st.session_state.show_sample_data = False
                    else:
                        missing_cols = [col for col in required_columns if col not in df.columns]
                        st.error(f"The CSV file is missing the following required columns: {', '.join(missing_cols)}")
                except Exception as e:
                    st.error(f"Error loading CSV file: {str(e)}")
            
            # Download sample CSV template
            sample_df = pd.DataFrame({
                'Asset': ['AAPL', 'VTI'],
                'Category': ['Stocks', 'ETFs'],
                'Quantity': [10, 5],
                'Purchase Price': [150, 200],
                'Current Price': [180, 220]
            })
            
            csv = sample_df.to_csv(index=False)
            st.download_button(
                label="Download Sample CSV Template",
                data=csv,
                file_name="portfolio_template.csv",
                mime="text/csv"
            )
        
        elif input_method == "Use Sample Data":
            if st.button("Load Sample Portfolio Data"):
                st.session_state.portfolio_data = process_data(create_sample_data())
                st.session_state.show_sample_data = True
                st.success("Sample portfolio data loaded!")
    
    with tab3:
        if st.session_state.portfolio_data is not None and not st.session_state.portfolio_data.empty:
            st.markdown('<div class="sub-header">Advanced Portfolio Analytics</div>', unsafe_allow_html=True)
            
            # Risk vs Return Chart
            st.markdown("### Risk vs. Return Analysis")
            risk_return_chart = create_risk_return_chart(st.session_state.portfolio_data)
            st.plotly_chart(risk_return_chart, use_container_width=True)
            
            # Historical Performance Chart
            st.markdown("### Historical Performance")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                selected_assets = st.multiselect(
                    "Select assets to compare:",
                    options=sorted(st.session_state.portfolio_data['Asset'].tolist()),
                    default=sorted(st.session_state.portfolio_data['Asset'].tolist())[:3]
                )
            
            with col2:
                time_period = st.selectbox(
                    "Time period:",
                    options=["1m", "3m", "6m", "1y", "2y", "5y"],
                    index=3
                )
            
            if selected_assets:
                historical_chart = create_historical_chart(selected_assets, st.session_state.portfolio_data, time_period)
                if historical_chart:
                    st.plotly_chart(historical_chart, use_container_width=True)
                else:
                    st.info("Historical data not available for the selected assets. Try selecting publicly traded securities.")
            else:
                st.info("Please select at least one asset to view historical performance.")
        else:
            st.info("No portfolio data available. Please add investments or upload a portfolio file to access advanced analytics.")

if __name__ == "__main__":
    main()