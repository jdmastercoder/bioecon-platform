import numpy as np
import yfinance as yf


def run_monte_carlo_live(ticker_symbol="SPY", years_back=2, future_years=5, simulations=500):
    """
    Pulls live historical stock data to calculate real mean return and volatility,
    then runs Monte Carlo simulations for future risk.
    """
    try:
        # Fetch live data from Yahoo Finance
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period=f"{years_back}y")

        if df.empty:
            return None, "Ticker not found"

        # Calculate daily percentage returns
        daily_returns = df['Close'].pct_change().dropna()

        # Convert daily metrics to annualized metrics
        mean_return = daily_returns.mean() * 252
        volatility = daily_returns.std() * np.sqrt(252)
        current_price = df['Close'].iloc[-1]

        # Run Monte Carlo simulation grid
        trading_days = int(future_years * 252)
        daily_sim_returns = np.random.normal(
            mean_return / 252, volatility / np.sqrt(252), (trading_days, simulations))

        # Calculate asset trajectories starting from the latest real market price
        price_paths = current_price * np.cumprod(1 + daily_sim_returns, axis=0)

        return price_paths, {
            "current_price": round(current_price, 2),
            "annual_return": round(mean_return * 100, 2),
            "volatility": round(volatility * 100, 2)
        }
    except Exception as e:
        return None, str(e)
