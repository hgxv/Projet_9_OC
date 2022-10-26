from django.contrib import admin
from Webapp.models import *


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "image")

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("ticket", "rating")

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)