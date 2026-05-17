import csv, random, math
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

DATA = Path(__file__).parent.parent / 'data'
Q1_START = date(2024, 1, 1)
Q1_END   = date(2024, 3, 31)

# Channel config: partners with volume share, and per-channel benchmarks
CHANNELS = {
    'Paid Search': {
        'partners': {'Google': 0.78, 'Bing': 0.22},
        'base_impr': 55000, 'cpm': 22,  'ctr': 0.046, 'eng_rate': 0.012, 'cvr': 0.062, 'aov': 118,
    },
    'Paid Social': {
        'partners': {'Facebook': 0.48, 'Instagram': 0.33, 'TikTok': 0.19},
        'base_impr': 115000, 'cpm': 10, 'ctr': 0.018, 'eng_rate': 0.038, 'cvr': 0.026, 'aov': 82,
    },
    'Display': {
        'partners': {'Google Display Network': 0.62, 'The Trade Desk': 0.38},
        'base_impr': 240000, 'cpm': 4,  'ctr': 0.005, 'eng_rate': 0.005, 'cvr': 0.012, 'aov': 72,
    },
    'Email': {
        'partners': {'Mailchimp': 0.55, 'Klaviyo': 0.45},
        'base_impr': 38000,  'cpm': 1.5,'ctr': 0.210, 'eng_rate': 0.082, 'cvr': 0.042, 'aov': 96,
    },
    'Video': {
        'partners': {'YouTube': 0.65, 'Connected TV': 0.35},
        'base_impr': 175000, 'cpm': 18, 'ctr': 0.008, 'eng_rate': 0.255, 'cvr': 0.016, 'aov': 102,
    },
}

CAMPAIGNS = [
    {'name': 'New Year Push',     'start': date(2024, 1, 1),  'end': date(2024, 1, 21)},
    {'name': 'Brand Awareness',   'start': date(2024, 1, 1),  'end': date(2024, 3, 31)},
    {"name": "Valentine's Promo", 'start': date(2024, 2, 1),  'end': date(2024, 2, 14)},
    {'name': 'Spring Launch',     'start': date(2024, 3, 1),  'end': date(2024, 3, 31)},
]

ADS = {
    'New Year Push':     ['Fresh Start',         'Countdown Offer',   'Resolution Ready'],
    'Brand Awareness':   ['Hero Brand',           'Our Story',         'Why Choose Us'],
    "Valentine's Promo": ['Hearts and Savings',   'Gift Guide',        'Last Chance Love'],
    'Spring Launch':     ['Spring Into Savings',  'New Arrivals',      'Fresh Refresh'],
}

def day_multiplier(d):
    """Combines seasonality, day-of-week, and campaign-adjacent spikes."""
    # Slight new year dip then recovery
    yday = d.timetuple().tm_yday
    season = 0.85 + 0.15 * (yday / 91)

    # Weekend: social up, search/display down
    is_weekend = d.weekday() >= 5

    # Valentine's spike window
    if date(2024, 2, 10) <= d <= date(2024, 2, 14):
        promo_boost = 1.35
    elif date(2024, 2, 7) <= d <= date(2024, 2, 9):
        promo_boost = 1.15
    else:
        promo_boost = 1.0

    return season, is_weekend, promo_boost

def generate_row(d, campaign, channel_name, cfg, partner, partner_share, ad):
    season, is_weekend, promo_boost = day_multiplier(d)

    # Weekend adjustments per channel
    if channel_name == 'Paid Search':
        wknd = 0.72 if is_weekend else 1.0
    elif channel_name == 'Paid Social':
        wknd = 1.18 if is_weekend else 1.0
    elif channel_name == 'Email':
        wknd = 0.60 if is_weekend else 1.0   # email tanks on weekends
    else:
        wknd = 0.90 if is_weekend else 1.0

    # Valentine's only boosts promo-relevant channels
    pb = promo_boost if channel_name in ('Paid Social', 'Email', 'Display') else 1.0

    impr = int(cfg['base_impr'] * partner_share * season * wknd * pb * random.uniform(0.88, 1.12))
    clicks = int(impr * cfg['ctr'] * random.uniform(0.82, 1.18))
    spend = round(impr / 1000 * cfg['cpm'] * random.uniform(0.95, 1.05), 2)
    engagement = int(impr * cfg['eng_rate'] * random.uniform(0.75, 1.25))
    sales = int(clicks * cfg['cvr'] * random.uniform(0.70, 1.30))
    revenue = round(sales * cfg['aov'] * random.uniform(0.85, 1.15), 2)

    return {
        'day':        d.isoformat(),
        'campaign':   campaign,
        'channel':    channel_name,
        'partner':    partner,
        'ad':         ad,
        'impr':       impr,
        'clicks':     clicks,
        'spend':      spend,
        'engagement': engagement,
        'sales':      sales,
        'revenue':    revenue,
    }

rows = []
current = Q1_START
while current <= Q1_END:
    for camp in CAMPAIGNS:
        if not (camp['start'] <= current <= camp['end']):
            continue
        for ch_name, cfg in CHANNELS.items():
            for partner, share in cfg['partners'].items():
                for ad in ADS[camp['name']]:
                    rows.append(generate_row(current, camp['name'], ch_name, cfg, partner, share, ad))
    current += timedelta(days=1)

outfile = DATA / 'marketing_q1.csv'
with open(outfile, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows):,} rows to {outfile.name}")

# Sanity check
import collections
print(f"  Campaigns : {sorted(set(r['campaign'] for r in rows))}")
print(f"  Channels  : {sorted(set(r['channel'] for r in rows))}")
print(f"  Partners  : {sorted(set(r['partner'] for r in rows))}")
print(f"  Date range: {rows[0]['day']} → {rows[-1]['day']}")
total_spend = sum(r['spend'] for r in rows)
total_rev   = sum(r['revenue'] for r in rows)
print(f"  Total spend  : ${total_spend:,.0f}")
print(f"  Total revenue: ${total_rev:,.0f}")
print(f"  Overall ROAS : {total_rev/total_spend:.2f}x")
