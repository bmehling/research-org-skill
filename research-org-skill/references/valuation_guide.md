# Valuation Estimation Guide

When funding valuations aren't publicly disclosed, estimate them using raise-to-valuation ratios from disclosed rounds.

## Estimation Method

**Formula:**
```
Ratio = Amount Raised / Post-Money Valuation
Estimated Valuation = Amount Raised / Ratio
```

**Example:**
```
Known: Series C raised $80M at $1.6B valuation → Ratio = 0.05 (5%)
Unknown: Series D raised $125M → Estimated = $125M / 0.05 = $2.5B
```

**When multiple rounds have disclosed valuations:**
- Calculate ratio for each
- Use median ratio (exclude outliers like down rounds or unusual market conditions)
- Apply median to estimate unknown rounds

**Mark all estimates clearly:** Use `~$X (estimated)` format in tables.

## Funding Table Format

Always use HTML `<table>` format (not pipe tables) for proper Notion rendering:

```markdown
<table header-row="true">
<tr>
<td>Round</td>
<td>Date</td>
<td>Amount Raised</td>
<td>Post-Money Valuation</td>
<td>Lead Investors</td>
<td>Notes</td>
</tr>
<tr>
<td>Seed</td>
<td>Q1 2020</td>
<td>$3M</td>
<td>~$15M (estimated)</td>
<td>Investor Name</td>
<td>First institutional round</td>
</tr>
<tr>
<td>Series A</td>
<td>Q3 2021</td>
<td>$15M</td>
<td>$75M</td>
<td>Investor Name</td>
<td></td>
</tr>
</table>
```

**Valuation column formatting:**
- Disclosed: `$1.6B`
- Estimated: `~$1.0B (estimated)`
- Unknown: `Not available`
- Down round: `$800M (down from $1.6B)`

**Below the table, include:**
```
**Total Funding:** $XXM across N rounds
**Current Valuation:** ~$X.XB (estimated) or $X.XB (disclosed)
**Key Investors:** Names...
```

## Confidence Levels

| Confidence | Criteria |
|------------|----------|
| High | 3+ disclosed rounds with consistent ratios |
| Medium | 1-2 disclosed rounds, reasonable ratio |
| Low | Single data point or major market shifts between rounds |

For low-confidence estimates, note limitations in the valuation analysis section.
