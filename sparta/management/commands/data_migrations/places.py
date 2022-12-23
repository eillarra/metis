
from sparta.models.places import Place
from .base import DataMigration


class PlaceDataMigration(DataMigration):
    legacy_table = "TrainingPlace"
    model = Place

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

        """
        TODO: move this to merge part
        print("Adding websites...")

        for row in self.get_legacy_data():
            if row.TrainingPlaceWebsite:
                self.add_link(Place.objects.get(id=row.TrainingPlaceID), f"http://{row.TrainingPlaceWebsite}")
        """
