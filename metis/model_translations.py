# http://django-modeltranslation.readthedocs.io/en/latest/installation.html#setup
# flake8: noqa

from modeltranslation.translator import translator

from .models.faculties import Faculty, FacultyTranslationOptions, Education, EducationTranslationOptions
from .models.stages.programs import Program, ProgramTranslationOptions


translator.register(Education, EducationTranslationOptions)
translator.register(Faculty, FacultyTranslationOptions)
translator.register(Program, ProgramTranslationOptions)
