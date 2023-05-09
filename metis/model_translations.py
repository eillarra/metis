# http://django-modeltranslation.readthedocs.io/en/latest/installation.html#setup
# flake8: noqa

from modeltranslation.translator import translator

from .models.rel.contents import Content, ContentTranslationOptions

from .models.disciplines import Discipline, DisciplineTranslationOptions
from .models.educations import Faculty, FacultyTranslationOptions, Education, EducationTranslationOptions
from .models.places import Region, RegionTranslationOptions
from .models.stages.programs import Program, ProgramTranslationOptions


translator.register(Content, ContentTranslationOptions)
translator.register(Discipline, DisciplineTranslationOptions)
translator.register(Education, EducationTranslationOptions)
translator.register(Faculty, FacultyTranslationOptions)
translator.register(Program, ProgramTranslationOptions)
translator.register(Region, RegionTranslationOptions)
