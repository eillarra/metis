from django.core.exceptions import PermissionDenied
from django.views import View

from metis.models import Education, Period


class PeriodReportMixin(View):
    def get_education(self) -> Education:
        raise NotImplementedError("The mixin can only be used in a view that implements get_education()")

    def get_period(self) -> Period:
        if not hasattr(self, "period"):
            try:
                self.period = Period.objects.get(
                    id=self.kwargs.get("period_id"), project__education=self.get_education()
                )
            except Period.DoesNotExist as exc:
                raise PermissionDenied from exc

        return self.period

    def get_report(self):
        if not hasattr(self, "available_reports"):
            raise NotImplementedError("The mixin can only be used in a view that has `available_reports` defined")

        try:
            file_type = self.kwargs.get("file_type", "__KeyError__")
            report_code = self.kwargs.get("code", "__KeyError__")
            report = self.available_reports[file_type][report_code](self.get_period().id)  # type: ignore
        except KeyError as exc:
            raise PermissionDenied from exc

        return report

    def get(self, request, *args, **kwargs):
        return self.get_report().get_response()
