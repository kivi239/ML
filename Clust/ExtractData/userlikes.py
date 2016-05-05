user_likes = dict()

with open('../../OK/big_likes_file.tsv/big_likes_file.tsv') as f:
    cnt = 0
    for line in f:
        line = line.rstrip('\n')
        data = line.split("\t")
        #print(data)
        data[0] = data[0].lstrip('(')
        data[0] = data[0].rstrip(')')
        post = data[0].split(',')

        data[1] = data[1].lstrip('{').rstrip('}')
        data[1] = data[1].replace('(', '').replace(')', '')

        likes = data[1].split(',')[0::2]

        post_id = (int(post[1]), int(post[2]))
        for user in likes:
            user = int(user)
            if user not in user_likes:
                user_likes[user] = []
            user_likes[user].append(post_id)

        cnt += 1
        if cnt % 10000 == 0:
            print("%d lines proceed" % cnt)


f = open('../../OK/userlikes.txt', 'w', encoding='utf-8')
for user in user_likes:
    f.write(str(user) + ':')
    for post in user_likes[user]:
        f.write(str(post))
    f.write('\n')
