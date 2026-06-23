import pandas as pd
import numpy as np
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PerformanceAnalytics:
    """
    Computes performance metrics like Sharpe Ratio, Sortino Ratio, and Max Drawdown.
    """
    def __init__(self, risk_free_rate: float = 0.0, periods_per_year: int = 252):
        self.risk_free_rate = risk_free_rate
        self.periods_per_year = periods_per_year

    def compute_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculates performance metrics based on net strategy returns.
        """
        logger.info("Computing performance analytics...")
        
        if 'net_strategy_return' not in df.columns:
            raise ValueError("DataFrame must contain 'net_strategy_return' column.")
            
        returns = df['net_strategy_return']
        
        # Cumulative Return
        cum_return = df['cumulative_returns'].iloc[-1] - 1.0 if 'cumulative_returns' in df.columns else 0.0
        
        # Annualized Return
        total_years = len(returns) / self.periods_per_year
        ann_return = (1 + cum_return) ** (1 / total_years) - 1 if total_years > 0 else 0.0
        
        # Annualized Volatility
        ann_volatility = returns.std() * np.sqrt(self.periods_per_year)
        
        # Sharpe Ratio
        if ann_volatility > 0:
            sharpe_ratio = (ann_return - self.risk_free_rate) / ann_volatility
        else:
            sharpe_ratio = 0.0
            
        # Sortino Ratio
        downside_returns = returns[returns < 0]
        downside_deviation = downside_returns.std() * np.sqrt(self.periods_per_year)
        if downside_deviation > 0:
            sortino_ratio = (ann_return - self.risk_free_rate) / downside_deviation
        else:
            sortino_ratio = 0.0
            
        # Maximum Drawdown
        cum_returns = df['cumulative_returns']
        rolling_max = cum_returns.cummax()
        drawdown = cum_returns / rolling_max - 1.0
        max_drawdown = drawdown.min()
        
        # Calmar Ratio
        if abs(max_drawdown) > 0:
            calmar_ratio = ann_return / abs(max_drawdown)
        else:
            calmar_ratio = 0.0
            
        # Win Rate
        winning_days = len(returns[returns > 0])
        losing_days = len(returns[returns < 0])
        total_trades_days = winning_days + losing_days
        win_rate = winning_days / total_trades_days if total_trades_days > 0 else 0.0
        
        metrics = {
            "Cumulative Return": cum_return,
            "Annualized Return": ann_return,
            "Annualized Volatility": ann_volatility,
            "Sharpe Ratio": sharpe_ratio,
            "Sortino Ratio": sortino_ratio,
            "Max Drawdown": max_drawdown,
            "Calmar Ratio": calmar_ratio,
            "Win Rate": win_rate
        }
        
        return metrics

    def print_summary(self, metrics: Dict[str, Any]):
        """
        Prints a formatted summary of the performance metrics.
        """
        print("\n" + "="*40)
        print("PERFORMANCE ANALYTICS SUMMARY")
        print("="*40)
        print(f"Cumulative Return:     {metrics['Cumulative Return']:.2%}")
        print(f"Annualized Return:     {metrics['Annualized Return']:.2%}")
        print(f"Annualized Volatility: {metrics['Annualized Volatility']:.2%}")
        print("-" * 40)
        print(f"Sharpe Ratio:          {metrics['Sharpe Ratio']:.2f}")
        print(f"Sortino Ratio:         {metrics['Sortino Ratio']:.2f}")
        print(f"Calmar Ratio:          {metrics['Calmar Ratio']:.2f}")
        print("-" * 40)
        print(f"Max Drawdown:          {metrics['Max Drawdown']:.2%}")
        print(f"Win Rate:              {metrics['Win Rate']:.2%}")
        print("="*40 + "\n")
