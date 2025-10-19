# sistema/anuncio/forms.py

from django.forms import ModelForm
from .models import Anuncio

class FormularioAnuncio(ModelForm):
    """
    Formulário para o model Anuncio
    """

    class Meta:
        model = Anuncio
        # O 'exclude' define campos que não devem aparecer no formulário.
        # Vamos excluir 'usuario' e 'status', pois serão definidos automaticamente na view.
        exclude = ['usuario', 'status']