# 🎰 Sports Betting Arbitrage — Live Reports

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
