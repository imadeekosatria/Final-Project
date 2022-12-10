from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Berita, Ringkasan
from pathlib import Path
from .teks_processing import *
from .pso import *
from .pfnet import *
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
    if request.method == 'POST' and request.POST.get('title') and request.POST.get('mode') != 'comparison':
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

def comparison(request):
    data ={
        'id':'comparison',
        'title': 'UJI Coba',
    }
    return render(request, 'comparison.html', data)