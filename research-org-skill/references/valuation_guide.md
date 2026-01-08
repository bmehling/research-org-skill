# Valuation Estimation Guide

This guide provides methodology for estimating missing funding valuations.

## Valuation Estimation Methodology

### Overview

Funding valuations are not always publicly disclosed, particularly for earlier-stage companies. When valuations are missing, we can estimate them using the raise-to-valuation ratios observed in disclosed rounds.

**Key Principle:** Estimation should be transparent, methodical, and clearly marked as such in the research.

### Valuation Estimation Workflow

**Step 1: Identify All Known Valuations**

From research, extract all rounds with disclosed valuations:

```
Example: Cresta funding data
- Seed (2020): Amount unknown, Valuation unknown
- Series A (2021): Amount unknown, Valuation unknown
- Series B (2021): Amount unknown, Valuation unknown
- Series C (March 2022): $80M raised, $1.6B valuation → Ratio: 1:20 (or 5% of valuation)
- Series D (Nov 2024): $125M raised, Valuation unknown
```

**Step 2: Calculate Raise:Valuation Ratios**

For each round with both raise amount and valuation, calculate the ratio:

```
Ratio = Amount Raised / Post-Money Valuation

Cresta Series C: $80M / $1.6B = 0.05 (or 5%, or "1:20")
```

This means: In Series C, they raised capital equal to 5% of their post-money valuation.

**Step 3: Determine Median or Average Ratio**

If multiple rounds have disclosed valuations, calculate the median ratio:

```
Example with multiple known rounds:
- Series A: $5M / $25M = 0.20 (20%)
- Series B: $10M / $50M = 0.20 (20%)
- Series C: $80M / $1.6B = 0.05 (5%)

Median: 0.20 (ignoring outlier Series C with different market conditions)
```

**Step 4: Apply Ratio to Estimate Missing Valuations**

For rounds missing valuations, divide the raised amount by the median ratio:

```
Estimated Valuation = Amount Raised / Median Ratio

If Seed was $2M with median ratio of 0.20:
Estimated Valuation = $2M / 0.20 = $10M (estimated)

If Series D was $125M and we use 0.20 ratio:
Estimated Valuation = $125M / 0.20 = $625M (estimated)
```

**Note:** Some later-stage rounds may have different ratios due to market conditions (2021 vs. 2024). If possible, use the ratio from the most recent disclosed round for the most recent unknown rounds.

### Special Cases

**Series with Only One Known Data Point**

If only one round has both raise and valuation data, use that ratio for all estimations. Mark these estimations with higher uncertainty:

```
Example: If only Series C has valuation data
- Mark all estimates as "~$X (estimated from Series C ratio)"
- Note in methodology that this is based on single data point
- Consider whether Series C ratio is representative
```

**Rounds with Extreme Ratios**

Some rounds may have unusual ratios due to:
- Down rounds (company raised at lower valuation than previous round)
- Strategic rounds with special terms
- Acquisition scenarios

When you encounter extreme ratios:
1. Note them but potentially exclude from median calculation
2. If down round is followed by recovery, use later ratios
3. Document your methodology in the notes

**Post-IPO or Recently Acquired Companies**

If the company went public or was acquired:
- Use actual market valuation (for public companies) or acquisition price (for acquired)
- Mark clearly that valuation is from alternative source
- Note the date of IPO/acquisition

### Methodology Documentation

In the funding table, include a note below explaining the estimation approach:

```
**Valuation Estimation Methodology:**
Estimations for rounds lacking disclosed valuations were calculated using 
the median raise:valuation ratio of 0.15 (15%) observed across disclosed rounds 
(Series A: $5M/$25M, Series B: $10M/$50M). Series C ratio of 0.05 was excluded 
as an outlier potentially reflecting 2022 market conditions. Estimated valuations 
are marked with "~" and represent best-effort calculations from available data.
```

### Quality Indicators for Estimates

After estimation, assess the quality:

**High Confidence Estimates (✓✓✓):**
- Based on 3+ disclosed valuations with consistent ratios
- Recent rounds have consistent patterns
- Ratio is reasonable and not an extreme outlier

**Medium Confidence Estimates (✓✓):**
- Based on 1-2 disclosed valuations
- Ratio seems reasonable but limited data points
- Clear methodology documented

**Low Confidence Estimates (✓):**
- Based on single data point
- Company experienced significant pivots
- Market conditions very different from original round
- Mark these clearly and note limitations

---

## Part 3: Funding Table Format and Best Practices

### Table Structure

Create tables with these columns (in order):

| Round | Date | Amount Raised | Post-Money Valuation | Lead Investors | Notes |
|---|---|---|---|---|---|
| Seed | Q1 2020 | $X | ~$Y (estimated) | Name | Context |

### Valuation Column Details

**Format Guidance:**
- Disclosed valuations: `$1.6B`
- Estimated valuations: `~$1.0B (estimated)`
- Unknown valuations: `Not disclosed`
- Down rounds: `$800M (down from $1.6B)`
- Acquisition price: `$2.1B (acquisition)`

**Dating the Valuation:**
- Include the valuation date if different from round close date
- Note historical valuations: `$1.6B (March 2022)`

### Notes Column Examples

```
"Tiger Global led, with participation from Zoom, Genesys, Five9"
"Down round following market correction; existing investors participated"
"Strategic acquisition by Salesforce; all equity converted"
"Includes $20M secondary sales from early investors"
"Pro-rata round from existing investors"
```

### Total Funding Summary

Below the table, include a summary line:

```
**Total Funding:** $276M across 7 rounds
**Current Implied Valuation:** ~$2.0B (estimated from Series D round)
**Key Investors:** Andreessen Horowitz, Greylock Partners, Sequoia Capital, ...
```

---
