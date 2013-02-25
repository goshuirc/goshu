category_output = {
    'Ad': 9,
    'Al': 14,
    'Co': 8,
    'Cr': 11,
    'Da': 5,
    'Hu': 14,
    'Ra': 12,
    'Ro': 6,
    'Sa': 4,
    'Sl': 12,
    'Tr': 7,
}


def categories(format_json, input_json):
    output = []
    for key in sorted(input_json['story']['categories']):
        if input_json['story']['categories'][key]:
            if key[:2] in category_output:
                output.append('@c{colour}{category}@r'.format(colour=category_output[key[:2]],
                                                              category=key))
            else:
                output.append(key)
    return ';'.join(output)
