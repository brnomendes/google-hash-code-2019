
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


if __name__ == "__main__":
    Common.read_input_file('data/a_example.txt')
