from heapq import *
import numpy as np

import pickle

file_name = "kittens.in"
# file_name = "me_at_the_zoo.in"
# file_name = "trending_today.in"
# file_name = "videos_worth_spreading.in"

output_file_name = file_name + ".out"


pickled_file_name = file_name + '_requests'


parse = True

def best_request(cache_latencies, endpoint_id, video_id):
    best_score = -1
    best_cache_id = -1

    if cache_count - len(cache_latencies) > 120 :
        return None

    for cache_id, cache_latency in cache_latencies.iteritems():
        score = video_request_count * (endpoints[endpoint_id]["center"] - cache_latency)
        if score > best_score:
            best_score = score
            best_cache_id = cache_id

    if best_score > 0:
        return (-best_score, (video_id, endpoint_id, best_cache_id, cache_latencies))
    return None


f = open(file_name)
data = f.readlines()

numbers = map(int, data[0].split(" "))

video_count = int(numbers[0])
endpoint_count = int(numbers[1])
request_count = int(numbers[2])
cache_count = int(numbers[3])
cache_capacity = int(numbers[4])

video_sizes = map(int, data[1].split(" "))

if parse:

    parsed_endpoint_count = 0
    parsed_request_count = 0

    endpoints = []

    # mat = np.zeros((video_count, endpoint_count, cache_count))

    requests = []

    line_number = 2
    while line_number < len(data):
        # print "line number: ", str(line_number)
        if parsed_endpoint_count < endpoint_count:
            endpoint = {}
            endpoint["center"], num_caches = map(int, data[line_number].split(" "))

            caches = {}

            for cahce_line_number in xrange(line_number + 1, line_number + 1 + num_caches):
                cache_index, cache_latency = map(int, data[cahce_line_number].split(" "))
                caches[cache_index] = cache_latency

            endpoint["caches"] = caches
            endpoints.append(endpoint)

            parsed_endpoint_count += 1
            line_number += num_caches + 1
            continue

        if parsed_request_count < request_count:
            video_id, endpoint_id, video_request_count = map(int, data[line_number].split(" "))

            video_size = video_sizes[video_id]
            endpoint = endpoints[endpoint_id]

            # best_score = -1
            # best_cache_id = -1
            # for cache_id, cache_latency in endpoint["caches"].iteritems():
            #     score = video_request_count * (endpoint["center"] - cache_latency)
            #     if score > best_score:
            #         best_score = score
            #         best_cache_id = cache_id
            #
            # if best_score > 0:
            #     heappush(requests, (-best_score, (video_id, endpoint_id, best_cache_id)))

            request = best_request(endpoint["caches"], endpoint_id, video_id)

            if request != None:
                heappush(requests, request)

            line_number += 1
            continue


print "parsed"

#     with open(pickled_file_name, 'wb') as fp:
#         pickle.dump(requests, fp)
#
# with open (pickled_file_name, 'rb') as fp:
#     pickledRequests = pickle.load(fp)

# requests = pickledRequests


remaining_cache_size = []
cache_videos = []

for i in xrange(0, cache_count):
    remaining_cache_size.append(cache_capacity)
    cache_videos.append([])



while len(requests) > 0:

    # print len(requests)

    request = heappop(requests)
    video_id, endpoint_id, cache_id, cache_latencies = request[1]
    video_size = video_sizes[video_id]

    if not video_id in cache_videos[cache_id]:
        if remaining_cache_size[cache_id] > video_size:
            cache_videos[cache_id].append(video_id)
            remaining_cache_size[cache_id] = remaining_cache_size[cache_id] - video_size
        else:
            caches = cache_latencies.copy()

            caches.pop(cache_id)

            new_request = best_request(caches, endpoint_id, video_id)
            if new_request != None:
                heappush(requests, new_request)



# print remaining_cache_size
# print cache_videos
#
# print "=" * 20
# print len(cache_videos)
# for i in xrange(0, len(cache_videos)):
#     print i, " ".join(map(str,cache_videos[i]))


output_array = [str(len(cache_videos))]
for i in xrange(0, len(cache_videos)):
    output_array.append(str(i) + " " +  " ".join(map(str,cache_videos[i])))


output_file = open(output_file_name, "w")
output_file.write("\n".join(map(str, output_array)))
output_file.close()


print "DONE DONE DONE"
