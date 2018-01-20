# coding: utf-8
"""
test_ioprobe
"""
import ioprobe
from ioprobe import helper
import pytest
import sys
import datetime
from collections import OrderedDict

if sys.version_info.major != 2:
    from unittest.mock import patch
else:
    from mock.mock import patch


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

def test_DeltaReport_header():
    report = ioprobe.DeltaReport( ["a", "b"],
            [{"a":0, "b": 0}, {"a": 100, "b": -100}])
    assert report.header() == "# date\ta/s\tb/s"


def test_DeltaReport():
    def mock_now():
        yield datetime.datetime(2018, 1, 1, 0, 0, 0)
        yield datetime.datetime(2018, 1, 1, 0, 0, 1)
        yield datetime.datetime(2018, 1, 1, 0, 0, 2)

    with patch("ioprobe.time.sleep") as mock_sleep:
        mock_sleep.return_value = None
        with patch("ioprobe.datetime") as mock_datetime:
            mock_now_generator = mock_now()
            mock_datetime.now = wrapped_next(mock_now_generator)

            report = ioprobe.DeltaReport( ["a", "b"],
                    [{"a":0, "b": 0}, {"a": 100, "b": -100}])
            lines = report.start()
            assert wrapped_next(lines)() == r'{"date": "2018-01-01 00:00:01", "a/s": 100.0, "b/s": -100.0}'

            mock_now_generator = mock_now()
            if sys.version_info.major == 2:
                mock_datetime.now = mock_now_generator.next
            else:
                mock_datetime.now = mock_now_generator.__next__

            report = ioprobe.DeltaReport( ["a", "b"],
                    [{"a":0, "b": 0}, {"a": 100, "b": -100}, {"a": 50, "b": 100}],
                    block_line_num = 1, json = False)
            lines = report.start()
            for expected_line in [
                    "# date\ta/s\tb/s",
                    "2018-01-01 00:00:01\t100.0\t-100.0",
                    "# date\ta/s\tb/s",
                    "2018-01-01 00:00:02\t-50.0\t200.0",
                    "# date\ta/s\tb/s" ]:
                assert wrapped_next(lines)() == expected_line

def wrapped_next(generator):
    if sys.version_info.major == 2:
        return generator.next
    else:
        return generator.__next__
