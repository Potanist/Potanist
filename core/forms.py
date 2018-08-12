from django.forms import ModelForm, Textarea

from .models import Measurement


class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement
        exclude = ('plant', )
        widgets = {
            'notes': Textarea(
                attrs={'placeholder': 'Did you make any adjustments, e.g, add nutrients?'}),
        }

    required_css_class = 'field-required'

    def __init__(self, *args, **kwargs):
        if 'plants' in kwargs:
            self.plants = kwargs.pop('plants')
            plantlist = "".join(["<li>%s</li>" % p.name for p in self.plants])
            self.info_msg = "This measurement is for the following plants: <ul>%s</ul>" % plantlist
        super(MeasurementForm, self).__init__(*args, **kwargs)

    def header(self):
        if self.instance.pk:
            return "Update Measurement"
        else:
            return "Create New Measurement"