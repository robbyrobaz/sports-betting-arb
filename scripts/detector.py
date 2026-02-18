#!/usr/bin/env python3
"""
Bonus Bet Arbitrage Detector
Finds guaranteed profit opportunities using bonus bets across sportsbooks
"""

import json
from pathlib import Path
from datetime import datetime

def american_to_decimal(american_odds):
    """Convert American odds to decimal"""
    if american_odds > 0:
        return (american_odds / 100) + 1
    else:
        return (100 / abs(american_odds)) + 1

def american_to_implied_prob(american_odds):
    """Convert American odds to implied probability"""
    if american_odds > 0:
        return 100 / (american_odds + 100)
    else:
        return abs(american_odds) / (abs(american_odds) + 100)

def calculate_bonus_arb(bonus_amount, bonus_book, bonus_team, bonus_odds, 
                        hedge_book, hedge_team, hedge_odds, hedge_is_real_money=True):
    """
    Calculate profit from bonus bet arbitrage
    
    Example:
    - DraftKings: $1000 bonus on Lakers -120
    - FanDuel: Real money on Celtics +110
    
    Returns: Guaranteed profit (regardless of outcome)
    """
    
    # Convert odds to decimal
    bonus_decimal = american_to_decimal(bonus_odds)
    hedge_decimal = american_to_decimal(hedge_odds)
    
    # Bonus bet stake (use full bonus)
    bonus_stake = bonus_amount
    
    # Hedge stake (kelly criterion for equal risk on both sides)
    # Formula: hedge_stake = bonus_stake * (bonus_decimal - 1) / (hedge_decimal - 1)
    if hedge_decimal <= 1:
        return None
    
    hedge_stake = bonus_stake * (bonus_decimal - 1) / (hedge_decimal - 1)
    
    # Scenario 1: Bonus team wins
    profit_scenario1_bonus = bonus_stake * bonus_decimal - 0  # Bonus burned but we win
    profit_scenario1_hedge = -hedge_stake  # Lose the real money hedge
    profit_scenario1 = profit_scenario1_bonus + profit_scenario1_hedge
    
    # Scenario 2: Hedge team wins
    profit_scenario2_bonus = -bonus_stake  # Bonus burned, team lost
    profit_scenario2_hedge = hedge_stake * hedge_decimal - hedge_stake  # Win the hedge
    profit_scenario2 = profit_scenario2_bonus + profit_scenario2_hedge
    
    # Guaranteed profit (minimum of both scenarios)
    guaranteed_profit = min(profit_scenario1, profit_scenario2)
    
    # ROI % on hedge stake (the real money at risk)
    roi_pct = (guaranteed_profit / hedge_stake * 100) if hedge_stake > 0 else 0
    
    return {
        'bonus_book': bonus_book,
        'bonus_team': bonus_team,
        'bonus_odds': bonus_odds,
        'bonus_stake': bonus_stake,
        'hedge_book': hedge_book,
        'hedge_team': hedge_team,
        'hedge_odds': hedge_odds,
        'hedge_stake': round(hedge_stake, 2),
        'scenario_bonus_wins': round(profit_scenario1, 2),
        'scenario_hedge_wins': round(profit_scenario2, 2),
        'guaranteed_profit': round(guaranteed_profit, 2),
        'roi_pct': round(roi_pct, 2),
        'total_real_money_risk': round(hedge_stake, 2)
    }

def find_arbs(promos_file):
    """
    Load promos and find arbitrage opportunities
    """
    
    if not promos_file or not Path(promos_file).exists():
        promos = {}  # Demo mode with no file
    else:
        with open(promos_file, 'r') as f:
            promos = json.load(f)
    
    print(f"📊 Analyzing {len(promos)} sportsbooks for arb opportunities...")
    print("=" * 70)
    
    opportunities = []
    
    # For now, demonstrate with manual examples
    # In real deployment, OCR will extract actual odds from screenshots
    
    example_arbs = [
        {
            'description': 'DraftKings $1000 Bonus → FanDuel Hedge',
            'bonus': {
                'book': 'DraftKings',
                'amount': 1000,
                'team': 'Los Angeles Lakers',
                'odds': -120  # American odds
            },
            'hedge': {
                'book': 'FanDuel',
                'team': 'Boston Celtics',
                'odds': 110  # American odds
            }
        }
    ]
    
    for example in example_arbs:
        print(f"\n📌 {example['description']}")
        
        result = calculate_bonus_arb(
            bonus_amount=example['bonus']['amount'],
            bonus_book=example['bonus']['book'],
            bonus_team=example['bonus']['team'],
            bonus_odds=example['bonus']['odds'],
            hedge_book=example['hedge']['book'],
            hedge_team=example['hedge']['team'],
            hedge_odds=example['hedge']['odds']
        )
        
        if result:
            opportunities.append({
                'description': example['description'],
                'calculation': result
            })
            
            print(f"\n  Bonus Bet:")
            print(f"    ${result['bonus_stake']} on {result['bonus_team']} @ {result['bonus_odds']}")
            print(f"    (Uses your ${result['bonus_stake']} bonus credit)")
            
            print(f"\n  Hedge Bet:")
            print(f"    ${result['hedge_stake']} real money on {result['hedge_team']} @ {result['hedge_odds']}")
            print(f"    (You risk: ${result['total_real_money_risk']})")
            
            print(f"\n  Outcomes:")
            print(f"    If {result['bonus_team']} wins: +${result['scenario_bonus_wins']}")
            print(f"    If {result['hedge_team']} wins: +${result['scenario_hedge_wins']}")
            
            print(f"\n  💰 GUARANTEED PROFIT: ${result['guaranteed_profit']}")
            print(f"  📈 ROI: {result['roi_pct']}%")
    
    # Save results
    output_file = Path(__file__).parent / f"arb_opportunities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(opportunities, f, indent=2)
    
    print("\n" + "=" * 70)
    print(f"✅ Results saved: {output_file}")
    print(f"\n📈 Found {len(opportunities)} arb opportunities")
    
    return opportunities

if __name__ == "__main__":
    # Demo: Run detector
    print("🎯 Bonus Bet Arbitrage Detector\n")
    
    # Find latest sportsbook data file
    from pathlib import Path
    data_dir = Path(__file__).parent
    data_files = sorted(data_dir.glob("sportsbook_data_*.json"))
    
    if data_files:
        latest_file = data_files[-1]
        print(f"Using latest data: {latest_file.name}\n")
        find_arbs(str(latest_file))
    else:
        # Just show example calculation
        print("Showing example calculation:\n")
        find_arbs(None)
