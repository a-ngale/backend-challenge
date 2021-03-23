"""Business logic handlers for the application endpoints."""
from itertools import groupby
from typing import List

from app.models import Metric


def get_metrics_crossing(metric_value: int) -> List:
    """Returns a list of artists and dates when their metrics crossed provided value.

    Includes all days when any existing artist 'crossed' that metric value, i.e.
    when the artist's metric_value on that day is larger than or equal to the passed
    parameter value and its metric_value on the previous day is lower than the passed
    parameter value.

    Args:
        metric_value (int): Threshold value that artist's metric should exceed.

    Returns:
        dicts of artist id and days the metric crossed the specified value in format:
        [{"artist_id": 1, "crossings": ["2020-01-01"]}]
    """
    artists_crossings = []

    # Order queryset by artist_id and date to keep the response consistently ordered.
    metrics_queryset = Metric.query.order_by(Metric.artist_id, Metric.date)

    metrics = groupby(metrics_queryset, key=lambda item: item.artist_id)
    for artist_id, artist_metrics in metrics:
        previous_metric = None
        crossings = []

        for metric in artist_metrics:
            # TODO: Should we compare the metric with the previous date or previous
            #  _available_ date? Is it possible to have gaps between metrics?
            previous_metric_value = 0
            if previous_metric and (metric.date - previous_metric.date).days == 1:
                previous_metric_value = previous_metric.value

            if metric.value >= metric_value > previous_metric_value:
                crossings.append(metric.date.strftime('%Y-%m-%d'))
            previous_metric = metric

        artists_crossings.append({"artist_id": artist_id, "crossings": crossings})
    return artists_crossings
