from operator import itemgetter
import pymorphy2

file = "text/ch.txt"

morph = pymorphy2.MorphAnalyzer()

separators = ['...', '.', ',', '?', '!', ';']
trash = ['"', '--', '(', ')']

# we will cache normal forms of words
normal_forms = dict()
id_words = dict()
word_ids = ['?']
graph = [set()]

cur_id = 1

with open(file) as f:
    for line in f:
        line = line.rstrip("\n")
        print(line)
        for sep in separators:
            line = line.replace(sep, '|')
        data = line.split('|')
        for sentence in data:
            words = sentence.split(" ")
            for word in words:
                for t in trash:
                    word = word.replace(t, "")
                if word == "":
                    continue
                if word in normal_forms:
                    word = normal_forms[word]
                else:
                    norm_word = morph.parse(word)[0].normal_form
                    normal_forms[word] = norm_word
                    word = norm_word
                    id_words[word] = cur_id
                    word_ids.append(word)
                    cur_id += 1

                if len(graph) < id_words[word] + 1:
                    graph.append(set())

            for word in words:
                for t in trash:
                    word = word.replace(t, "")

                if word == "":
                    continue

                word = normal_forms[word]
                id_word = id_words[word]
                for neighbor in words:
                    for t in trash:
                        neighbor = neighbor.replace(t, "")
                    if neighbor == "":
                        continue

                    neighbor = normal_forms[neighbor]
                    if neighbor == word:
                        continue
                    id_neighbor = id_words[neighbor]
                    graph[id_word].add(id_neighbor)


node_with_d = [('?', -1)] * cur_id
for i in range(1, cur_id):
    node_with_d[i] = (word_ids[i], len(graph[i]))

node_with_d.sort(key=itemgetter(1), reverse=True)
g = open('clusters/words_degrees.txt', 'w')
for t in node_with_d:
    g.write(t[0] + ' ' + str(t[1]))
    g.write('\n')





