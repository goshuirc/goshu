from gbot.libs.helper import time_metric, metric


def length(format_json, input_json):
    return time_metric(secs=input_json['data']['duration'])


def dislikes(format_json, input_json):
    dislikes = int(input_json['data']['ratingCount']) - int(input_json['data']['likeCount'])
    return metric(dislikes)
