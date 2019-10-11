from django.shortcuts import render, HttpResponse

from .models import Post, Tag, User
from .forms import PostForm


def index(request):
    context_dict = {}
    all_tags = Tag.objects.all().values('name')
    # all_tags_value = Tag.objects.values_list('name', flat=True)
    post_form = PostForm()

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user_id = request.user.id
            post.save()
            # new_post_instance = Post.objects.get(id=post.id)

            print("post.tags", request.POST)
            if request.POST.get('tags'):
                tags_for_post = request.POST.get('tags')
                for tag in tags_for_post:
                    print("all_tags_value", list(all_tags))
                    if tag not in all_tags:
                        new_tag = Tag.objects.create(name=tag)
                        post.tags.add(new_tag)
                    post.tags.add(tag)
                post.save()

            context_dict['success'] = True
            return render(request, 'index.html', context_dict)

        elif post_form.errors:
            context_dict['form_errors'] = post_form.errors
            context_dict['post_form'] = post_form

            return render(request, 'index.html', context_dict)

    context_dict['post_form'] = post_form
    context_dict['available_tags'] = all_tags
    return render(request, 'index.html', context_dict)