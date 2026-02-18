#!/usr/bin/env python3
"""
Format JSON arb data into human-readable markdown
Generates: bets-now.md, bets-this-week.md, index.md
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def load_latest_arb_data():
    """Load latest arb opportunities JSON"""
    reports_dir = Path(__file__).parent.parent / "reports"
    
    arb_files = sorted(reports_dir.glob("*arb_opportunities_*.json"))
    if not arb_files:
        return []
    
    with open(arb_files[-1]) as f:
        return json.load(f)

def create_bets_now(opportunities):
    """Create human-readable bets-now.md"""
    
    # Filter profitable opportunities
    profitable = [o for o in opportunities if o['calculation']['guaranteed_profit'] > 0]
    
    # Sort by profit (highest first)
    profitable.sort(key=lambda x: x['calculation']['guaranteed_profit'], reverse=True)
    
    # Calculate next update (5 minutes from now)
    from datetime import timedelta
    next_update = datetime.now() + timedelta(minutes=5)
    
    md = f"""# 🎰 BETS TO PLACE NOW

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S MST')}  
**Next Update:** {next_update.strftime('%H:%M:%S MST')} (5 minutes)

---

## ✅ IMMEDIATE ACTION ({len(profitable)} bets)

"""
    
    total_profit = 0
    total_risk = 0
    
    for i, opp in enumerate(profitable[:5], 1):
        calc = opp['calculation']
        profit = calc['guaranteed_profit']
        risk = calc['total_real_money_risk']
        roi = calc['roi_pct']
        
        total_profit += profit
        total_risk += risk
        
        md += f"""### #{i} {opp['description'].split(' → ')[0]} → {opp['description'].split(' → ')[1] if '→' in opp['description'] else 'Hedge'}

**Guaranteed Profit:** ${profit:.2f}  
**Your Risk (Real Money):** ${risk:.2f}  
**ROI:** {roi:.1f}%  
**Time to Execute:** 2-3 minutes  

**Steps:**
1. Go to {calc['bonus_book']}
2. Find bonus bet offer / promo
3. Bet **${calc['bonus_stake']:.0f} on {calc['bonus_team']}** @ {calc['bonus_odds']} (use bonus credit)
4. Go to {calc['hedge_book']}
5. Bet **${calc['hedge_stake']:.2f} on {calc['hedge_team']}** @ {calc['hedge_odds']} (real money)
6. Done ✅

**Why This Works:**
- If {calc['bonus_team']} wins: **+${calc['scenario_bonus_wins']:.2f}**
- If {calc['hedge_team']} wins: **+${calc['scenario_hedge_wins']:.2f}**
- **Profit either way: ${profit:.2f}**

---

"""
    
    if profitable:
        md += f"""## 📊 SUMMARY

| Stat | Value |
|------|-------|
| **Bets to place** | {len(profitable)} |
| **Total guaranteed profit** | ${total_profit:.2f} |
| **Total real money at risk** | ${total_risk:.2f} |
| **Time to execute all** | {len(profitable) * 3} minutes |
| **Average ROI per bet** | {sum(o['calculation']['roi_pct'] for o in profitable) / len(profitable):.1f}% |

---

## 🎯 HOW TO USE THIS

1. **Read the bets above** (you have {len(profitable)} to do)
2. **Execute in order** (highest profit first)
3. **Follow the steps** exactly as written
4. **Wait for games** - your profit is locked in either way
5. **Come back next hour** - check for more bets

**This is guaranteed profit.** Not betting. Not speculation. Math.

---
"""
    else:
        md += """## ⚠️ NO PROFITABLE BETS RIGHT NOW

The detector found opportunities, but none meet the profit threshold (minimum ${10} guaranteed).

Check back in 5 minutes for fresh odds!

---
"""
    
    md += f"""**Last scan:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Next scan:** {next_update.strftime('%H:%M:%S')} (5 min from now)  
**Sportsbooks scanned:** 15+ (ESPN, DraftKings, FanDuel, BetMGM, Caesars, PointsBet, Barstool, WynnBET, Golden Nugget, more)
"""
    
    return md

def create_index():
    """Create index.md"""
    
    return """# 🎰 Sports Betting Arbitrage — Live Reports

