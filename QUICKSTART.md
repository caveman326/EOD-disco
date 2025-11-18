# Quick Start Guide

Get up and running with EOD Stock Scans in minutes!

## Prerequisites

- Python 3.7+
- pip
- Stock market data access

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/eodstockscans.git
cd eodstockscans
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Settings

Edit `config.yaml` and set your data path:

```yaml
BASE_PATH: /path/to/your/stock/data
```

## Running Your First Scan

### Run All Markets

```bash
python update_scans.py
```

### Run Specific Market

```bash
python update_scans.py --market "United States"
```

### Run Multiple Markets

```bash
python update_scans.py --market "United States,Canada"
```

## View Results

After running scans, open the generated HTML files:

```bash
# Open the main index page
open site/index.html  # macOS
xdg-open site/index.html  # Linux
start site/index.html  # Windows
```

## Command-Line Options

```bash
# Only run scans (skip site generation)
python update_scans.py --gen-site False

# Only generate site (skip running scans)
python update_scans.py --run-scans False

# Run for specific date
python update_scans.py --date "2023-03-07"
```

## Project Structure

```
eodstockscans/
├── src/              # Source code
├── templates/        # HTML templates
├── site/            # Generated website (created after first run)
├── config.yaml      # Configuration
└── update_scans.py  # Main script
```

## Next Steps

1. **Explore Scans**: Check `src/scans.py` to see all available scan strategies
2. **Customize**: Modify scan criteria to match your trading style
3. **Add Scans**: Create your own custom scans
4. **Automate**: Set up cron jobs for daily execution

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run scans
python update_scans.py

# Deactivate virtual environment
deactivate
```

## Troubleshooting

### Import Errors

Make sure you're in the project root directory and virtual environment is activated.

### Data Not Found

Verify `BASE_PATH` in `config.yaml` points to your data directory.

### Missing Dependencies

Reinstall requirements:
```bash
pip install -r requirements.txt --force-reinstall
```

## Getting Help

- Read the [full README](README.md)
- Check [setup documentation](docs/SETUP.md)
- Review [scan strategies](docs/SCAN_STRATEGIES.md)
- Open an issue on GitHub

## What's Next?

- Learn about [scan strategies](docs/SCAN_STRATEGIES.md)
- Read the [detailed setup guide](docs/SETUP.md)
- Contribute to the project (see [CONTRIBUTING.md](CONTRIBUTING.md))

Happy scanning! 📈
