import csv, random, math
from datetime import date, timedelta

random.seed(42)

CHANNELS = {
    'paid_search': {'ctr': 0.045, 'cvr_signup': 0.08, 'cvr_sale': 0.25, 'cpm': 18, 'base_impressions': 80000},
    'paid_social':  {'ctr': 0.018, 'cvr_signup': 0.05, 'cvr_sale': 0.15, 'cpm': 9,  'base_impressions': 150000},
    'display':      {'ctr': 0.005, 'cvr_signup': 0.03, 'cvr_sale': 0.10, 'cpm': 4,  'base_impressions': 300000},
    'email':        {'ctr': 0.022, 'cvr_signup': 0.12, 'cvr_sale': 0.35, 'cpm': 2,  'base_impressions': 50000},
    'video':        {'ctr': 0.008, 'cvr_signup': 0.04, 'cvr_sale': 0.12, 'cpm': 12, 'base_impressions': 200000},
}

CAMPAIGNS = ['brand_awareness_q1', 'summer_promo', 'retargeting_q2', 'new_product_launch']

start = date(2024, 1, 1)
rows = []

for day_offset in range(365):
    d = start + timedelta(days=day_offset)
    # Seasonal multiplier: peaks in summer and holiday season
    day_of_year = d.timetuple().tm_yday
    season = 1 + 0.3 * math.sin((day_of_year - 80) * 2 * math.pi / 365)
    # Weekend dip for search/display, boost for social
    is_weekend = d.weekday() >= 5

    for channel, params in CHANNELS.items():
        campaign = CAMPAIGNS[(day_offset // 90) % len(CAMPAIGNS)]
        weekend_factor = 0.75 if (channel in ('paid_search', 'display') and is_weekend) else (1.15 if (channel == 'paid_social' and is_weekend) else 1.0)

        impressions = int(params['base_impressions'] * season * weekend_factor * random.uniform(0.85, 1.15))
        clicks      = int(impressions * params['ctr'] * random.uniform(0.8, 1.2))
        signups     = int(clicks * params['cvr_signup'] * random.uniform(0.7, 1.3))
        sales       = int(signups * params['cvr_sale'] * random.uniform(0.6, 1.4))
        spend       = round(impressions / 1000 * params['cpm'] * random.uniform(0.95, 1.05), 2)

        rows.append({
            'date':        d.isoformat(),
            'campaign':    campaign,
            'channel':     channel,
            'impressions': impressions,
            'clicks':      clicks,
            'signups':     signups,
            'sales':       sales,
            'spend':       spend,
        })

with open('channels.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Written {len(rows)} rows to channels.csv")
print("Sample:")
for r in rows[:3]:
    print(r)
