# coding: utf-8

import signal
from datetime import datetime
import time
import argparse
import json
from collections import OrderedDict
from ioprobe import helper

def safe_exit(signum, frame):
    print("\r[catch sig int]")
    exit()

class DeltaReport(object):
    """Report manages format, interval, display items"""
    def __init__(self, source_items, snapshots,
            interval = 1, block_line_num = 10,
            json = True):
        """new Report(pid, interval, format, nums)"""
        self.source_items = source_items
        self.snapshots = snapshots
        self.interval = interval
        self.block_line_num = block_line_num
        self.json = json

    def header(self):
        return header(self.source_items)

    def start(self):
        if not self.json:
            yield self.header()
        before_timestamp = None
        before = None
        line_num = 1
        self.block_line_num
        for snapshot in self.snapshots:
            timestamp = datetime.now()
            if not before is None:
                record = OrderedDict(
                        date = timestamp.replace(microsecond=0).isoformat(" "))
                helper.note_delta(record, self.source_items, snapshot, before,
                        (timestamp - before_timestamp).total_seconds())
                if self.json:
                    yield json.dumps(record)
                else:
                    yield separeted_records("\t", record)
                    line_num = line_num + 1
                    if line_num > self.block_line_num:
                        yield self.header()
                        line_num = 1
            before = snapshot
            before_timestamp = timestamp
            time.sleep(self.interval)

def header(order):
    return "# date\t" + "\t".join((term+"/s" for term in order))
def separeted_records(separator, record):
    return separator.join([ str(val) for val in record.values()])

def main():
    parser = argparse.ArgumentParser(description='I/O probe for process.')
    parser.add_argument('pid', metavar='pid', type=int,
                        help='target process\'s pid.')
    parser.add_argument('--json', dest='json_output', action='store_const',
                        const=True, default=False,
                        help='change command\'s output to JSON.')
    args = parser.parse_args()
    signal.signal(signal.SIGINT, safe_exit)
    report = DeltaReport(helper.source_items(args.pid), helper.snapshots(args.pid),
            json = args.json_output)
    for line in report.start():
        print(line)

if __name__ == "__main__":
    main()
