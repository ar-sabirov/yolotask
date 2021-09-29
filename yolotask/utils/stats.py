from typing import Any, Dict


def process_stats(
    ad_requests: Dict[str, int],
    impressions: Dict[str, int]
) -> Dict[str, Dict[str, Any]]:
    fill_rate = {}
    for k in ad_requests:
        try:
            fill_rate[k] = impressions[k] / ad_requests[k]
        except KeyError:
            fill_rate[k] = 0

    return {
        "ad_requests": ad_requests,
        "impressions": impressions,
        "fill_rate": fill_rate,
    }
