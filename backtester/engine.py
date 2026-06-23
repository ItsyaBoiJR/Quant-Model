import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class VectorizedBacktester:
    """
    Vectorized execution simulator that handles transaction costs and slippage.
    """
    def __init__(self, initial_capital: float = 100000.0, transaction_cost_pct: float = 0.0005, slippage_pct: float = 0.0001):
        """
        Initializes the backtester.
        
        Args:
            initial_capital (float): Starting portfolio value.
            transaction_cost_pct (float): Transaction cost per trade as a percentage (e.g., 0.0005 = 0.05%).
            slippage_pct (float): Assumed slippage per trade as a percentage.
        """
        self.initial_capital = initial_capital
        self.transaction_cost_pct = transaction_cost_pct
        self.slippage_pct = slippage_pct

    def run_backtest(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Runs the vectorized backtest given a DataFrame with 'Close' and 'position' columns.
        Returns the DataFrame with equity curves and trade info appended.
        """
        logger.info("Running vectorized backtest execution...")
        
        if 'position' not in df.columns or 'Close' not in df.columns:
            raise ValueError("DataFrame must contain 'position' and 'Close' columns.")
            
        data = df.copy()
        
        # Calculate strategy returns (position from previous day * today's return)
        # Using simple returns for equity curve
        data['strategy_return'] = data['position'].shift(1) * (data['Close'].pct_change())
        
        # Identify trades to apply costs
        # A trade occurs when the position changes
        data['trade'] = data['position'].diff().fillna(0.0)
        
        # Calculate costs: transaction costs + slippage on the notional value traded
        cost_multiplier = self.transaction_cost_pct + self.slippage_pct
        data['costs'] = np.abs(data['trade']) * cost_multiplier
        
        # Net strategy return
        data['net_strategy_return'] = data['strategy_return'] - data['costs']
        
        # Calculate equity curve
        # Fill NaN in returns with 0 before cumulative product
        data['net_strategy_return'] = data['net_strategy_return'].fillna(0.0)
        
        # Cumulative compounding
        data['cumulative_returns'] = (1 + data['net_strategy_return']).cumprod()
        data['equity_curve'] = self.initial_capital * data['cumulative_returns']
        
        # Benchmark (Buy and Hold)
        data['benchmark_return'] = data['Close'].pct_change().fillna(0.0)
        data['benchmark_cumulative'] = (1 + data['benchmark_return']).cumprod()
        data['benchmark_equity'] = self.initial_capital * data['benchmark_cumulative']
        
        logger.info("Backtest execution completed.")
        return data
