import json

def pfnet():
    print('running PFNet')
    #Load edge
    f = open('pso/jsonfile/edge.json')
    edge = json.load(f)
    f.close()


    #Load cosine similarity
    f = open('pso/jsonfile/cosine_similarity.json')
    cosine_similarity = json.load(f)
    f.close()
        
    for ed in edge:
        # Get start and end
        compar = {}
        start = ed[0]
        end = ed[1]
        direct = cosine_similarity['kalimat '+str(start)]['kalimat '+str(end)]
        indirect = 0
        compar[str(start)+','+str(end)] = direct
        for e in edge:
            if e[0] == start and e[1] != end: # jika posisi awal edge sama
                mid = e[1] # Jadi nilai tengah
                weight_start_mid = cosine_similarity['kalimat '+str(start)]['kalimat '+str(mid)]
                weight_mid_end = 0
                for f in edge:
                    if f[0] == mid and f[1] == end: # Jika posisi edge mid sama dengan posisi akhir
                        # print(start, end)
                        # print(start, mid, end)
                        weight_mid_end = cosine_similarity['kalimat '+str(mid)]['kalimat '+str(end)]
                        indirect = weight_start_mid + weight_mid_end
                        compar[str(start)+','+str(mid)+','+str(end)] = indirect
                        # print(compar)
                        temp = min(compar.values())
                        # print(temp)
                        if compar[str(start)+','+str(end)] == temp:
                            # print(True)
                            cosine_similarity['kalimat '+str(start)]['kalimat '+str(end)] = 0

    with open('pso/jsonfile/pfnet_cosine_similarity.json', 'w') as json_file:
        json.dump(cosine_similarity, json_file)