"""
Polygon.io data fetcher for EOD market scanner
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from polygon import RESTClient
from pathlib import Path


class PolygonDataFetcher:
    """Fetches and processes market data from Polygon.io"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")
        if not self.api_key:
            raise ValueError("POLYGON_API_KEY environment variable or api_key parameter required")

        self.client = RESTClient(self.api_key)
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)

    def get_trading_days(self, days_back: int = 100) -> List[str]:
        """Get list of recent trading days"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back * 1.5)  # Extra buffer for weekends

        # Simple approach: get all days and filter out weekends
        # TODO: Consider market holidays
        trading_days = []
        current = start_date
        while current <= end_date:
            if current.weekday() < 5:  # Monday = 0, Friday = 4
                trading_days.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)

        return trading_days[-days_back:]

    def fetch_ticker_universe(self, market: str = "stocks", use_cache: bool = True) -> pd.DataFrame:
        """
        Fetch all available tickers
        Cache for 7 days to minimize API calls
        """
        cache_file = self.cache_dir / "ticker_universe.json"

        if use_cache and cache_file.exists():
            # Check if cache is less than 7 days old
            mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - mtime < timedelta(days=7):
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                return pd.DataFrame(data)

        # Fetch from Polygon
        print("Fetching ticker universe from Polygon.io...")
        tickers = []

        for ticker in self.client.list_tickers(
            market=market,
            active=True,
            limit=1000
        ):
            tickers.append({
                'ticker': ticker.ticker,
                'name': ticker.name,
                'market': getattr(ticker, 'market', 'stocks'),
                'locale': getattr(ticker, 'locale', 'us'),
                'type': getattr(ticker, 'type', ''),
                'active': True
            })

        df = pd.DataFrame(tickers)

        # Cache the results
        with open(cache_file, 'w') as f:
            json.dump(df.to_dict(orient='records'), f)

        print(f"Found {len(df)} active tickers")
        return df

    def fetch_snapshot_all_tickers(self) -> pd.DataFrame:
        """
        Fetch current snapshot for all tickers
        Returns EOD data with volume, price, and basic metrics
        """
        print("Fetching market snapshot from Polygon.io...")

        try:
            # Get all tickers snapshot
            snapshots = self.client.get_snapshot_all("stocks")

            data = []
            for snapshot in snapshots:
                ticker_data = {
                    'ticker': snapshot.ticker,
                    'close': snapshot.day.c if snapshot.day else None,
                    'open': snapshot.day.o if snapshot.day else None,
                    'high': snapshot.day.h if snapshot.day else None,
                    'low': snapshot.day.l if snapshot.day else None,
                    'volume': snapshot.day.v if snapshot.day else None,
                    'prev_close': snapshot.prev_day.c if snapshot.prev_day else None,
                    'updated': snapshot.updated if hasattr(snapshot, 'updated') else None,
                }
                data.append(ticker_data)

            df = pd.DataFrame(data)
            print(f"Fetched snapshots for {len(df)} tickers")
            return df

        except Exception as e:
            print(f"Error fetching snapshots: {e}")
            return pd.DataFrame()

    def fetch_aggregates(self, ticker: str, days: int = 90) -> pd.DataFrame:
        """
        Fetch historical OHLCV data for a single ticker
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days * 1.5)  # Buffer for weekends

        try:
            aggs = self.client.get_aggs(
                ticker=ticker,
                multiplier=1,
                timespan="day",
                from_=start_date.strftime("%Y-%m-%d"),
                to=end_date.strftime("%Y-%m-%d"),
                limit=50000
            )

            data = []
            for agg in aggs:
                data.append({
                    'date': pd.to_datetime(agg.timestamp, unit='ms'),
                    'open': agg.open,
                    'high': agg.high,
                    'low': agg.low,
                    'close': agg.close,
                    'volume': agg.volume,
                })

            df = pd.DataFrame(data)
            if not df.empty:
                df = df.sort_values('date').tail(days)
            return df

        except Exception as e:
            print(f"Error fetching aggregates for {ticker}: {e}")
            return pd.DataFrame()

    def fetch_ticker_details(self, ticker: str) -> Dict:
        """Fetch detailed ticker information"""
        try:
            details = self.client.get_ticker_details(ticker)
            return {
                'ticker': ticker,
                'name': getattr(details, 'name', ''),
                'market_cap': getattr(details, 'market_cap', None),
                'shares_outstanding': getattr(details, 'share_class_shares_outstanding', None),
                'description': getattr(details, 'description', ''),
                'sic_description': getattr(details, 'sic_description', ''),
                'homepage_url': getattr(details, 'homepage_url', ''),
            }
        except Exception as e:
            print(f"Error fetching details for {ticker}: {e}")
            return {'ticker': ticker}

    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate technical indicators needed for scans
        Input: DataFrame with OHLCV data (multiple tickers with MultiIndex)
        Output: Same DataFrame with additional indicator columns
        """

        def calc_sma(series, period):
            return series.rolling(window=period, min_periods=period).mean()

        def calc_ema(series, period):
            return series.ewm(span=period, adjust=False, min_periods=period).mean()

        def calc_roc(series, period=1):
            """Rate of Change as percentage"""
            return ((series / series.shift(period)) - 1) * 100

        def calc_adr(df, period=20):
            """Average Daily Range as percentage"""
            daily_range = ((df['high'] - df['low']) / df['close']) * 100
            return daily_range.rolling(window=period, min_periods=period).mean()

        def calc_trend_intensity(series, period=20):
            """
            Trend Intensity indicator
            Measures consistency of trend direction
            """
            roi = series / series.shift(period) - 1
            # Simplified TI: ratio of close to period average
            sma = series.rolling(window=period, min_periods=period).mean()
            return series / sma

        # Work on copy
        df = df.copy()

        # Price-based SMAs
        for period in [20, 50, 100, 150, 200]:
            df[f'sma_{period}'] = calc_sma(df['close'], period)

        # EMAs
        for period in [9, 10, 21, 50, 200]:
            df[f'ema_{period}'] = calc_ema(df['close'], period)

        # Volume indicators
        df['sma_50_volume'] = calc_sma(df['volume'], 50)
        df['volume_ratio'] = df['volume'] / df['sma_50_volume']

        # Price changes
        df['roc'] = calc_roc(df['close'])
        df['close_prev'] = df['close'].shift(1)
        df['daily_change'] = (df['close'] / df['close_prev'] - 1) * 100

        # Range indicators
        df['adr_20'] = calc_adr(df, 20)
        df['trend_intensity'] = calc_trend_intensity(df['close'], 20)

        # Min/Max over periods
        for period in [5, 21, 63, 126, 252]:
            df[f'min_{period}'] = df['close'].rolling(window=period, min_periods=period).min()
            df[f'max_{period}'] = df['close'].rolling(window=period, min_periods=period).max()

        # Dollar volume
        df['dollar_volume'] = df['volume'] * df['close']
        df['avg_dollar_volume_50'] = calc_sma(df['dollar_volume'], 50)

        # Market cap (will need to join with ticker details)
        # For now, approximate using shares outstanding if available

        return df

    def build_scan_dataset(self, date: Optional[str] = None) -> pd.DataFrame:
        """
        Build complete dataset for scanning
        Fetches snapshot + calculates all technical indicators
        """
        if date is None:
            date = datetime.now().date().strftime("%Y-%m-%d")

        print(f"Building scan dataset for {date}...")

        # Get current snapshot
        snapshot = self.fetch_snapshot_all_tickers()

        if snapshot.empty:
            print("No snapshot data available")
            return pd.DataFrame()

        # Filter out tickers with missing data
        snapshot = snapshot.dropna(subset=['close', 'volume'])
        snapshot = snapshot[snapshot['close'] > 0]
        snapshot = snapshot[snapshot['volume'] > 0]

        print(f"Processing {len(snapshot)} tickers with valid data...")

        # For each ticker, we need historical data to calculate indicators
        # This is expensive - we'll need to batch this intelligently

        # For MVP: fetch historical data for top N liquid stocks
        # Sort by volume and take top 2000
        snapshot = snapshot.sort_values('volume', ascending=False).head(2000)

        results = []

        for idx, row in snapshot.iterrows():
            ticker = row['ticker']

            # Fetch 252 days (1 year) of historical data for indicators
            hist = self.fetch_aggregates(ticker, days=252)

            if len(hist) < 50:  # Need at least 50 days for indicators
                continue

            # Calculate indicators
            hist = self.calculate_technical_indicators(hist)

            # Get most recent row (today's data)
            latest = hist.iloc[-1].to_dict()
            latest['ticker'] = ticker
            latest['name'] = row.get('name', ticker)

            results.append(latest)

            if len(results) % 50 == 0:
                print(f"Processed {len(results)} tickers...")

        df = pd.DataFrame(results)
        print(f"Built dataset with {len(df)} tickers")

        return df


if __name__ == "__main__":
    # Test the fetcher
    fetcher = PolygonDataFetcher()

    # Test ticker universe
    # universe = fetcher.fetch_ticker_universe()
    # print(f"Universe: {len(universe)} tickers")

    # Test snapshot
    # snapshot = fetcher.fetch_snapshot_all_tickers()
    # print(snapshot.head())

    # Test single ticker historical
    hist = fetcher.fetch_aggregates("AAPL", days=90)
    print(hist.tail())
