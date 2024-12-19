from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm



def home(request):
    # Display list of recent Posts in Card
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:6]
    context = {
        "posts": posts,

    }
    return render(request, 'blog/home.html', context)


def post_list(request):
    #Display list of recent published posts
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})


def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_date")

    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author = form.cleaned_data["author"],
                body = form.cleaned_data["body"],
                post =post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
        
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, 'blog/post_detail.html', context)


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
