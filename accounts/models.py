from django.db import models

from django.contrib.auth.models import AbstractUser
from profiles.models import DonorProfile, Profile


class User(AbstractUser):
    authorized_donor_profile = models.ForeignKey(DonorProfile,
                                                 on_delete=models.SET_NULL,
                                                 default=None,
                                                 blank=True,
                                                 null=True)

    def get_role(self):
        if self.is_authenticated:
            if hasattr(self, "profile"):
                return self.profile.profile_type
            else:
                return "NO_PROFILE"
        else:
            return "ANONYMOUS"

    def can_edit_scholarship(self, scholarship):
        return self.get_role() == Profile.DONOR and self.authorized_donor_profile_id == scholarship.organization_id
