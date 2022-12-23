from sparta.models.places import Place
from sparta.models.stages.trainings import Training


class PlaceDataMerge:
    model = Place
    models_to_clean = [Training]

    def get_fields(self, row) -> dict:
        return {
            "id": row.TrainingPlaceID,
            "name": row.TrainingPlaceName,
        }

    def post_save(self) -> None:
        print("Adding parent information...")

        for row in self.get_legacy_data():
            if row.TrainingPlaceParentPlaceID:
                obj = Place.objects.get(id=row.TrainingPlaceID)
                obj.parent_id = row.TrainingPlaceParentPlaceID
                obj.save()
