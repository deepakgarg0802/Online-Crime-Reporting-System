from django import ModelForm
from .models import Comment


class CommenForm(ModelForm):
    class Meta:
        model = Comment
        fields = "comment"
