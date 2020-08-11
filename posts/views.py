from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect,Http404
from .models import Post
from .forms import PostForm
from django.contrib import messages

# Create your views here.
def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            #title = form.clean_data.get('title')
            instance = form.save(commit=False)
            form.save()
            messages.success(request,"Succesfully created a post",extra_tags='btn btn-danger')
            return HttpResponseRedirect(instance.get_absolute_url())
            #redirect
        else:
            messages.error(request,"Error......")

    context = {
        "form": form
    }
    return render(request,'post/post_form.html',context)
#try catch block 
def post_detail(request,slug=None):
    instance = get_object_or_404(Post,slug=slug)
    print(f'Checking for = {instance}')
    context = { 
        'obj': instance
    }
    return render(request,'post/post_detail.html',context)

#checkout queryset filters
def post_list(request):
    #if request.user.is_authenticated
    queryset = Post.objects.all().order_by("-timestamp") 
    context = {
        "object_lists" :queryset
    }
    return render(request,'post/post_list.html',context)

def post_update(request,slug=None):
    if not request.user.is_staff or not request.user.is_supperuser:
        raise Http404
    instance = get_object_or_404(Post,slug=slug)
    form = PostForm(instance=instance)
    if request.method == 'POST':
        form = PostForm(request.POST,instance= instance)
        if form.is_valid():
            #title = form.clean_data.get('title')
            instance = form.save(commit=False)
            form.save()

    context = { 
        'title' : instance.title,
        'instance': instance,
        'form': form
    }
    return render(request,'post/post_form.html',context)

def post_delete(request,pk=None):
    instance = get_object_or_404(Post,id=pk)
    instance.delete()
    messages.success(request,'Successfully Deleted')
    return redirect('posts:list')
