from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    """
    Custom user registration form that includes phone and other profile details.
    Handles both User creation and UserProfile creation.
    """
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'flex w-full min-w-0 flex-1 bg-transparent text-background-dark dark:text-white focus:outline-0 focus:ring-0 border-none h-14 placeholder:text-background-dark/30 dark:placeholder:text-white/30 px-4 text-base font-medium',
            'placeholder': '7XX XXX XXX',
        }),
        label='Phone Number (without +254)'
    )
    
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'flex w-full min-w-0 flex-1 bg-transparent text-background-dark dark:text-white focus:outline-0 focus:ring-0 border-none h-14 placeholder:text-background-dark/30 dark:placeholder:text-white/30 px-5 text-base font-medium',
            'placeholder': 'First name',
        }),
        label='First Name'
    )
    
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'flex w-full min-w-0 flex-1 bg-transparent text-background-dark dark:text-white focus:outline-0 focus:ring-0 border-none h-14 placeholder:text-background-dark/30 dark:placeholder:text-white/30 px-5 text-base font-medium',
            'placeholder': 'Last name',
        }),
        label='Last Name'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'flex w-full min-w-0 flex-1 bg-transparent text-background-dark dark:text-white focus:outline-0 focus:ring-0 border-none h-14 placeholder:text-background-dark/30 dark:placeholder:text-white/30 px-5 text-base font-medium',
            'placeholder': 'e.g. jumabakari@example.com',
        }),
        label='Email Address'
    )
    
    preferred_payment_method = forms.ChoiceField(
        choices=[('cash', 'Cash'), ('mpesa', 'M-Pesa'), ('card', 'Card')],
        required=False,
        initial='cash',
        widget=forms.Select(attrs={
            'class': 'flex w-full min-w-0 flex-1 bg-transparent text-background-dark dark:text-white focus:outline-0 focus:ring-0 border-none h-14 placeholder:text-background-dark/30 dark:placeholder:text-white/30 px-5 text-base font-medium',
        }),
        label='Preferred Payment Method'
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'flex w-full min-w-0 flex-1 bg-transparent text-background-dark dark:text-white focus:outline-0 focus:ring-0 border-none h-14 placeholder:text-background-dark/30 dark:placeholder:text-white/30 px-5 text-base font-medium',
            'placeholder': 'Create a strong password',
        })
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'flex w-full min-w-0 flex-1 bg-transparent text-background-dark dark:text-white focus:outline-0 focus:ring-0 border-none h-14 placeholder:text-background-dark/30 dark:placeholder:text-white/30 px-5 text-base font-medium',
            'placeholder': 'Confirm your password',
        })
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2', 'preferred_payment_method')
    
    def clean_email(self):
        """Validate that email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email
    
    def clean_phone(self):
        """Validate that phone is unique and properly formatted"""
        phone = self.cleaned_data.get('phone')
        
        # Add +254 prefix
        if not phone.startswith('+254'):
            phone = '+254' + phone.lstrip('0')
        
        if UserProfile.objects.filter(phone=phone).exists():
            raise ValidationError("This phone number is already registered.")
        
        return phone
    
    def clean_password2(self):
        """Validate that passwords match"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        
        return password2
    
    def save(self, commit=True):
        """
        Save the user and create a linked UserProfile.
        """
        user = super().save(commit=False)
        
        # Set username as email
        user.username = self.cleaned_data['email']
        
        if commit:
            user.save()
            
            # Create UserProfile with phone and payment preference
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                preferred_payment_method=self.cleaned_data.get('preferred_payment_method', 'cash'),
                notification_enabled=True,
                smart_alerts_enabled=True,
            )
        
        return user


class UserLoginForm(forms.Form):
    """
    Custom login form using phone number and password.
    """
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'flex w-full min-w-0 flex-1 bg-transparent text-background-dark dark:text-white focus:outline-0 focus:ring-0 border-none h-14 placeholder:text-background-dark/30 dark:placeholder:text-white/30 px-4 text-base font-medium',
            'placeholder': '7XX XXX XXX',
        }),
        label='Phone Number'
    )
    
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'flex w-full min-w-0 flex-1 bg-transparent text-background-dark dark:text-white focus:outline-0 focus:ring-0 border-none h-14 placeholder:text-background-dark/30 dark:placeholder:text-white/30 px-5 text-base font-medium',
            'placeholder': 'Enter your password',
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 rounded border-primary text-primary',
        }),
        label='Remember me'
    )
    
    def clean(self):
        """Validate phone format"""
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        
        if phone and not phone.startswith('+254'):
            phone = '+254' + phone.lstrip('0')
            cleaned_data['phone'] = phone
        
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    first_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First name',
        }),
        label='First Name'
    )
    
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last name',
        }),
        label='Last Name'
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email address',
        }),
        label='Email Address'
    )
    
    class Meta:
        model = UserProfile
        fields = ('phone', 'date_of_birth', 'gender', 'bio', 'home_address', 
                  'work_address', 'preferred_payment_method', 
                  'notification_enabled', 'smart_alerts_enabled', 'alert_notification_minutes')
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Phone number',
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-input',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Tell us about yourself',
            }),
            'home_address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Home address',
            }),
            'work_address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Work address',
            }),
            'preferred_payment_method': forms.Select(attrs={
                'class': 'form-input',
            }),
            'notification_enabled': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
            'smart_alerts_enabled': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
            'alert_notification_minutes': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 1,
                'max': 60,
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate user fields if instance exists
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        """
        Save both UserProfile and User data.
        """
        profile = super().save(commit=False)
        
        # Update User fields
        if self.cleaned_data.get('first_name'):
            profile.user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data.get('last_name'):
            profile.user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data.get('email'):
            profile.user.email = self.cleaned_data['email']
        
        if commit:
            profile.user.save()
            profile.save()
        
        return profile
