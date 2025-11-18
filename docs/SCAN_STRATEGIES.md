# Scan Strategies Reference

This document provides detailed information about the stock scanning strategies included in this project. Each strategy is based on methodologies from professional traders.

## Table of Contents

- [Kristjan Kullamägi](#kristjan-kullamägi)
- [Mark Minervini](#mark-minervini)
- [Brad Schulz](#brad-schulz)
- [Stockbee](#stockbee)
- [Ben (Pattern Profits)](#ben-pattern-profits)
- [Ray](#ray)
- [Blake Davis](#blake-davis)
- [Leif Soreide](#leif-soreide)
- [Vo](#vo)

---

## Kristjan Kullamägi

**Twitter**: [@Qullamaggie](https://twitter.com/Qullamaggie)

### Biggest Gainers (1M, 3M, 6M, 12M)

Identifies stocks with the highest percentage gains over different time periods.

**Criteria**:
- Minimum price and volume requirements
- High trend intensity (TI > 0.9)
- Average daily range > 4%
- Sorted by gain percentage over specified period

### Earnings Power (EP)

Finds stocks breaking out on high volume with strong moving average alignment.

**Criteria**:
- Price > 50-day SMA
- 20-day SMA > 50-day SMA
- Gap up > 3% from previous close
- Market cap between $500M and $100B
- Sorted by relative volume

### EP with Growth

Same as EP scan but with additional fundamental growth filters.

**Additional Criteria**:
- Revenue growth > 30%
- Earnings estimate growth > 15%

### High Trend Intensity

Stocks with exceptionally strong trending behavior.

**Criteria**:
- Trend intensity > 1.08
- Price < $20
- Average daily range > 4%
- High volume requirements

### Small Stock Momentum

Focuses on lower-priced stocks with explosive momentum.

**Criteria**:
- Daily gain > 10%
- Price < $10
- Average volume > 200,000 shares

---

## Mark Minervini

**Twitter**: [@markminervini](https://twitter.com/markminervini)

### Trend Template

Mark Minervini's famous trend template criteria for identifying stocks in strong uptrends.

**Criteria**:
- Price > 50-day SMA
- 50-day SMA > 150-day SMA
- 150-day SMA > 200-day SMA
- 200-day SMA trending up
- Price within 25% of 52-week high
- Price at least 30% above 52-week low
- IBD RS Rank > 70

---

## Brad Schulz

**Twitter**: [@BSchulz33868165](https://twitter.com/BSchulz33868165)

### Pocket Pivot

Identifies pocket pivot buy points based on volume analysis.

**Criteria**:
- Daily gain ≥ 5%
- Volume > 50-day EMA of volume
- Price > 200-day EMA
- Closes in upper half of daily range
- Pocket pivot indicator triggered

---

## Stockbee

**Twitter**: [@PradeepBonde](https://twitter.com/PradeepBonde)

### 4% Gainers

Stocks breaking out with 4%+ gains after consolidation.

**Criteria**:
- Daily gain > 4%
- Previous day gain ≤ 2%
- Expanding range vs previous day
- Volume > previous day
- Closes in upper 70% of range

### Combo Scan

Combines multiple Stockbee methodologies.

**Criteria**:
- Either 4% gainer criteria OR
- Strong range expansion with volume

### Ants

Stocks in tight consolidation with high trend intensity.

**Criteria**:
- Trend intensity > 1.04
- Price relatively flat (±1%) on the day
- Minimum 3-day volume > 100,000

### Breakout Scans (1M, 3M Base)

Stocks breaking out from consolidation bases.

**Criteria**:
- Consolidation within 10% range
- Breakout with 4%+ gain
- High volume
- Closes in upper range

---

## Ben (Pattern Profits)

**Twitter**: [@PatternProfits](https://twitter.com/PatternProfits)

### Power of 3

Stocks at key moving average support levels.

**Criteria**:
- Price within 1.5% of 10-day EMA
- Price within 1.5% of 21-day EMA
- Price within 1.5% of 50-day SMA
- IBD RS Rank ≥ 70

### Velocity

High-momentum stocks with strong relative strength.

**Criteria**:
- Daily gain > 3%
- Relative volume > 1.3x average
- IBD RS Rank > 70
- Float < 100M shares
- Trend intensity > 1.05

### Focus

Fundamentally strong stocks in leading industries.

**Criteria**:
- IBD Industry RS Rank > 70
- IBD 3M RS Rank > 70
- Earnings growth estimate ≥ 25%
- Revenue growth > 30%

---

## Ray

**Twitter**: [@RayTL_](https://twitter.com/RayTL_)

### RS New High Base Pullback (RSNHBP)

Stocks at relative strength highs pulling back from price highs.

**Variations**: 5D, 1M, 3M, 6M, 12M

**Criteria**:
- Relative strength at period high
- Price below period high (pullback)
- Minimum volume requirements
- Sorted by price gain from period low

---

## Blake Davis

**Twitter**: [@blakedavis50](https://twitter.com/blakedavis50)

### Strength

Stocks with strong relative strength and industry positioning.

**Criteria**:
- Price > $7
- IBD RS Rank > 70
- IBD Industry RS Rank > 50
- Closes in upper 70% of range
- Daily gain (positive)

---

## Leif Soreide

**Twitter**: [@LeifSoreide](https://twitter.com/LeifSoreide)

### HTF (High Tight Flag)

Stocks forming high tight flag patterns.

**Criteria**:
- Price > 50-day SMA
- 50-day SMA > 200-day SMA
- 200-day SMA trending up
- Volume declining
- 60-day gain > 50%
- 40-day gain > 90%
- Low volatility (NATR < 8)

---

## Vo

**Twitter**: [@LignoL23](https://twitter.com/LignoL23)

### Top Gainers

Highest percentage gainers meeting volume requirements.

### Top Gainers From Open

Stocks with largest intraday gains.

### Volume Gainers

Stocks with highest relative volume.

### 52W High

Stocks making new 52-week highs with volume.

### Darvas Scan

Based on Nicolas Darvas's box theory.

**Criteria**:
- Price within 15% of 52-week high
- 52-week gain ≥ 70%
- Strong sector relative strength
- High relative volume

### Quiet and Tight

Stocks in tight consolidation after strong moves.

**Criteria**:
- Declining volatility
- Low relative volume
- Strong prior trend
- Tight 3-week range

### Mo Scan

Momentum scan with moving average alignment.

**Criteria**:
- All key moving averages trending up
- Moving averages properly aligned
- Decreasing volatility
- Trend intensity > 1.05

---

## Custom Scan Parameters

All scans use configurable minimum requirements:

- **Minimum Price**: Scaled by market (typically $4 USD equivalent)
- **Minimum Volume**: 200,000 shares × market scale
- **Minimum Dollar Volume**: $2,000,000 × market scale
- **Average Volume**: 50-day SMA > minimum requirements

## Technical Indicators Used

- **SMA**: Simple Moving Average
- **EMA**: Exponential Moving Average
- **TI**: Trend Intensity
- **ADR**: Average Daily Range
- **ATR**: Average True Range
- **ROC**: Rate of Change
- **RS**: Relative Strength
- **NATR**: Normalized Average True Range
- **IBD Metrics**: Investor's Business Daily rankings

## Modifying Scans

To modify or add scans, edit the `src/scans.py` file. Each scan requires:

- `query`: Filter criteria in query language
- `order`: Sort field
- `limit`: Maximum number of results

Example:
```python
"My Custom Scan": {
    "query": "close>10 AND volume>100000 AND roc>5",
    "order": "volume",
    "limit": 100,
}
```

---

## Disclaimer

These scans are based on publicly shared methodologies. Always verify the current strategies from the original sources and do your own research before making investment decisions.
