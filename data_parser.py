from heapq import *
import numpy as np

f = open("me_at_the_zoo.in")
data = f.readlines()

numbers = map(int, data[0].split(" "))

video_count = int(numbers[0])
endpoint_count = int(numbers[1])
request_count = int(numbers[2])
cache_count = int(numbers[3])
cache_capacity = int(numbers[4])

video_sizes = map(int, data[1].split(" "))


parsed_endpoint_count = 0
parsed_request_count = 0

endpoints = []

# mat = np.zeros((video_count, endpoint_count, cache_count))

requests = []

line_number = 2
while line_number < len(data):
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

        best_score = -1
        best_cache_id = -1
        for cache_id, cache_latency in endpoint["caches"].iteritems():
            score = video_request_count * (endpoint["center"] - cache_latency)
            if score > best_score:
                best_score = score
                best_cache_id = cache_id

        if best_score > 0:
            heappush(requests, (-best_score, (video_id, endpoint_id, best_cache_id)))

        line_number += 1
        continue


print heappop(requests)
print heappop(requests)
print heappop(requests)

