from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Berita
from pathlib import Path
from .teks_processing import *
from .pso import *
# Create your views here.
def index(request):
    content = {
        'title' : 'Peringkasan Teks menggunakan PSO dan PFNet',
        'id': 'home',
        'js': 'index.js',
    }
    
    return render(request, 'index.html', content)

def file_upload(request):
    if request.method == 'POST' and request.FILES['berita']:
        myfile = request.FILES['berita']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        filedb = Berita(name=myfile.name)
        filedb.save()
        
        
        # return render(request, 'index.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })
        return redirect('overview/'+str(myfile.name))
    # return render(request, 'index.html')
    elif request.method == 'POST' and request.POST.get('title'):
        filename = request.POST.get('title')
        text = request.POST.get('teks')
        file = open('pso/berita/'+str(filename)+'.txt', 'w+', encoding='utf-8')
        file.write(text)
        file.close()
        filedb = Berita(name=str(filename)+'.txt')
        filedb.save()
        return redirect('overview/'+str(filename)+'.txt')


def overview(request, name):
    f = open('pso/berita/'+str(name), encoding= 'utf-8')
    text = f.read()
    title = Path(f.name).stem
    f.close()
    # text_preprocessing(text, title)
    data = {'title': title, 'teks': text, 'js': 'overview.js', 'id': 'overview'}
    return render(request, 'overview.html', data)

def pso_process(request):
    if request.method == 'POST' and request.POST.get('title'):
        text_preprocessing(request.POST.get('teks'), request.POST.get('title'), request.POST.get('population'), request.POST.get('summary'))

        p = PSO(request.POST.get('c1'), request.POST.get('c2'), request.POST.get('iteration'), request.POST.get('inertia'), request.POST.get('mode'))
        p.init_particle()
        summarization = p.run_pso()
        
        data = {'title': request.POST.get('title'), 'summarization': summarization, 'js':'result.js', 'id':'result', 'iteration': request.POST.get('iteration'),'particle':request.POST.get('population'), 'mode': request.POST.get('mode')}
        return render(request, 'result.html', data)