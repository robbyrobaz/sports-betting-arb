#!/usr/bin/env python3
"""
Generate summary report from latest arb detection results
"""

import json
from pathlib import Path
from datetime import datetime

def generate_report():
    """Generate summary report"""
    
    reports_dir = Path(__file__).parent.parent / "reports"
    
    # Find latest arb results
    arb_files = sorted(reports_dir.glob("arb_opportunities_*.json"))
    
    if not arb_files:
        print("❌ No arb opportunities found yet. Run detector.py first.")
        return
    
    latest_arb_file = arb_files[-1]
    
    with open(latest_arb_file, 'r') as f:
        opportunities = json.load(f)
    
    # Find profitable arbs
    profitable = [o for o in opportunities if o['calculation']['guaranteed_profit'] > 0]
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'total_opportunities': len(opportunities),
            'profitable': len(profitable),
            'total_guaranteed_profit': sum(o['calculation']['guaranteed_profit'] for o in profitable),
            'average_roi': sum(o['calculation']['roi_pct'] for o in profitable) / len(profitable) if profitable else 0
        },
        'opportunities': profitable,
        'source_file': str(latest_arb_file.name)
    }
    
    # Save report
    report_file = reports_dir / f"daily_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 70)
    print("📊 REPORT GENERATED")
    print("=" * 70)
    print(f"\n✅ Summary:")
    print(f"   Total Opportunities: {report['summary']['total_opportunities']}")
    print(f"   Profitable: {report['summary']['profitable']}")
    print(f"   Total Guaranteed Profit: ${report['summary']['total_guaranteed_profit']:.2f}")
    if profitable:
        print(f"   Average ROI: {report['summary']['average_roi']:.1f}%")
    
    print(f"\n📂 Report saved: {report_file.name}")
    print(f"📂 Location: {reports_dir}/")
    
    # Print top opportunities
    if profitable:
        print(f"\n🎯 Top {min(3, len(profitable))} Opportunities:")
        for i, opp in enumerate(profitable[:3], 1):
            print(f"   {i}. {opp['description']}")
            print(f"      Guaranteed Profit: ${opp['calculation']['guaranteed_profit']:.2f}")
            print(f"      ROI: {opp['calculation']['roi_pct']:.1f}%")
    
    return report_file

if __name__ == "__main__":
    generate_report()
