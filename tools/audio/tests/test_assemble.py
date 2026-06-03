"""Tests for the transcript assembly module."""

from shattered_audio.assemble import format_timestamp, parse_timestamp


def test_parse_timestamp_mm_ss():
    assert parse_timestamp("1:30") == 90


def test_parse_timestamp_hh_mm_ss():
    assert parse_timestamp("1:02:30") == 3750


def test_format_timestamp():
    assert format_timestamp(3750) == "1:02:30"
    assert format_timestamp(90) == "0:01:30"
    assert format_timestamp(0) == "0:00:00"


def test_round_trip():
    for seconds in [0, 1, 59, 60, 3599, 3600, 7261]:
        assert parse_timestamp(format_timestamp(seconds)) == seconds
