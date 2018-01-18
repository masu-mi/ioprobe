# coding: utf-8
"""
test_ioprobe
"""
import ioprobe
from ioprobe import helper
import pytest
from unittest.mock import patch
import datetime
from collections import OrderedDict

def test_io_path():
    assert helper.io_path(100) == "/proc/100/io"

def test_header():
    assert ioprobe.header(["foo", "bar"]) == "# date\tfoo/s\tbar/s"

def test_report_items():
    assert helper.source_items("self") == [
        "rchar", "wchar", "syscr", "syscw",
        "read_bytes", "write_bytes", "cancelled_write_bytes" ]

def test_delta():
    assert helper.note_delta(OrderedDict(), ["a", "b"],
            {"a": 100, "b": -100}, {"a":0, "b": 0},
            2) == { "a/s": 50.0, "b/s": -50.0}

def test_DeltaReport():
    with patch("ioprobe.time.sleep") as mock_sleep:
        mock_sleep.return_value = None
        def mock_now():
            yield datetime.datetime(2018, 1, 1, 0, 0, 0)
            yield datetime.datetime(2018, 1, 1, 0, 0, 1)
            yield datetime.datetime(2018, 1, 1, 0, 0, 2)

        report = ioprobe.DeltaReport( ["a", "b"],
                [{"a":0, "b": 0}, {"a": 100, "b": -100}])
        assert report.header() == "# date\ta/s\tb/s"

        with patch("ioprobe.datetime") as mock_datetime:
            mock_datetime.now = mock_now().__next__
            report = ioprobe.DeltaReport( ["a", "b"],
                    [{"a":0, "b": 0}, {"a": 100, "b": -100}])
            lines = report.start()
            assert lines.__next__() == r'{"date": "2018-01-01 00:00:01", "a/s": 100.0, "b/s": -100.0}'

            mock_datetime.now = mock_now().__next__
            report = ioprobe.DeltaReport( ["a", "b"],
                    [{"a":0, "b": 0}, {"a": 100, "b": -100}, {"a": 50, "b": 100}],
                    block_line_num = 1, json = False)
            lines = report.start()
            assert lines.__next__() == "# date\ta/s\tb/s"
            assert lines.__next__() == "2018-01-01 00:00:01\t100.0\t-100.0"
            assert lines.__next__() == "# date\ta/s\tb/s"
            assert lines.__next__() == "2018-01-01 00:00:02\t-50.0\t200.0"
            assert lines.__next__() == "# date\ta/s\tb/s"
