# http://django-modeltranslation.readthedocs.io/en/latest/installation.html#setup
# flake8: noqa

from modeltranslation.translator import translator

from .models.disciplines import Discipline, DisciplineTranslationOptions
from .models.faculties import Faculty, FacultyTranslationOptions, Education, EducationTranslationOptions
from .models.institutions import Region, RegionTranslationOptions
from .models.stages.programs import Program, ProgramTranslationOptions


translator.register(Discipline, DisciplineTranslationOptions)
translator.register(Education, EducationTranslationOptions)
translator.register(Faculty, FacultyTranslationOptions)
translator.register(Program, ProgramTranslationOptions)
translator.register(Region, RegionTranslationOptions)
