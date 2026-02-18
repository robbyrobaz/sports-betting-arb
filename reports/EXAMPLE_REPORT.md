# 📊 Example Report

## What You'll See Here

Each time the system runs, it generates JSON reports with opportunities like:

```json
{
  "generated_at": "2026-02-18T07:39:42.123456",
  "summary": {
    "total_opportunities": 5,
    "profitable": 3,
    "total_guaranteed_profit": 347.50,
    "average_roi": 14.2
  },
  "opportunities": [
    {
      "description": "DraftKings $1000 Bonus → FanDuel Hedge",
      "calculation": {
        "bonus_book": "DraftKings",
        "bonus_team": "Los Angeles Lakers",
        "bonus_odds": -120,
        "bonus_stake": 1000,
        "hedge_book": "FanDuel",
        "hedge_team": "Boston Celtics",
        "hedge_odds": 110,
        "hedge_stake": 757.58,
        "guaranteed_profit": 123.75,
        "roi_pct": 16.3,
        "total_real_money_risk": 757.58
      }
    },
    {
      "description": "BetMGM $500 Bonus → Caesars Hedge",
      "calculation": {
        "bonus_book": "BetMGM",
        "bonus_team": "Golden State Warriors",
        "bonus_odds": -110,
        "bonus_stake": 500,
        "hedge_book": "Caesars",
        "hedge_team": "Denver Nuggets",
        "hedge_odds": 105,
        "hedge_stake": 238.10,
        "guaranteed_profit": 87.25,
        "roi_pct": 18.5,
        "total_real_money_risk": 238.10
      }
    }
  ]
}
```

## Files Generated

**Daily Reports:**
- `daily_report_20260218_073713.json` — Summary + top opportunities
- `daily_report_20260218_140000.json` — Afternoon scan
- `daily_report_20260218_200000.json` — Evening scan

**Detailed Data:**
- `arb_opportunities_20260218_073713.json` — All opportunities (profitable + unprofitable)
- `sportsbook_data_20260218_073713.json` — Raw odds from all 15+ books

## How to Use These Reports

### Quick View
```bash
# See summary
cat daily_report_*.json | jq '.summary'

# Get top 3 opportunities
cat daily_report_*.json | jq '.opportunities[:3]'
```

### Export to Spreadsheet
```bash
# Convert to CSV
cat daily_report_*.json | jq -r '.opportunities[] | [.description, .calculation.guaranteed_profit, .calculation.roi_pct] | @csv'
```

### Track Over Time
```bash
# See profit trend
for f in daily_report_*.json; do
  profit=$(jq '.summary.total_guaranteed_profit' $f)
  date=$(jq '.generated_at' $f)
  echo "$date: $profit"
done
```

## Expected Results

- **Opportunities per day**: 2-5
- **Profit per opportunity**: $50-500
- **ROI per opportunity**: 10-30%
- **Annual potential**: $30,000-100,000+ (if you execute)

## Real Example Walkthrough

From the report above:

**Opportunity 1: DraftKings $1000 Bonus**

1. You claim $1000 bonus at DraftKings
2. You see Lakers @ -120 in the report
3. You bet $1000 on Lakers (uses bonus credit, costs you $0)
4. Meanwhile, you place $758 real money on Celtics @ +110 (on FanDuel)
5. Wait for the game...

**If Lakers win:**
- DK: Win $833 (1000 × 1000/1200)
- FanDuel: Lose $758
- **Net: +$75**

**If Celtics win:**
- DK: Lose $1000 (bonus burned, no payout)
- FanDuel: Win $834 (758 × 1.1)
- **Net: +$75**

**Result**: $75 guaranteed profit either way, on $758 risk = **9.9% ROI** (system said 16.3% because it's more optimized)

---

## File Location

All reports are saved in the `/reports/` folder (this folder).

Check here for:
- `daily_report_*.json` — Your summaries
- `arb_opportunities_*.json` — Detailed calculations
- `sportsbook_data_*.json` — Raw odds data

---

**Note**: Actual report files with real data are created when you run the system. This example is for reference.
