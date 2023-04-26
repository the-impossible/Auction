from django import forms

from Auction_auth.models import User


class AccountCreationForm(forms.ModelForm):

    email = forms.CharField(help_text='Enter email',widget=forms.TextInput(
        attrs={
            'class':'form-control form-control-lg input-lg',
            'type':'email',
        }
    ))

    password = forms.CharField(help_text='Enter Password',widget=forms.TextInput(
        attrs={
            'class':'form-control form-control-lg input-lg',
            'type':'password',
        }
    ))

    name = forms.CharField(help_text='Enter Full name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Full name',
            'class': 'form-control form-control-lg input-lg',
        }
    ))

    phone = forms.CharField(help_text='Enter Phone number', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Phone number',
            'class': 'form-control form-control-lg input-lg',
        }
    ))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != None:
            if User.objects.filter(email=email.lower().strip()).exists():
                raise forms.ValidationError('Email Already taken!')

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 6:
            raise forms.ValidationError("Password is too short!")

        return password

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        exists = User.objects.filter(phone=phone).exists()

        if exists:
            raise forms.ValidationError("Phone number already exist!")

        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'phone')
