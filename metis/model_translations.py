# http://django-modeltranslation.readthedocs.io/en/latest/installation.html#setup
# flake8: noqa

from modeltranslation.translator import translator

from .models.rel.texts import TextEntry, TextEntryTranslationOptions

from .models.disciplines import Discipline, DisciplineTranslationOptions
from .models.educations import Faculty, FacultyTranslationOptions, Education, EducationTranslationOptions
from .models.places import PlaceType, PlaceTypeTranslationOptions
from .models.stages.programs import Program, ProgramTranslationOptions


translator.register(Discipline, DisciplineTranslationOptions)
translator.register(Education, EducationTranslationOptions)
translator.register(Faculty, FacultyTranslationOptions)
translator.register(PlaceType, PlaceTypeTranslationOptions)
translator.register(Program, ProgramTranslationOptions)
translator.register(TextEntry, TextEntryTranslationOptions)
