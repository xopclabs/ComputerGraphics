def obj_to_coords(path):
    v = []
    f = []
    coords = []
    with open(path, 'r') as file:
       for l in file.readlines():
            l = l.split()
            if l == []:
                continue
            if l[0] == 'v':
                l = [float(x) for x in l[1:]]
                v.append(l)
            elif l[0] == 'f':
                l = [int(x.split('/')[0]) - 1 for x in l[1:]]
                fix_negatives = lambda x: -1 if x <= -2 else x
                l = [fix_negatives(x) for x in l]
                f.append(l)
    for p in f:
        coords.append([v[i] for i in p[:3]])
    return coords
