from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .models import Berita, Ringkasan, Comparison, Testing
from pathlib import Path
from .teks_processing import *
from .pso import *
from .pfnet import *
import json, os
# Create your views here.
def index(request):
    content = {
        'title' : 'Peringkasan Teks menggunakan PSO dan PFNet',
        'id': 'home',
        'js': 'index.js',
    }
    
    return render(request, 'index.html', content)

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def file_upload(request):
    if request.method == 'POST' and request.FILES['berita']:
        myfile = request.FILES['berita']
        # print(myfile.read().decode('utf-8'))
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        filedb = Berita(judul=myfile.name, teks=myfile.read().decode('utf-8'), file=myfile)
        filedb.save()
        
        
        # return render(request, 'index.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })
        return redirect('overview/'+str(myfile.name))
    # return render(request, 'index.html')
def manual(request):
    if request.method == 'POST' and request.POST.get('title'):
        filename = request.POST.get('title')
        text = request.POST.get('teks')
        file = open('pso/berita/'+str(filename)+'.txt', 'w+', encoding='utf-8')
        file.write(text)
        file.close()
        filedb = Berita(judul=str(filename)+'.txt', teks = text, file=str(filename)+'.txt')
        filedb.save()
        return redirect('overview/'+str(filename)+'.txt')


def overview(request, name):
    t = Berita.objects.get(judul=name)
    f = open('pso/berita/'+str(t.file), encoding='utf-8')
    text = f.read()
    title = Path(name).stem
    f.close()
    # text_preprocessing(text, title)
    data = {'title': title, 'teks': text, 'js': 'overview.js', 'id': 'overview'}
    return render(request, 'overview.html', data)

