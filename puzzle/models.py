from django.db import models
from django.utils import timezone

class Question(models.Model):
    # the test fields are all in json. use json.load to get the original string
    name=models.CharField(max_length=256,null=False)
    description=models.CharField(max_length=8192,default='""',blank=True)
    pre_solution=models.CharField(max_length=8192,default='""',blank=True)
    test_code=models.CharField(max_length=8192,default='""',blank=True)
    test_cases=models.CharField(max_length=65536,default='""',blank=True)
    solution=models.CharField(max_length=8192,default='""',blank=True)
    solution_code=models.CharField(max_length=8192,default='""',blank=True)
    have_solution=models.BooleanField(default=False)
    creator=models.ForeignKey("auth.User",on_delete=models.SET_NULL,null=True)
    SUBMITTED="1"
    ACCEPTED="2"
    DRAFT="0"
    audit_choices=(
        (SUBMITTED,"Submitted"),
        (ACCEPTED,"Accepted" ),
        (DRAFT,"Draft")
        )
    audited=models.CharField(max_length=1,default='3',choices=audit_choices)
    def __str__(self):
        return self.name
class Submission(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    creator=models.ForeignKey("auth.User",on_delete=models.SET_NULL,null=True)
    code=models.CharField(max_length=8192)
    create_time=models.DateTimeField(default=timezone.now)
    result=models.CharField(max_length=256,default='""')
    # result : [Succeed. xx/yy passed.] or [Exceed time limit. xx/yy passed.] or [Error. ]
    score=models.FloatField(default=0)
    log=models.CharField(max_length=655360,null=True)
    private=models.BooleanField(default=True)
    def __str__(self):
        return str(self.creator)
class Discussion(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    creator=models.ForeignKey("auth.User",on_delete=models.SET_NULL,null=True)
    title=models.CharField(max_length=256)
    content=models.CharField(max_length=8192)
    create_time=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
class Comment(models.Model):
    discussion=models.ForeignKey(Discussion,on_delete=models.CASCADE)
    creator=models.ForeignKey("auth.User",on_delete=models.SET_NULL,null=True)
    content=models.CharField(max_length=4096)
    create_time=models.DateTimeField(default=timezone.now)
