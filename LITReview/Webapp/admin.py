from django.contrib import admin
from Webapp.models import *


class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "has_response", "image")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "ticket", "rating")

class UserFollowAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user")


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollow, UserFollowAdmin)
