from metis import models


def check_file_access(file: "models.File", user: "models.User"):
    """
    Check if a user has access to a file.
    This is done in one place to have a better overview of the access control for private files.

    :param file: The file to check access for
    :param user: The user to check access for
    :return: True if the user has access to the file
    :raises: NotImplementedError if no access control is implemented for the file's content object
    """

    try:
        education = file.content_object.education  # type: ignore
        if education.can_be_managed_by(user):
            return True
    except AttributeError:
        pass

    if isinstance(file.content_object, models.Project):
        project: models.Project = file.content_object

        if file.code == "stagegids":
            return models.Contact.objects.filter(place__in=project.places.all(), user=user).exists()

    raise NotImplementedError("No access control implemented yet for this object type.")
