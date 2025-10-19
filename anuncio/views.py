# sistema/anuncio/views.py

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from anuncio.models import Anuncio
from veiculo.models import Veiculo
from django.contrib.auth.mixins import LoginRequiredMixin
from anuncio.forms import FormularioAnuncio
from django.urls import reverse_lazy

# A classe está aqui!
class ListarAnuncios(ListView):
    model = Anuncio
    context_object_name = 'lista_anuncio'
    template_name = 'anuncio/listar.html'

class DetalheAnuncio(DetailView):
    model = Anuncio
    template_name = 'anuncio/detalhe_anuncio.html'
    context_object_name = 'anuncio'

class CriarAnuncio(LoginRequiredMixin, CreateView):
    model = Anuncio
    form_class = FormularioAnuncio
    template_name = 'anuncio/novo.html'
    success_url = reverse_lazy('listar-anuncios')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        veiculos_com_anuncios = Anuncio.objects.filter(status='ativo').values_list('veiculo_id', flat=True)
        form.fields['veiculo'].queryset = Veiculo.objects.exclude(id__in=veiculos_com_anuncios)
        return form

class EditarAnuncio(LoginRequiredMixin, UpdateView):
    model = Anuncio
    form_class = FormularioAnuncio
    template_name = 'anuncio/editar_anuncio.html'
    success_url = reverse_lazy('listar-anuncios')

    def get_queryset(self):
        return Anuncio.objects.filter(usuario=self.request.user)

class DeletarAnuncio(LoginRequiredMixin, DeleteView):
    model = Anuncio
    template_name = 'anuncio/deletar.html'
    success_url = reverse_lazy('listar-anuncios')

    def get_queryset(self):
        return Anuncio.objects.filter(usuario=self.request.user)