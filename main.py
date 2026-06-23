import logging
from data.ingestor import GoldDataIngestor
from research.math_models import QuantitativeModel
from backtester.engine import VectorizedBacktester
from analytics.performance import PerformanceAnalytics
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("GoldQuantEngine")

def main():
    logger.info("Starting Gold Quantitative Engine Pipeline")

    # 1. Data Ingestion
    ingestor = GoldDataIngestor(ticker="GC=F")
    # Fetching last 10 years of data
    df_raw = ingestor.fetch_data(start_date="2014-01-01", end_date="2024-01-01", interval="1d")
    
    if df_raw is None or df_raw.empty:
        logger.error("Failed to fetch data. Exiting pipeline.")
        return

    # 2. Research & Signal Generation
    # Using default Moving Average Crossover / Bollinger Bands strategy parameters
    model = QuantitativeModel(short_window=50, long_window=200, bb_window=20, bb_std=2.0)
    df_signals = model.generate_signals(df_raw)

    # 3. Vectorized Backtesting
    # Assuming $100,000 initial capital, 0.05% transaction cost, 0.01% slippage
    backtester = VectorizedBacktester(initial_capital=100000.0, transaction_cost_pct=0.0005, slippage_pct=0.0001)
    df_backtest = backtester.run_backtest(df_signals)

    # 4. Performance Analytics
    # Assuming 2% risk-free rate for Sharpe/Sortino
    analytics = PerformanceAnalytics(risk_free_rate=0.02) 
    metrics = analytics.compute_metrics(df_backtest)
    
    # Print results
    analytics.print_summary(metrics)
    logger.info("Pipeline executed successfully.")

if __name__ == "__main__":
    main()
