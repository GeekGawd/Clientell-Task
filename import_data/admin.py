from django.contrib import admin
from .models import User, Account, Opportunity

# Register your models here.

class OpportunityAdmin(admin.ModelAdmin):
    model = Opportunity
    list_per_page = 10

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Opportunity, OpportunityAdmin)
