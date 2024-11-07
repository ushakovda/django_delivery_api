from django.contrib import admin

from registration.models import ParcelType, Parcel

admin.site.register(ParcelType)
admin.site.register(Parcel)