from django.contrib import admin
from django.conf import settings
from .models import User, Food, Produce, FoodChoice, ProduceChoice, ProduceCategory, Doctor, Dietician, Order

admin.site.site_header = "DiaCare Administration"

def to_str(obj):
    return str(obj)

class UserAdmin(admin.ModelAdmin):
    def admin(obj):
        return obj.is_superuser or obj.is_staff
    admin.boolean = True
    
    to_str.short_description = 'Full Name (First Middle Last)'
    list_display = (
        to_str,
        'email',
        'gender',
        'doctor',
        'dietician',
        'last_clinic_visit',
        'last_food_received',
        'is_active',
        admin,
        'user_comments',
        'medical_comments',
        'admin_comments',
    )
    
    list_filter = (
        'gender',
        'doctor',
        'dietician',
        'last_clinic_visit',
        'last_food_received',
        'is_active',
    )
    
    search_fields = (
        'first_name',
        'middle_name',
        'last_name',
        'email',
        'user_comments',
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
    
    list_display = (
        'user',
        'date_ordered',
        'date_scheduled',
        'date_fulfilled',
        fulfilled,
        'type',
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
    )
    
    actions = (
        'mark_fulfilled',
    )
    
    @admin.action(description="Mark selected orders as fulfilled")
    def mark_fulfilled(self, request, queryset):
        queryset.update(date_fulfilled=timezone.now())
    

admin.site.register(User, UserAdmin)

admin.site.register(Doctor, DoctorDieticianAdmin)
admin.site.register(Dietician, DoctorDieticianAdmin)

admin.site.register(FoodChoice, FoodChoiceAdmin)
admin.site.register(ProduceChoice, ProduceChoiceAdmin)

admin.site.register(ProduceCategory, ProduceCategoryAdmin)

admin.site.register(Order, OrderAdmin)

if settings.DEBUG:
    admin.site.register(Food)
    admin.site.register(Produce)

