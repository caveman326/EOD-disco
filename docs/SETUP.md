# Setup Guide

This guide will help you set up the EOD Stock Scans project for development or personal use.

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git
- Access to stock market data (see Data Requirements section)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/eodstockscans.git
cd eodstockscans
```

### 2. Create Virtual Environment

It's recommended to use a virtual environment to isolate project dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Project

Edit the `config.yaml` file to match your setup:

```yaml
BASE_PATH: /path/to/your/data/directory
RESULTS_PATH: results
IMAGES_PATH: images
SUMMARY_PATH: summary
```

**Important Configuration Settings:**

- `BASE_PATH`: Root directory where your stock data is stored
- `RESULTS_PATH`: Subdirectory for scan results
- `IMAGES_PATH`: Subdirectory for generated charts
- `SUMMARY_PATH`: Subdirectory for summary data

### 5. Data Requirements

This project requires access to stock market data. You'll need:

- **Price Data**: Historical OHLCV (Open, High, Low, Close, Volume) data
- **Fundamental Data**: Earnings, revenue, market cap, etc.
- **Technical Indicators**: Pre-calculated or calculated on-the-fly
- **Market Data**: Exchange information, sectors, industries

**Data Format:**

The project expects data in a format compatible with PyArrow/DuckDB. Organize your data directory as follows:

```
/your/data/directory/
├── results/
│   └── summary/
│       └── [partitioned data files]
└── images/
    └── [generated charts]
```

### 6. Test Your Setup

Run a test scan for a single market:

```bash
python update_scans.py --market "United States"
```

This will:
1. Execute all configured scans for the US market
2. Generate charts
3. Create HTML pages in the `site/` directory

## Directory Structure After Setup

```
eodstockscans/
├── venv/                  # Virtual environment (not in git)
├── src/                   # Source code
├── templates/             # HTML templates
├── site/                  # Generated website (not in git)
├── config.yaml           # Configuration file
├── update_scans.py       # Main script
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
```

## Common Issues

### Issue: Module Not Found

**Solution**: Ensure you've activated your virtual environment and installed all dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Data Path Not Found

**Solution**: Verify that `BASE_PATH` in `config.yaml` points to an existing directory with the correct structure.

### Issue: Import Errors

**Solution**: The project uses relative imports. Ensure you're running scripts from the project root directory.

## Next Steps

- Review the [README.md](../README.md) for usage instructions
- Explore scan definitions in `src/scans.py`
- Customize templates in the `templates/` directory
- Add your own scan strategies

## Getting Help

If you encounter issues:

1. Check this setup guide thoroughly
2. Review the main README.md
3. Search existing GitHub issues
4. Open a new issue with detailed information

## Development Mode

For development, you may want to:

1. Install additional development tools:
```bash
pip install pytest black flake8
```

2. Set up pre-commit hooks for code quality

3. Enable debug mode in your configuration

## Production Deployment

For production use:

1. Use environment variables for sensitive configuration
2. Set up automated data updates
3. Configure a web server to serve the static site
4. Set up scheduled tasks (cron jobs) for regular scans

---

Happy scanning!
