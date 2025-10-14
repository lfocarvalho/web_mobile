from django.db import models
from veiculo.consts import OPCOES_MARCAS, OPCOES_COR, OPCOES_COMBUSTIVEL

# Create your models here.
class Veiculo(models.Model):
    marca = models.SmallIntegerField(choices=OPCOES_MARCAS)
    modelo = models.CharField(max_length=100)
    ano = models.SmallIntegerField()
    cor = models.SmallIntegerField(choices=OPCOES_COR)
    combustivel = models.SmallIntegerField(choices=OPCOES_COMBUSTIVEL)
    foto = models.ImageField( blank=True, null=True , upload_to='veiculo/fotos')

    def delete(self, *args, **kwargs):
        # Primeiro, apaga o arquivo de imagem físico do sistema de arquivos.
        # O 'save=False' impede que o modelo seja salvo novamente após a exclusão do arquivo.
        if self.foto:
            self.foto.delete(save=False)
        
        # Em seguida, chama o método 'delete' original da classe pai para
        # apagar o registro do banco de dados.
        super().delete(*args, **kwargs)