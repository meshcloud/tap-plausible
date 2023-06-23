"""Stream type classes for tap-plausible."""

from __future__ import annotations
from datetime import datetime, timezone

from pathlib import Path
from typing import Any
import pendulum
import requests

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_plausible.client import PlausibleStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class StatsStream(PlausibleStream):
    name = "stats"
    path = "/api/v1/stats/timeseries"
    primary_keys = ["date"]

    replication_key = None
   
    schema_filepath = SCHEMAS_DIR / "stats.json"  # noqa: ERA001

    def get_url_params(self, context: dict | None, next_page_token: Any | None) -> dict[str, Any]:
        params = super().get_url_params(context, next_page_token)

        start_date = pendulum.parse(self.config.get('start_date', "2019-01-01")).date().isoformat()
        utc_now = pendulum.now(timezone.utc).date().isoformat()

        # Retrieves all available metrics.
        # See https://plausible.io/docs/stats-api#metrics
        params['metrics'] = "visitors,pageviews,bounce_rate,visit_duration,visits"
        params['period'] = "custom"
        params['date'] =   f"{start_date},{utc_now}"

        self.compare_start_date
        self.logger.warn(params)
        return params
    
    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        if (row.get('bounce_rate') is not None): # indicates no data is recorded for that day
            return row
        
        return None
    
    def response_error_message(self, response: requests.Response) -> str:
        self.logger.error(response.json())

        return super().response_error_message(response)