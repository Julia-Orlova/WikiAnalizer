from datetime import date, datetime, timedelta

import matplotlib.dates as mdates
import matplotlib.pylab as plt
import reactivex as rx
from reactivex import operators as ops
from typing import Tuple, List


def track_user_activity(
    stream: rx.Observable[dict], users: list
) -> rx.Observable[dict]:
    return stream.pipe(ops.filter(lambda event: event.get("user") in users))


def most_active_user_over_timespan(
    stream: rx.Observable[dict], timespan: timedelta
) -> rx.Observable[Tuple[str, int]]:
    return stream.pipe(
        ops.map(lambda event: event.get("user")),
        ops.window_with_time(timespan),
        ops.flat_map(_find_most_active_user),
    )


def _find_most_active_user(
    stream: rx.Observable[dict],
) -> rx.Observable[Tuple[str, int]]:
    return stream.pipe(
        ops.group_by(lambda user: user),
        ops.flat_map(lambda grp: grp.pipe(ops.to_list())),
        ops.map(lambda grp: (grp[0], len(grp))),
        ops.max(lambda x1, x2: x1[1] - x2[1]),
    )


def merge_user_activity(
    typos: rx.Observable[dict], edits: rx.Observable[dict]
) -> rx.Observable[dict]:
    return typos.pipe(
        ops.map(lambda event: {**event, "is_typos_edit": True}),
        ops.merge(edits),
    )


def user_activity_over_day(
    changes: rx.Observable[dict],
) -> rx.Observable[List[Tuple[date, int]]]:
    return changes.pipe(
        ops.map(
            lambda event: datetime.strptime(
                event.get("timestamp"), "%Y-%m-%dT%H:%M:%SZ"
            ).date()
        ),
        ops.group_by(lambda _: _),
        ops.flat_map(lambda group: group.pipe(ops.to_list())),
        ops.map(lambda i: (i[0], len(i))),
        ops.to_list(),
    )


def plot_hist(data: List[Tuple[date, int]], title: str = None) -> None:
    # todo plot data in the same fig
    data.sort(key=lambda pair: pair[0])
    x, y = zip(*data)

    with plt.style.context("ggplot"):
        fig, ax = plt.subplots()
        locator = mdates.AutoDateLocator()
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.set_ylabel("number of edits")
        ax.set_xlabel("date")
        if title:
            ax.set_title(title)
        ax.plot(x, y)
        plt.show()
