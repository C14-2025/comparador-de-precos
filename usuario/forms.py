from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuario

class CadastroForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ["nome", "email", "senha", "cep", "idade", 
                  "aniversario", "nacionalidade"]

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.senha_hash = make_password(self.cleaned_data["senha"])
        if commit:
            usuario.save()
        return usuario


class LoginForm(forms.Form):
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)
