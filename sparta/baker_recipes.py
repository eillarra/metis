import maya

from model_bakery.recipe import Recipe, foreign_key, related

from sparta.models import Link, Place


now = maya.now()


# projects

project = Recipe("sparta.Project", start_at=now.subtract(days=20).datetime(), end_at=now.add(days=10).datetime())
project_closed = project.extend(end_at=now.subtract(days=10).datetime())
project_open_but_inactive = project.extend(is_active=False)


# disciplines

discipline1 = Recipe("sparta.Discipline")
discipline2 = Recipe("sparta.Discipline")

discipline_group1 = Recipe("sparta.TrainingDisciplineGroup")
discipline_group2 = Recipe("sparta.TrainingDisciplineGroup")

training_discipline1 = Recipe(
    "sparta.TrainingDiscipline", group=foreign_key(discipline_group1), discipline=foreign_key(discipline1)
)
training_discipline2 = Recipe(
    "sparta.TrainingDiscipline", group=foreign_key(discipline_group1), discipline=foreign_key(discipline2)
)


# institutions

hospital = Recipe("sparta.Place", type=Place.HOSPITAL, disciplines=[foreign_key(discipline1), foreign_key(discipline2)])
ward = Recipe("sparta.Place", type=Place.WARD, parent=foreign_key(hospital))
private_center = Recipe("sparta.Place", type=Place.PRIVATE)
uz = Recipe("sparta.Place", type=Place.HOSPITAL, name="UZ")


# users

user = Recipe("auth.User", is_staff=False)
staff = user.extend(is_staff=True)
