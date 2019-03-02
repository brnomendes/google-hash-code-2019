import sys
import copy
import random
import datetime

import common


Z_DICT = {
    0.90: 1.645,
    0.91: 1.695,
    0.92: 1.751,
    0.93: 1.812,
    0.94: 1.881,
    0.95: 1.96,
    0.96: 2.054,
    0.97: 2.17,
    0.98: 2.326,
    0.99: 2.576
}


def append_slide(dataset, slides, id):
    tags = dataset[id]['tags']

    if isinstance(id, int):
        slides.append([id])
    else:
        id_split = id.split(' ')
        slides.append([int(id_split[0]), int(id_split[1])])

    dataset.pop(id)
    return dataset, slides, tags


def best_combination(dataset, last_tags):
    sample_dataset = random.sample(list(dataset.keys()), sample_size(len(dataset)))

    max_score = int(len(last_tags) / 2)

    best_id = sample_dataset[0]
    best_score = common.score_between(last_tags, dataset[best_id]['tags'])
    for id in sample_dataset:
        id_score = common.score_between(last_tags, dataset[id]['tags'])
        if id_score >= max_score:
            return id
        elif id_score >= best_score:
            best_id = id
            best_score = id_score

    return best_id


def sample_size(population_size, margin_error=0.01, confidence_level=0.99):
    if population_size <= 1:
        return population_size

    z = Z_DICT[confidence_level]
    sigma = 1 / 2
    numerator = z**2 * sigma**2 * (population_size / (population_size - 1))
    denominator = margin_error**2 + ((z**2 * sigma**2) / (population_size - 1))
    return int(numerator / denominator)


def combine_verticals(dataset):
    id1v = None
    for id in list(dataset.keys()):
        if id in dataset and dataset[id]['orientation'] == 'V':
            if id1v is None:
                id1v = id
            else:
                dataset["{} {}".format(id1v, id)] = {'tags': dataset[id1v]['tags'].union(dataset[id]['tags'])}
                dataset.pop(id1v)
                dataset.pop(id)
                id1v = None
    return dataset


def create_slideshow(dataset):
    print('Creating slideshow...')
    dataset = combine_verticals(dataset)
    dataset, slides, last_tags = append_slide(dataset, list(), random.choice(list(dataset.keys())))

    while dataset:
        dataset, slides, last_tags = append_slide(dataset, slides, best_combination(dataset, last_tags))

    return slides


def get_file_name_out(file_name):
    file_name_split = file_name.split('.')
    return "{}-out.{}".format(".".join(file_name_split[:-1]), file_name_split[-1])


def run(file_name):
    dataset = common.read_input_file(file_name)

    start = datetime.datetime.now()
    slides = create_slideshow(copy.deepcopy(dataset))
    end = datetime.datetime.now()

    file_name_out = get_file_name_out(file_name)
    common.write_result(slides, file_name_out)

    print('Write: {}'.format(file_name_out))
    print('Time: {}'.format(end - start))
    print('Score: {}'.format(common.score(dataset, slides)))


if __name__ == "__main__":
    run(sys.argv[1])
