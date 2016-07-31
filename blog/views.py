from django.shortcuts import render,get_object_or_404,redirect
from urllib import quote_plus
from django.http import HttpResponse,HttpResponseRedirect,Http404
from blog.models import post
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required


# Create your views here.
from .forms import PostForm

@login_required
def posts_create(request):
    form=PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        instance.save()
        messages.success(request,"Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context={
        "form":form,
    }
    return render(request, "post_form.html", context)


def posts_detail(request,slug=None):
    instance=get_object_or_404(post,slug=slug)
    if instance.publish > timezone.now().date():
        messages.success(request,"Your post will be published on the given date")
    if instance.draft:
        messages.success(request,"Your post is saved as draft. Only you can view it.")
    initial_data={
        "content_type":instance.get_content_type,
        "object_id":instance.id
    }
    form=CommentForm(request.POST or None,initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
         c_type=form.cleaned_data.get("content_type")
         content_type=ContentType.objects.get(model=c_type)
         obj_id=form.cleaned_data.get("object_id")
         content_data=form.cleaned_data.get("content")
         parent_obj=None
         try:
             parent_id=int(request.POST.get("parent_id"))
         except:
             parent_id=None

         if parent_id:
             parent_qs=Comment.objects.filter(id=parent_id)
             if parent_qs.exists() and parent_qs.count()==1:
                 parent_obj=parent_qs.first()
         new_comment, created= Comment.objects.get_or_create(
                                   user=request.user,
                                   content_type=content_type,
                                   object_id=obj_id,
                                   content=content_data,
                                   parent=parent_obj
                                   )
         return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    comments = instance.comments
    context={
        "title":instance.title,
        "instance":instance,
        "comments":comments,
        "comment_form":form,
    }
    return render(request,"post_detail.html",context)


def posts_list(request):
    today=timezone.now().date()
    queryset_list=post.objects.active()
    if  request.user.is_staff or  request.user.is_superuser:
        queryset_list=post.objects.all()

    query=request.GET.get("q")
    if query:
        queryset_list=queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 2)  # Show 25 contacts per page
    page_request_var="page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset=paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context={
        "object_list":queryset,
        "title":"List",
        "page_request_var":page_request_var,
        "today":today
    }
    return render(request,"post_list.html",context)

@login_required
def posts_update(request, slug=None):
    instance = get_object_or_404(post, slug=slug)
    if request.user != instance.user:
            messages.error(request,"You cannot edit this post")
            return redirect("posts:list")
    else:
        form = PostForm(request.POST or None,request.FILES or None,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Successfully saved")
            return HttpResponseRedirect(instance.get_absolute_url())
        context = {
              "title": instance.title,
              "instance": instance,
              "form":form
            }
        return render(request, "post_form.html", context)

@login_required
def posts_delete(request,slug=None):
    instance=get_object_or_404(post,slug=slug)
    if request.user != instance.user:
        messages.success(request,"You cannot delete this post")
    else:
        instance.delete()
        messages.success(request, "Successfully deleted")
    return redirect("posts:list")

