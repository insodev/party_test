from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import Party, PartyRegistration, User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('timezone',)}),
    )


admin.site.register(User, MyUserAdmin)

admin.site.register(PartyRegistration)


class PartyRegistrationInline(admin.TabularInline):
    model = PartyRegistration


class PartyAdmin(admin.ModelAdmin):
    inlines = [
        PartyRegistrationInline,
    ]


admin.site.register(Party, PartyAdmin)