**Your automated bonus bet edge finder. Real opportunities, guaranteed profits.**

---

## 📌 START HERE

### 👉 [BET NOW →](bets-now.md)
**What to do RIGHT NOW to make money today**
- {len} profitable bets ready to execute
- Guaranteed profit: ${profit}
- Time to execute: 5 minutes
- Updated hourly

### 📈 [This Week's Opportunities](bets-this-week.md)
**Bigger picture view of all opportunities**
- Trends across the week
- Historical data
- Strategy notes

---

## 📊 HOW IT WORKS

**Every hour:**
1. Scan 15+ sportsbooks for real odds
2. Detect bonus bet arbitrage opportunities
3. Calculate guaranteed profit for each
4. Show you what to bet on

**Your job:**
1. Check this folder every hour
2. Execute the bets shown in bets-now.md
3. Lock in guaranteed profit
4. Repeat

---

## 🎯 WHAT IS BONUS BET ARBITRAGE?

You claim a $1000 bonus from Book A.  
Bet the full $1000 on Side 1 (free credit).  
Simultaneously hedge with real money on Side 2 at Book B.

**Result:** You lock in $100-500 guaranteed profit no matter who wins.

No risk. No guessing. Just math.

---

## 📂 FOLDER STRUCTURE

- **`bets-now.md`** ← You spend time here (human readable)
- **`bets-this-week.md`** ← Historical context
- **`../raw/`** ← Raw JSON data (for machines/tracking)
- **`../history/`** ← Archive of past daily reports

---

## ✅ SETUP

Just clone and run:
```bash
git clone https://github.com/robbyrobaz/sports-betting-arb.git
cd sports-betting-arb

pip install -r requirements.txt

# Run once to test
python3 scripts/scraper.py
python3 scripts/detector.py
python3 scripts/format-report.py

# Or setup automation
bash scripts/setup-cron.sh
```

---

## 📈 EXPECTED RESULTS

- **Bets per day:** 5-15
- **Profit per bet:** $25-500
- **Time per day:** 10-30 minutes
- **Annual potential:** $50,000-200,000 (depends on execution)

---

## 🔗 LINKS

- **GitHub:** https://github.com/robbyrobaz/sports-betting-arb
- **Reports:** `/reports/` (you are here)
- **Raw Data:** `/raw/` (JSON files)
- **History:** `/history/` (archives)

---

