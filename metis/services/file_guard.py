from metis import models


def check_file_access(file: "models.File", user: "models.User") -> bool:
    """Check if a user has access to a file.

    This is done in one place to have a better overview of the access control for private files.

    Args:
        file: The File to check access for.
        user: The User to check access for.

    Returns:
        A bool indicating whether or not the user has access to the file.

    Raises:
        NotImplementedError: No access control is implemented for the file's content object.
    """
    try:
        education = file.content_object.education  # type: ignore
        if education.can_be_managed_by(user):
            return True
    except AttributeError:
        pass

    if isinstance(file.content_object, models.Project):
        project: models.Project = file.content_object

        if file.code and file.code.startswith("place:"):
            return models.Contact.objects.filter(place__in=project.places.all(), user=user).exists()

        if file.code and file.code.startswith("student:"):
            return models.Student.objects.filter(project=project, user=user).exists()

        return project.can_be_managed_by(user)

    raise NotImplementedError("No access control implemented yet for this object type.")
