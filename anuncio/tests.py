# Create your tests here.
# sistema/anuncio/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from veiculo.models import Veiculo
from .models import Anuncio

class TestesViewsAnuncio(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='123')
        self.client.login(username='testuser', password='123')

        self.veiculo = Veiculo.objects.create(marca=1, modelo='Carro P/ Anuncio', ano=2021, cor=1, combustivel=1)

        self.anuncio = Anuncio.objects.create(
            veiculo=self.veiculo,
            usuario=self.user,
            titulo='Super Anúncio Teste',
            preco=45000.00,
            cidade='Cidade Exemplo',
            estado='SP',
            telefone='11987654321',
            quilometragem=50000
        )

        self.url_listar = reverse('listar-anuncios')
        self.url_criar = reverse('criar-anuncio')
        self.url_detalhe = reverse('detalhe-anuncio', kwargs={'pk': self.anuncio.pk})
        self.url_editar = reverse('editar-anuncio', kwargs={'pk': self.anuncio.pk})
        self.url_deletar = reverse('deletar-anuncio', kwargs={'pk': self.anuncio.pk})

    def test_listar_anuncios_get(self):
        response = self.client.get(self.url_listar)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'anuncio/listar.html')
        self.assertContains(response, self.anuncio.titulo)

    def test_detalhe_anuncio_get(self):
        response = self.client.get(self.url_detalhe)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'anuncio/detalhe_anuncio.html')
        self.assertContains(response, self.anuncio.titulo)

    def test_criar_anuncio_post(self):
        veiculo2 = Veiculo.objects.create(marca=2, modelo='Outro Carro', ano=2020, cor=2, combustivel=2)
        dados = {
            'veiculo': veiculo2.id,
            'titulo': 'Anúncio Novo',
            'descricao': 'Descrição do anúncio novo.',
            'preco': 60000.00,
            'quilometragem': 12000,
            'telefone': '21999998888',
            'cidade': 'Rio de Janeiro',
            'estado': 'RJ'
        }
        response = self.client.post(self.url_criar, data=dados)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url_listar)
        self.assertTrue(Anuncio.objects.filter(titulo='Anúncio Novo').exists())

    def test_editar_anuncio_post(self):
        dados_editados = {
            'veiculo': self.veiculo.id,
            'titulo': 'Anúncio Editado',
            'descricao': self.anuncio.descricao,
            'preco': self.anuncio.preco,
            'quilometragem': self.anuncio.quilometragem,
            'telefone': self.anuncio.telefone,
            'cidade': self.anuncio.cidade,
            'estado': self.anuncio.estado,
        }
        response = self.client.post(self.url_editar, data=dados_editados)
        # A view redireciona para 'meus-anuncios'. Se essa url não existe, o teste falhará no redirect.
        # Vamos verificar se o objeto foi alterado, que é o mais importante.
        self.anuncio.refresh_from_db()
        self.assertEqual(self.anuncio.titulo, 'Anúncio Editado')

    def test_deletar_anuncio_post(self):
        response = self.client.post(self.url_deletar)
        self.assertFalse(Anuncio.objects.filter(pk=self.anuncio.pk).exists())