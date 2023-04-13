from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    """
    Base model admin class.
    All models that extend the BaseModel class should extend this class in the admin area to get user info populated.
    """

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user

        super().save_model(request, obj, form, change)
