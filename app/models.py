from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.utils import timezone

from address.models import AddressField


# Create your models here.
class UserManager(DjangoUserManager):
    pass


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    user_created_at = models.DateTimeField(default=timezone.now)
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(choices=(
        ("male", "Male"),
        ("female", "Female"),
        ("nonbinary", "Non-binary"),
    ), max_length=255)
    
    
    active = models.BooleanField(
        default=False, 
        help_text="Whether the user is currently enrolled in the Food Pharmacy program and is authorized to log in and order food.", 
    )
    
    address = AddressField(null=True)

    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    dietician = models.ForeignKey('Dietician', on_delete=models.CASCADE)

    last_clinic_visit = models.DateTimeField(blank=True, null=True)
    last_food_received = models.DateTimeField(blank=True, null=True)
    next_clinic_visit = models.DateTimeField(blank=True, null=True)
    next_food_batch = models.DateTimeField(blank=True, null=True)
    
    patient_comments = models.TextField(blank=True, help_text="Comments from the patient")
    medical_comments = models.TextField(blank=True, help_text="Comments from the doctor, dietician, or clinic regarding the patient's medical conditions. Not visible to patient.")
    admin_comments = models.TextField(blank=True, help_text="Comments from DiaCare administrators. Not visible to patient.")


    @property
    def completed_screening_questionnaire(self):
        return hasattr(self, 'screening_questionnaire')
    
    """
        active determines if the user is able to use the app.
        eligible determines if the user is eligible for the Food Pharmacy program.
        
        An eligible user becomes active after they are approved by Food Pharmacy staff, their doctor or dietician, or an administrator.
        
        active = True, eligible = True:   The user is active and eligible for the Food Pharmacy program.
        active = True, eligible = False:  Should not happen unless access was override-granted by an administrator.
        active = False, eligible = True:  The user is eligible for the Food Pharmacy program but has not been approved yet.
        active = False, eligible = False: The user is not eligible for the Food Pharmacy program.
    """
    
    @property
    def eligible(self):
        """Returns whether the user is eligible for the Food Pharmacy program."""
        return self.screening_questionnaire.is_eligible if hasattr(self, 'screening_questionnaire') else False

    def __str__(self):
        return f"{self.first_name} {self.middle_name + ' ' if self.middle_name else ''}{self.last_name}"


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Dr. {self.name}" if self.name != "Other" else "Other"
    
    def save(self, *args, **kwargs):
        if self.name == "Other":
            self.id = 999999999
        super().save(*args, **kwargs)


class Dietician(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.name == "Other":
            self.id = 999999999
        super().save(*args, **kwargs)


class Produce(models.Model):
    """Selected by users"""
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    produce = models.ForeignKey('ProduceChoice', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order}: {self.produce}"

    class Meta:
        ordering = ['produce']


class ProduceChoice(models.Model):
    """Admin-defined produce choices"""
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255, default="1")
    active = models.BooleanField(default=True,  help_text="Whether this produce choice is currently available for selection")
    category = models.ForeignKey('ProduceCategory', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.quantity})"

    class Meta:
        ordering = ['name']


class ProduceCategory(models.Model):
    """Admin-defined produce categories"""
    id = models.CharField(max_length=255, primary_key=True, help_text="Unique identifier for this category")
    name = models.CharField(max_length=255)
    maximum_choices = models.IntegerField(
        default=1,
        help_text="Maximum number of produce choices allowed in this category"
    )
    display_order = models.IntegerField(default=0, help_text="Order in which this category should be displayed to users")

    @property
    def produces(self):
        return ProduceChoice.objects.filter(category=self)
    
    @property
    def active_produces(self):
        return self.produces.filter(active=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = "produce categories"


class Food(models.Model):
    """Required for all users"""
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    food = models.ForeignKey('FoodChoice', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order}: {self.food}"

    class Meta:
        ordering = ['food']


class FoodChoice(models.Model):
    """Admin-defined food choices"""
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255, default="1")
    active = models.BooleanField(default=True, help_text="Whether this food choice is currently available for selection")

    def __str__(self):
        return f"{self.name} ({self.quantity})"

    class Meta:
        ordering = ['name']


