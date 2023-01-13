import json
from datetime import datetime

import reactivex as rx
import requests
from reactivex import operators as ops
from sseclient import SSEClient
from typing import List


class WikiApi:
    def __init__(self, api_url: str, stream_url: str) -> None:
        self._url = api_url
        self._stream_url = stream_url

    def get_event_stream(self) -> rx.Observable[dict]:
        return rx.from_iterable(SSEClient(self._stream_url)).pipe(
            ops.skip(1),
            ops.map(lambda event: json.loads(event.data)),
            ops.share(),
        )

    def _get_user_changes_history(
        self,
        user: str,
        start_date: datetime,
        continue_params: dict = None,
        **kwargs
    ) -> List[dict]:
        payload = {
            "action": "query",
            "list": "recentchanges",
            "rcdir": "newer",
            "rcstart": start_date,
            "rclimit": "max",
            "format": "json",
            "rcuser": user,
            **kwargs,
        }
        if continue_params:
            payload.update(continue_params)

        data: dict = requests.get(self._url, params=payload).json()
        recent_changes_data: List[dict] = data.get("query").get(
            "recentchanges"
        )

        if data.get("continue"):
            recent_changes_data.extend(
                self._get_user_changes_history(
                    user,
                    start_date,
                    continue_params=data.get("continue"),
                )
            )

        return recent_changes_data

    def get_user_changes_history(
        self, user: str, start_date: datetime, **kwargs
    ) -> rx.Observable[dict]:
        return rx.from_iterable(
            self._get_user_changes_history(user, start_date, **kwargs)
        )
