import json, random, time

class PSO():
    def __init__(self, c1, c2, iteration, inertia, mode):
        # print('init')
        self.c1 = int(c1)
        self.c2 = int(c2)
        self.iteration = int(iteration)
        self.inertia = float(inertia)
        self.mode = mode
        # Read json file
        f = open('pso/jsonfile/cosine_similarity.json')

        self.cosine = json.load(f)
        f.close()

        self.cosine_similarity = {}

        for d in self.cosine:
            self.cosine_similarity[d] = self.cosine[d]

        f = open('pso/jsonfile/dict.json')

        self.dic = json.load(f)
        f.close()

        f = open('pso/jsonfile/ISCORE.json')

        self.info = json.load(f)
        f.close()

        f = open('pso/jsonfile/particle.json')

        self.particle = json.load(f)

        # print(particle)
        f.close()

    def init_particle(self):
        # print('init_particle')
        self.swarm = {}
        for d in self.particle: #inisiasi partikel
            self.swarm[d] = {} # init dictonary

            self.swarm[d]['posisi'] = self.particle[d] # init posisi

            # init velocity
            self.swarm[d]['velocity'] = []  
            for p in range(len(self.swarm[d]['posisi'])):
                self.swarm[d]['velocity'].append(0)
            # swarm[d]['gbest'] = False
            self.swarm[d]['prev_fitness'] = 0
            self.swarm[d]['prev_posisi'] = []
        return self.swarm

    def fitness(self, posisi):
        # print('fitness')
        total_fitness = 0
        for i in posisi:
            iscore = self.info['kalimat ' + str(i)] # Ambil Iscore
            sum = 0
            for d in posisi[1:3]: # Ambil cosine_similarity
                if d == i:
                    cos = 1 # posisi sama
                else:
                    cos = self.cosine_similarity['kalimat ' +str(i)]['kalimat ' +str(d)]
                sum += iscore * cos
            total_fitness += sum
        return total_fitness


    def find_iscore(self,pos):
        return self.info['kalimat '+ str(pos)]

    def velocity(self, v0, xbest, gbest, xi, p):
        # print('velocity')
        r1 = random.random()
        r2 = random.random()
        c1 = self.c1
        c2 = self.c2
        v = []
        for x in range(len(xi)):
            # Velocity
            # V = w*v0 + (c1*r1*(pBest - xi)) + (c2*r2*(gBest - xi))
            # V = velocity
            # w = inertia [0,1]
            # c1, c2 = cognitive [0,2]
            # r1, r2 = random [0,1]
            # xi = current position
            # pBest, gBest
            vt = 0.1*v0[x] + (c1*r1*(self.find_iscore(xbest[x]) - self.find_iscore(xi[x]))) + (c2*r2*(self.find_iscore(gbest[x]) - self.find_iscore(xi[x])))
            v.append(vt)
        self.swarm[p]['velocity'] = v
        

    def find_iscore_key(self,iscore):
        for i in self.info:
            if self.info[i] == iscore:
                return int(i[8:])

    def update_posisi(self, pos, velo,p):
        # print('update_posisi')
        atas = max(self.info, key=lambda x:self.info[x])
        bawah = min(self.info, key=lambda x:self.info[x])
        
        x_new = []
        for x in range(len(pos)):
            xt = self.find_iscore(pos[x]) + velo[x]
            if xt > self.info[atas]:
                xt = self.info[atas]
            if xt < self.info[bawah]:
                xt = self.info[bawah]
            x_new.append(xt)


        new_pos = []
        for x in range(len(x_new)):
            temp = []
            for i in self.info:
                calc = self.info[i] - x_new[x]
                # if calc >= 0:
                temp.append((int(i[8:]), abs(calc))) # Absolut
            
            # a_list = list(range(1, len(info))) # Simpan list iscore
            s = sorted(temp, key=lambda x:x[1])
        
            # Kemungkinan kepakai
            for m in s:
                if m[0] not in new_pos:
                    new_pos.append(m[0])
                    break

        self.swarm[p]['posisi'] = new_pos
        # print(p + ':' + str(new_pos))
        return self.swarm[p]['posisi']

    def run_pso(self):
        print('run_pso')
        gbest_pos = []
        gbest = 0
        final = []
        for it in range(self.iteration):
            print(it)
            total_fitness = []
            for p in self.swarm:
                posisi = self.swarm[p]['posisi']
                fitness_partikel = self.fitness(posisi)
                total_fitness.append(fitness_partikel)

                self.swarm[p]['fitness'] = fitness_partikel


            # Gbest
            gbest = max(total_fitness)
            for p in self.swarm:
                if gbest == self.swarm[p]['fitness']:
                    # swarm[p]['gbest'] = True
                    gbest_pos = self.swarm[p]['posisi']
                else:
                    # swarm[p]['gbest'] = False
                    pass

            print("GBest iterasi " +str(it) + ": "+str(gbest))
            print("GBest Solusi : " + str(gbest_pos))
            
            if not final:
                final = gbest_pos
            elif final == gbest_pos:
                length_swarm = len(self.swarm)
                count = 0
                for p in self.swarm:
                    if self.swarm[p]['posisi'] == gbest_pos:
                        count += 1
                if count == length_swarm:
                    break
            else:
                final = gbest_pos
                

            #Pbest
            for p in self.swarm:
                if self.swarm[p]['prev_fitness'] < self.swarm[p]['fitness']:
                    self.swarm[p]['prev_fitness'] = self.swarm[p]['fitness']
                    self.swarm[p]['prev_posisi'] = self.swarm[p]['posisi']


            # Update velocity
            for p in self.swarm:
                v0 = self.swarm[p]['velocity']
                pb = self.swarm[p]['prev_posisi']
                gb = gbest_pos
                xi = self.swarm[p]['posisi']
                self.velocity(v0, pb, gb, xi, p)
            # print(swarm)

            # Update Posisi
            for p in self.swarm:
                pos = self.swarm[p]['posisi']
                velo = self.swarm[p]['velocity']
                self.update_posisi(pos, velo, p)

        # print("best position : ", final)
        # print("\n")
        final = sorted(final)
        get_kalimat = []
        for f in final:
            get_kalimat.append(self.dic["kalimat " +str(f)]['kalimat'])
        
        data_pso = {'kalimat': get_kalimat, 'final': final, 'totalSebelum': len(self.info), 'totalSesudah': len(final)}
        return data_pso