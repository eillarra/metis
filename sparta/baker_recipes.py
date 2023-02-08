import maya

from model_bakery.recipe import Recipe, foreign_key

from sparta.models import Place


now = maya.now()


# projects

education_1 = Recipe("sparta.Education")
education_2 = Recipe("sparta.Education")


# projects

project_1 = Recipe("sparta.Project", education=foreign_key(education_1))
project_1_inactive = project_1.extend(is_active=False)
project_2 = Recipe("sparta.Project", education=foreign_key(education_2))


# periods

period_1 = Recipe(
    "sparta.Period",
    project=foreign_key(project_1),
    start_date=now.subtract(days=20).date,
    end_date=now.add(days=10).date,
)
period_1_closed = period_1.extend(end_at=now.subtract(days=10).datetime())
period_1_open_but_inactive = period_1.extend(project=foreign_key(project_1_inactive))


# programmes

programme_1 = Recipe("sparta.Programme", education=foreign_key(education_1))
programme_block_0 = Recipe("sparta.ProgrammeBlock", programme=foreign_key(programme_1), position=0)
programme_block_1 = Recipe("sparta.ProgrammeBlock", programme=foreign_key(programme_1), position=1)


# disciplines

discipline1 = Recipe("sparta.Discipline")
discipline2 = Recipe("sparta.Discipline")


# institutions

hospital = Recipe("sparta.Place", type=Place.HOSPITAL, disciplines=[foreign_key(discipline1), foreign_key(discipline2)])
ward = Recipe("sparta.Place", type=Place.WARD, parent=foreign_key(hospital))
private_center = Recipe("sparta.Place", type=Place.PRIVATE)
uz = Recipe("sparta.Place", type=Place.HOSPITAL, name="UZ")


# users

user = Recipe("auth.User", is_staff=False)
staff = user.extend(is_staff=True)
