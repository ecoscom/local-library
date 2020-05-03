import datetime
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from app04.models import BookInstance

class RenewBookModelForm(ModelForm):
    
    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        # Checa se a data não é passada
        if data < datetime.date.today():
            raise ValidationError(_('Data inválida - data no passado'))

        #Checa se a data não é maior que 4 semanas
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Data inválida - maior que 4 semanas'))
        return data
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Data de renovação')}
        help_texts = {'due_back': _('Insira uma data entre hoje e quatro semanas (padrão é 3 semanas),')}