from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from apps.mascota.forms import MascotaForm
from apps.mascota.models import Mascota
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.

def listado(request):
    lista = serializers.serialize('json', Mascota.objects.all(), fields = ['nombre'])
    return HttpResponse(lista, content_type = 'application/json')

def index_mascota(request):
    return render(request, 'mascota/index.html')

def mascota_view(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('index')
    else:
        form = MascotaForm()
    
    return render(request, 'mascota/mascota-form.html', {'form': form})

def mascota_list(request):
    mascota = Mascota.objects.all().order_by('id')
    context = {'mascotas': mascota}
    return render(request, 'mascota/mascota-list.html', context)

def mascota_edit(request, id_mascota):
    mascota = Mascota.objects.get(id=id_mascota)
    if request.method== 'GET':
        form = MascotaForm(instance = mascota)
    else:
        form = MascotaForm(request.POST, instance = mascota)
        if form.is_valid():
            form.save()
        return redirect('mascota_listar')
    return render(request, 'mascota/mascota-form.html', {'form': form})

def mascota_delete(request, id_mascota):
    mascota = Mascota.objects.get(id=id_mascota)
    if request.method == 'POST':
        mascota.delete()
        return redirect('mascota_listar')
    return render(request, 'mascota/mascota-delete.html', {'mascota': mascota})

class MascotaList(ListView):
    model = Mascota
    template_name= 'mascota/mascota-list.html'
    paginate_by = 2

class MascotaCreate(CreateView):
    model = Mascota
    form_class = MascotaForm
    template_name = 'mascota/mascota-form.html'
    success_url = reverse_lazy('mascota_listar')

class MascotaUpdate(UpdateView):
    model = Mascota
    form_class = MascotaForm
    template_name = 'mascota/mascota-form.html'
    success_url = reverse_lazy('mascota_listar')

class MascotaDelete(DeleteView):
    model = Mascota
    template_name = 'mascota/mascota-delete.html'
    success_url = reverse_lazy('mascota_listar')
