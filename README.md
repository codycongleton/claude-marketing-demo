# Claude Marketing Demo

Datasets and scripts for demonstrating Claude-powered marketing analytics.

## Datasets

| File | Rows | Description |
|------|------|-------------|
| `data/channels.csv` | 1,825 | Synthetic daily ad funnel data — impressions, clicks, signups, sales across 5 channels and 4 campaigns (full year 2024) |
| `data/ad_campaigns.csv` | 1,143 | Real Facebook ad campaign data — audience targeting by age, gender, interest with conversion metrics |
| `data/superstore.csv` | 10,800 | Tableau sample retail dataset — orders, customers, segments, regions, products, sales, profit |

## Channels dataset columns

`date`, `campaign`, `channel`, `impressions`, `clicks`, `signups`, `sales`, `spend`

Channels: `paid_search`, `paid_social`, `display`, `email`, `video`

Campaigns: `brand_awareness_q1`, `summer_promo`, `retargeting_q2`, `new_product_launch`

## Scripts

- `scripts/generate_channels.py` — regenerates `channels.csv` with configurable parameters