def pso_process(request):
    if request.method == 'POST' and request.POST.get('mode') != 'comparison' :
        start = time.perf_counter()
        title = request.POST.get('title')
        teks = request.POST.get('teks')
        mode = request.POST.get('mode')

        text_preprocessing(request.POST.get('teks'), request.POST.get('title'), request.POST.get('population'), request.POST.get('summary'))
    
        if mode == 'pso_pfnet':
            pfnet()
        
        p = PSO(request.POST.get('c1'), request.POST.get('c2'), request.POST.get('iteration'), request.POST.get('inertia'), mode = mode)
        p.init_particle()
        summarization = p.run_pso()
        summary = ' '.join(map(str, summarization['kalimat']))        
        end = time.perf_counter()
        timelapsed = (end - start)

        # Save DB
        dbringkasan = Ringkasan(judul=title, teks_asli =teks, ringkasan = summary, kalimat=summarization['final'], iteration=request.POST.get('iteration'), particle=request.POST.get('population'), timelapsed = timelapsed, total_sebelum = summarization['totalSebelum'], total_sesudah=summarization['totalSesudah'], mode=request.POST.get('mode'))
        dbringkasan.save()

        data = {'timelapsed': int(timelapsed),'title': request.POST.get('title'), 'summarization': summarization, 'js':'result.js', 'id':'result', 'iteration': summarization['iteration'], 'iteration_base': request.POST.get('iteration'),'particle':request.POST.get('population'), 'mode': request.POST.get('mode')}
        return render(request, 'result.html', data)

    elif request.method == 'POST' and request.POST.get('mode') == 'comparison':
        #Text Processing 
        start_text_prep =time.perf_counter()
        title = request.POST.get('title')
        teks = request.POST.get('teks')
        c1 = request.POST.get('c1')
        c2 = request.POST.get('c2')
        iteration = request.POST.get('iteration')
        inertia = request.POST.get('inertia')
        population = request.POST.get('population')
        summary = request.POST.get('summary')

        text_preprocessing(text=teks, title=title, population=population, summary=summary)

        end_text_prep = time.perf_counter()
        text_prep_time = (end_text_prep - start_text_prep)
        
        #PSO
        start_pso_only = time.perf_counter()
        
        #init Object
        pso_only = PSO(c1=c1, c2=c2, iteration=iteration, inertia=inertia)
        pso_only.init_particle()
        data_pso = pso_only.run_pso()
        summary_pso = ' '.join(map(str, data_pso['kalimat']))        

        # Calculate timelapsed_pso
        end_pso_only = time.perf_counter()
        pso_time = (end_pso_only - start_pso_only)
        timelapsed_pso = int(text_prep_time + pso_time)

        # PFNet
        start_pfnet = time.perf_counter()
        pfnet()
        mode = 'pso_pfnet'

        #ini Object
        pfnet_mode = PSO(c1=c1, c2=c2, iteration=iteration, inertia=inertia, mode=mode)
        pfnet_mode.init_particle()
        data_pfnet = pfnet_mode.run_pso()
        summary_pfnet = ' '.join(map(str, data_pfnet['kalimat']))        
        
        # Calculate timelapsed_pfnet
        end_pfnet = time.perf_counter()
        pfnet_time = (end_pfnet - start_pfnet)
        timelapsed_pfnet = int(text_prep_time + pfnet_time)

        #Save DB
        dbcomparison = Comparison(
            judul=title,
            teks_asli = teks,

            ringkasan_pso = summary_pso,
            kalimat_pso = data_pso['final'],
            iteration_done_pso = data_pso['iteration'],
            iteration_pso = iteration,
            particle_pso = population,
            timelapsed_pso = timelapsed_pso,
            total_sebelum_pso = data_pso['totalSebelum'],
            total_sesudah_pso = data_pso['totalSesudah'],

            ringkasan_pfnet = summary_pfnet,
            kalimat_pfnet = data_pfnet['final'],
            iteration_done_pfnet = data_pfnet['iteration'],
            iteration_pfnet = iteration,
            particle_pfnet = population,
            timelapsed_pfnet = timelapsed_pfnet,
            total_sebelum_pfnet = data_pfnet['totalSebelum'],
            total_sesudah_pfnet = data_pfnet['totalSesudah']
        )

        dbcomparison.save()

        # Return Data
        data = {
            'pfnet':data_pfnet,
            'pfnet_summary':summary_pfnet,
            'pfnet_time':timelapsed_pfnet,
            'pso':data_pso,
            'pso_summary':summary_pso,
            'pso_time':timelapsed_pso,
            'title':title,
            'id': 'comparison',
            'particle': population,
            'iteration':iteration,
            }
        return render(request, 'comparison.html', data)
    elif request.method == 'POST' and request.POST.get('testing_iteration'):
        start_text_prep =time.perf_counter()
        title = request.POST.get('title')
        teks = request.POST.get('teks')
        c1 = request.POST.get('c1')
        c2 = request.POST.get('c2')
        iteration = request.POST.get('iteration')
        inertia = request.POST.get('inertia')
        population = request.POST.get('population')
        summary = request.POST.get('summary')
        testing_iteration = int(request.POST.get('testing_iteration'))
        mode = request.POST.get('mode')
        play_sound()
        text_preprocessing(text=teks, title=title, population=population, summary=summary)

        end_text_prep = time.perf_counter()
        text_prep_time = (end_text_prep - start_text_prep)
        play_sound()
        data = {'c1':c1, 'c2':c2, 'inertia':inertia, 'iteration':iteration,'text_prep_time':text_prep_time, 'name':title, 'populations': population}

        testing = testingMode(iteration=testing_iteration,mode=mode, data=data)
        play_sound()
        return render(request, 'resultTesting.html', testing)

        # return JsonResponse(testing)

def play_sound():
    from playsound import playsound
    alarm = ['Mina.wav', 'tzuyu 1.wav', 'tzuyu 2.wav', 'tzuyu 3.wav', 'tzuyu 4.wav', 'tzuyu 5.wav']
    sound = random.choice(alarm)
    playsound('pso/alarm/'+str(sound))
        
