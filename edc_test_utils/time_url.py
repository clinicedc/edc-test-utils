import operator
from functools import reduce
from statistics import mean, median, stdev

import requests


def time_url(iterations: int, url: str):
    """Returns stats on the response time of an url"""
    timedeltas = []
    for i in range(iterations):
        timedeltas.append(requests.get(url, timeout=10).elapsed)
    total_seconds = [t.total_seconds() for t in timedeltas]
    sorted(total_seconds)
    mn = mean(total_seconds)
    md = median(total_seconds)
    std = stdev(total_seconds)
    total_seconds = reduce(operator.add, timedeltas).total_seconds()
    return dict(
        mean=mn, median=md, stdev=std, iterations=iterations, total_seconds=total_seconds
    )
