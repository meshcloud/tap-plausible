"""Plausible tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_plausible import streams


class TapPlausible(Tap):
    """Plausible tap class."""

    name = "tap-plausible"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="Plausible API Key. See the <a" +
            "*href=\"https://plausible.io/docs/stats-api\">docs</a>" +
            "for information on how to generate this key."
        ),
        th.Property(
            "site_ids",
            th.ArrayType(th.StringType),
            required=True,
            description="The domain of the site you want to retrieve data for. " +
                "Enter the name of your site as configured on Plausible," +
                "i.e., excluding \"https://\" and \"www\". Can be retrieved from " +
                "the 'domain' field in your Plausible site settings."
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.mysample.com",
            description="The url for the API service (without /api/v1 prefix!)",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.PlausibleStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.StatsStream(self)
        ]


if __name__ == "__main__":
    TapPlausible.cli()
