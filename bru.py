import copy
import random

from common import Common

if __name__ == "__main__":
    file_name = 'data/b_lovely_landscapes.txt'

    dataset = Common.read_input_file(file_name)
    original_dataset = copy.deepcopy(dataset)

    verticals = set()
    slides = list()
    last_tags = None

    for id in range(0, len(dataset)):
        if dataset[id]['orientation'] == 'H':
            slides.append([id])
            last_tags = dataset[id]['tags']

    for id in range(0, len(dataset)):
        if id not in dataset:
            continue

        if dataset[id]['orientation'] == 'V':
            verticals.add(id)
            dataset.pop(id)

    while len(dataset) > 0:
        last_slide = slides[-1][0]

        hasCombination = False
        for id in range(0, len(dataset)):
            if id not in dataset or last_slide == id:
                continue

            if Common.score_between(last_tags, dataset[id]['tags']) > 0:
                hasCombination = True
                slides.append([id])
                last_tags = dataset[id]['tags']
                dataset.pop(id)
                break

        if not hasCombination:
            r = list(dataset.keys())[0]
            slides.append([r])
            last_tags = dataset[r]['tags']
            dataset.pop(r)

    file_name_split = file_name.split('.')
    Common.write_result(slides, f'{".".join(file_name_split[:-1])}-out.{file_name_split[-1]}')

    print(Common.score(original_dataset, slides))
