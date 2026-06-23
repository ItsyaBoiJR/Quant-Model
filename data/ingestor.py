import yfinance as yf
import pandas as pd
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class GoldDataIngestor:
    """
    Fetches and preprocesses historical XAUUSD data from Yahoo Finance.
    """
    def __init__(self, ticker: str = "GC=F"):
        """
        Initialize the ingestor with a specific ticker. GC=F is Gold Futures on Yahoo Finance.
        """
        self.ticker = ticker
        
    def fetch_data(self, start_date: str, end_date: str, interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        Fetches historical price data.
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.
            interval (str): Data interval (e.g., '1d', '1wk', '1mo', '1h').
            
        Returns:
            pd.DataFrame: DataFrame containing Open, High, Low, Close, Volume.
        """
        logger.info(f"Fetching {self.ticker} data from {start_date} to {end_date} with interval {interval}")
        try:
            # Setting progress=False avoids stdout spam during backtesting
            data = yf.download(self.ticker, start=start_date, end=end_date, interval=interval, progress=False)
            
            if data.empty:
                logger.warning(f"No data returned for {self.ticker} in the specified date range.")
                return None
                
            # yfinance>=0.2.30 returns a MultiIndex for columns if there are multiple tickers or fields. 
            # If it's a single ticker, it might still return MultiIndex depending on the exact call.
            # We flatten it to standard OHLCV if needed.
            if isinstance(data.columns, pd.MultiIndex):
                # Usually level 0 is Price (Open, High, Low, Close, Adj Close, Volume) and level 1 is Ticker
                data.columns = data.columns.droplevel(1)
                
            # Ensure we have standard column names capitalized
            expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing = [col for col in expected_cols if col not in data.columns]
            if missing:
                logger.warning(f"Missing expected columns in downloaded data: {missing}")
                
            # Drop NaN rows (e.g. days with no trading)
            data.dropna(subset=['Close'], inplace=True)
            
            logger.info(f"Successfully fetched {len(data)} rows of data.")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {self.ticker}: {e}", exc_info=True)
            return None