def get_result_json(request, name):
    berita = Testing.objects.get(judul=name)
    if request.method == 'GET':
        f = open(berita.jsonfile)
        data = json.load(f)
        f.close()
    return JsonResponse(data)

def testingMode(iteration, mode, data):
    print("Mode Testing...\n")
    name = data['name']
    data_test = {}
    if mode == 'pso_only':
        data_test
        data_test['Mode']= 'PSO'
        data_test['iteration'] = data['iteration']
        data_test['populations'] = data['populations']
        data_test['Uji']= testingProses(iteration=iteration, data=data, mode=mode, text_time=data['text_prep_time'])
        
    elif mode == 'pso_pfnet':
        pfnet()
        data_test['Mode'] ='PSO + PFNet'
        data_test['iteration'] = data['iteration']
        data_test['populations'] = data['populations']
        data_test['Uji']=testingProses(iteration=iteration, data=data, mode=mode, text_time=data['text_prep_time'])
                
    elif mode == 'comparison':
        data_test['Mode'] = 'comparison'
        data_test['iteration'] = data['iteration']
        data_test['populations'] = data['populations']
        data_test['Uji'] = {}
        print("Running PSO Testing") 
        play_sound()
        data_test['Uji']['PSO'] = testingProses(iteration=iteration, data=data, mode='pso_only', text_time=data['text_prep_time'])
        
        print("Running PFNet")
        play_sound()
        pfnet()
        print("Running PSO + PFNet Testing") 
        data_test['Uji']['PFNet'] =testingProses(iteration=iteration, data=data, mode='pso_pfnet', text_time=data['text_prep_time'])
    
    counter = 0
    filename = 'pso/jsonfile/data pengujian/'+str(name)+'{}.json'
    while os.path.isfile(filename):
        counter += 1
    filename = filename.format(counter)

    with open(filename, 'w') as json_file:
        json.dump(data_test, json_file)

    dbTesting = Testing(judul=name, jsonfile=filename)
    dbTesting.save()    

    testing = {'id':'testing','name':name,'testing':True,'js':'result.js', 'mode': data_test['Mode'], 'iteration': data_test['iteration'], 'populations':data['populations']}

    return testing

def testingProses(iteration, data, mode, text_time):
    data_dict = {}
    print("Testing Proses")
    time.sleep(1)
    
    for i in range(iteration):
        print("Testing "+str(i+1))
        time.sleep(3)
        play_sound()
        data_dict['test '+ str(i+1)] = {}
        start_pso = time.perf_counter()
        pso = PSO(c1=data['c1'], c2=data['c2'], inertia=data['inertia'], iteration=data['iteration'], mode=mode)
        pso.init_particle()
        result = pso.run_pso()
        end_pso = time.perf_counter()
        timelapsed = int(end_pso - start_pso)
        data_dict['test '+ str(i+1)]['kalimat'] = result['final']
        data_dict['test '+ str(i+1)]['iteration finish'] = result['iteration']
        data_dict['test '+ str(i+1)]['timelapsed'] = int(timelapsed+text_time)
        data_dict['test '+ str(i+1)]['gbest'] = result['gbest']
        data_dict['test '+ str(i+1)]['total_sebelum'] = result['totalSebelum']
        data_dict['test '+ str(i+1)]['total_sesudah'] = result['totalSesudah']
                 

    return data_dict

    

def comparison(request):
    data ={
        'id':'comparison',
        'title': 'UJI Coba',
    }
    return render(request, 'resultTesting.html', data)

def resultTesting(request, name):
    berita = Testing.objects.get(judul=name)
    f = open(berita.jsonfile)
    data_json = json.load(f)
    f.close()
    data = {
        'id': 'testing',
        'testing': True,
        'name': name,
        'mode': data_json['Mode'],
        'iteration': data_json['iteration'],
        'populations': data_json['populations'],
    }

    return render(request, 'resultTesting.html', data)