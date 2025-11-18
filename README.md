# EOD Market Scanner

A lightweight, automated stock market scanner that generates static HTML sites with EOD scan results from trading guru strategies. Powered by Polygon.io and deployed via GitHub Pages.

## Architecture

**Static Site + GitHub Actions = Zero Hosting Costs**

This project runs daily scans at market close, generates a static HTML site with embedded charts, and deploys automatically to GitHub Pages. No backend servers, no databases, no ongoing costs.

## Features

- **Trading Guru Strategies**: Pre-configured scans from Kristjan Kullamägi, Mark Minervini, Stockbee, Brad Schulz, and others
- **Interactive Charts**: 90-day candlestick charts using TradingView's lightweight-charts library
- **Automated Daily Updates**: GitHub Actions runs scans at 4:05 PM ET (M-F)
- **Zero Cost**: Free hosting on GitHub Pages, free CI/CD with GitHub Actions
- **Fast & Reliable**: Pre-rendered static HTML, no server processing

## Project Structure

```
EOD-disco/
├── .github/workflows/
│   └── daily-scan.yml          # GitHub Actions workflow (runs 4:05 PM ET)
├── scanner/
│   ├── fetch_data.py            # Polygon.io data integration
│   ├── generate_site.py         # Static site generator
│   ├── strategies/
│   │   └── scans.py             # All guru scan strategies
│   └── requirements.txt
├── templates/
│   ├── index.html               # Landing page template
│   └── strategy.html            # Scan results page template
└── docs/                        # Generated static site (GitHub Pages serves this)
```

## Setup

### 1. Get Polygon.io API Key

Sign up at [polygon.io](https://polygon.io) and get your API key. Free tier works for testing.

### 2. Configure GitHub Repository

1. Fork/clone this repository
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Add new repository secret:
   - Name: `POLYGON_API_KEY`
   - Value: Your Polygon.io API key

### 3. Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** (or your default branch) / **/docs**
4. Save

### 3b. Enable Workflow Permissions

1. Go to **Settings** → **Actions** → **General**
2. Scroll to **"Workflow permissions"**
3. Select **"Read and write permissions"**
4. Click **"Save"**

### 4. Run First Scan

**Option A: Manual Trigger (for testing)**
1. Go to **Actions** tab
2. Select "Daily EOD Market Scan" workflow
3. Click "Run workflow"

**Option B: Wait for Scheduled Run**
- Runs automatically at 4:05 PM ET Monday-Friday

## Local Development

### Install Dependencies

```bash
cd scanner
pip install -r requirements.txt
```

### Set API Key

```bash
export POLYGON_API_KEY="your_api_key_here"
```

### Run Scanner Locally

```bash
cd scanner
python generate_site.py
```

This will:
1. Fetch EOD data from Polygon.io
2. Run all scan strategies
3. Fetch 90-day OHLCV for qualifying stocks
4. Generate HTML pages in `docs/`
5. Open `docs/index.html` in your browser to preview

## How It Works

### Daily Workflow

1. **4:05 PM ET**: GitHub Actions triggers
2. **Fetch Data**: Pull historical data from Polygon.io (500 tickers with free tier)
3. **Calculate Indicators**: SMAs, EMAs, volume ratios, trend intensity, etc.
4. **Run Scans**: Execute all guru strategies (filters + sorting)
5. **Fetch Charts**: Get 90-day OHLCV for qualifying stocks
6. **Generate HTML**: Render templates with embedded chart data
7. **Deploy**: Commit to docs/ folder, GitHub Pages auto-publishes

### Scan Strategies Included

#### Kristjan Kullamägi (@Qullamaggie)
- Biggest Gainers (1M, 3M, 6M)
- High Trend Intensity
- Small Stock Momo

#### Mark Minervini (@markminervini)
- Trend Template

#### Stockbee (@PradeepBonde)
- 4% Gainers
- High Trend Intensity

#### Brad Schulz (@BSchulz33868165)
- Pocket Pivot

#### Ben (@PatternProfits)
- Velocity

#### Vo (@LignoL23)
- Top Gainers
- Volume Gainers
- 52W High

#### Leif Soreide (@LeifSoreide)
- High Tight Flag (HTF)

## Customization

### Add New Scans

Edit `scanner/strategies/scans.py`:

```python
"Your Guru Name": {
    "link": "https://twitter.com/yourhandle",
    "scans": {
        "Your Scan Name": {
            "description": "What this scan looks for",
            "query": lambda df: (
                (df['close'] > 10) &
                (df['volume'] > 100000) &
                (df['roc'] > 5)
            ),
            "order_by": "roc",
            "limit": 100,
        }
    }
}
```

### Modify Templates

- `templates/index.html` - Landing page layout
- `templates/strategy.html` - Individual scan results page

Uses Tailwind CSS (CDN) for styling.

## Data & API Usage

### Polygon.io Limits

Free tier: 5 API calls/minute. This scanner makes:
- 1 call for ticker universe (cached 7 days)
- 1 call for snapshot (all tickers)
- ~100-500 calls for historical data (qualifying stocks)

**Total**: ~500 calls per run

For production, consider Polygon.io paid plans for higher limits.

### Optimization

The scanner currently processes top 2000 most liquid stocks to stay within API limits. For full market coverage, upgrade to a paid Polygon.io plan.

## Troubleshooting

### Workflow Fails

Check **Actions** tab for error logs:
- Missing API key? Add `POLYGON_API_KEY` secret
- API rate limit? Wait 1 minute and re-run
- No data? Check Polygon.io subscription status

### Charts Not Rendering

- Check browser console for JavaScript errors
- Verify chart data is embedded in HTML (view source)
- Try different browser

### Outdated Results

- Workflow only runs weekdays at 4:05 PM ET
- Manually trigger via Actions tab if needed

## Cost Breakdown

| Item | Cost |
|------|------|
| GitHub Pages hosting | $0 (free) |
| GitHub Actions (2000 min/month) | $0 (free) |
| Polygon.io Free Tier | $0 (limited) |
| **Total Monthly Cost** | **$0** |

For production use with full market coverage:
- Polygon.io Starter: $29/month (unlimited API calls)

## License

MIT License - see LICENSE file

## Disclaimer

This software is for educational and research purposes only. It is not financial advice. Always do your own research and consult with a qualified financial advisor before making investment decisions.

## Credits

Scan strategies inspired by professional traders. Please refer to their original work and give credit where appropriate.

## Support

Open an issue on GitHub for bugs or feature requests.
