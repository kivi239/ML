
separators = ['...', '.', '?', '!', ',', ';']
trash = ['"', '--', '(', ')', ':']


def remove_empty_lists(stream):
    new_stream = []
    for l in stream:
        if len(l) != 0:
            new_stream.append(l)

    return new_stream


def file_to_stream(filename, seps=separators, trs=trash):
    print("here")
    sentence_stream = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            print(line)
            for sep in seps:
                line = line.replace(sep, '|')
            paragraph = line.split('|')
            for sentence in paragraph:
                sentence_stream.append([])
                words = sentence.split(" ")
                for word in words:
                    for t in trs:
                        word = word.replace(t, "")
                    if word == "":
                        continue
                    cur_id = len(sentence_stream) - 1
                    sentence_stream[cur_id].append(word)

    sentence_stream = remove_empty_lists(sentence_stream)
    return sentence_stream