class Order(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_scheduled = models.DateTimeField(blank=True, null=True)
    date_fulfilled = models.DateTimeField(blank=True, null=True)
    date_cancelled = models.DateTimeField(blank=True, null=True)
    type = models.CharField(choices=(
        ("pickup", "Pickup"),
        ("delivery", "Delivery"),
    ), max_length=255, default="Pickup")
    patient_comments = models.TextField(blank=True, help_text="Comments from the patient regarding this order")
    admin_comments = models.TextField(blank=True, help_text="Comments from food pharmacy staff regarding this order. Not visible to patient.")
    number = models.IntegerField(default=0, help_text="Order number, incremented individually for each user")
    
    @property
    def fulfilled(self):
        return self.date_fulfilled is not None and self.date_fulfilled < timezone.now()
    
    @property
    def cancelled(self):
        return self.date_cancelled is not None

    @property
    def foods(self):
        return Food.objects.filter(order=self)

    @property
    def produces(self):
        return Produce.objects.filter(order=self)

    def __str__(self):
        return f"Order by {self.user} on {self.date_ordered.strftime('%a, %b %d %Y at %I:%M:%S %p')}"

    class Meta:
        ordering = ['-date_scheduled']


class ScreeningQuestionnaire(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name="screening_questionnaire")
    date_completed = models.DateTimeField(default=timezone.now)
    
    ### Questionnaire fields ###
    
    ## Category 1
    c1_choices = (
        ("yes", "Yes"),
        ("no", "No"),
        ("unsure", "Unsure"),
    )
    c1_label = "General Information"
    
    c1_q1 = models.CharField(choices=c1_choices, max_length=255, verbose_name="Have you received groceries from us before?")    
    c1_q2 = models.CharField(choices=c1_choices, max_length=255, verbose_name="Does your family participate in WIC or SNAP (EBT)?")   
    
    ## Category 2
    c2_choices = (
        ("often", "Often"),
        ("sometimes", "Sometimes"),
        ("never", "Never"),
        ("dont_know_or_decline_to_answer", "Don't know or decline to answer"),
    )
    c2_label = "Please indicate how often you have experienced the following in the past 12 months:"

    c2_q1 = models.CharField(choices=c2_choices, max_length=255, verbose_name="We worried our food would run out before we got money to buy more.")
    c2_q2 = models.CharField(choices=c2_choices, max_length=255, verbose_name="The food we ordered didn't last and we didn't have money to buy more.")
    c2_q3 = models.CharField(choices=c2_choices, max_length=255, verbose_name="We couldn't afford to eat balanced meals (protein with starch, fruits/vegetables at each meal for the entire family).")
    c2_q4 = models.CharField(choices=c2_choices, max_length=255, verbose_name="We (you or other adults in your household) have had to cut the size of our meals or skip meals because there wasn't enough money for food.")
    c2_q5 = models.CharField(choices=c2_choices, max_length=255, verbose_name="We often choose prepackaged food over fresh due to price.")
    ## Category 3
    c3_label = "Other Information"
    
    c3_q1 = models.CharField(choices=(
        ("car", "Car"),
        ("bus", "Bus"),
        ("metro", "Metro"),
        ("ride_share_service", "Ride share service"),
    ), max_length=255, verbose_name="How did you get here today?")
    
    c3_q2 = models.CharField(choices=(
        ("almonds", "Almond"),
        ("1_cows_milk", "1% Cow's Milk"),
    ), max_length=255, verbose_name="Which type of milk do you prefer?")
    
    c3_q3 = models.CharField(choices=(
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8_or_more", "8+"),
    ), max_length=255, verbose_name="How many people live in your house?")
    
    
    ## Questionnaire information
    QUESTION_STRS = [
        'c1_q1', 'c1_q2',
        'c2_q1', 'c2_q2', 'c2_q3', 'c2_q4', 'c2_q5',
        'c3_q1', 'c3_q2', 'c3_q3',
    ]
    
    QUESTION_OBJS = [
        c1_q1, c1_q2,
        c2_q1, c2_q2, c2_q3, c2_q4, c2_q5,
        c3_q1, c3_q2, c3_q3,
    ]
    
   


    QUESTION_STR_TO_OBJ_MAP = dict(zip(QUESTION_STRS, QUESTION_OBJS))
    
    QUESTIONS_DETERMINING_ELIGIBILITY = [
        'c2_q1', 'c2_q2', 'c2_q3', 'c2_q4', 'c2_q5',
    ]
    
    @property
    def is_eligible(self):
        """Returns whether the response to this questionnaire indicates that the user is eligible for the Food Pharmacy program"""
        return any([getattr(self, q) in ("often", "sometimes") for q in self.QUESTIONS_DETERMINING_ELIGIBILITY])
    
    class Meta:
        ordering = ['-date_completed']
