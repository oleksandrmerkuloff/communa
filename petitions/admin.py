from django.contrib import admin

from .models import Petition, PetitionVote


admin.site.register(Petition)
admin.site.register(PetitionVote)
