# coding: utf-8

import os
import signal
import datetime
import time
import argparse


def safe_exit(signum, frame):
    print("\r[catch sig int]")
    exit()

signal.signal(signal.SIGINT, safe_exit)


def main():
    parser = argparse.ArgumentParser(description='I/O probe for process.')
    parser.add_argument('pid', metavar='pid', type=int,
                        help='target process\'s pid.')
    parser.add_argument('--json', dest='json_output', action='store_const',
                        const=True, default=False,
                        help='change command\'s output to JSON.')
    args = parser.parse_args()
    pid, json_output = str(args.pid), args.json_output
    io_sum = fetch_io(pid)
    order = convert_to_order(io_sum)
    if (not json_output):
        print(header(order))
    line_num = 1
    block_line_num = 10
    pre_val = dict(io_sum)
    while True:
        time.sleep(1)
        cur_val = dict(fetch_io(pid))
        print(delta(pre_val, cur_val, order, json_output))
        pre_val = cur_val
        line_num = line_num + 1
        if (not json_output and line_num > block_line_num):
            print(header(order))
            line_num = 1


def header(order):
    return order[0]+"\t" + "\t".join((term+"/s" for term in order[1:]))


def delta(pre, cur, order, json_output):
    if (json_output):
        row = {order[0]: cur[order[0]]}
        row.update(dict((key, (cur[key] - pre[key])) for key in order[1:]))
        return row
    else:
        return cur[order[0]]+"\t" + "\t".join(
                (str(cur[key] - pre[key]) for key in order[1:]))


def convert_to_order(io_sum):
    return [pair[0] for pair in io_sum]


def fetch_io(pid):
    try:
        with open(os.path.join("/", "proc", pid, "io")) as f:
            io_sum = [(
                "date",
                datetime.datetime.now().replace(microsecond=0).isoformat(" "))]
            io_sum.extend(
                [(pair[0], int(pair[1]))
                 for pair in (line.rstrip().split(":")
                 for line in f.readlines())])
        return io_sum
    except IOError as e:
        print('[Can\'t open file.]')
        exit()


if __name__ == "__main__":
    main()
