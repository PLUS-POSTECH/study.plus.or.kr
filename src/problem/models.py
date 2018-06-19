import os

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model

from website.models import Category, Session


User = get_user_model()


# TODO: Use problem_attachments or attachments/problem
ProblemAttachmentStorage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'problem'))


class ProblemAttachment(models.Model):
    # TODO: Use upload_to to generate storage folder (to remove name collision)
    file = models.FileField(storage=ProblemAttachmentStorage)

    class Meta:
        verbose_name = '문제 첨부파일'
        verbose_name_plural = '문제 첨부파일들'

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return '%s' % self.filename()


class Problem(models.Model):
    # TODO: Title may not be unique
    title = models.CharField(max_length=50, unique=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    auth_key = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)
    attachments = models.ManyToManyField(ProblemAttachment, blank=True)

    class Meta:
        verbose_name = '문제'
        verbose_name_plural = '문제들'

    # TODO: Add spaces after comma
    def categories_title(self):
        return ','.join(map(lambda x: x.title, self.categories.all()))

    def __str__(self):
        return '%s' % self.title


# TODO: Add allow_question field
class ProblemList(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    session = models.ForeignKey(Session, on_delete=models.PROTECT)

    class Meta:
        verbose_name = '문제 리스트'
        verbose_name_plural = '문제 리스트들'

    def __str__(self):
        return '%s' % self.title


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
