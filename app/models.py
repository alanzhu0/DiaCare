from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager


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
        ("other", "Other"),
    ), max_length=255, blank=True)
    
    address = models.CharField(max_length=255, blank=True)
    
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, blank=True, null=True)
    dietician = models.ForeignKey('Dietician', on_delete=models.CASCADE, blank=True, null=True)
    
    last_clinic_visit = models.DateTimeField(blank=True, null=True)
    last_food_received = models.DateTimeField(blank=True, null=True)
    next_clinic_visit = models.DateTimeField(blank=True, null=True)
    next_food_batch = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.first_name + " " + self.last_name
    

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
        return self.name
    
    
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
    active = models.BooleanField(default=True)
    category = models.ForeignKey('ProduceCategory', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} ({self.quantity}) - Inactive" if not self.active else f"{self.name} ({self.quantity})"

    class Meta:
        ordering = ['name']
        
        
class ProduceCategory(models.Model):
    """Admin-defined produce categories"""
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    maximum_choices = models.IntegerField(
        default=1,
        help_text="Maximum number of produce choices allowed in this category"
    )
    
    @property
    def produces(self):
        return ProduceChoice.objects.filter(category=self)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


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
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.quantity}) - Inactive" if not self.active else f"{self.name} ({self.quantity})"
    
    class Meta:
        ordering = ['name']
    

class Order(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    date_scheduled = models.DateTimeField(blank=True, null=True)
    date_fulfilled = models.DateTimeField(blank=True, null=True)
    type = models.CharField(choices=(
        ("pickup", "Pickup"),
        ("delivery", "Delivery"),
    ), max_length=255, default="Pickup")
    
    @property
    def foods(self):
        return Food.objects.filter(order=self)

    @property
    def produces(self):
        return Produce.objects.filter(order=self)
    
    def __str__(self):
        return f"{self.user}: {self.date}"

    class Meta:
        ordering = ['-date']