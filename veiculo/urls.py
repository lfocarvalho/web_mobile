from django.urls import path
from .views import ListarVeiculos, CriarVeiculo, EditarVeiculo, ExcluirVeiculo

app_name='veiculos'

urlpatterns = [
    path('', ListarVeiculos.as_view(), name='listar-veiculos'),
    path('novo/', CriarVeiculo.as_view(), name='criar-veiculo'),
    path('editar/<int:pk>/', EditarVeiculo.as_view(), name='editar-veiculo'),
    path('excluir/<int:pk>/', ExcluirVeiculo.as_view(), name='excluir-veiculo'),
]