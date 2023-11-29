from rest_framework import serializers

from metis.models.rel.files import File


class FileSerializer(serializers.ModelSerializer):
    url = serializers.URLField()

    class Meta:
        model = File
        exclude = (
            "content_type",
            "object_id",
            "file",
        )
