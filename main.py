# -*- coding: utf-8 -*-
import optparse
from collections import namedtuple

Rules = namedtuple('Rules', ['num_videos', 'num_endpoints', 'num_requests_descriptions', 'num_caches', 'cache_size'])
endpoint_Cache = namedtuple('endpoint_Cache', ['id', 'latency'])
Request = namedtuple('Request', ['endpoint_id', 'num_requests'])

my_videos = {}
my_endpoints = {}
my_caches = {}


class Combination(object):
    def __init__(self, videos, caches):
        self._videos_caches = {}
        self._current_cost = 0
        self._caches_videos = {}


    def set_video(self, video_id, cache_id):
        # there is room left for video in cache
        if Videos[video_id] < (Cache[cache_id] - self._caches_videos[cache_id]):
            self._videos_caches[video_id] = cache_id
            self._caches_videos[cache_id] = video_id

            self._current_cost += cost

    def is_complete():
        print 'yolo'



tmp_cos = 0
class CombinationsExplorer(object):
    def __init__(self, available_caches_per_endpoint_and_videos):
        self.available_caches = available_caches_per_endpoint_and_videos

    def get(self,video_id, cache_id, cache_cost, max_cost=tmp_cos):
        combinations = []
        combination = Combination()
        #combination.set_video(video_id=video_id, cache_id=cache_id, cost)



def select_combination(combinations, endpoints, videos):
    to_explore = {}
    for endpoint in endpoints:
        for video_id, nb_requests in endpoint.videos.iteritems():
            # best available caches for given video and endpoint
            available_caches = sort(
                [(cache.id, cache.latency * nb_requests) for cache in endpoint.caches],
                key=lambda x: x[1])
            to_explore[(endpoint_id, video_id,)] = available_caches
    tmp_cost = sys.max_int
    combination = CombinationsExplorer(to_explore)
    # for (endpoint_id, video_id,), available_caches in sorted(to_explore.items(), key=lambda x: x[1][0], reverse=True):
    #     cache_id, cache_cost = available_caches[0]
    #     combination, cost = combinations.get(video_id=video_id, cache_id=cache_id, cache_cost=cache_cost, max_cost=tmp_cost)
    #     if combination:
    #         tmp_cost = cost
    return combination



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
            new_endpoint.caches.append(endpoint_Cache(id=l_elts[0], latency=l_elts[1]))
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
    caches_obj = []
    for id in range(rules.num_caches):
        caches_obj.append(Cache(id=id,size=rules.cache_size))
    print rules
    #for id in videos_ind:
        #print 'Video',id,videos_ind[id].size
    #for end in endpoints:
        #print 'Endpoint', end.id
    print 'videos', len(videos_ind)
    print 'endpoints', len(endpoints)
    print 'caches', len(caches_obj)
    print 'requests', requests
    my_videos = videos_ind
    for video in videos_ind.values():
        for request in video.requests:
            my_endpoints.setdefault(request.endpoint_id,{}).update({'video_id':video.id,'num_requests':request.num_requests})
    for cache in caches_obj:
        my_caches[cache.id]={'size':cache.size, 'videos':[]}

class Cache(object):
    def __init__(self, id, size):
        self.id = id
        self.videos = []
        self.size = size


class Video(object):

    def __init__(self, id, size):
        self.caches = []
        self.requests = []
        self.size = size
        self.id = id


class EndPoint(object):

    def __init__(self, id, datacenter_latency, caches):
        self.id = id
        self.datacenter_latency = datacenter_latency
        self.caches = caches


def main():

    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="write report to FILE", default='requirements.txt')
    (options, args) = parser.parse_args()
    parse_input_file(options.filename)

if __name__ == '__main__':
    main()
