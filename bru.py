import sys
import copy
import random

from common import Common

if __name__ == "__main__":
    file_name = sys.argv[1]

    dataset = Common.read_input_file(file_name)
    original_dataset = copy.deepcopy(dataset)

    slides = list()
    verticals = list()
    last_tags = None

    for id in list(dataset.keys()):
        if dataset[id]['orientation'] == 'H':
            slides.append([id])
            last_tags = dataset[id]['tags']
            dataset.pop(id)
            break

    for id in list(dataset.keys()):
        if id not in dataset:
            continue

        if dataset[id]['orientation'] == 'V':
            verticals.append(id)

    for i in range(0, len(verticals), 2):
        if i + 1 < len(verticals):
            id1 = verticals[i]
            id2 = verticals[i+1]

            if last_tags is None:
                last_tags = dataset[id1]['tags'].union(dataset[id2]['tags'])
                slides.append([id1, id2])
            else:
                dataset[f"{id1} {id2}"] = {
                    'orientation': 'VV',
                    'tags': dataset[id1]['tags'].union(dataset[id2]['tags'])
                }

            dataset.pop(id1)
            dataset.pop(id2)

    while len(dataset) > 0:
        last_slide = slides[-1]

        hasCombination = False
        for id in list(dataset.keys()):
            if id in last_slide:
                continue

            if Common.score_between(last_tags, dataset[id]['tags']) > 1:
                hasCombination = True
                id_split = str(id).split(' ')
                if len(id_split) > 1:
                    slides.append([int(id_split[0]), int(id_split[1])])
                else:
                    slides.append([id])
                last_tags = dataset[id]['tags']
                dataset.pop(id)
                break

        if not hasCombination:
            r = list(dataset.keys())[0]

            id_split = str(r).split(' ')
            if len(id_split) > 1:
                slides.append([int(id_split[0]), int(id_split[1])])
            else:
                slides.append([r])
            last_tags = dataset[r]['tags']
            dataset.pop(r)

    file_name_split = file_name.split('.')
    Common.write_result(slides, f'{".".join(file_name_split[:-1])}-out.{file_name_split[-1]}')

    print(Common.score(original_dataset, slides))
