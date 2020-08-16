from django.contrib import admin
from puzzle.models import Question,Submission
# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Question,QuestionAdmin)
admin.site.register(Submission)
