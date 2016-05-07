from TrainSmall import training
import build_words_graph
from os import listdir
from os import mkdir
import os
import extract_text_topics
import gensim

files = listdir('../../OK/groups_sorted')

print("Building model...")
model = gensim.models.Word2Vec.load_word2vec_format('../../Word2Vec/all.s200.w11.n1.v20.cbow.bin', binary=True, unicode_errors='ignore')
print("Build model")

K = 30


def read_post(group_id, post_id):
    if group_id + '.txt' not in files:
        return "-1"
    with open('../../OK/groups_sorted/' + group_id + '.txt', encoding='utf-8') as g:
        for line in g:
            data = line.split('\t')
            if data[0] == post_id:
                return data[1]

    return "-1"


with open('../../OK/user_likes.txt', encoding='utf-8') as f:
    cnt = 0
    for line in f:
        line = line.rstrip('\n')
        data = line.split(':')
        user_id = data[0]
        likes = data[1].replace(')(', '|').rstrip(')').lstrip('(')
        likes = likes.split("|")
        if len(likes) < 20:
            continue

        g = open('texts.txt', 'w', encoding='utf-8')

        cnt_existing_posts = 0
        for like in likes:
            Id = like.split(", ")
            group_id = Id[0]
            post_id = Id[1]
            text = read_post(group_id, post_id)
            if text == "-1":
                continue

            cnt_existing_posts += 1
            g.write(text)
        g.close()
        if cnt_existing_posts < 15:
            continue

        if not os.path.isdir('../OK_results/user' + user_id):
            mkdir('../OK_results/user' + user_id)

        build_words_graph.build_graph('texts.txt', '../OK_results/user' + user_id + '/words_degrees.txt')
        training.train_small('texts.txt')
        extract_text_topics.extract_text_topics('texts.txt', K, user_id, model)

        cnt += 1
        print("For %d users interests profile was built", cnt)


