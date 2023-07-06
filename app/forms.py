from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML, Field, Div, Button
from crispy_forms.bootstrap import PrependedText, InlineRadios
from .models import User, ScreeningQuestionnaire


   
class ScreeningQuestionnaireForm(forms.ModelForm):
    accept_privacy_policy = forms.BooleanField(required=True)
    accept_privacy_policy.label = mark_safe(
        "I agree to the <a href='' target='_blank'>Privacy Policy</a> and consent to the use of the information I provide to determine eligibility for the Food Pharmacy Program and to provide me access to the Food Pharmacy App."
    )
    
    for question in ScreeningQuestionnaire.QUESTION_STRS:
        vars()[question] = forms.ChoiceField(
            choices=ScreeningQuestionnaire.QUESTION_STR_TO_OBJ_MAP[question].choices,
            widget=forms.RadioSelect,
            required=True,
            label=ScreeningQuestionnaire.QUESTION_STR_TO_OBJ_MAP[question].verbose_name,
        )
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
                  
        self.helper = FormHelper()    
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                ScreeningQuestionnaire.c1_label,
                InlineRadios('c1_q1'),
                InlineRadios('c1_q2'),
            ),
            Fieldset(
                ScreeningQuestionnaire.c2_label,
                InlineRadios('c2_q1'),
                InlineRadios('c2_q2'),
                InlineRadios('c2_q3'),
                InlineRadios('c2_q4'),
                InlineRadios('c2_q5'),
            ),
            Fieldset(
                ScreeningQuestionnaire.c3_label,
                InlineRadios('c3_q1'),
                InlineRadios('c3_q2'),
                InlineRadios('c3_q3'),
            ),
            Field('accept_privacy_policy'),
            Submit('submit', 'Submit'),
        )
        
    class Meta:
        model = ScreeningQuestionnaire
        fields = ScreeningQuestionnaire.QUESTION_STRS


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    accept_privacy_policy = forms.BooleanField(required=True)
    accept_privacy_policy.label = mark_safe(
        "I agree to the <a href='' target='_blank'>Privacy Policy</a> and consent to the use of my information to provide me access to the Food Pharmacy App."
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()    
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Login Information',
                Row(
                    Column('email'),
                    Column('password'),
                ),
            ),
            Fieldset(
                'Personal Information',
                Row(
                    Column('first_name'),
                    Column('middle_name'),
                    Column('last_name'),
                ),
                'gender',
                'address',
            ),
            Fieldset(
                'Medical Information',
                HTML("This section is optional. Fill out this section if there is a doctor or dietician you regularly see.<br><br>"),
                Row(
                    Column('doctor'),
                    Column('dietician'),
                ),
            ),
            Field('accept_privacy_policy'),
            Submit('submit', 'Sign Up')
        )
    
    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            validate_password(password)
        except forms.ValidationError as error:
            self.add_error('password', error) 
        return make_password(password)
    
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'first_name',
            'middle_name',
            'last_name',
            'gender',
            'address',
            'doctor',
            'dietician',
        ]
    
    
class ProfileForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, required=False)
    first_name = forms.CharField(disabled=True, required=False)
    middle_name = forms.CharField(disabled=True, required=False)
    last_name = forms.CharField(disabled=True, required=False)
    patient_comments = forms.CharField(widget=forms.Textarea, required=False, label='Comments', help_text='Enter any comments you would like to share with Food Pharmacy staff.')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()    
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Login Information',
                Field('email'),
                HTML(
                    """
                    <a href="{% url 'change_password' %}" class="btn btn-primary" style="margin-bottom: 10px">
                        <i class="fas fa-key"></i>&nbsp;
                        Change Password
                    </a>
                    """
                )
            ),
            Fieldset(
                'Personal Information',
                Row(
                    Column('first_name'),
                    Column('middle_name'),
                    Column('last_name'),
                ),
                'gender',
                'address',
            ),
            Fieldset(
                'Medical Information',
                Row(
                    Column('doctor'),
                    Column('dietician'),
                ),
            ),
            Fieldset(
                'Other Information',
                'patient_comments',
            ),
            Submit('submit', 'Edit Profile')
        )
    
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'gender',
            'address',
            'doctor',
            'dietician',
            'patient_comments'
        ]

class PasswordResetForm(forms.ModelForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput, label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm New Password')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs['instance']
        self.helper = FormHelper()    
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('new_password1'),
                Column('new_password2'),
            ),
            Submit('submit', 'Reset Password')
        )
    
    def clean_new_password2(self):
        new_password1 = self.cleaned_data['new_password1']
        new_password2 = self.cleaned_data['new_password2']
        
        if new_password1 != new_password2:
            raise forms.ValidationError('New passwords do not match.')
                
        try:
            validate_password(new_password1)
        except forms.ValidationError as error:
            self.add_error('new_password1', error) 
        return make_password(new_password1)
    
    
    def save(self):
        self.user.set_password(self.cleaned_data['new_password1'])
        self.user.save()
    
    class Meta:
        model = User
        fields = [
            'new_password1',
            'new_password2',
        ]
class PasswordChangeForm(PasswordResetForm):
    old_password = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                'old_password',
            ),
            Row(
                Column('new_password1'),
                Column('new_password2'),
            ),
            Submit('submit', 'Change Password')
        )
    
    def clean_new_password2(self):
        new_password1 = self.cleaned_data['new_password1']
        new_password2 = self.cleaned_data['new_password2']
        
        if new_password1 != new_password2:
            raise forms.ValidationError('New passwords do not match.')
        
        if new_password1 == self.cleaned_data['old_password']:
            raise forms.ValidationError('New password cannot be the same as old password.')
        
        try:
            validate_password(new_password1)
        except forms.ValidationError as error:
            self.add_error('new_password1', error) 
        return make_password(new_password1)
    
    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Old password is incorrect.')
        return old_password
    
    def save(self):
        self.user.set_password(self.cleaned_data['new_password1'])
        self.user.save()
    
    class Meta:
        model = User
        fields = [
            'old_password',
            'new_password1',
            'new_password2',
        ]