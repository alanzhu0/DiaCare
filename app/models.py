from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.utils import timezone



# Create your models here.
class feed(models.Model):
    id = models.IntegerField(primary_key=True)
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    body = models.TextField()


class UserManager(DjangoUserManager):
    pass


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(choices=(
        ("male", "Male"),
        ("female", "Female"),
        ("nonbinary", "Non-binary"),
    ), max_length=255, blank=True)
    
    is_active = models.BooleanField(
        default=True, 
        help_text="Whether the user is currently enrolled in the program and is authorized to log in and order food.", 
        verbose_name="Active"
    )

    address = models.CharField(max_length=255, blank=True)

    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, blank=True, null=True)
    dietician = models.ForeignKey('Dietician', on_delete=models.CASCADE, blank=True, null=True)

    last_clinic_visit = models.DateTimeField(blank=True, null=True)
    last_food_received = models.DateTimeField(blank=True, null=True)
    next_clinic_visit = models.DateTimeField(blank=True, null=True)
    next_food_batch = models.DateTimeField(blank=True, null=True)
    
    patient_comments = models.TextField(blank=True, help_text="Comments from the patient")
    medical_comments = models.TextField(blank=True, help_text="Comments from the doctor, dietician, or clinic regarding the patient's medical conditions. Not visible to patient.")
    admin_comments = models.TextField(blank=True, help_text="Comments from DiaCare administrators. Not visible to patient.")

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.first_name} {self.middle_name + ' ' if self.middle_name else ''}{self.last_name}"


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Dr. {self.name}"


class Dietician(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.name)


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
