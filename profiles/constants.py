from profiles.models import Profile

HS_GRADUATION_LABEL_TEXT_BY_STUDENT_TYPE_DICT = {
    "H": "Projected High School Graduation Date:",
    "C": "High School Graduation Date:",
    "G": "High School Graduation Date:"
}


def HS_GRADUATION_LABEL_TEXT_BY_STUDENT_TYPE(student_type):
    return HS_GRADUATION_LABEL_TEXT_BY_STUDENT_TYPE_DICT[student_type]


COLLEGE_GRADUATION_LABEL_TEXT_BY_STUDENT_TYPE_DICT = {
    "H": "College Graduation Date (best guess):",
    "C": "Intended College Graduation Date",
    "G": "College Graduation Date:"
}


def COLLEGE_GRADUATION_LABEL_TEXT_BY_STUDENT_TYPE(student_type):
    return COLLEGE_GRADUATION_LABEL_TEXT_BY_STUDENT_TYPE_DICT[student_type]


STUDENT = Profile.STUDENT
ADMIN = Profile.ADMIN
DONOR = Profile.DONOR
