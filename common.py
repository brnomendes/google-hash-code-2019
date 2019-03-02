def read_input_file(file_name):
    dataset = dict()

    with open(file_name, 'r') as file:
        header = file.readline().replace('\n', '')

        for id, line in enumerate(file.readlines()):
            data = line.replace('\n', '').split(' ')
            dataset[id] = {'orientation': data[0], 'tags': set(data[2:])}

    return dataset


def write_result(slides, file_name):
    # slides example = [[0], [3], [4], [5, 1], [2]]
    with open(file_name, 'w') as file:
        file.write(str(len(slides)) + '\n')
        file.writelines([''.join([''.join([str(image) + ' ' for image in slide]).strip()] + ['\n']) for slide in slides])


def _get_tags(dataset, id):
    if len(id) == 1:
        return dataset[id[0]]['tags']

    return dataset[id[0]]['tags'].union(dataset[id[1]]['tags'])


def score(dataset, slides):
    # slides example = [[0], [3], [4], [5, 1], [2]]
    score_total = 0

    for i in range(len(slides) - 1):
        tags1 = _get_tags(dataset, slides[i])
        tags2 = _get_tags(dataset, slides[i + 1])
        score_total += score_between(tags1, tags2)

    return score_total


def score_between(tags1, tags2):
    return min([len(tags1.difference(tags2)), len(tags2.difference(tags1)), len(tags1.intersection(tags2))])
