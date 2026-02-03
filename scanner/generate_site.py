"""
Static site generator for EOD market scanner
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import pandas as pd
from jinja2 import Environment, FileSystemLoader

from fetch_data import PolygonDataFetcher
from strategies.scans import get_all_scans, ScanEngine, prepare_derived_columns


class SiteGenerator:
    """Generate static HTML site with scan results"""

    def __init__(self, output_dir: str = "docs"):
        # Always use absolute path relative to project root
        self.output_dir = Path(__file__).parent.parent / output_dir
        self.output_dir.mkdir(exist_ok=True)

        # Set up Jinja2 templates
        template_dir = Path(__file__).parent.parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))

        self.fetcher = PolygonDataFetcher()

    def run_all_scans(self, market_data: pd.DataFrame) -> Dict:
        """
        Execute all scan strategies

        Returns:
            Dict with structure: {guru_name: {scan_name: DataFrame}}
        """
        print("\nRunning all scans...")

        # Prepare data
        market_data = prepare_derived_columns(market_data)
        engine = ScanEngine(market_data)

        all_scans = get_all_scans()
        results = {}

        for guru_name, guru_info in all_scans.items():
            print(f"\n{guru_name}")
            results[guru_name] = {
                'link': guru_info['link'],
                'description': guru_info.get('description', ''),
                'scans': {}
            }

            for scan_name, scan_config in guru_info['scans'].items():
                print(f"  Running: {scan_name}...", end=" ")

                try:
                    scan_results = engine.run_scan(
                        query_func=scan_config['query'],
                        order_by=scan_config['order_by'],
                        limit=scan_config['limit'],
                        ascending=False
                    )

                    results[guru_name]['scans'][scan_name] = {
                        'description': scan_config.get('description', ''),
                        'data': scan_results,
                        'count': len(scan_results)
                    }

                    print(f"{len(scan_results)} results")

                except Exception as e:
                    print(f"ERROR: {e}")
                    results[guru_name]['scans'][scan_name] = {
                        'description': scan_config.get('description', ''),
                        'data': pd.DataFrame(),
                        'count': 0,
                        'error': str(e)
                    }

        return results

    def fetch_chart_data(self, tickers: List[str], days: int = 90) -> Dict:
        """
        Fetch 90-day OHLCV data for tickers

        Returns:
            Dict: {ticker: [{date, open, high, low, close, volume}, ...]}
        """
        print(f"\nFetching chart data for {len(tickers)} tickers...")

        chart_data = {}

        for idx, ticker in enumerate(tickers):
            try:
                df = self.fetcher.fetch_aggregates(ticker, days=days)

                if not df.empty:
                    # Convert to list of dicts for JSON embedding
                    chart_data[ticker] = df.to_dict(orient='records')

                    # Convert datetime to string for JSON serialization
                    for record in chart_data[ticker]:
                        if 'date' in record:
                            record['date'] = record['date'].strftime('%Y-%m-%d')

                if (idx + 1) % 50 == 0:
                    pct = ((idx + 1) / len(tickers)) * 100
                    print(f"  Charts: {idx + 1}/{len(tickers)} ({pct:.1f}%)")

            except Exception as e:
                print(f"  Error fetching {ticker}: {e}")
                chart_data[ticker] = []

        print(f"Fetched chart data for {len(chart_data)} tickers")
        return chart_data

    def generate_index_page(self, scan_results: Dict, scan_date: str):
        """Generate landing page"""
        print("\nGenerating index page...")

        template = self.env.get_template('index.html')

        # If no results, show available scans structure
        if not scan_results:
            from strategies.scans import get_all_scans
            all_scans = get_all_scans()
            summary = []
            for guru_name, guru_info in all_scans.items():
                guru_summary = {
                    'name': guru_name,
                    'link': guru_info['link'],
                    'description': guru_info.get('description', ''),
                    'scans': []
                }
                for scan_name, scan_config in guru_info['scans'].items():
                    guru_summary['scans'].append({
                        'name': scan_name,
                        'description': scan_config.get('description', ''),
                        'count': 0,
                        'url': '#'
                    })
                summary.append(guru_summary)
        else:
            # Prepare summary for index
            summary = []
            for guru_name, guru_data in scan_results.items():
                guru_summary = {
                    'name': guru_name,
                    'link': guru_data['link'],
                    'description': guru_data.get('description', ''),
                    'scans': []
                }

                for scan_name, scan_data in guru_data['scans'].items():
                    guru_summary['scans'].append({
                        'name': scan_name,
                        'description': scan_data['description'],
                        'count': scan_data['count'],
                        'url': self.get_scan_url(guru_name, scan_name)
                    })

                summary.append(guru_summary)

        html = template.render(
            gurus=summary,
            scan_date=scan_date,
            generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        )

        output_file = self.output_dir / "index.html"
        with open(output_file, 'w') as f:
            f.write(html)

        print(f"  Saved to {output_file}")

    def generate_scan_pages(self, scan_results: Dict, chart_data: Dict, scan_date: str):
        """Generate individual scan result pages"""
        print("\nGenerating scan pages...")

        template = self.env.get_template('strategy.html')

        for guru_name, guru_data in scan_results.items():
            for scan_name, scan_data in guru_data['scans'].items():
                print(f"  {guru_name} - {scan_name}...", end=" ")

                df = scan_data['data']

                if df.empty:
                    print("No results, skipping")
                    continue

                # Prepare stock data with charts
                stocks = []
                for _, row in df.iterrows():
                    ticker = row['ticker']

                    stock_data = {
                        'ticker': ticker,
                        'name': row.get('name', ticker),
                        'close': row.get('close', 0),
                        'volume': row.get('volume', 0),
                        'daily_change': row.get('daily_change', 0),
                        'roc': row.get('roc', 0),
                        'volume_ratio': row.get('volume_ratio', 0),
                        'chart_data': chart_data.get(ticker, [])
                    }

                    # Add any other relevant metrics
                    for col in df.columns:
                        if col not in stock_data:
                            stock_data[col] = row.get(col)

                    stocks.append(stock_data)

                html = template.render(
                    guru_name=guru_name,
                    guru_link=guru_data['link'],
                    guru_description=guru_data.get('description', ''),
                    scan_name=scan_name,
                    description=scan_data['description'],
                    stocks=stocks,
                    scan_date=scan_date,
                    generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
                )

                # Save to file
                output_file = self.output_dir / self.get_scan_filename(guru_name, scan_name)
                output_file.parent.mkdir(parents=True, exist_ok=True)

                with open(output_file, 'w') as f:
                    f.write(html)

                print(f"{len(stocks)} stocks")

    def get_scan_url(self, guru_name: str, scan_name: str) -> str:
        """Generate URL for scan page"""
        return self.get_scan_filename(guru_name, scan_name)

    def get_scan_filename(self, guru_name: str, scan_name: str) -> str:
        """Generate filename for scan page"""
        # Sanitize names for filesystem
        guru_slug = guru_name.split('(')[0].strip().replace(' ', '_').lower()
        scan_slug = scan_name.replace(' ', '_').replace('/', '_').lower()
        return f"{guru_slug}_{scan_slug}.html"

    def generate(self):
        """Main generation workflow"""
        print("=" * 60)
        print("EOD Market Scanner - Static Site Generation")
        print("=" * 60)

        scan_date = datetime.now().strftime('%Y-%m-%d')

        # Step 1: Fetch market data
        print("\n[1/5] Fetching market data from Polygon.io...")
        try:
            market_data = self.fetcher.build_scan_dataset()
        except Exception as e:
            print(f"ERROR fetching data: {e}")
            import traceback
            traceback.print_exc()
            market_data = pd.DataFrame()

        if market_data.empty:
            print("WARNING: No market data available. Generating empty scan results...")
            # Generate empty results page
            scan_results = {}
            all_tickers = set()
            chart_data = {}
        else:
            print(f"  Loaded data for {len(market_data)} tickers")

            # Step 2: Run all scans
            print("\n[2/5] Running scans...")
            scan_results = self.run_all_scans(market_data)

            # Step 3: Collect all qualifying tickers
            print("\n[3/5] Collecting qualifying tickers...")
            all_tickers = set()
            for guru_data in scan_results.values():
                for scan_data in guru_data['scans'].values():
                    if not scan_data['data'].empty:
                        all_tickers.update(scan_data['data']['ticker'].tolist())

            print(f"  Found {len(all_tickers)} unique qualifying tickers")

            # Step 4: Fetch chart data
            print("\n[4/5] Fetching chart data...")
            chart_data = self.fetch_chart_data(list(all_tickers), days=90)

        # Step 5: Generate HTML pages (always, even if empty)
        print("\n[5/5] Generating HTML pages...")
        self.generate_index_page(scan_results, scan_date)
        self.generate_scan_pages(scan_results, chart_data, scan_date)

        print("\n" + "=" * 60)
        print("COMPLETE!")
        print("=" * 60)
        print(f"Site generated in: {self.output_dir}")
        print(f"Open {self.output_dir}/index.html in your browser")


if __name__ == "__main__":
    generator = SiteGenerator()
    generator.generate()
