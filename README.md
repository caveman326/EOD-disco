# EOD Stock Scans

A Python-based stock market scanning and analysis tool that generates static HTML websites displaying end-of-day (EOD) stock scans across multiple markets and trading strategies.

## Overview

This project automates the process of running technical stock scans based on various trading methodologies from well-known traders and generates interactive HTML reports with charts, data tables, and market analysis. The scans cover multiple international markets and include strategies from traders like Kristjan Kullamägi, Mark Minervini, Brad Schulz, and others.

## Features

- **Multi-Market Support**: Scans stocks across 14+ international markets including US, Canada, Europe, Asia-Pacific
- **Multiple Trading Strategies**: Pre-configured scans based on proven trading methodologies
- **Automated Chart Generation**: Creates both full-size and mini charts with technical indicators
- **Static HTML Output**: Generates a complete static website with scan results
- **Customizable Scans**: Easy-to-modify scan criteria and parameters
- **Market Monitor**: Overview dashboard for market-wide analysis

## Project Structure

```
eodstockscans-repo/
├── src/                    # Source code
│   ├── scans.py           # Scan definitions and criteria
│   ├── run_scans.py       # Scan execution logic
│   ├── gen_site.py        # HTML site generation
│   ├── _config.py         # Configuration utilities
│   └── _update_data.py    # Data update utilities
├── templates/             # Jinja2 HTML templates
│   ├── index.html         # Main landing page
│   ├── result_table.html  # Scan results table
│   ├── charts.html        # Chart display pages
│   ├── criteria.html      # Scan criteria display
│   └── ...                # Additional templates
├── examples/              # Example output files
├── docs/                  # Documentation
├── config.yaml           # Main configuration file
├── update_scans.py       # Main execution script
└── README.md             # This file
```

## Configuration

The `config.yaml` file contains all major configuration settings:

- **Markets**: Supported exchanges and scaling parameters
- **Chart Parameters**: Chart styling and technical indicators
- **Paths**: Data storage locations

### Supported Markets

- United States (NASDAQ, NYSE)
- Canada (Toronto, TSXV, CSE)
- United Kingdom (London)
- Germany (XETRA)
- France (Paris)
- Nordic Markets (Stockholm, Oslo, Copenhagen, Helsinki)
- Australia (Sydney)
- Japan (Tokyo)
- Hong Kong
- Singapore
- And more...

## Scan Strategies

The project includes pre-configured scans from various trading methodologies:

### Kristjan Kullamägi (@Qullamaggie)
- Biggest Gainers (1M, 3M, 6M, 12M)
- Earnings Power (EP) with Growth
- High Trend Intensity
- Small Stock Momentum

### Mark Minervini (@markminervini)
- Trend Template

### Brad Schulz (@BSchulz33868165)
- Pocket Pivot

### Stockbee (@PradeepBonde)
- 4% Gainers
- Breakout Scans
- Combo Scans

### Ben (@PatternProfits)
- Power of 3
- Velocity
- Focus

### Ray (@RayTL_)
- RS New High Base Pullback (5D, 1M, 3M, 6M, 12M)

### And more...

## Requirements

This project requires Python 3.7+ and the following key dependencies:

- `jinja2` - Template engine for HTML generation
- `pandas` - Data manipulation and analysis
- `pyarrow` - Columnar data format
- `duckdb` - Analytical database
- `pyyaml` - YAML configuration parsing
- `typer` - CLI framework

**Note**: A complete `requirements.txt` file should be created based on your specific environment and dependencies.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/eodstockscans.git
cd eodstockscans
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your settings in `config.yaml`

## Usage

### Running Scans

Execute the main script to run scans and generate the website:

```bash
python update_scans.py
```

### Command-Line Options

The script supports various command-line arguments:

```bash
# Run scans for a specific market
python update_scans.py --market "United States"

# Run scans for multiple markets
python update_scans.py --market "United States,Canada,United Kingdom"

# Skip scan execution, only generate site
python update_scans.py --run-scans False

# Skip site generation, only run scans
python update_scans.py --gen-site False

# Run for a specific date
python update_scans.py --date "2023-03-07"
```

## Output

The generated website includes:

- **Index Page**: Market overview and navigation
- **Market Monitor**: Market-wide statistics and trends
- **Scan Results**: Detailed tables with stock data
- **Charts**: Interactive stock charts with technical indicators
- **Criteria**: Display of scan criteria and parameters

## Customization

### Adding New Scans

Edit `src/scans.py` to add new scan definitions:

```python
"Your Scan Name": {
    "query": "close>10 AND volume>100000",
    "order": "volume",
    "limit": 100,
}
```

### Modifying Templates

HTML templates are located in the `templates/` directory and use Jinja2 syntax for customization.

### Adjusting Chart Parameters

Modify chart settings in `config.yaml` under the `CHART_PARAMS` section.

## Data Requirements

This project expects access to stock market data. The `BASE_PATH` in `config.yaml` should point to your data directory containing:

- Historical price data
- Volume data
- Fundamental data (earnings, revenue, etc.)
- Technical indicators

**Note**: Data sourcing and storage implementation is not included in this repository.

## License

Please specify your license here (e.g., MIT, Apache 2.0, GPL, etc.)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This software is for educational and research purposes only. It is not financial advice. Always do your own research and consult with a qualified financial advisor before making investment decisions.

## Acknowledgments

This project incorporates trading strategies and scan criteria inspired by various professional traders. Please refer to their original work and give credit where appropriate.

## Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This is a personal development project. Please ensure you have proper data access and comply with all relevant data provider terms of service.
