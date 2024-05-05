from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from content.forms import PostForm
from content.models import Post


def view_posts(request):
    return render(request, template_name="content/content.html", context={"posts": Post.objects.order_by("-created")})


@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post_instance = form.save(commit=False)
            assert isinstance(post_instance, Post)
            post_instance.author = request.user.profile
            post_instance.save()
            return redirect("view-posts")
        else:
            return render(request, "content/add_post.html", {'form': form})
    else:
        form = PostForm()
        return render(request, "content/add_post.html", {'form': form})

