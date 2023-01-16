import traceback
import streamlit as st
from datetime import date, datetime, timedelta

import reactivex as rx
from reactivex.abc import DisposableBase

from src.wiki_api import WikiApi
from src.wiki_streams import (
    merge_user_activity,
    most_active_user_over_timespan,
    st_plot,
    track_user_activity,
    user_activity_over_day,
    users_top_title_contributions
)

# 1. Recent Changes as a real-time stream
def task1():
    api_url: str = "https://en.wikipedia.org/w/api.php"
    stream_url: str = "https://stream.wikimedia.org/v2/stream/recentchange"

    api: WikiApi = WikiApi(api_url, stream_url)

    changes_stream: rx.Observable[dict] = api.get_event_stream()

    sub1: DisposableBase = changes_stream.subscribe(
        on_next=lambda item: st.text(f"on next: {item}"),
        on_error=lambda e: st.text(f"Error: {traceback.print_exc()}"),
    )


# 2. Track in real time the activity of a particular user or a set of users
def task2(users_to_track):
    api_url: str = "https://en.wikipedia.org/w/api.php"
    stream_url: str = "https://stream.wikimedia.org/v2/stream/recentchange"

    api: WikiApi = WikiApi(api_url, stream_url)

    changes_stream: rx.Observable[dict] = api.get_event_stream()

    sub2: DisposableBase = track_user_activity(
        changes_stream, users_to_track
    ).subscribe(
        on_next=lambda item: st.text(f'on next: {item.get("user")} {item}'),
        on_error=lambda e: st.text(f"Error: {e}"),
    )


# 3. Retrieve a statistic of a particular user which include:
# 3.a Information about user contribution as a series of points over time.
def task3a(username, days_from_today):
    api_url: str = "https://en.wikipedia.org/w/api.php"
    stream_url: str = "https://stream.wikimedia.org/v2/stream/recentchange"

    api: WikiApi = WikiApi(api_url, stream_url)

    start_date: datetime = datetime.combine(
        date.today() - timedelta(days=days_from_today),
        datetime.min.time(),
    )

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
        on_next=lambda data: st_plot(data, "All changes"),
        on_error=lambda e: st.text(f"on_error: {e}\n{traceback.print_exc()}"),
    )


def task3b(username, days_from_today):
    api_url: str = "https://en.wikipedia.org/w/api.php"
    stream_url: str = "https://stream.wikimedia.org/v2/stream/recentchange"

    api: WikiApi = WikiApi(api_url, stream_url)

    start_date: datetime = datetime.combine(
        date.today() - timedelta(days=days_from_today),
        datetime.min.time(),
    )

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

    users_top_title_contributions(user_all_changes_history).subscribe(
        on_next=st.write,
        on_error=lambda e: st.text(f"on_error: {e}\n{traceback.print_exc()}")
    )


def task3c(username, days_from_today):
    api_url: str = "https://en.wikipedia.org/w/api.php"
    stream_url: str = "https://stream.wikimedia.org/v2/stream/recentchange"

    api: WikiApi = WikiApi(api_url, stream_url)

    start_date: datetime = datetime.combine(
        date.today() - timedelta(days=days_from_today),
        datetime.min.time(),
    )

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

    user_activity_over_day(user_typos_history).subscribe(
        on_next=lambda data: st_plot(data, "Typos editing"),
        on_error=lambda e: st.text(f"on_error: {e}\n{traceback.print_exc()}"),
    )

    user_activity_over_day(user_edits_history).subscribe(
        on_next=lambda data: st_plot(data, "Content adding"),
        on_error=lambda e: st.text(f"on_error: {e}\n{traceback.print_exc()}"),
    )


# 4. Retrieve the most active user during the given time window
def task4():
    api_url: str = "https://en.wikipedia.org/w/api.php"
    stream_url: str = "https://stream.wikimedia.org/v2/stream/recentchange"

    api: WikiApi = WikiApi(api_url, stream_url)

    changes_stream: rx.Observable[dict] = api.get_event_stream()
    
    time_window = timedelta(seconds=2)
    sub4 = most_active_user_over_timespan(changes_stream, time_window).subscribe(
        on_next=lambda item: print(
            f"\nTop edits user for last {time_window}\nUser: {item[0]}\nEdits count: {item[1]}"
        ),
        on_error=lambda e: print(f"Error: {traceback.print_exc()}"),
    )
