import traceback
from datetime import date, datetime, timedelta
from pprint import pprint

import reactivex as rx
from reactivex.abc import DisposableBase

from wiki_api import WikiApi
from wiki_streams import (
    merge_user_activity,
    most_active_user_over_timespan,
    show_graph,
    track_user_activity,
    user_activity_over_day,
    users_top_title_contributions
)


def main() -> None:
    api_url: str = "https://en.wikipedia.org/w/api.php"
    stream_url: str = "https://stream.wikimedia.org/v2/stream/recentchange"

    api: WikiApi = WikiApi(api_url, stream_url)

    changes_stream: rx.Observable[dict] = api.get_event_stream()

    # 1. Recent Changes as a real-time stream
    sub1: DisposableBase = changes_stream.subscribe(
        on_next=lambda item: print(f"on next: {item}"),
        on_error=lambda e: print(f"Error: {traceback.print_exc()}"),
    )

    # 2. Track in real time the activity of a particular user or a set of users
    users_to_track = ["Cewbot", "Research Bot"]
    sub2: DisposableBase = track_user_activity(
        changes_stream, users_to_track
    ).subscribe(
        on_next=lambda item: print(f'on next: {item.get("user")} {item}'),
        on_error=lambda e: print(f"Error: {e}"),
    )
    # 3. Retrieve a statistic of a particular user which include:
    # 3.a Information about user contribution as a series of points over time.

    days_from_today: int = 30
    start_date: datetime = datetime.combine(
        date.today() - timedelta(days=days_from_today),
        datetime.min.time(),
    )
    username = "Bluejay14"

    user_typos_history: rx.Observable[dict] = api.get_user_changes_history(
        username,
        start_date,
        rcshow="minor",
        rctype="edit",
    )
    user_edits_history: rx.Observable[dict] = api.get_user_changes_history(
        username,
        start_date,
        rcshow="!minor",
    )

    user_all_changes_history: rx.Observable[dict] = merge_user_activity(
        user_typos_history, user_edits_history
    )
    user_activity_over_day(user_all_changes_history).subscribe(
        on_next=lambda data: show_graph(data, "All changes"),
        on_error=lambda e: print(f"on_error: {e}\n{traceback.print_exc()}"),
    )

    # 3.b Pages to which the user has contributed the most

    users_top_title_contributions(user_all_changes_history).subscribe(
        on_next=pprint,
        on_error=lambda e: traceback.print_exc()
    )

    # 3.c Type of contribution

    user_activity_over_day(user_typos_history).subscribe(
        on_next=lambda data: show_graph(data, "Typos editing"),
        on_error=lambda e: print(f"on_error: {e}\n{traceback.print_exc()}"),
    )

    user_activity_over_day(user_edits_history).subscribe(
        on_next=lambda data: show_graph(data, "Content adding"),
        on_error=lambda e: print(f"on_error: {e}\n{traceback.print_exc()}"),
    )

    # 4. Retrieve the most active user during the given time window
    time_window = timedelta(seconds=10)
    most_active_user_over_timespan(changes_stream, time_window).subscribe(
        on_next=lambda item: print(
            f"Top edits user for last {time_window}\nUser: {item[0]}\nEdits count: {item[1]}"
        ),
        on_error=lambda e: print(f"Error: {traceback.print_exc()}"),
    )


if __name__ == "__main__":
    main()
