import operator
from os import listdir
import datetime

path = '../../OK/groups_sorted/'


def sort_posts(posts):
    sorted_posts = sorted(posts, key=operator.itemgetter(1), reverse=True)
    return sorted_posts


def print_sort_posts(file, posts):
    posts = sort_posts(posts)
    g = open(path + file, 'w', encoding='utf-8')
    for post in posts:
        g.write(str(post[0]) + '\t' + post[2])


def read_posts(file):
    rposts = []
    with open("../../OK/groups/" + file, encoding='utf-8') as f:
        for line in f:
            data = line.split("\t")
            date = datetime.datetime.strptime(data[1][:-6], "%Y-%m-%dT%H:%M:%S.%f")
            rposts.append((data[0], date, data[2]))
    return rposts

files = listdir('../../OK/groups')
for file_name in files:
    #print(file_name)
    posts = read_posts(file_name)
    print_sort_posts(file_name, posts)


