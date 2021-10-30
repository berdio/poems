from django import forms

from poem.models.poem import Poem


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


class PoemForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = '__all__'
