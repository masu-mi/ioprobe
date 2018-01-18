# coding: utf-8

import os

def source_items(pid):
    return [record[0] for record in fetch_snapshot(pid)]

def snapshots(pid, limit = -1):
    while limit != 0:
        yield dict(fetch_snapshot(pid))
        if limit > 0:
            limit = limit - 1

def io_path(pid):
    return os.path.join("/", "proc", str(pid), "io")

def fetch_snapshot(pid):
    try:
        with open(io_path(pid)) as f:
            io_sum = [(pair[0], int(pair[1]))
                 for pair in (line.rstrip().split(":")
                 for line in f.readlines())]
        return io_sum
    except IOError as e:
        print('[Can\'t open file.]')
        exit(1)


def note_delta(record, items, current, before, interval):
    for item in items:
        record[item+"/s"] = float(current[item] - before[item]) / interval
    return record
