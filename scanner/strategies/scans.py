"""
Stock scanning strategies from various trading gurus
Adapted for pandas DataFrame filtering
"""
import pandas as pd
import numpy as np


class ScanEngine:
    """Execute scans on market data"""

    def __init__(self, data: pd.DataFrame):
        """
        Initialize with market data containing OHLCV + indicators

        Args:
            data: DataFrame with columns: ticker, close, volume, sma_50, etc.
        """
        self.data = data.copy()

    def run_scan(self, query_func, order_by: str, limit: int = 100, ascending: bool = False) -> pd.DataFrame:
        """
        Execute a scan query

        Args:
            query_func: Function that takes DataFrame and returns boolean mask
            order_by: Column name to sort by
            limit: Maximum results to return
            ascending: Sort order
        """
        # Apply filter
        filtered = self.data[query_func(self.data)].copy()

        # Sort
        if order_by in filtered.columns:
            filtered = filtered.sort_values(order_by, ascending=ascending)

        # Limit
        return filtered.head(limit)


def get_all_scans():
    """
    Return all scan definitions
    Each scan has: name, group, query_func, order_by, limit
    """

    scans = {
        "Kristjan Kullamägi (@Qullamaggie)": {
            "link": "https://twitter.com/Qullamaggie",
            "scans": {
                "Biggest Gainers 1M": {
                    "description": "Highest percentage gains over 1 month with high trend intensity",
                    "query": lambda df: (
                        (df['close'] > 4) &
                        (df['sma_50_volume'] > 200000) &
                        (df['avg_dollar_volume_50'] > 2000000) &
                        (df['adr_20'] > 4) &
                        (df['trend_intensity'] > 0.9)
                    ),
                    "order_by": "close_to_min_21",
                    "limit": 200,
                },
                "Biggest Gainers 3M": {
                    "description": "Highest percentage gains over 3 months with high trend intensity",
                    "query": lambda df: (
                        (df['close'] > 4) &
                        (df['sma_50_volume'] > 200000) &
                        (df['avg_dollar_volume_50'] > 2000000) &
                        (df['adr_20'] > 4) &
                        (df['trend_intensity'] > 0.9)
                    ),
                    "order_by": "close_to_min_63",
                    "limit": 200,
                },
                "Biggest Gainers 6M": {
                    "description": "Highest percentage gains over 6 months with high trend intensity",
                    "query": lambda df: (
                        (df['close'] > 4) &
                        (df['sma_50_volume'] > 200000) &
                        (df['avg_dollar_volume_50'] > 2000000) &
                        (df['adr_20'] > 4) &
                        (df['trend_intensity'] > 0.9)
                    ),
                    "order_by": "close_to_min_126",
                    "limit": 200,
                },
                "High Trend Intensity": {
                    "description": "Stocks with exceptionally strong trending behavior",
                    "query": lambda df: (
                        (df['close'] > 4) &
                        (df['close'] < 20) &
                        (df['sma_50_volume'] > 200000) &
                        (df['avg_dollar_volume_50'] > 2000000) &
                        (df['trend_intensity'] > 1.08) &
                        (df['adr_20'] > 4)
                    ),
                    "order_by": "close_to_min_126",
                    "limit": 200,
                },
                "Small Stock Momo": {
                    "description": "Lower-priced stocks with explosive momentum",
                    "query": lambda df: (
                        (df['daily_change'] > 10) &
                        (df['close'] < 10) &
                        (df['sma_50_volume'] > 200000)
                    ),
                    "order_by": "roc",
                    "limit": 200,
                },
            }
        },

        "Mark Minervini (@markminervini)": {
            "link": "https://twitter.com/markminervini",
            "scans": {
                "Trend Template": {
                    "description": "Mark Minervini's famous trend template for strong uptrends",
                    "query": lambda df: (
                        (df['close'] > df['sma_50']) &
                        (df['sma_50'] > df['sma_150']) &
                        (df['sma_150'] > df['sma_200']) &
                        # 200-day SMA trending up (current > 22 days ago)
                        (df['close'] >= df['min_252'] * 1.30) &  # At least 30% above 52w low
                        (df['close'] >= df['max_252'] * 0.75)  # Within 25% of 52w high
                    ),
                    "order_by": "close_to_min_252",
                    "limit": 200,
                }
            }
        },

        "Stockbee (@PradeepBonde)": {
            "link": "https://twitter.com/PradeepBonde",
            "scans": {
                "4% Gainers": {
                    "description": "Stocks breaking out with 4%+ gains after consolidation",
                    "query": lambda df: (
                        (df['close'] > 4) &
                        (df['daily_change'] > 4) &
                        (df['sma_50_volume'] > 200000) &
                        (df['avg_dollar_volume_50'] > 2000000)
                    ),
                    "order_by": "roc",
                    "limit": 100,
                },
                "High Trend Intensity": {
                    "description": "Stocks in tight consolidation with high trend intensity",
                    "query": lambda df: (
                        (df['close'] > 4) &
                        (df['trend_intensity'] > 1.04) &
                        (df['daily_change'] >= -1.01) &
                        (df['daily_change'] <= 1.01)
                    ),
                    "order_by": "trend_intensity",
                    "limit": 100,
                },
            }
        },

        "Brad Schulz (@BSchulz33868165)": {
            "link": "https://twitter.com/BSchulz33868165",
            "scans": {
                "Pocket Pivot": {
                    "description": "Pocket pivot buy points based on volume analysis",
                    "query": lambda df: (
                        (df['close'] > 4) &
                        (df['sma_50_volume'] > 200000) &
                        (df['avg_dollar_volume_50'] > 2000000) &
                        (df['volume'] > df['ema_50']) &  # Volume > 50-day EMA
                        (df['daily_change'] >= 5) &
                        (df['close'] > df['ema_200'])
                    ),
                    "order_by": "volume_ratio",
                    "limit": 100,
                }
            }
        },

        "Ben (@PatternProfits)": {
            "link": "https://twitter.com/PatternProfits",
            "scans": {
                "Velocity": {
                    "description": "High-momentum stocks with strong relative strength",
                    "query": lambda df: (
                        (df['close'] > 4) &
                        (df['sma_50_volume'] > 200000) &
                        (df['avg_dollar_volume_50'] > 2000000) &
                        (df['daily_change'] > 3) &
                        (df['volume_ratio'] > 1.3) &
                        (df['trend_intensity'] > 1.05)
                    ),
                    "order_by": "daily_change",
                    "limit": 100,
                },
            }
        },

        "Vo (@LignoL23)": {
            "link": "https://twitter.com/LignoL23",
            "scans": {
                "Top Gainers": {
                    "description": "Highest percentage gainers meeting volume requirements",
                    "query": lambda df: (
                        (df['close'] > 4) &
                        (df['sma_50_volume'] > 200000) &
                        (df['avg_dollar_volume_50'] > 2000000) &
                        (df['roc'] > 4)
                    ),
                    "order_by": "roc",
                    "limit": 100,
                },
                "Volume Gainers": {
                    "description": "Stocks with highest relative volume",
                    "query": lambda df: (
                        (df['close'] > 4) &
                        (df['sma_50_volume'] > 200000) &
                        (df['avg_dollar_volume_50'] > 2000000) &
                        (df['roc'] > 0)
                    ),
                    "order_by": "volume_ratio",
                    "limit": 200,
                },
                "52W High": {
                    "description": "Stocks making new 52-week highs with volume",
                    "query": lambda df: (
                        (df['close'] > 4) &
                        (df['sma_50_volume'] > 200000) &
                        (df['avg_dollar_volume_50'] > 2000000) &
                        (df['close'] >= df['max_252'] * 0.999) &  # At or near 52w high
                        (df['volume_ratio'] > 1)
                    ),
                    "order_by": "volume_ratio",
                    "limit": 200,
                },
            }
        },

        "Leif Soreide (@LeifSoreide)": {
            "link": "https://twitter.com/LeifSoreide",
            "scans": {
                "High Tight Flag (HTF)": {
                    "description": "Stocks forming high tight flag patterns",
                    "query": lambda df: (
                        (df['close'] > 4) &
                        (df['sma_50_volume'] > 250000) &
                        (df['close'] > df['sma_50']) &
                        (df['sma_50'] > df['sma_200']) &
                        (df['close_to_min_63'] > 1.5)  # Strong prior move
                    ),
                    "order_by": "close_to_min_63",
                    "limit": 100,
                }
            }
        },
    }

    return scans


def prepare_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate derived columns needed for scans
    (ratio columns, etc.)
    """
    df = df.copy()

    # Price to min/max ratios
    for period in [21, 63, 126, 252]:
        min_col = f'min_{period}'
        max_col = f'max_{period}'

        if min_col in df.columns:
            df[f'close_to_min_{period}'] = df['close'] / df[min_col]

        if max_col in df.columns:
            df[f'close_to_max_{period}'] = df['close'] / df[max_col]

    return df


if __name__ == "__main__":
    # Test with dummy data
    test_data = pd.DataFrame({
        'ticker': ['AAPL', 'MSFT', 'GOOGL'],
        'close': [150, 300, 100],
        'volume': [1000000, 800000, 600000],
        'sma_50': [145, 295, 98],
        'sma_50_volume': [900000, 750000, 550000],
        'avg_dollar_volume_50': [130000000, 221250000, 53900000],
        'adr_20': [5, 4.5, 6],
        'trend_intensity': [1.1, 0.95, 1.05],
        'roc': [3.4, 1.7, 2.0],
        'daily_change': [2.5, 1.2, 1.8],
    })

    scans = get_all_scans()
    print(f"Loaded {sum(len(s['scans']) for s in scans.values())} scans from {len(scans)} gurus")
