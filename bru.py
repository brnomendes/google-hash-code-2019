import sys
import copy
import random

from common import Common

if __name__ == "__main__":
    file_name = sys.argv[1]

    dataset = Common.read_input_file(file_name)
    original_dataset = copy.deepcopy(dataset)

    verticals = list()
    slides = list()
    last_tags = None

    for id in range(0, len(original_dataset)):
        if dataset[id]['orientation'] == 'H':
            slides.append([id])
            last_tags = dataset[id]['tags']
            dataset.pop(id)
            break

    for id in range(0, len(original_dataset)):
        if id not in dataset:
            continue

        if dataset[id]['orientation'] == 'V':
            verticals.append(id)
            dataset.pop(id)

    while len(dataset) > 0:
        last_slide = slides[-1][0]

        hasCombination = False
        for id in range(0, len(original_dataset)):
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

    for i in range(0, len(verticals), 2):
        if i + 1 < len(verticals):
            slides.append([verticals[i], verticals[i+1]])

    file_name_split = file_name.split('.')
    Common.write_result(slides, f'{".".join(file_name_split[:-1])}-out.{file_name_split[-1]}')

    print(Common.score(original_dataset, slides))
