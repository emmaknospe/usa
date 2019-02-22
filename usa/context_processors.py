
import profiles.constants
import django.conf


def constants(request):
    return {'STUDENT': profiles.constants.STUDENT,
            'DONOR': profiles.constants.DONOR,
            'ADMIN': profiles.constants.ADMIN,
            'VERSION': django.conf.settings.VERSION}
