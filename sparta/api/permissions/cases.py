from rest_framework.permissions import IsAuthenticated


class ReviewPermission(IsAuthenticated):
    """
    Only reviewers or staff can read reviews.
    Reviewers can only list their own reviews.
    Students cannot see the reviews for their assignments.
    """

    def has_permission(self, request, view):
        return request.user.is_staff()

    def has_object_permission(self, request, view, obj):
        return (
            obj.reviewer == request.user
            or obj.student.mentors.filter(user=request.user).exists()
            or request.user.is_staff()
        )
