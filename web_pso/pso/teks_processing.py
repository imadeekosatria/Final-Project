import string
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import math, json, random


def text_preprocessing(text, title, population, summary):
    new_text =  ' '.join(text.splitlines())
        
    # Segmentasi
    print('Segmentasi')
    dict = {}
    n = 1
    for i in new_text.split('. '):
        for k in i.split('\n'):
            if i == '':
                break
            # i = re.sub('\s+', ' ', i)
            tes = {'kalimat' : i+'.'}
            dict['kalimat ' + str(n)] = tes
            n += 1

    # Filterisasi dan lower case
    print('filterisasi dan lower case')
    no = 1
    for dic in dict:
        text_example = dict['kalimat ' + str(no)]['kalimat'].lower()
            # re_punct = "".join([char for char in text_example if char not in string.punctuation])
        text = re.sub(r"\d+", "", text_example)
        text = text.translate(str.maketrans("","", string.punctuation))
        text = re.sub('\s+', ' ', text)

        dict['kalimat ' + str(no)]['lower_punct'] = text
        no +=1

    title_lower = title.lower()
    count_title = len(title_lower.split())

    # Tokenisasi
    print('tokenisasi')
    bag_of_word = []

    no = 1
    for dic in dict:
        token = word_tokenize(dict['kalimat ' + str(no)]['lower_punct'])
        dict['kalimat ' + str(no)]['token'] = token
        bag_of_word.append(token)
        no += 1        
    
    # get Indonesian stopword 
    print('get Indonesia stopword')
    list_stopwords = set(stopwords.words('indonesian'))
    no = 1
    for kalimat in dict:
        for token in dict['kalimat ' + str(no)]['token']:
            new_token = [token for token in dict['kalimat ' + str(no)]['token'] if not token in list_stopwords]
            dict['kalimat ' + str(no)]['token'] = new_token


    # Stemming
    print('stemming')
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    for x in range(len(dict)):
        token = dict['kalimat ' + str(x+1)]['token']
        new_token = []
        for i in token: 
            hasil = stemmer.stem(i)
            new_token.append(hasil)
        dict['kalimat ' + str(x+1)]['token'] = new_token
    
    # Bag of Word Proccess
    print('bag_of_word')
    bag_of_word = []
    no = 1
    for token in dict:
        bag_of_word += dict['kalimat ' + str(no)]['token']
        no += 1
    # Remove duplicate of bag_of_word
    print('remove duplicate of bag_of_word')
    new_bag_of_word = []
    [new_bag_of_word.append(x) for x in bag_of_word if x not in new_bag_of_word]

    #TF
    print('TF')
    for kalimat in dict:
        token = dict[kalimat]['token']
        time_freq = {}
        for word in new_bag_of_word:
            count = 0
            for x in token:
                if(x == word):
                    count += 1
            time_freq[word] = count / len(token)
        dict[kalimat]['time_freq_normalized'] = time_freq

    #DF
    print('DF')
    df = {}
    for word in new_bag_of_word:
        count = 0
        for x in dict:
            for y in dict[x]['token']:
                if word == y:
                    count +=1
            df[word] = count
    
    #IDF
    print('IDF')
    idf = {}
    for word in new_bag_of_word:
        idf[word] = math.log(len(dict)/df[word])

    #TF.IDF
    print('TF-IDF')
    # all_tf_idf =[]
    
    for kalimat in dict:
        tf_idf_sentence_with_sentence = {}
        tf_idf_sentence = []
        tf = dict[kalimat]['time_freq_normalized']
        
        for word in new_bag_of_word:
            tf_idf = tf[word] * idf[word]
            tf_idf_sentence.append(tf_idf)
            tf_idf_sentence_with_sentence[word] = tf_idf 

        dict[kalimat]['TF-IDF'] = tf_idf_sentence
        dict[kalimat]['TF-IDF with sentence'] = tf_idf_sentence_with_sentence
    
    #SUM TF-IDF per kalimat
    print('Sum TF-IDF per kalimat')
    for kalimat in dict:
        tf_idf = dict[kalimat]['TF-IDF']
        # print(len(tf_idf))
        sum = 0
        for n in range(len(tf_idf)):
            sum += tf_idf[n]
        dict[kalimat]['Sum TF-IDF'] = sum

    # Tittle Similarity
    print('Title Similarity')
    for kalimat in dict:
        word_in_title = 0
        sentence = dict[kalimat]['kalimat'].split()
        for word in sentence:
            for word_title in title_lower.split():
                if word == word_title:
                    word_in_title += 1
        title_similarity = word_in_title / len(title_lower.split())
        dict[kalimat]['title_similarity'] = title_similarity

    # Sentence length feature (L)
    print('Sentence length feature')
    # Max Length of Text
    print('Max Length of Text')
    max_length = 0
    for kalimat in dict:
        length_sentence = dict[kalimat]['kalimat'].split()
        if max_length <= len(length_sentence):
            max_length = len(length_sentence)
    print(max_length)    

    # Length feature each sentence
    print('Length feature each sentence')
    for kalimat in dict:
        count = 0
        sentence = len(dict[kalimat]['kalimat'].split())

        
        dict[kalimat]['length'] = sentence / max_length
    
    # Location feature
    print('Location feature')
    for kalimat in dict:
        loc_s = kalimat[8:] 
        loc = 1 - (int(loc_s) / len(dict))
        dict[kalimat]['Loc'] = loc

    # ISCORE
    print('ISCORE')
    iscore_list = {}
    for kalimat in dict:
        t = dict[kalimat]['title_similarity']
        l = dict[kalimat]['length']
        loc = dict[kalimat]['Loc']
        sum_tf_idf = dict[kalimat]['Sum TF-IDF']
        iscore = t + l + loc + sum_tf_idf

        dict[kalimat]['ISCORE'] = iscore
        iscore_list[kalimat] = iscore 

    print('Export Iscore JSON')
    with open('pso/jsonfile/ISCORE.json', 'w') as json_file:
        json.dump(iscore_list, json_file)

    #Cosine Similarity
    print('Cosine Similarity')
    for kalimat1 in dict:

        kalimat_1 = dict[kalimat1]['TF-IDF']
        # cosine_similarity = {} 
        dict[kalimat1]['cosine_similarity'] = {}
        dict[kalimat1]['edge ' + kalimat1] = {}

        for kalimat2 in (dict): 
            kalimat_2 = dict[kalimat2]['TF-IDF']
            ab = [] # atas
            a = [] # ||A||
            b = [] # ||B||

            if kalimat_2 != kalimat_1:
            # Calculate Cosine
                # cosine_similarity= {}
                for x in range(len(kalimat_1)):
                    ab.append(kalimat_1[x] * kalimat_2[x]) # A * B
                    a.append(pow(kalimat_1[x],2)) # ||A||
                    b.append(pow(kalimat_2[x],2)) # ||B||
            
                sum_ab = 0 # init sum A * B
                for y in (ab):
                    sum_ab += y 
                
                sum_a = 0 # init sum ||A||
                sum_b = 0 # init sum ||B||

                for z in (a):
                    sum_a += z

                for z in (b):
                    sum_b += z
            
                a_b = math.sqrt(sum_a) * math.sqrt(sum_b) # ||A|| * ||B||
                cosine_similarity = sum_ab / a_b
                dict[kalimat1]['cosine_similarity'][kalimat2] = cosine_similarity
                dict[kalimat1]['edge ' + kalimat1][int(kalimat2[8:])] = cosine_similarity

    # DUMP cosine_similarity
    print('Export Cosine Similarity JSON')
    cosine_similarity = {}
    for x in dict:
        cosine_similarity[x] = dict[x]['cosine_similarity']
            # Export JSON
           
        with open('pso/jsonfile/cosine_similarity.json', 'w') as json_file:
            json.dump(cosine_similarity, json_file)

    # Graf I
    # Edge
    print('Graf I')
    for kalimat in dict:
        edge_kalimat = []
        kalimat1 = dict[kalimat]['cosine_similarity']
        for key in kalimat1:
            if (kalimat1[key] != 0):
                tupple = (int(kalimat[8:]), int(key[8:]))
                edge_kalimat.append(tupple)
        dict[kalimat]['edge'] = edge_kalimat

    edge = []
    # Kumpulkan semua edge
    for kalimat in dict:
        edge1 = dict[kalimat]['edge']
        for e in edge1:
            edge.append(e) 
                            
    # Hapus duplikat edge
    for e in edge:
        a = e[0]
        b = e[1]
        for x in edge:
            if e != x:
                c = x[0]
                d = x[1]
                if a == d and b == c:
                    edge.remove(x)
    print('Export edge JSON')
    with open('pso/jsonfile/edge.json', 'w') as json_file:
        json.dump(edge, json_file)
    # Graf II
    print('Graf II')
    vertex = [] # Vertex
    for i in range(len(dict)):
        vertex.append(i + 1)

    #Create particles
    print('Create particles')
    particle = {}
    # percentage = int(summary)/100
    # print(percentage)
    for i in range(int(population)):
        # print('Loop ',i)
        jalur = []
        while len(jalur) != math.ceil(len(vertex)*int(summary)/100): # <--- len(vertex)*2/10 atau int 4
            r = random.choice(vertex)
            if r not in jalur:
                jalur.append(r)
            jalur.sort()
            
        particle[i+1] = jalur
    
    print('Export particle JSON')
    with open('pso/jsonfile/particle.json', 'w') as json_file:
        json.dump(particle, json_file)
    print('Export dict JSON')
    with open('pso/jsonfile/dict.json', 'w') as json_file:
        json.dump(dict, json_file)