# -*- coding: utf-8 -*-
import optparse
from collections import namedtuple


def write_final_submission(videos_caches, output_name):
    # We write the file
    file = open(output_name, 'w')
    # first line : number of final caches
    file.write(str(len(videos_caches)) + '\n')
    for cache_id in videos_caches.keys():
        cache = videos_caches[cache_id]
        line = str(cache['id'])
        line += ' '.join(str(video_id) for video_id in cache['videos'])
        line += '\n'
        file.write(line)
    file.close()


def parse_rules(rules_line):
    rules_raw = rules_line.split(' ')
    rules_raw = [int(rule) for rule in rules_raw]
    rules = {'num_videos':rules_raw[0], 'num_endpoints':rules_raw[1],
             'num_requests_descriptions':rules_raw[2], 'num_caches':rules_raw[3],
             'cache_size':rules_raw[4]}
    return rules

def parse_videos(videos_line):
    videos = []
    videos_raw = videos_line.split(' ')
    sizes_raw = [int(size) for size in videos_raw]
    for i in range(len(videos_raw)):
        videos.append({'id':i,'size':int(videos_raw[i]),'requests':[]})
    return videos

def parse_endpoint_lines(id,endpoint_line,endpoint_index,all_shit):
    elts = map(int, endpoint_line.split(' '))
    caches = []
    new_endpoint = {'id':id, 'datacenter_latency':elts[0], 'caches':[]}
    if elts[1] == 0:
        return new_endpoint, endpoint_index+1, caches
    for line in all_shit[endpoint_index+1:endpoint_index+1+elts[1]]:
        l_elts = map(int, line.split(' '))
        # it is a latency line
        if l_elts[0] == 0:
            #it is the datacenter id
            new_endpoint['datacenter_latency'] = l_elts[1]
        else:
            caches.append(l_elts[0])
            new_endpoint['caches'].append({'id':l_elts[0], 'latency':l_elts[1]})
    return new_endpoint,endpoint_index+elts[1]+1, caches


def parse_input_file(filename):
    my_videos = {}
    my_endpoints = {}
    my_caches = {}
    endpoints_obj = {}
    caches_obj = {}
    endpoints = []
    caches = []
    with open(filename, 'r') as file:
        all_shit = file.read().split('\n')
        rules = parse_rules(all_shit[0])
        all_videos = parse_videos(all_shit[1])
        videos_ind = dict((vid['id'], vid) for vid in all_videos)
        # indexed
        requests = 0
        endpoint_id = 0
        endpoint_index = 2
        total_endpoints = rules['num_endpoints']
        while total_endpoints > 0:
                new_endpoint, endpoint_index, listed_caches = parse_endpoint_lines(endpoint_id,all_shit[endpoint_index],endpoint_index,all_shit)
                caches.extend(listed_caches)
                endpoints.append(new_endpoint)
                total_endpoints -= 1
                endpoint_id +=1
        for line in all_shit[endpoint_index:]:
            if line == '':
                continue
            elts = map(int, line.split(' '))
            assert len(elts) == 3
            #it is a request line
            videos_ind[elts[0]]['requests'].append({'endpoint_id':elts[1],'num_requests':elts[2]})
            requests += 1
        caches = list(set(caches))
    cachess = []
    for id in range(rules['num_caches']):
        cachess.append({'id':id,'size':rules['cache_size'], 'videos':[]})
    print rules
    #for id in videos_ind:
        #print 'Video',id,videos_ind[id].size
    #for end in endpoints:
        #print 'Endpoint', end.id
    print 'videos', len(videos_ind)
    print 'endpoints', len(endpoints)
    print 'caches', len(cachess)
    print 'requests', requests
    my_videos = videos_ind
    for video in videos_ind.values():
        for request in video['requests']:
            my_endpoints.setdefault(request['endpoint_id'],{}).update({video['id']:request['num_requests']})
    for cache in cachess:
        my_caches[cache['id']]={'size':cache['size'], 'videos':[]}
    for endpoint in endpoints:
        endpoints_obj[endpoint['id']] = endpoint
    for cache in cachess:
        caches_obj[cache['id']] = cache
    return my_videos ,my_endpoints,my_caches,endpoints_obj,caches_obj,endpoints


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
    import operator
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="write report to FILE", default='requirements.txt')
    (options, args) = parser.parse_args()
    my_videos ,my_endpoints,my_caches,endpoints_obj,caches_obj,endpoints = parse_input_file(options.filename)
    for endpoint in my_endpoints:
        available_caches = [c['id'] for c in endpoints_obj[endpoint]['caches']]
        for vid,requests in sorted(my_endpoints[endpoint].items(),key=operator.itemgetter(1), reverse=True):
            for available_cache in available_caches:
                if caches_obj[available_cache]['size'] > 0 and caches_obj[available_cache]['size']- my_videos[vid]['size'] >0:
                    caches_obj[available_cache]['videos'].append(vid)
                    caches_obj[available_cache]['size']=caches_obj[available_cache]['size']- my_videos[vid]['size']

    for ca in caches_obj:
        print caches_obj[ca]
    write_final_submission(caches_obj,'{}output'.format(options.filename))

if __name__ == '__main__':
    main()
