from typing import Dict


def process_stats(ad_requests: Dict[str, int], impressions: Dict[str, int]):
    fill_rate = {}
    for k in ad_requests:
        try:
            fill_rate[k] = ad_requests[k] / impressions[k]
        except KeyError:
            fill_rate[k] = 0

    return {
        "ad_requests": ad_requests,
        "impressions": impressions,
        "fill_rate": fill_rate,
    }
