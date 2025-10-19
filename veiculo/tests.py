# Create your tests here.
# sistema/veiculo/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from veiculo.models import Veiculo
from django.contrib.auth.models import User

class TestesViewsVeiculo(TestCase):

    def setUp(self):
        # Configuração inicial para os testes
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='123')
        self.client.login(username='testuser', password='123')

        # URLs
        self.url_listar = reverse('veiculos:listar-veiculos')
        self.url_criar = reverse('veiculos:criar-veiculo')

        # Criar um veículo para testes de edição e exclusão
        self.veiculo = Veiculo.objects.create(marca=1, modelo='Carro Teste', ano=2022, cor=2, combustivel=3)
        self.url_editar = reverse('veiculos:editar-veiculo', kwargs={'pk': self.veiculo.pk})
        self.url_excluir = reverse('veiculos:excluir-veiculo', kwargs={'pk': self.veiculo.pk})

    def test_listar_veiculos_get(self):
        # Testa se a página de listagem carrega corretamente
        response = self.client.get(self.url_listar)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'veiculo/listar.html')

    def test_criar_veiculo_post(self):
        # Testa a criação de um novo veículo
        dados = {
            'marca': '2', 'modelo': 'Novo Carro', 'ano': '2023',
            'cor': '3', 'combustivel': '1'
        }
        response = self.client.post(self.url_criar, data=dados)
        # Verifica se redireciona para a listagem após criar
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url_listar)
        # Verifica se o veículo foi realmente criado no banco
        self.assertTrue(Veiculo.objects.filter(modelo='Novo Carro').exists())

    def test_editar_veiculo_post(self):
        # Testa a edição de um veículo existente
        dados_editados = {
            'marca': self.veiculo.marca, 'modelo': 'Carro Teste Editado', 'ano': self.veiculo.ano,
            'cor': self.veiculo.cor, 'combustivel': self.veiculo.combustivel
        }
        response = self.client.post(self.url_editar, data=dados_editados)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url_listar)
        # Atualiza o objeto do banco de dados e verifica a alteração
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.modelo, 'Carro Teste Editado')

    def test_excluir_veiculo_post(self):
        # Testa a exclusão de um veículo
        response = self.client.post(self.url_excluir)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url_listar)
        # Verifica se o veículo foi removido do banco
        self.assertFalse(Veiculo.objects.filter(pk=self.veiculo.pk).exists())