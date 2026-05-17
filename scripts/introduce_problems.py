import csv, random, re
from pathlib import Path

random.seed(7)
DATA = Path(__file__).parent.parent / 'data'

def bad_choice(variants):
    """Pick a wrong variant; skip if no alternatives exist."""
    alts = variants[:-1]
    return random.choice(alts) if alts else variants[0]

def jitter_decimal(val, extra_places=8):
    """Add floating point noise to a numeric string."""
    try:
        f = float(val)
        return str(f + random.uniform(-0.000001, 0.000001) * 10 ** random.randint(0, 4))
    except (ValueError, TypeError):
        return val

def corrupt_channels():
    CHANNEL_VARIANTS = {
        'paid_search': ['Paid Search', 'PaidSearch', 'paid-search', 'search_paid', 'paid_search'],
        'paid_social':  ['Paid Social', 'Social Paid', 'paid-social', 'social', 'paid_social'],
        'display':      ['Display Ads', 'DISPLAY', 'display_ads', 'banner', 'display'],
        'email':        ['Email', 'EMAIL', 'e-mail', 'eMail', 'email'],
        'video':        ['Video Ads', 'VIDEO', 'video_ads', 'Video', 'video'],
    }
    CAMPAIGN_VARIANTS = {
        'brand_awareness_q1': ['Brand Awareness Q1', 'brand-awareness-q1', 'BrandAwarenessQ1', 'brand_awareness_q1'],
        'summer_promo':        ['Summer Promo', 'SummerPromo', 'summer-promo', 'summer_promo'],
        'retargeting_q2':      ['Retargeting Q2', 'retargeting-q2', 'RetargetingQ2', 'retargeting_q2'],
        'new_product_launch':  ['New Product Launch', 'new-product-launch', 'NewProductLaunch', 'new_product_launch'],
    }

    with open(DATA / 'channels.csv') as f:
        rows = list(csv.DictReader(f))

    out = []
    for i, row in enumerate(rows):
        r = dict(row)

        # ~20% chance: swap impressions and clicks
        if random.random() < 0.20:
            r['impressions'], r['clicks'] = r['clicks'], r['impressions']

        # ~25% chance: mangle channel name
        if random.random() < 0.25:
            variants = CHANNEL_VARIANTS.get(r['channel'], [r['channel']])
            r['channel'] = bad_choice(variants)  # exclude the correct one

        # ~20% chance: mangle campaign name
        if random.random() < 0.20:
            variants = CAMPAIGN_VARIANTS.get(r['campaign'], [r['campaign']])
            r['campaign'] = bad_choice(variants)

        # ~15% chance: decimal noise on spend
        if random.random() < 0.15:
            r['spend'] = jitter_decimal(r['spend'])

        # ~10% chance: signups or sales stored as float
        if random.random() < 0.10:
            try:
                r['signups'] = str(float(r['signups'])) + '0'
            except ValueError:
                pass

        out.append(r)

    with open(DATA / 'channels_toFix.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(out)

    print(f"channels_toFix.csv  — {len(out)} rows")


def corrupt_ad_campaigns():
    GENDER_VARIANTS = {
        'M': ['Male', 'male', 'MALE', 'm', 'M'],
        'F': ['Female', 'female', 'FEMALE', 'f', 'F'],
    }
    AGE_VARIANTS = {
        '30-34': ['30 to 34', '30-34 yrs', 'Ages 30-34', '30-34'],
        '35-39': ['35 to 39', '35-39 yrs', 'Ages 35-39', '35-39'],
        '40-44': ['40 to 44', '40-44 yrs', 'Ages 40-44', '40-44'],
        '45-49': ['45 to 49', '45-49 yrs', 'Ages 45-49', '45-49'],
    }

    with open(DATA / 'ad_campaigns.csv') as f:
        rows = list(csv.DictReader(f))

    out = []
    for row in rows:
        r = dict(row)

        # ~25% chance: swap Impressions and Clicks
        if random.random() < 0.25:
            r['Impressions'], r['Clicks'] = r['Clicks'], r['Impressions']

        # ~30% chance: mangle gender
        if random.random() < 0.30:
            variants = GENDER_VARIANTS.get(r['gender'], [r['gender']])
            r['gender'] = bad_choice(variants)

        # ~20% chance: mangle age range format
        if random.random() < 0.20:
            variants = AGE_VARIANTS.get(r['age'], [r['age']])
            r['age'] = bad_choice(variants)

        # ~15% chance: Spent has excessive decimal places
        if random.random() < 0.15:
            r['Spent'] = jitter_decimal(r['Spent'])

        # ~8% chance: Total_Conversion stored as float string
        if random.random() < 0.08:
            try:
                r['Total_Conversion'] = str(float(r['Total_Conversion']))
            except ValueError:
                pass

        out.append(r)

    with open(DATA / 'ad_campaigns_toFix.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(out)

    print(f"ad_campaigns_toFix.csv — {len(out)} rows")


def corrupt_superstore():
    REGION_VARIANTS = {
        'South':   ['south', 'SOUTH', 'Southern', 'Southern Region', 'South'],
        'North':   ['north', 'NORTH', 'Northern', 'Northern Region', 'North'],
        'East':    ['east',  'EAST',  'Eastern',  'Eastern Region',  'East'],
        'West':    ['west',  'WEST',  'Western',  'Western Region',  'West'],
        'Central': ['central', 'CENTRAL', 'Central Region', 'Central'],
    }
    CATEGORY_VARIANTS = {
        'Furniture':        ['furniture', 'FURNITURE', 'Furnishings', 'Furniture'],
        'Technology':       ['technology', 'TECHNOLOGY', 'Tech', 'Technology'],
        'Office Supplies':  ['office supplies', 'OFFICE SUPPLIES', 'Office_Supplies', 'Supplies', 'Office Supplies'],
    }
    SHIP_VARIANTS = {
        'Second Class': ['2nd Class', 'second class', 'SECOND CLASS', 'Second Class'],
        'First Class':  ['1st Class', 'first class',  'FIRST CLASS',  'First Class'],
        'Standard Class': ['Standard', 'standard class', 'Std Class', 'Standard Class'],
        'Same Day':     ['Sameday', 'same day', 'SAME DAY', 'Same Day'],
    }

    with open(DATA / 'superstore.csv') as f:
        rows = list(csv.DictReader(f))

    out = []
    for row in rows:
        r = dict(row)

        # ~20% chance: mangle Region
        if random.random() < 0.20:
            variants = REGION_VARIANTS.get(r['Region'], [r['Region']])
            r['Region'] = bad_choice(variants)

        # ~15% chance: mangle Category
        if random.random() < 0.15:
            variants = CATEGORY_VARIANTS.get(r['Category'], [r['Category']])
            r['Category'] = bad_choice(variants)

        # ~15% chance: mangle Ship Mode
        if random.random() < 0.15:
            variants = SHIP_VARIANTS.get(r['Ship Mode'], [r['Ship Mode']])
            r['Ship Mode'] = bad_choice(variants)

        # ~10% chance: decimal noise on Sales
        if random.random() < 0.10:
            r['Sales'] = jitter_decimal(r['Sales'])

        # ~10% chance: Order Date format changed
        if random.random() < 0.10:
            date_str = r['Order Date']
            try:
                m, d, y = date_str.split('/')
                r['Order Date'] = random.choice([
                    f'{y}-{m.zfill(2)}-{d.zfill(2)}',   # ISO
                    f'{d.zfill(2)}-{m.zfill(2)}-{y}',   # DD-MM-YYYY
                    f'{m.zfill(2)}.{d.zfill(2)}.{y}',   # dots
                ])
            except Exception:
                pass

        out.append(r)

    with open(DATA / 'superstore_toFix.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(out)

    print(f"superstore_toFix.csv   — {len(out)} rows")


corrupt_channels()
corrupt_ad_campaigns()
corrupt_superstore()
print("Done.")
