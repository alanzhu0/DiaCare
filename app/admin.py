from django.contrib import admin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from .models import (
    User, Food, Produce, FoodChoice, ProduceChoice, ProduceCategory, Doctor, Dietician, Order, ScreeningQuestionnaire, 
    EmailVerificationLink, PasswordResetLink, AccountApprovalLink
)
admin.site.site_header = "Food Pharmacy App Administration"

def to_str(obj):
    return str(obj)

class UserAdmin(admin.ModelAdmin):
    def admin(obj):
        return obj.is_superuser or obj.is_staff
    admin.boolean = True
    
    def eligible(obj):
        return obj.eligible
    eligible.boolean = True
    
    def large_household(obj):
        return obj.large_household
    large_household.boolean = True
    
    to_str.short_description = 'Full Name (First Middle Last)'
    
    readonly_fields = ('user_created_at',)
    
    list_display = (
        to_str,
        'email',
        'gender',
        'doctor',
        'dietician',
        #'last_clinic_visit',
        #'last_food_received',
        'active',
        eligible,
        admin,
        large_household,
        'patient_comments',
        'medical_comments',
        'admin_comments',
    )
    
    list_filter = (
        'gender',
        'doctor',
        'dietician',
        #'last_clinic_visit',
        #'last_food_received',
        'active',
    )
    
    search_fields = (
        'first_name',
        'middle_name',
        'last_name',
        'email',
        'patient_comments',
        'medical_comments',
        'admin_comments',
    )
    
class DoctorDieticianAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
    )
    
    search_fields = (
        'name',
        'email',
        'phone',
    )

class FoodChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'quantity',
        'active',
    )
    
    list_filter = (
        'active',
    )
    
    search_fields = (
        'name',
        'quantity',
    )
    
    actions = (
        'mark_active',
        'mark_inactive',
    )
    
    @admin.action(description="Mark selected choices as active")
    def mark_active(self, request, queryset):
        queryset.update(active=True)
    
    @admin.action(description="Mark selected choices as inactive")
    def mark_inactive(self, request, queryset):
        queryset.update(active=False)
    
class ProduceChoiceAdmin(FoodChoiceAdmin):
    list_display = (
        'name',
        'quantity',
        'category',
        'active',
    )
    
    list_filter = (
        'active',
        'category',
    )
    
class ProduceCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'maximum_choices',
    )
    
    search_fields = (
        'name',
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('id',)
        return self.readonly_fields

class OrderAdmin(admin.ModelAdmin):
    def fulfilled(obj):
        return obj.fulfilled
    fulfilled.boolean = True
    
    def cancelled(obj):
        return obj.cancelled
    cancelled.boolean = True
    
    list_display = (
        'id',
        'user',
        'date_ordered',
        'date_scheduled',
        'date_fulfilled',
        fulfilled,
        cancelled,
        'type',
        'patient_comments',
        'admin_comments',
    )
    
    list_filter = (
        'type',
        'date_ordered',
        'date_scheduled',
        'date_fulfilled',
        'user',
    )
    
    search_fields = (
        'user',
        'patient_comments',
        'admin_comments',
    )
    
    actions = (
        'mark_fulfilled',
    )
    
    @admin.action(description="Mark selected orders as fulfilled")
    def mark_fulfilled(self, request, queryset):
        queryset.update(date_fulfilled=timezone.now())


class ScreeningQuestionnaireAdmin(admin.ModelAdmin):
    def eligible(obj):
        return obj.is_eligible
    eligible.boolean = True
    
    def large_household(obj):
        return obj.large_household
    large_household.boolean = True
    
    list_display = (
        'user',
        'date_completed',
        eligible,
        large_household,
        'c1_q1',
        'c1_q2',
        'c2_q1',
        'c2_q2',
        'c2_q3',
        'c2_q4',
        'c2_q5',
        'c3_q1',
        'c3_q2',
        'c3_q3',
    )
    
    search_fields = (
        'user',
    )
    
    actions = ('download_csv',)
    
    @admin.action(description="Download questionnaire responses as CSV (Excel spreadsheet)")
    def download_csv(self, request, queryset):
        return redirect(reverse('download_questionnaire'))


class SecureLinkAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'time_created',
        'valid'
    )

class EmailVerificationLinkAdmin(SecureLinkAdmin):
    list_display = (
        'user',
        'email',
        'time_created',
        'valid',
    )

admin.site.register(User, UserAdmin)

admin.site.register(Doctor, DoctorDieticianAdmin)
admin.site.register(Dietician, DoctorDieticianAdmin)

admin.site.register(FoodChoice, FoodChoiceAdmin)
admin.site.register(ProduceChoice, ProduceChoiceAdmin)

admin.site.register(ProduceCategory, ProduceCategoryAdmin)

admin.site.register(Order, OrderAdmin)

admin.site.register(ScreeningQuestionnaire, ScreeningQuestionnaireAdmin)

admin.site.register(EmailVerificationLink, EmailVerificationLinkAdmin)

admin.site.register(PasswordResetLink, SecureLinkAdmin)

admin.site.register(AccountApprovalLink, SecureLinkAdmin)

if settings.DEBUG:
    admin.site.register(Food)
    admin.site.register(Produce)

