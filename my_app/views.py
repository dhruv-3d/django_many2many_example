from django.shortcuts import render, HttpResponse

from .models import Post, Tag, User
from .forms import PostForm


def index(request):
    context_dict = {}
    all_tags = Tag.objects.all().values('name')
    post_form = PostForm()

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user_id = request.user.id
            post.save()

            tags_in_post = request.POST.get('tags').split(',')
            if tags_in_post:
                for tag in tags_in_post:
                    tag_instance, created = Tag.objects.get_or_create(name=tag.strip())
                    post.tags.add(tag_instance)

            context_dict['success'] = True
            return render(request, 'index.html', context_dict)

        elif post_form.errors:
            context_dict['form_errors'] = post_form.errors
            context_dict['post_form'] = post_form

            return render(request, 'index.html', context_dict)

    context_dict['post_form'] = post_form
    context_dict['available_tags'] = all_tags
    return render(request, 'index.html', context_dict)