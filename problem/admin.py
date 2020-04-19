from django.contrib import admin
from .models import Problem, ProblemResult, ProblemInOut
# Register your models here.


class InputOutput(admin.TabularInline):
    model = ProblemInOut
    extra = 1


class ProblemAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['title', 'desc',
                           'full_score', 'testcases_amount'],
                }),
    ]

    inlines = [InputOutput]


admin.site.register(Problem, ProblemAdmin)
admin.site.register(ProblemResult)
