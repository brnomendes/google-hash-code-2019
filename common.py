
class Common:

    @staticmethod
    def read_input_file(file_name):
        dataset = dict()

        with open(file_name, 'r') as file:
            header = file.readline().replace('\n', '')

            for id, line in enumerate(file.readlines()):
                data = line.replace('\n', '').split(" ")

                dataset[id] = {
                    'orientation': data[0],
                    'tags': set(data[2:])
                }

        return dataset

    # param example
    # slides = [[0], [3], [4], [5, 1]]
    @staticmethod
    def write_result(slides, file_name):
        with open(file_name, 'w') as file:
            file.write(str(len(slides)) + '\n')
            file.writelines([''.join([''.join([str(image) + ' ' for image in slide]).strip()] + ['\n']) for slide in slides])

    # param example
    # slides = [[0], [3], [4], [5, 1]]
    @staticmethod
    def score(dataset, slides):
        score_total = 0

        for i in range(0, len(slides)):
            if(i == len(slides) - 1):
                break

            if(len(slides[i]) == 1):
                tags1 = dataset[slides[i][0]]['tags']
            else:
                tags1 = dataset[slides[i][0]]['tags'].union(dataset[slides[i][1]]['tags'])

            if(len(slides[i+1]) == 1):
                tags2 = dataset[slides[i+1][0]]['tags']
            else:
                tags2 = dataset[slides[i+1][0]]['tags'].union(dataset[slides[i+1][1]]['tags'])

            score_total += Common.score_between(tags1, tags2)

        return score_total

    @staticmethod
    def score_between(tags1, tags2):
        return min([len(tags1 - tags2), len(tags2 - tags1), len(tags1.intersection(tags2))])
