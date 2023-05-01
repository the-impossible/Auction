from django import forms
from Auction_auth.models import *


class AccountCreationForm(forms.ModelForm):

    email = forms.CharField(help_text='Enter email', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'email',
        }
    ))

    password = forms.CharField(help_text='Enter Password', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'password',
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


class BiddersCreationForm(AccountCreationForm, forms.ModelForm):

    address = forms.CharField(help_text='Enter Full name', required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Full name',
            'class': 'form-control form-control-lg input-lg',
        }
    ))

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'phone', 'address', 'picture')


class BiddersUpdateForm(forms.ModelForm):

    email = forms.CharField(help_text='Enter email', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'email',
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

    address = forms.CharField(help_text='Enter address', required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter address',
            'class': 'form-control form-control-lg input-lg',
        }
    ))

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'name', 'phone', 'address', 'picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        check = User.objects.filter(email=email)
        if self.instance:
            check = check.exclude(pk=self.instance.pk)
        if check.exists():
            raise forms.ValidationError('Email Already taken!')

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        check = User.objects.filter(phone=phone)
        if self.instance:
            check = check.exclude(pk=self.instance.pk)
        if check.exists():
            raise forms.ValidationError('phone Already taken!')

        return phone


class FurnitureForm(forms.ModelForm):

    furniture_name = forms.CharField(help_text='Enter furniture_name', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'text',
        }
    ))

    start_price = forms.CharField(help_text='Enter start_price', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'number',
        }
    ))

    furniture_desc = forms.CharField(help_text='Enter Furniture Description', widget=forms.Textarea(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'rows': 3,
        }
    ))

    start_date_and_time = forms.CharField(help_text='Enter Start Date and Time', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'datetime-local',
        }
    ))

    end_date_and_time = forms.CharField(help_text='Enter End Date and Time', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'datetime-local',
        }
    ))

    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = Furniture
        fields = ('furniture_name', 'start_price', 'furniture_desc',
                  'image', 'start_date_and_time', 'end_date_and_time')


class EditFurnitureForm(FurnitureForm, forms.ModelForm):

    image = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    is_sold = forms.BooleanField(required=False, help_text='Is the furniture sold?', widget=forms.CheckboxInput(
        attrs={
            'class': 'form-control',
            'type': 'checkbox',
        }
    ))

    class Meta:
        model = Furniture
        fields = ('furniture_name', 'start_price', 'furniture_desc',
                  'image', 'start_date_and_time', 'end_date_and_time', 'is_sold')


class AdminCreationForm(AccountCreationForm, forms.ModelForm):

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'phone', 'picture')


class UpdateAdminForm(forms.ModelForm):

    email = forms.CharField(help_text='Enter email', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'email',
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

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'name', 'phone', 'picture')


class BiddingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.furniture_id = kwargs.pop('furniture_id', 'fail')
        super(BiddingForm, self).__init__(*args, **kwargs)
        # self.fields['stud_id'].queryset=StudentProfile.objects.filter(dept_id=self.dept_id)

    bid_price = forms.CharField(help_text='Enter bid_price', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'number',
        }
    ))

    class Meta:
        model = Bidding
        fields = ('bid_price',)

    def clean_bid_price(self, *args, **kwargs):
        bid_price = self.cleaned_data.get('bid_price')
        start_price = Furniture.objects.get(
            furniture_id=self.furniture_id).start_price

        if float(bid_price) < start_price:

            raise forms.ValidationError("You can't bid below the start price")

        return bid_price
