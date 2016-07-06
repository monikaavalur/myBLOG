from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import  slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from django.contrib.contenttypes.models import ContentType

# Create your models here.
from comments.models import Comment
def upload_location(instance,filename):
    return "%s/%s" %(instance.id,filename)

class PostManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())

class post(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    title=models.CharField(max_length=120)
    slug=models.SlugField(unique=True)
    image=models.ImageField(upload_to=upload_location,
                            null=True,blank=True,
                            width_field="width_field",
                            height_field="height_field")
    height_field=models.IntegerField(default=0)
    width_field=models.IntegerField(default=0)
    draft=models.BooleanField(default=False)
    publish=models.DateField(auto_now=False,auto_now_add=False)
    content=models.TextField(max_length=1000)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)

    objects = PostManager()
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail",kwargs={"id":self.id})

    def get_edit_url(self):
        return reverse("posts:edit",kwargs={"id":self.id})

    def get_delete_url(self):
        return reverse("posts:delete", kwargs={"id": self.id})

    class Meta:
        ordering=["-timestamp","-updated"]

    def get_markdown(self):
        content=self.content
        markdown_text=markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance=self
        queryset=Comment.objects.filter_by_instance(instance)
        return queryset

    @property
    def get_content_type(self):
        instance = self
        content_type=ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance,new_slug=None):
    slug=slugify(instance.title)
    if new_slug is not None:
        slug=new_slug
    qs=post.objects.filter(slug=slug).order_by("-id")
    exists=qs.exists()
    if exists:
        new_slug="%s-%s" %(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)

pre_save.connect(pre_save_post_receiver,sender=post)