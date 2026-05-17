import csv, random
from pathlib import Path

random.seed(7)
DATA = Path(__file__).parent.parent / 'data'

CHANNEL_VARIANTS = {
    'Paid Search':  ['paid_search', 'PaidSearch', 'Search', 'SEM', 'paid search'],
    'Paid Social':  ['paid_social', 'PaidSocial', 'Social', 'Social Ads', 'paid social'],
    'Display':      ['display',     'Display Ads', 'DISPLAY', 'Banner', 'display ads'],
    'Email':        ['email',       'EMAIL',       'E-Mail',  'eMail',  'Email Marketing'],
    'Video':        ['video',       'VIDEO',       'Video Ads','vid',   'online video'],
}

PARTNER_VARIANTS = {
    'Google':                    ['google', 'GOOGLE', 'Google Ads', 'Goog'],
    'Bing':                      ['bing', 'BING', 'Microsoft Ads', 'Bing Ads'],
    'Facebook':                  ['facebook', 'FB', 'FACEBOOK', 'Meta'],
    'Instagram':                 ['instagram', 'IG', 'INSTAGRAM', 'Insta'],
    'TikTok':                    ['tiktok', 'TIKTOK', 'Tik Tok', 'TT'],
    'Google Display Network':    ['GDN', 'google display', 'Google Display', 'google_display_network'],
    'The Trade Desk':            ['TTD', 'Trade Desk', 'the_trade_desk', 'TradeDesk'],
    'Mailchimp':                 ['mailchimp', 'MailChimp', 'MAILCHIMP', 'mail chimp'],
    'Klaviyo':                   ['klaviyo', 'KLAVIYO', 'Klayvio', 'Klaviyo'],  # note: Klayvio is a common misspelling
    'YouTube':                   ['youtube', 'YOUTUBE', 'YT', 'Youtube'],
    'Connected TV':              ['CTV', 'ctv', 'connected_tv', 'ConnectedTV'],
}

CAMPAIGN_VARIANTS = {
    'New Year Push':     ['new_year_push',    'NewYearPush',    'New Year',       'NY Push'],
    'Brand Awareness':   ['brand_awareness',  'BrandAwareness', 'Branding',       'brand awareness'],
    "Valentine's Promo": ['valentines_promo', 'ValentinesPromo','Valentines',     "valentine's promo"],
    'Spring Launch':     ['spring_launch',    'SpringLaunch',   'Spring',         'spring launch'],
}

def bad_choice(variants):
    return random.choice(variants) if variants else ''

def jitter(val):
    try:
        f = float(val)
        noise = random.choice([1e-7, 1e-6, 1e-5]) * random.uniform(1, 9)
        return str(f + noise)
    except (ValueError, TypeError):
        return val

with open(DATA / 'marketing_q1.csv') as f:
    rows = list(csv.DictReader(f))
    fieldnames = list(rows[0].keys())

out = []
for row in rows:
    r = dict(row)

    # ~20%: swap impr and clicks
    if random.random() < 0.20:
        r['impr'], r['clicks'] = r['clicks'], r['impr']

    # ~25%: mangle channel name
    if random.random() < 0.25:
        variants = CHANNEL_VARIANTS.get(r['channel'], [])
        if variants:
            r['channel'] = bad_choice(variants)

    # ~25%: mangle partner name
    if random.random() < 0.25:
        variants = PARTNER_VARIANTS.get(r['partner'], [])
        if variants:
            r['partner'] = bad_choice(variants)

    # ~20%: mangle campaign name
    if random.random() < 0.20:
        variants = CAMPAIGN_VARIANTS.get(r['campaign'], [])
        if variants:
            r['campaign'] = bad_choice(variants)

    # ~15%: decimal noise on spend or revenue
    if random.random() < 0.15:
        r['spend'] = jitter(r['spend'])
    if random.random() < 0.10:
        r['revenue'] = jitter(r['revenue'])

    # ~8%: sales or engagement stored as float
    if random.random() < 0.08:
        try:
            r['sales'] = str(float(r['sales']))
        except ValueError:
            pass

    # ~5%: date format changed
    if random.random() < 0.05:
        try:
            y, m, d = r['day'].split('-')
            r['day'] = random.choice([
                f'{m}/{d}/{y}',          # US format
                f'{d}-{m}-{y}',          # DD-MM-YYYY
                f'{m}.{d}.{y}',          # dots
            ])
        except Exception:
            pass

    out.append(r)

outfile = DATA / 'marketing_q1_toFix.csv'
with open(outfile, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(out)

# Summary of damage
swapped   = sum(1 for r in out if r['impr'].isdigit() and r['clicks'].isdigit() and int(r['impr']) < int(r['clicks']))
ch_vars   = len(set(r['channel'] for r in out))
part_vars = len(set(r['partner'] for r in out))
camp_vars = len(set(r['campaign'] for r in out))

print(f"Wrote {len(out):,} rows to {outfile.name}")
print(f"  Rows with clicks > impr (swapped): {swapped}")
print(f"  Channel name variants : {ch_vars}")
print(f"  Partner name variants : {part_vars}")
print(f"  Campaign name variants: {camp_vars}")
