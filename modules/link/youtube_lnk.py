

def length(format_json, input_json):
    return input_json['items'][0]['contentDetails']['duration'].lower().replace('pt', '')
