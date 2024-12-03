from django.contrib import admin

from immarot.models import Contractor, Customer, Lead, LeadSource, LeadStatus, Project, ProjectLocation, Sell, Seller, Vendor

# Register your models here.
admin.site.register(ProjectLocation)
admin.site.register(Project)
admin.site.register(LeadStatus)
admin.site.register(LeadSource)
admin.site.register(Lead)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Sell)
admin.site.register(Vendor)
admin.site.register(Contractor)