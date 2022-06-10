

from que import queue
t = [3, 6, 7]
e = [8, 4, 7]
d = map(lambda x: x, enumerate(t))


def getMinCost(crew_id, job_id):
    crew_id.sort()
    job_id.sort()
    # Write your code here
    assign = list(
        map(lambda x: abs(crew_id[x[0]] - job_id[x[0]]), enumerate(crew_id)))
    return sum(assign)


print(getMinCost(t, e))


def decrypPassword(s):
    # Write your code here
    res = []
    skip = None
    for i, j in enumerate(s):
        if i == skip:
            skip = None
            print("skipping", s[i])
            continue
        if j.isdigit():
            print("int", j)
            res.append('0')
            res.insert(0, s[i])
            continue
        if i <= len(s)-2:
            if s[i].islower() and s[i+1].isupper():
                res.append(f"{s[i+1]}{s[i]}*")
                skip = i+1
                continue
        res.append(j)
    return ''.join(res)


def decryptPassword(s):
    # Write your code here
    _s = [i for i in s]
    queue = []

    skip = []
    for i, j in enumerate(s):
        if j.isdigit() and not j == "0":
            queue.append(j)
            _s[i] = '-'
        if j == '0':
            _s[i] = queue.pop(-1)

        if i <= len(s)-3:
            if j.isupper() and s[i+1].islower() and s[i+2] == '*':
                skip.append(i)
                skip.append(i+1)
                # skip.append(i+2)
                _s[i] = s[i+1]
                _s[i+1] = s[i]
                _s[i+2] = '-'
    print(skip)
    return ''.join([e for e in _s if e != "-"])


print(decryptPassword("51Pa*0Lp*0eyy"))
