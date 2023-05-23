from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML, Field, Div, Button
from crispy_forms.bootstrap import PrependedText, InlineRadios
from .models import User, ScreeningQuestionnaire
from address.forms import AddressField


   
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
    address = AddressField()
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
                    <a href="" class="btn btn-primary" style="margin-bottom: 10px">
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