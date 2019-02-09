
import profiles.constants


def constants(request):
    return {'STUDENT': profiles.constants.STUDENT,
            'DONOR': profiles.constants.DONOR,
            'ADMIN': profiles.constants.ADMIN}
