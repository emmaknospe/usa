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
                if self.profile.profile_type == Profile.STUDENT:
                    return "STUDENT"
                elif self.profile.profile_type == Profile.DONOR:
                    return "DONOR"
                elif self.profile.profile_type == Profile.ADMIN:
                    return "ADMIN"
                else:
                    print("Error: Invalid profile")
            else:
                return "NO_PROFILE"
        else:
            return "ANONYMOUS"
