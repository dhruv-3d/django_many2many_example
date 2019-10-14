from django import forms
from .models import *
from .widgets import BootstrapDateTimePickerInput


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'description']


class SessionSlotForm(forms.ModelForm):

    start_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput()
    )
    end_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput()
    )

    class Meta:
        model = SessionSlot
        fields = '__all__'