import pytz
import stripe
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.utils import dateparse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse, reverse

from paypal.standard.forms import PayPalPaymentsForm
from .models import Post, Tag, User, Session, SessionSlot, UserRating, SessionSlotBooking
from .forms import PostForm, SessionSlotForm


stripe.api_key = settings.STRIPE_SECRET_KEY


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
            # post.picture = post_form.cleaned_data['picture']
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


def calender_poc(request):
    context_dict = {}

    session_slots = [
        {
            'id': 1,
            'title': 'Session 1',
            'start_time': datetime.strptime('2019-11-14 8:00:00', '%Y-%m-%d %H:%M:%S'),
            'end_time': datetime.strptime('2019-11-14 11:30:00', '%Y-%m-%d %H:%M:%S'),
            'session_id': 14
        },
        {
            'id': 2,
            'title': 'Session 2',
            'start_time': datetime.strptime('2019-11-15 16:30:00', '%Y-%m-%d %H:%M:%S'),
            'end_time': datetime.strptime('2019-11-15 18:30:00', '%Y-%m-%d %H:%M:%S'),
            'session_id': 14
        },
                {
            'id': 3,
            'title': 'Session 3',
            'start_time': datetime.strptime('2019-11-16 12:30:00', '%Y-%m-%d %H:%M:%S'),
            'end_time': datetime.strptime('2019-11-16 13:30:00', '%Y-%m-%d %H:%M:%S'),
            'session_id': 14
        },
                {
            'id': 4,
            'title': 'Session 4',
            'start_time': datetime.strptime('2019-11-17 11:00:00', '%Y-%m-%d %H:%M:%S'),
            'end_time': datetime.strptime('2019-11-17 12:00:00', '%Y-%m-%d %H:%M:%S'),
            'session_id': 14
        },
    ]

    context_dict['session_slots'] = session_slots
    return render(request, 'calender_poc.html', context_dict)


def event_schedule(request):
    context_dict = {}
    all_session = Session.objects.all()
    sess_slots = SessionSlot.objects.all()

    if request.method == 'POST':
        if request.POST.get('created'):
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            sesion_id = request.POST.get('sesion_id')
            slot_id = request.POST.get('slot_id')
            print(f"{start_time}\n{end_time}\n{sesion_id}")

    context_dict['session_slots'] = sess_slots
    # context_dict['session_list'] = all_session
    return render(request, 'slot_schedule.html', context_dict)


def profile_detailed_view(request):
    context_dict = {}

    session_slots = [
        {
            'id': 1,
            'title': 'Session 1',
            'start_time': datetime.strptime('2019-10-31 1:00:00', '%Y-%m-%d %H:%M:%S'),
            'end_time': datetime.strptime('2019-10-31 2:30:00', '%Y-%m-%d %H:%M:%S'),
            'session_id': 14
        },
        {
            'id': 2,
            'title': 'Session 2',
            'start_time': datetime.strptime('2019-10-30 5:30:00', '%Y-%m-%d %H:%M:%S'),
            'end_time': datetime.strptime('2019-10-30 6:30:00', '%Y-%m-%d %H:%M:%S'),
            'session_id': 14
        },
                {
            'id': 3,
            'title': 'Session 3',
            'start_time': datetime.strptime('2019-11-7 10:00:00', '%Y-%m-%d %H:%M:%S'),
            'end_time': datetime.strptime('2019-11-7 12:30:00', '%Y-%m-%d %H:%M:%S'),
            'session_id': 14
        },
                {
            'id': 4,
            'title': 'Session 4',
            'start_time': datetime.strptime('2019-10-25 11:00:00', '%Y-%m-%d %H:%M:%S'),
            'end_time': datetime.strptime('2019-10-25 12:00:00', '%Y-%m-%d %H:%M:%S'),
            'session_id': 14
        },
    ]

    related_things = Post.objects.filter(subjects__name__icontains="maths")
    # print("related_things: ", related_things.user.first_name)

    rating_list = {}
    for post_inst in related_things:
        rating_list[post_inst.title] = [post_inst ,UserRating.objects.get(user_id=post_inst.user_id)]

    context_dict['user_data'] = rating_list
    context_dict['session_slots'] = session_slots
    return render(request, 'profile.html', context_dict)


@csrf_exempt
def payment_done(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=3000,
            currency='inr',
            description='A Django Charge',
            source=request.POST['stripeToken']
        )
    return render(request, 'payment_done.html')
 
 
@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')


def process_payment(request):
    host = request.get_host()
 
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': 10.00,
        'item_name': 'Order 175931',
        'invoice': '175931',
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }
 
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'form': form})


def process_booking(request):
    context_dict = {}
    
    context_dict['key'] = settings.STRIPE_PUBLISHABLE_KEY

    return render(request, 'book_session.html', context_dict)


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------


# to render calender
def render_calender(request):
    context_dict = {}

    all_slots = SessionSlotBooking.objects.all()

    slots_list = []
    for slot in all_slots:
        print("newTime:",slot.start_time.strftime("%Y-%m-%dT%H:%M"))
        slots_list.append({
            'start_time':slot.start_time.strftime("%Y-%m-%dT%H:%M"),
            'end_time': slot.end_time.strftime("%Y-%m-%dT%H:%M"),
            'id': slot.id
        })
    context_dict['session_slots'] = slots_list

    return render(request, 'schedule_test.html', context_dict)

# to fetch all events
def fetch_events(request):
    context_dict = {}

    all_slots = SessionSlotBooking.objects.all()

    slots_list = []
    for slot in all_slots:
        # aware_start_time = pytz.utc.localize(slot.start_time)
        # aware_end_time = pytz.utc.localize(slot.end_time)
        slots_list.append({
            'start_time':slot.start_time.strftime("%Y-%m-%dT%H:%M"),
            'end_time': slot.end_time.strftime("%Y-%m-%dT%H:%M"),
            'id': slot.id
        })

    return JsonResponse({'status':200, 'all_slots': slots_list})

# to create new events
def create_new_event(request):
    if request.method == 'POST':
        start_time = request.POST.get('start_time', None)
        end_time = request.POST.get('end_time', None)

        date_format = '%a, %d %b %Y %H:%M:%S %Z'
        unaware_start_time = datetime.strptime(start_time, date_format)
        aware_start_time = pytz.utc.localize(unaware_start_time)

        unaware_end_time = datetime.strptime(end_time, date_format)
        aware_end_time = pytz.utc.localize(unaware_end_time)

        print(f"\n\n unaware: {unaware_start_time}\n type: {type(unaware_start_time)}\n")
        print(f"\n\n aware: {aware_start_time}\n type: {type(aware_start_time)}\n")

        new_slot = SessionSlotBooking.objects.create(start_time=aware_start_time, end_time=aware_end_time)
    
    return JsonResponse({'status':200, 'new_slot': {'start_time':new_slot.start_time, 'end_time':new_slot.end_time, 'id':new_slot.id}})
