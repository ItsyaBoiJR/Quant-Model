import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class QuantitativeModel:
    """
    Vectorized mathematical feature engineering and signal generation.
    Strategy: Moving Average Crossover with Bollinger Bands Mean Reversion filter.
    """
    def __init__(self, short_window: int = 50, long_window: int = 200, bb_window: int = 20, bb_std: float = 2.0):
        self.short_window = short_window
        self.long_window = long_window
        self.bb_window = bb_window
        self.bb_std = bb_std

    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Computes necessary mathematical features for the strategy.
        Operates directly on the DataFrame using vectorized operations.
        """
        logger.info("Generating mathematical features (MAs, Bollinger Bands, Log Returns)...")
        data = df.copy()
        
        # Log Returns for mathematical stability in performance calcs
        data['log_return'] = np.log(data['Close'] / data['Close'].shift(1))
        
        # Moving Averages
        data['sma_short'] = data['Close'].rolling(window=self.short_window, min_periods=1).mean()
        data['sma_long'] = data['Close'].rolling(window=self.long_window, min_periods=1).mean()
        
        # Bollinger Bands
        data['bb_middle'] = data['Close'].rolling(window=self.bb_window, min_periods=1).mean()
        data['bb_std_val'] = data['Close'].rolling(window=self.bb_window, min_periods=1).std()
        data['bb_upper'] = data['bb_middle'] + (data['bb_std_val'] * self.bb_std)
        data['bb_lower'] = data['bb_middle'] - (data['bb_std_val'] * self.bb_std)
        
        return data

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates trading signals. 
        1 = Long, -1 = Short, 0 = Flat
        
        Rules:
        - Long if Short MA > Long MA AND Close < Upper BB (avoid buying overextended)
        - Short if Short MA < Long MA AND Close > Lower BB (avoid shorting overextended)
        """
        logger.info("Generating vectorized trading signals...")
        data = self.generate_features(df)
        
        # Initialize signal column
        data['signal'] = 0
        
        # Bullish condition
        bullish = (data['sma_short'] > data['sma_long']) & (data['Close'] < data['bb_upper'])
        
        # Bearish condition
        bearish = (data['sma_short'] < data['sma_long']) & (data['Close'] > data['bb_lower'])
        
        # Assign signals using NumPy where for vectorized speed
        data['signal'] = np.where(bullish, 1, np.where(bearish, -1, 0))
        
        # We need to shift the signal by 1 period so we don't have look-ahead bias
        # If signal is generated at end of day t, we execute at open/close of day t+1
        data['position'] = data['signal'].shift(1).fillna(0)
        
        return data
