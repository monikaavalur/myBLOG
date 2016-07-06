from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CommentManager(models.Manager):
    def all(self):
        queryset=super(CommentManager,self).filter(parent=None)
        return queryset

    def filter_by_instance(self,instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        queryset=super(CommentManager,self).filter(content_type=content_type,object_id=obj_id).filter(parent=None)
        return queryset


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
    parent=models.ForeignKey("self",null=True,blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    objects=CommentManager()

    def __unicode__(self):
        return str(self.user.username)

    class Meta:
        ordering=['-timestamp']

    def children(self):
        return Comment.objects.filter(parent=self)

    def get_absolute_url(self):
        return reverse("comments:thread",kwargs={"id":self.id})

    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"id": self.id})
    @property
    def isParent(self):
        if self.parent is not None:
            return False
        else:
            return True