# Quantitative Time-Series Forecasting and Backtesting Engine for Gold (XAUUSD)

A robust, production-grade, end-to-end quantitative backtesting engine built entirely from scratch in Python. This framework uses high-performance vectorized operations via `pandas` and `numpy` to ensure absolute mathematical control and maximum execution speed, eliminating the need for black-box trading libraries like Backtrader or Zipline.

## System Architecture

The engine is modularized into institutional-grade layers:
- **`data/`**: Ingestion layer utilizing `yfinance` to reliably fetch historical XAUUSD data (`GC=F`). Includes rigorous exception handling and data normalization.
- **`research/`**: Core mathematical modeling layer. Implements highly optimized, vectorized feature engineering and signal generation (e.g., Moving Average Crossovers, Bollinger Bands).
- **`backtester/`**: Execution simulator that processes trades and rigorously applies institutional constraints like execution slippage and transaction costs.
- **`analytics/`**: Performance evaluation layer. Computes standard metrics including Annualized Volatility, Sharpe Ratio, Sortino Ratio, Maximum Drawdown, Calmar Ratio, and Win Rate.

## Installation

Ensure you have Python installed (Python 3.10+ recommended). The project provides automated environment setup scripts.

**For Windows:**
```powershell
.\setup_env.ps1
```

**For Linux / macOS:**
```bash
./setup_env.sh
```

## Usage

To run the full end-to-end pipeline (Data Ingestion ➡️ Signal Generation ➡️ Vectorized Execution ➡️ Analytics):

```bash
python main.py
```

### Extending the Engine

The codebase is designed for quantitative researchers to easily swap in proprietary alpha models. To test a new mathematical strategy:
1. Navigate to `research/math_models.py`.
2. Update the `generate_signals` method within the `QuantitativeModel` class to output customized long (1) or short (-1) positions.
3. Re-run `main.py` to evaluate your new strategy's performance metrics net of fees.