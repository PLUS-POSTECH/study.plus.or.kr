import os

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model

from website.models import Category, Session


User = get_user_model()


ProblemAttachmentStorage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'attachments', 'problem'))


# TODO: Manual migration required
class Problem(models.Model):
    title = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    auth_key = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '문제'
        verbose_name_plural = '문제들'

    def categories_title(self):
        return ', '.join(map(lambda x: x.title, self.categories.all()))

    def __str__(self):
        return '%s' % self.title


class ProblemList(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    allow_question = models.BooleanField()
    session = models.ForeignKey(Session, on_delete=models.PROTECT)

    class Meta:
        verbose_name = '문제 리스트'
        verbose_name_plural = '문제 리스트들'

    def __str__(self):
        return '%s' % self.title


class ProblemAttachment(models.Model):
    def target_folder(self):
        return str(self.problem.id)

    file = models.FileField(storage=ProblemAttachmentStorage, upload_to=target_folder())
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)

    class Meta:
        verbose_name = '문제 첨부파일'
        verbose_name_plural = '문제 첨부파일들'

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return '%s' % self.filename()


class ProblemInstance(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    problem_list = models.ForeignKey(ProblemList, on_delete=models.PROTECT)
    points = models.IntegerField()
    distributed_points = models.IntegerField()
    breakthrough_points = models.IntegerField()
    hidden = models.BooleanField()

    class Meta:
        verbose_name = '문제 인스턴스'
        verbose_name_plural = '문제 인스턴스들'

    def __str__(self):
        return '%s' % self.problem.title


class ProblemAuthLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    problem_instance = models.ForeignKey(ProblemInstance, on_delete=models.PROTECT)
    auth_key = models.TextField()
    datetime = models.DateTimeField()

    class Meta:
        unique_together = (('user', 'problem_instance', 'auth_key'),)
        verbose_name = '문제 인증 로그'
        verbose_name_plural = '문제 인증 로그들'

# TODO: Add ProblemQuestion model
