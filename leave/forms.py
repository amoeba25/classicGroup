from django.forms import ModelForm
from .models import LeaveApp


# leave application form
class LeaveAppForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(LeaveAppForm, self).__init__(*args, **kwargs)
        self.fields['status'].required = False

    class Meta:
        model = LeaveApp
        fields = '__all__'