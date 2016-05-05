from ExtractBigrams import prepare_sentence_stream
import datetime
import operator

from os import listdir

separators = ['...', '.', '?', '!', ',', ';', '…']
trash = ['"', '---','--', '(', ')', ':', '***']

prev_id = -1
posts = []

path = '../../OK/Parts/'
files = listdir('../../OK/Parts/')

for file in files:
    print(path + file)
    with open(path + file, encoding='utf-8') as f:
        cnt = 0
        g = open('../../OK/groups/-1.txt', 'w', encoding='utf-8')
        for line in f:
            cnt += 1
            if cnt % 10000 == 0:
                print("%d lines proceed" % cnt)

            line = line.rstrip('\n')
            data = line.split('\t')
            if len(data) != 5:
                print("Warning, tab appears in text")
            group_id = data[0]
            post_id = data[2]
            if group_id != prev_id:
                if prev_id != -1:
                    #sorted_posts = sorted(posts, key=operator.itemgetter(2))
                    for post in posts:
                        try:
                            g.write(str(post[0]) + '\t' + post[1] + '\t' + post[2] + '\n')
                        except UnicodeEncodeError:
                            print("Error in %s %d" % (file, cnt))
                g = open('../../OK/groups/' + group_id + '.txt', 'a', encoding='utf-8')
                posts = []

            #date = datetime.datetime.strptime(data[3][:-6], "%Y-%m-%dT%H:%M:%S.%f")
            posts.append((post_id, data[3], data[4]))

            prev_id = group_id

    for post in posts:
        g.write(str(post[0]) + '\t' + post[1] + '\t' + post[2] + '\n')
