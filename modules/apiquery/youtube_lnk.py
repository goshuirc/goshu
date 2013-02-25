from gbot.libs.helper import time_metric, metric


def length(format_json, input_json):
    return time_metric(secs=input_json['data']['items'][0]['duration'])


def dislikes(format_json, input_json):
    dislikes = int(input_json['data']['items'][0]['ratingCount']) - int(input_json['data']['items'][0]['likeCount'])
    return metric(dislikes)
