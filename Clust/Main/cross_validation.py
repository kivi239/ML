from TrainSmall import training
import build_words_graph
from os import listdir
from os import mkdir
import os
import extract_text_topics
import gensim
from ExtractBigrams import prepare_sentence_stream
import re

files = listdir('../../OK/groups_sorted')


def is_image(s):
    return re.match('^I|images\[\[\d+\]\]$', s) is not None


print("Building model...")
model = gensim.models.Word2Vec.load_word2vec_format('../../Word2Vec/all.s200.w11.n1.v20.cbow.bin', binary=True, unicode_errors='ignore')
print("Build model")

K = 40


def read_post(group_id, post_id):
    if group_id + '.txt' not in files:
        return "-1"
    with open('../../OK/groups_sorted/' + group_id + '.txt', encoding='utf-8') as g:
        for line in g:
            data = line.split('\t')
            if data[0] == post_id:
                return data[1]

    return "-1"

f = open('../../OK/user_likes.txt', 'r', encoding='utf-8')
g = open('../../OK/user_dislikes.txt', 'r', encoding='utf-8')

line_f = f.readline()
line_g = g.readline()

cnt_all_users = 0
cnt_good_users = 0

tp = 0
tn = 0
fp = 0
fn = 0


while line_f != '' and line_g != '':
    cnt_all_users += 1

    line_f = line_f.rstrip('\n')
    line_g = line_g.rstrip('\n')
    data_f = line_f.split(':')
    data_g = line_g.split(':')
    if data_f[1] == '' or data_g[1] == '':
        line_f = f.readline()
        line_g = g.readline()
        continue

    user_id = data_f[0]
    if user_id != data_g[0]:
        print("WTF??? Wrong IDs!")
    print("user " + user_id)
    likes = data_f[1].replace(')(', '|').rstrip(')').lstrip('(')
    likes = likes.split("|")

    dislikes = data_g[1].replace(')(', '|').rstrip(')').lstrip('(')
    dislikes = dislikes.split("|")

    like_text_posts = open('like_texts.txt', 'w', encoding='utf-8')
    dislike_text_posts = open('dislike_texts.txt', 'w', encoding='utf-8')

    existing_likes = []
    for like in likes:
        Id = like.split(", ")
        group_id = Id[0]
        post_id = Id[1]
        text = read_post(group_id, post_id)
        if text == "-1" or is_image(text):
            continue

        existing_likes.append(text)

    cnt_likes = len(existing_likes)
    train_likes = existing_likes[0:int(cnt_likes * 0.8)]
    test_likes = existing_likes[int(cnt_likes * 0.8):]

    for like in train_likes:
        like_text_posts.write(like)
    like_text_posts.close()

    dislike_posts = []
    for dislike in dislikes:
        Id = dislike.split(", ")
        group_id = Id[0]
        post_id = Id[1]
        text = read_post(group_id, post_id)
        if is_image(text):
            continue
        dislike_posts.append(text)

    cnt_dislikes = len(dislike_posts)

    if cnt_dislikes < 20 or cnt_likes < 20:
        line_f = f.readline()
        line_g = g.readline()
        continue

    train_dislikes = dislike_posts[0:int(cnt_dislikes*0.8)]
    test_dislikes = dislike_posts[int(cnt_dislikes * 0.8):]

    for dislike in train_dislikes:
        dislike_text_posts.write(dislike)

    dislike_text_posts.close()

    if not os.path.isdir('../OK_recommend/user' + user_id):
        mkdir('../OK_recommend/user' + user_id)

    build_words_graph.build_graph('like_texts.txt', '../OK_recommend/user' + user_id + '/words_degrees_like.txt')
    training.train_small('like_texts.txt', 'like')
    build_words_graph.build_graph('dislike_texts.txt', '../OK_recommend/user' + user_id + '/words_degrees_dislike.txt')
    training.train_small('dislike_texts.txt', 'dislike')

    types = ['like', 'dislike']
    W_like = [0] * K
    W_dislike = [0] * K
    score_like = dict()
    score_dislike = dict()
    topic_of_words_like = dict()
    topic_of_words_dislike = dict()

    bad_user = False
    for typ in types:
        topic_score, word_in_topic, word_score, word_ids, id_words, newK = extract_text_topics.extract_text_topics(typ + '_texts.txt', typ, K, user_id, model)
        if newK != K:
            print("Too less words for that user :(")
            bad_user = True
            break
        W = None
        if typ == 'like':
            W = W_like
        else:
            W = W_dislike

        topic_scores_summary = 0
        for i in range(newK):
            topic_scores_summary += topic_score[i]

        for i in range(newK):
            W[i] = topic_score[i] #/ topic_scores_summary

        topic_of_words = dict()
        score = dict()
        for i in range(newK):
            word_score_summary = 0
            for p in word_in_topic[i]:
                word = p[1]
                word_score_summary += word_score[id_words[word]][0]

            for p in word_in_topic[i]:
                word = p[1]
                score[word] = word_score[id_words[word]][0]
                #if word_score_summary != 0:
                #    score[word] /= word_score_summary
                topic_of_words[word] = i
        if typ == 'like':
            score_like = score
            topic_of_words_like = topic_of_words
        else:
            score_dislike = score
            topic_of_words_dislike = topic_of_words

    # finish training

    if bad_user:
        line_f = f.readline()
        line_g = g.readline()
        continue
    PT = [0] * K

    for d in test_likes:
        sentences = prepare_sentence_stream.string_to_stream(d)
        if len(sentences) == 0:
            continue
        p_like = 0
        p_dislike = 0
        P_like = [0] * len(topic_of_words_like)
        P_dislike = [0] * len(topic_of_words_dislike)
        sum_like = 0
        sum_dislike = 0
        for sentence in sentences:
            for word in sentence:
                if word in topic_of_words_like:
                    P_like[topic_of_words_like[word]] += score_like[word]
                    sum_like += score_like[word]
                if word in topic_of_words_dislike:
                    P_dislike[topic_of_words_dislike[word]] += score_dislike[word]
                    sum_dislike += score_dislike[word]
        if sum_like == 0:
            sum_like = 1
        if sum_dislike == 0:
            sum_dislike = 1
        for i in range(K):
            p_like += (P_like[i] / sum_like) * W_like[i]
            p_dislike += (P_dislike[i] / sum_dislike) * W_dislike[i]

        if p_like >= p_dislike:
            tp += 1
        else:
            fn += 1

    for d in test_dislikes:
        sentences = prepare_sentence_stream.string_to_stream(d)
        if len(sentences) == 0:
            continue
        p_like = 0
        p_dislike = 0
        P_like = [0] * K
        P_dislike = [0] * K
        for sentence in sentences:
            for word in sentence:
                if word in topic_of_words_like:
                    P_like[topic_of_words_like[word]] += score_like[word]
                if word in topic_of_words_dislike:
                    P_dislike[topic_of_words_dislike[word]] += score_dislike[word]

        for i in range(K):
            p_like += P_like[i] * W_like[i]
            p_dislike += P_dislike[i] * W_dislike[i]

        if p_like < p_dislike:
            tn += 1
        else:
            fp += 1

    cnt_good_users += 1
    if cnt_good_users % 5 == 0:
        print("%d users were proceed (among of %d)" % (cnt_good_users, cnt_all_users))
        print("Precision: %.5f" % (tp / (tp + fp)))
        print("Recall: %.5f\n" % (tp / (tp + fn)))

    line_f = f.readline()
    line_g = g.readline()