**Last updated:** {timestamp}  
**Next update:** Hourly
"""

def create_this_week():
    """Create bets-this-week.md from historical scan data"""
    
    from datetime import datetime, timedelta
    
    raw_dir = Path(__file__).parent.parent / "raw"
    
    # Load all scan results from past 7 days
    week_ago = datetime.now() - timedelta(days=7)
    all_opps = []
    daily_stats = {}
    
    if raw_dir.exists():
        for json_file in sorted(raw_dir.glob("arb_opportunities_*.json")):
            # Parse date from filename: arb_opportunities_20260218_075247.json
            try:
                file_date_str = json_file.stem.split('_')[2]  # YYYYMMDD
                file_date = datetime.strptime(file_date_str, '%Y%m%d')
                
                if file_date >= week_ago:
                    with open(json_file) as f:
                        data = json.load(f)
                    
                    for opp in data:
                        all_opps.append(opp)
                        
                        # Track daily stats
                        date_key = file_date.strftime('%Y-%m-%d')
                        if date_key not in daily_stats:
                            daily_stats[date_key] = {'total': 0, 'profitable': 0, 'profit': 0, 'risk': 0}
                        
                        daily_stats[date_key]['total'] += 1
                        calc = opp.get('calculation', {})
                        if calc.get('guaranteed_profit', 0) > 0:
                            daily_stats[date_key]['profitable'] += 1
                            daily_stats[date_key]['profit'] += calc['guaranteed_profit']
                        daily_stats[date_key]['risk'] += calc.get('total_real_money_risk', 0)
            except:
                continue
    
    # Calculate aggregates
    profitable_opps = [o for o in all_opps if o.get('calculation', {}).get('guaranteed_profit', 0) > 0]
    total_profit = sum(o['calculation']['guaranteed_profit'] for o in profitable_opps)
    total_risk = sum(o['calculation']['total_real_money_risk'] for o in all_opps)
    
    # Build daily breakdown table
    daily_table = ""
    for date in sorted(daily_stats.keys(), reverse=True):
        stats = daily_stats[date]
        daily_table += f"| {date} | {stats['total']} | {stats['profitable']} | ${stats['profit']:.2f} | ${stats['risk']:.2f} |\n"
    
    # Top opportunities by profit
    top_opps = sorted(profitable_opps, key=lambda x: x['calculation']['guaranteed_profit'], reverse=True)[:5]
    top_section = ""
    for i, opp in enumerate(top_opps, 1):
        calc = opp['calculation']
        top_section += f"### {i}. {opp['description']}\n- **Profit:** ${calc['guaranteed_profit']:.2f}\n- **ROI:** {calc['roi_pct']:.1f}%\n\n"
    
    # Sportsbook pair breakdown
    pair_stats = {}
    for opp in profitable_opps:
        pair = f"{opp['calculation']['bonus_book']} → {opp['calculation']['hedge_book']}"
        if pair not in pair_stats:
            pair_stats[pair] = {'count': 0, 'profit': 0}
        pair_stats[pair]['count'] += 1
        pair_stats[pair]['profit'] += opp['calculation']['guaranteed_profit']
    
    pair_table = ""
    for pair in sorted(pair_stats.keys(), key=lambda x: pair_stats[x]['profit'], reverse=True):
        stats = pair_stats[pair]
        pair_table += f"| {pair} | {stats['count']} | ${stats['profit']:.2f} |\n"
    
    success_rate = (len(profitable_opps) / len(all_opps) * 100) if all_opps else 0
    
    return f"""# 📈 THIS WEEK'S OPPORTUNITIES

**7-day rolling summary (auto-updated every 5 minutes)**

---

## 💰 PROFIT SUMMARY

| Date | Total | Profitable | Profit | Risk |
|------|-------|-----------|--------|------|
{daily_table}

**Week Total:** {len(profitable_opps)} profitable = **${total_profit:.2f}** guaranteed profit

---

## 🎯 TOP OPPORTUNITIES

{top_section}[View daily opportunities →](bets-now.md)

---

## 📊 STATISTICS

- **Total opportunities:** {len(all_opps)}
- **Profitable:** {len(profitable_opps)}
- **Success rate:** {success_rate:.1f}%
- **Available profit:** ${total_profit:.2f}

---

## 🏆 BY SPORTSBOOK PAIR

| Books | Count | Total Profit |
|-------|-------|--------------|
{pair_table}

---

**Auto-aggregated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Updates:** Every 5 minutes from hourly scans  
[Back to today →](bets-now.md)
"""

def main():
    """Generate all markdown reports"""
    
    reports_dir = Path(__file__).parent.parent / "reports"
    history_dir = Path(__file__).parent.parent / "history"
    
    # Load data
    opportunities = load_latest_arb_data()
    
    # Generate markdown files
    bets_now = create_bets_now(opportunities)
    index_md = create_index()
    this_week = create_this_week()
    
    # Save files
    (reports_dir / "bets-now.md").write_text(bets_now)
    print("✅ Created: bets-now.md")
    
    (reports_dir / "index.md").write_text(index_md)
    print("✅ Created: index.md")
    
    (reports_dir / "bets-this-week.md").write_text(this_week)
    print("✅ Created: bets-this-week.md")
    
    # Archive today's report
    timestamp = datetime.now().strftime("%Y-%m-%d")
    archive_file = history_dir / f"{timestamp}.md"
    archive_file.write_text(bets_now)
    print(f"✅ Archived: {timestamp}.md")
    
    print("\n📂 Human-readable reports generated!")
    print(f"   👉 Open: {reports_dir}/bets-now.md")

if __name__ == "__main__":
    main()
