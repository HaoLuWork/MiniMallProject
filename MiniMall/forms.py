class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput())
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")
        return cleaned_data 

class RegistrationForm(forms.Form):
    
    username   = forms.CharField(max_length = 20,
                                label = 'Name')
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm',  
                                 widget = forms.PasswordInput())
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput())
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data
    
    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise
        return cleaned_data