from os import listdir

pathOK = '../../OK/'


def read_posts_from_group(filename):
    id_list = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            data = line.split('\t')
            id_list.append(data[0])
    return id_list


all_groups = listdir(pathOK + 'groups_sorted/')
cache = dict()

g = open(pathOK + 'user_dislikes.txt', 'w', encoding='utf-8')

with open(pathOK + 'user_likes.txt', encoding='utf-8') as f:
    cnt = 0
    cnt_unload = 0
    cnt_all = 0
    for line in f:
        line = line.rstrip('\n')
        data = line.split(':')
        user_id = data[0]
        likes = data[1].replace(')(', '|').rstrip(')').lstrip('(')
        likes = likes.split("|")

        dislikes = []
        print(user_id)
        for like in likes:
            cnt_all += 1
            Id = like.split(", ")
            group_id = Id[0]
            post_id = Id[1]

            if group_id + '.txt' not in all_groups:
                #print('this group was not loaded :(')
                cnt_unload += 1
                continue
            posts = []
            if group_id not in cache:
                posts = read_posts_from_group(pathOK + 'groups_sorted/' + group_id + '.txt')
                cache[group_id] = posts
            else:
                posts = cache[group_id]

            if post_id not in posts:
                #print('this post was not loaded :(')
                cnt_unload += 1
                continue
            pos_post = posts.index(post_id)
            if pos_post + 1 < len(posts) and (group_id + ', ' + posts[pos_post + 1] not in likes):
                dislikes.append((int(group_id), int(posts[pos_post + 1])))

        g.write(user_id + ":")
        for dislike in dislikes:
            g.write(str(dislike))
        g.write('\n')

        cnt += 1
        if cnt % 10000 == 0:
            print("%d users proceed" % cnt)

print("%d posts was not load of %d" % (cnt_unload, cnt_all))