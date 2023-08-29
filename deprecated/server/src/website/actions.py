import csv

from django.http import HttpResponse


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}.csv"
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "선택된 항목 을/를 CSV 로 내보냅니다."


class ProblemInstanceVisibilityMixin:
    def hide_problem_instance(self, request, queryset):
        queryset.update(hidden=True)

    def show_problem_instance(self, request, queryset):
        queryset.update(hidden=False)

    hide_problem_instance.short_description = "선택된 항목 을/를 문제 리스트에서 숨깁니다."

    show_problem_instance.short_description = "선택된 항목 을/를 문제 리스트에서 보입니다."
