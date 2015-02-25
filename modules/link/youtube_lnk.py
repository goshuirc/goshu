from gbot.libs.helper import time_metric, metric


def length(format_json, input_json):
    return time_metric(secs=input_json['data'].get('duration', 0))


def dislikes(format_json, input_json):
    dislikes = int(input_json['data'].get('ratingCount', 0)) - int(input_json['data'].get('likeCount', 0))
    return metric(dislikes)
