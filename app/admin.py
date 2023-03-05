from django.contrib import admin
from .models import *

admin.site.site_header = "DiaCare Administration"

admin.site.register(User)

admin.site.register(Doctor)
admin.site.register(Dietician)

admin.site.register(Food)
admin.site.register(FoodChoice)

admin.site.register(Produce)
admin.site.register(ProduceChoice)
admin.site.register(ProduceCategory)

admin.site.register(Order)
