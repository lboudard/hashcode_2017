# -*- coding: utf-8 -*-
import optparse
from collections import namedtuple

Rules = namedtuple('Rules', ['num_videos', 'num_endpoints', 'num_requests_descriptions', 'num_caches', 'cache_size'])
Cache = namedtuple('Cache', ['id', 'latency'])
Request = namedtuple('Request', ['endpoint_id', 'num_requests'])


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

def parse_endpoint_lines(id,endpoint_line,endpoint_index,all_shit):
    elts = map(int, endpoint_line.split(' '))
    caches = []
    new_endpoint = EndPoint(id=id, datacenter_latency=elts[0], caches=[])
    if elts[1] == 0:
        return new_endpoint, endpoint_index+1, caches
    for line in all_shit[endpoint_index+1:elts[1]]:
        l_elts = map(int, line.split(' '))
        # it is a latency line
        if l_elts[0] == 0:
            #it is the datacenter id
            new_endpoint.datacenter_latency = l_elts[1]
        else:
            caches.append(l_elts[0])
            new_endpoint.caches.append(Cache(id=l_elts[0], latency=l_elts[1]))
    return new_endpoint,endpoint_index+elts[1]+1, caches


def parse_input_file(filename):
    with open(filename, 'r') as file:
        all_shit = file.read().split('\n')
        rules = parse_rules(all_shit[0])
        all_videos = parse_videos(all_shit[1])
        videos_ind = dict((vid.id, vid) for vid in all_videos)
        # indexed
        endpoints = []
        requests = 0
        endpoint_id = 0
        caches = []
        endpoint_index = 2
        total_endpoints = rules.num_endpoints
        while total_endpoints > 0:
                new_endpoint, endpoint_index, listed_caches = parse_endpoint_lines(endpoint_id,all_shit[endpoint_index],endpoint_index,all_shit)
                caches.extend(listed_caches)
                endpoints.append(new_endpoint)
                total_endpoints -= 1
        for line in all_shit[endpoint_index:]:
            if line == '':
                continue
            elts = map(int, line.split(' '))
            assert len(elts) == 3
            #it is a request line
            videos_ind[elts[0]].requests.append(Request(endpoint_id= elts[1],num_requests = elts[2]))
            requests += 1
        caches = list(set(caches))
    print rules
    #for id in videos_ind:
        #print 'Video',id,videos_ind[id].size
    #for end in endpoints:
        #print 'Endpoint', end.id
    print 'videos', len(videos_ind)
    print 'endpoints', len(endpoints)
    print 'caches', len(caches)
    print 'requests', requests


class MyObject(object):
    def __str__(self):
        return str(self)


class Video(object):

    def __init__(self, id, size):
        self.caches = []
        self.requests = []
        self.size = size
        self.id = id


class EndPoint(MyObject):

    def __init__(self, id, datacenter_latency, caches):
        self.id = id
        self.datacenter_latency = datacenter_latency
        self.caches = caches
        self.videos = []


def main():

    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="write report to FILE", default='requirements.txt')
    (options, args) = parser.parse_args()
    parse_input_file(options.filename)

if __name__ == '__main__':
    main()
