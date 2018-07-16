import os


def create_project_dir(directory):
    if not os.path.exists(directory):
        print('creating project ' + directory)
        os.makedirs(directory)


def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'

    write_file(queue, base_url)
    write_file(crawled, '')


def write_file(fileName, data):
    if not os.path.isfile(fileName):
        with open(fileName, 'w+') as file:
            file.write(data)


def append_to_file(fileName, data):
    with open(fileName, 'a') as file:
        file.write(data + '\n')


def delete_file_contents(fileName):
    open(fileName, 'w').close()


def file_to_set(fileName):
    results = set()
    with open(fileName, 'rt') as file:
        for line in file:
            results.add(line.replace('\n', ''))
    return results


def set_to_file(links, fileName):
    with open(fileName, 'w') as file:
        for link in sorted(links):
            file.write(link + "\n")
