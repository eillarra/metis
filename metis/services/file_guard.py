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

    visible: list[bool] = []

    if isinstance(file.content_object, models.Project):
        project: models.Project = file.content_object

        if project.can_be_managed_by(user):
            return True

        if file.is_visible_for_target_group("place"):
            visible.append(models.Contact.objects.filter(place__in=project.places.all(), user=user).exists())

        if file.is_visible_for_target_group("student"):
            visible.append(models.Student.objects.filter(project=project, user=user).exists())

        return any(visible)

    if isinstance(file.content_object, models.Internship):
        internship: models.Internship = file.content_object

        if internship.can_be_managed_by(user):
            return True

        if file.is_visible_for_target_group("place"):
            visible.append(models.Contact.objects.filter(place=internship.place, user=user).exists())

        if file.is_visible_for_target_group("student"):
            visible.append(internship.student.user == user)  # type: ignore

        return any(visible)

    raise NotImplementedError("No access control implemented yet for this object type.")
