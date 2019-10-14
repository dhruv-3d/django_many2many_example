from django.shortcuts import render, HttpResponse

from .models import Post, Tag, User
from .forms import PostForm, SessionSlotForm


def index(request):
    context_dict = {}
    all_tags = Tag.objects.all().values('name')
    post_form = PostForm()

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        print(request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user_id = request.user.id
            post.picture = post_form.cleaned_data['picture']
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


def datepicker_poc(request):
    context_dict ={}
    slot_form = SessionSlotForm()

    if request.method == 'POST':
        slot_form = SessionSlotForm(request.POST)
        
        if slot_form.is_valid():
            slot = slot_form.save(commit=False)
            print(f"slot.start_time: {slot.start_time}")
            slot.save()
        elif slot_form.errors:
            context_dict['form_errors'] = slot_form.errors


    context_dict['slot_form'] = slot_form
    return render(request, 'datepicker_poc.html', context_dict)
