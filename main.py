# -*- coding: utf-8 -*-
import optparse
from collections import namedtuple

Rules = namedtuple('Rules', ['videos', 'endpoints', 'requests_descriptions', 'num_caches', 'cache_size'])


def parse_rules(rules_line):
    rules_raw = rules_line.split(' ')
    rules_raw = [int(rule) for rule in rules_raw]
    rules = Rules(*rules_raw)
    return rules


def parse_videos(videos_line):
    videos = []
    videos_raw = videos_line.split(' ')
    sizes_raw = [int(size) for size in videos_raw]
    for i in range(len(videos_raw)):
        videos.append(Video(i, videos_raw[i]))
    return videos


def parse_input_file(filename):
    with open(filename, 'r') as file:
        all_shit = file.read().split('\n')
        rules = parse_rules(all_shit[0])
        videos = parse_videos(all_shit[1])
    return rules, videos


class MyObject(object):
    def __str__(self):
        return repr(self)


class Video(MyObject):

    def __init__(self, id, size):
        self.caches = []
        self.popularity = 0
        self.size = size
        self.id = id

class EndPoint(MyObject):

    def __init__(self, datacenter_latency, caches):
        self.datacenter_latency = datacenter_latency
        self.caches = caches


def main():

    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="write report to FILE", default='requirements.txt')
    (options, args) = parser.parse_args()
    with open(options.filename) as f:
        data = f.read()
        print data

if __name__ == '__main__':
    main()
