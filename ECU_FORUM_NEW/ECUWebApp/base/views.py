from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Thread, Topic, Comment, SocialPage, User, Room, Reservation, Chat, Message, SocialPost, SocialComment
from .forms import ThreadForm, SocialPageForm, UserForm, MyUserCreationForm, ReservationForm, MessageForm, ChatbotMessageForm, SocialCommentForm
from django.db.models import Q
from time import sleep
from . import eliza
from . import utils
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
# Create your views here.

def send_notification(title, body, user_id = None):
    if user_id is not None:
        user = User.objects.get(pk=user_id)
        user.notifications.create(title=title, body=body)
    else:
        users = User.objects.all()
        for user in users:
            user.notifications.create(title=title, body=body)

def loginPage(request):
     page = 'login'
     
     if request.user.is_authenticated:
        return redirect('home')
     
     if request.method == 'POST':
          
          email=request.POST.get('email').lower()
          password=request.POST.get('password')

          try:
            user = User.objects.get(email=email)
          except:
            messages.error(request, 'User does not exist')

          user = authenticate(request, email=email, password=password)

          if user is not None:
            login(request, user)
            return redirect('home')
          else:
            messages.error(request, 'Username or password does not exist')
     context = {'page': page}
     return render(request, 'base/login_register.html', context)
     


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    
    form = MyUserCreationForm()

    if request.method =='POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})


# def home(request):

#     q = request.GET.get('q') if request.GET.get('q') != None else ''
#     threads = Thread.objects.filter(
#         Q(topic__name__icontains=q) |
#         Q(name__icontains=q) |
#         Q(description__icontains=q)
#         )#[0:5]
#     thread_count = threads.count()
# #############################################################################################3333
#     paginator = Paginator(threads, 5)  # Show 5 threads per page

#     page_number = request.GET.get('page')
#     try:
#         threads = paginator.page(page_number)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         threads = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         threads = paginator.page(paginator.num_pages)

# #####################################################################################################
#     topics = Topic.objects.all() #[0:5]
    
#     thread_comments = Comment.objects.filter(Q(thread__topic__name__icontains=q))[0:3]
#     context = {'threads': threads, 'topics': topics, 'thread_comments': thread_comments, 'thread_count': thread_count, 'q': q}
#     return render(request, 'base/home.html', context )

# def home(request):
#     q = request.GET.get('q') if request.GET.get('q') != None else ''
#     threads = Thread.objects.filter(
#         Q(topic__name__icontains=q) |
#         Q(name__icontains=q) |
#         Q(description__icontains=q)
#     )
#     thread_count = threads.count()

#     paginator = Paginator(threads, 6)  # Show 5 threads per page

#     page_number = request.GET.get('page')
#     try:
#         threads = paginator.page(page_number)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         threads = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         threads = paginator.page(paginator.num_pages)


#     topics = Topic.objects.all()

#     # Fetch recent news threads
#     recent_news_threads = Thread.objects.filter(Q(topic__name='General Announcements') | Q(topic__name='Educational Engagements'))[:3]

#     # Fetch recent events threads
#     recent_events_threads = Thread.objects.filter(Q(topic__name='University Events') | Q(topic__name='Student Events'))[:3]
#     thread_comments = Comment.objects.filter(Q(thread__topic__name__icontains=q))[0:3]
    
#     context = {
#         'threads': threads,
#         'topics': topics,
#         'thread_comments': thread_comments,
#         'thread_count': thread_count,
#         'q': q,
#         'recent_news_threads': recent_news_threads,
#         'recent_events_threads': recent_events_threads,
#     }
#     return render(request, 'base/home.html', context)
 


from django.db.models import Case, When, Value, IntegerField

def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    
    # Fetch all threads based on user input
    threads = Thread.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    
    # Define custom ordering to prioritize threads within specific topics
    topic_priority = Case(
        When(topic__name="General Announcements", then=Value(1)),
        When(topic__name="Educational Engagements", then=Value(2)),
        When(topic__name="University Events", then=Value(3)),
        When(topic__name="Student Events", then=Value(4)),
        When(topic__name="Project Group Requests", then=Value(5)),
        When(topic__name="Study Group Formations", then=Value(6)),
        default=Value(7),
        output_field=IntegerField(),
    )
    
    # Define custom ordering within specific topics to prioritize "Thread 1"
    thread1_priority = Case(
        When(topic__name="General Announcements", name="Official Announcements and Updates", then=Value(1)),
        When(topic__name="Educational Engagements", name="Explore Academic Horizons: Seminars, Workshops, and Guest Speakers", then=Value(1)),
        When(topic__name="University Events", name="University-Sponsored Events", then=Value(1)),
        When(topic__name="Student Events", name="Student-Sponsored Events and Activities Hub", then=Value(1)),
        When(topic__name="Project Group Requests", name="Project Group Formation and Collaboration", then=Value(1)),
        When(topic__name="Study Group Formations", name="Study Groups", then=Value(1)),
        When(topic__name="Software Engineering U65", name="Discuss anything and everything related to SE U65!", then=Value(1)),
        When(topic__name="Cyber Security Y89", name="Discuss anything and everything related to CS Y89!", then=Value(1)),
        default=Value(2),
        output_field=IntegerField(),
    )
    
    # If filtered by topic, prioritize "Thread 1" within specific topics
    if q:
        threads = threads.annotate(
            topic_priority=topic_priority,
            thread1_priority=thread1_priority
        ).order_by('topic_priority', 'thread1_priority', '-created')
    else:
        # If not filtered, maintain default ordering by creation date
        threads = threads.order_by('-created')

    # Count total number of threads
    thread_count = threads.count()

    # Paginate threads to display 6 per page
    paginator = Paginator(threads, 6)

    # Get current page number from the request
    page_number = request.GET.get('page')
    try:
        threads = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        threads = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        threads = paginator.page(paginator.num_pages)

    # Fetch all topics
    topics = Topic.objects.all()

    # Fetch recent news threads
    recent_news_threads = Thread.objects.filter(Q(topic__name='General Announcements') | Q(topic__name='Educational Engagements'))[:3]

    # Fetch recent events threads
    recent_events_threads = Thread.objects.filter(Q(topic__name='University Events') | Q(topic__name='Student Events'))[:3]
    
    # Fetch thread comments
    thread_comments = Comment.objects.filter(Q(thread__topic__name__icontains=q))[0:3]
    
    context = {
        'threads': threads,
        'topics': topics,
        'thread_comments': thread_comments,
        'thread_count': thread_count,
        'q': q,
        'recent_news_threads': recent_news_threads,
        'recent_events_threads': recent_events_threads,
    }
    return render(request, 'base/home.html', context)







def thread(request, pk):
     
     thread = get_object_or_404(Thread, id=pk)
     thread_comments = thread.comment_set.all()
     participants = thread.participants.all()

     if request.method == 'POST':
         comment = Comment.objects.create(
            user=request.user,
            thread=thread,
            body=request.POST.get('body')
         )
         thread.participants.add(request.user)
         return redirect('thread', pk=thread.id)
     
     
     context = {'thread': thread, 'thread_comments': thread_comments, 'participants': participants}
     return render(request, 'base/thread.html', context)


# def thread(request, pk):
#     thread = get_object_or_404(Thread, id=pk)
#     thread_comments = thread.comment_set.all()
#     participants = thread.participants.all()

#     pinned_thread = Thread.objects.filter(pinned=True).first()
#     print("Pinned Thread:", pinned_thread)  # Add this line for debugging

#     # Get the rest of the threads excluding the pinned thread
#     other_threads = Thread.objects.filter(pinned=False).exclude(id=pinned_thread.id) if pinned_thread else Thread.objects.exclude(id=thread.id)
    
#     # Combine pinned thread and other threads
#     threads = [pinned_thread] if pinned_thread else []
#     threads += list(other_threads)

#     if request.method == 'POST':
        
#         comment = Comment.objects.create(
#             user=request.user,
#             thread=thread,
#             body=request.POST.get('body')
#         )
#         thread.participants.add(request.user)
#         return redirect('thread', pk=thread.id)

#     context = {'thread': thread, 'thread_comments': thread_comments, 'participants': participants, 'threads': threads, 'pinned_thread': pinned_thread}
#     return render(request, 'base/thread.html', context)







def userProfile(request, pk):
    user = User.objects.get(id=pk)
    threads = user.thread_set.all()
    thread_comments = user.comment_set.all()
    topics = Topic.objects.all()
    context= {'user': user, 'threads': threads, 'thread_comments': thread_comments, 'topics': topics}
    return render(request, 'base/profile.html', context)

# @login_required(login_url='login')
# def createThread(request):
     
#      form = ThreadForm()
#      if request.method == 'POST':
#           form = ThreadForm(request.POST)
#           if form.is_valid():
#                thread = form.save(commit=False)
#                thread.host = request.user
#                thread.save()
#                return redirect('home')
#      context = {'form': form}
#      return render(request, 'base/thread_form.html', context)

@login_required(login_url='login')
def createThread(request):
    form = ThreadForm()
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.host = request.user
            # Check if the selected title is restricted
            if not is_title_restricted(thread.topic, request.user):
                # Redirect to a permission denied page or show an appropriate message
                return HttpResponse("You don't have permission to create threads in this title.")
            thread.save()

            if thread.topic.id == 2:
                send_notification('Test Notification', 'Test notification body')

            return redirect('home')
    context = {'form': form}
    return render(request, 'base/thread_form.html', context)

def is_title_restricted(topic, user):
    # Check if the current user is user1
    if user.username == 'admin_ecu' or user.username == 'admin_ecu2': #or user.username == 'user3':
        # Grant admin-like access to user1
        return True
    # For other users, restrict posting in Main Topic 1
    return topic.name != 'General Announcements' and topic.name != 'Educational Engagements' and topic.name != 'University Events' #and topic.name != 'Main Topic 2'




@login_required(login_url='login')
def updateThread(request, pk):
     thread = Thread.objects.get(id=pk)
     form = ThreadForm(instance= thread)

     if request.user != thread.host:
        return HttpResponse('You cannot do that!')

     if request.method == 'POST':
          form = ThreadForm(request.POST, instance= thread)
          if form.is_valid():
               form.save()
               return redirect('home')
               
     context = {'form': form}
     return render (request, 'base/thread_form.html', context)


@login_required(login_url='login')
def deleteThread(request, pk):
     thread = Thread.objects.get(id=pk)

     if request.user != thread.host:
        return HttpResponse('You cannot do that!')
     
     if request.method == 'POST':
          thread.delete()
          return redirect('home')
     return render(request, 'base/delete.html', {'obj': thread})

@login_required(login_url='login')
def deleteComment(request, pk):
     comment = Comment.objects.get(id=pk)

     if request.user != comment.user:
        return HttpResponse('You cannot do that!')
     
     if request.method == 'POST':
          comment.delete()
          return redirect('home')
     return render(request, 'base/delete.html', {'obj': comment})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance = user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk = user.id)
    return render(request, 'base/update_user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    thread_comments = Comment.objects.all()[0:5]
    return render(request, 'base/activity.html', {'thread_comments': thread_comments})

##################################################################################################
def socialPage(request):
    # Retrieve existing social page posts
    # q = request.GET.get('q') if request.GET.get('q') != None else ''
    # threads = Thread.objects.filter(
    #     Q(topic__name__icontains=q) |
    #     Q(name__icontains=q) |
    #     Q(description__icontains=q)
    # )
    posts = SocialPost.objects.all().order_by('-created')
    topics = Topic.objects.all()
    recent_news_threads = Thread.objects.filter(Q(topic__name='General Announcements') | Q(topic__name='Educational Engagements'))[:3]

    # Fetch recent events threads
    recent_events_threads = Thread.objects.filter(Q(topic__name='University Events') | Q(topic__name='Student Events'))[:3]
    # thread_comments = Comment.objects.filter(Q(thread__topic__name__icontains=q))[0:3]
    context = {'posts': posts, 'topics': topics, 'recent_news_threads': recent_news_threads, 'recent_events_threads': recent_events_threads}
    return render(request, 'base/social_page.html', context)

def socialPost(request, pk):
    post = get_object_or_404(SocialPost, pk=pk)
    comments = post.socialcomment_set.all()
    if request.method == 'POST':
        form = SocialCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('social_post', pk=pk)
    else:
        form = SocialCommentForm()
    return render(request, 'base/social_post.html', {'post': post, 'comments': comments, 'form': form})




def deleteSocialComment(request, pk):
    comment = get_object_or_404(SocialComment, pk=pk)
    if request.method == 'POST':
        if comment.user == request.user:
            comment.delete()
            return redirect('social_post', pk=comment.post.pk)  # Redirect to the social post comment after deletion
    return redirect('home')  # Redirect to the home page if the user is not authorized or request method is not POST

def editComment(request, pk):
    comment = get_object_or_404(SocialComment, pk=pk)
    if request.method == 'POST':
        form = SocialCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('social_post', pk=comment.post.pk)
    else:
        form = SocialCommentForm(instance=comment)
    return render(request, 'base/edit_comment.html', {'form': form})

@login_required(login_url='login')
def createSocialPost(request):
    # Create a new social page post
    if request.method == 'POST':
        form = SocialPageForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the social page post
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            
            # Create a corresponding SocialPost object
            social_post = SocialPost.objects.create(
                user=request.user,
                image=post.image,  # You can adjust this based on your model fields
                video=post.video,  # You can adjust this based on your model fields
                caption=post.caption  # You can adjust this based on your model fields
            )
            return redirect('social_page')
    else:
        form = SocialPageForm()
    
    context = {'form': form}
    return render(request, 'base/social_page_form.html', context)

@login_required(login_url='login')
def deleteSocialPost(request, pk):
    social_page_post = get_object_or_404(SocialPage, pk=pk)

    if request.user != social_page_post.user:
        return HttpResponse('You cannot do that!')

    if request.method == 'POST':
        social_page_post.delete()
        messages.success(request, 'Social page post deleted successfully.')
        return redirect('social_page')

    return render(request, 'base/delete.html', {'obj': social_page_post})



def uniMap(request):
    topics = Topic.objects.all()
    recent_news_threads = Thread.objects.filter(Q(topic__name='General Announcements') | Q(topic__name='Educational Engagements'))[:3]

    # Fetch recent events threads
    recent_events_threads = Thread.objects.filter(Q(topic__name='University Events') | Q(topic__name='Student Events'))[:3]
    context = {'topics': topics, 'recent_news_threads': recent_news_threads, 'recent_events_threads': recent_events_threads}
    return render(request, 'base/unimap.html', context)




def viewReservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'base/view_reservation.html', {'reservations': reservations})


def reserveRoom(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Check for reservation conflicts
            new_reservation = form.save(commit=False)  # Don't save to database yet
            if Reservation.objects.filter(
                room=new_reservation.room,
                date=new_reservation.date,
                start_time__lt=new_reservation.end_time,
                end_time__gt=new_reservation.start_time
            ).exists():
                # Conflicting reservation found
                return HttpResponse('Reservation unsuccessful: Room already reserved for this time slot.')
            else:
                # No conflicts, save the reservation
                new_reservation.save()
                return HttpResponse('RESERVATION SUCCESS! <a href="{}">Back</a>'.format(reverse('reserve_room')))  # Return success message
    else:
        form = ReservationForm()
    return render(request, 'base/reservation.html', {'form': form})

def deleteReservation(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Reservation deleted successfully.')
        return redirect('view_reservation')
    return render(request, 'base/delete.html', {'obj': reservation})

@login_required(login_url='login')
def chat(request, pk):
    receiver = User.objects.get(pk=pk)
    chat_instance = Chat.objects.filter(sender=request.user, receiver=receiver).first()
    if chat_instance:
        print("ok")
    else:
        receiver
        chat_instance = Chat.objects.create(sender=request.user, receiver=receiver)
    return redirect('chats', pk=chat_instance.id)

@login_required(login_url='login')
def allChats(request):
    chats = Chat.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-created')
    context = {'chats': chats, 'chatCount': chats.count()}
    return render(request, 'base/chats.html', context)

@login_required(login_url='login')
def singleChat(request, pk):
    chat = Chat.objects.get(pk=pk)
    if chat.sender != request.user and chat.receiver != request.user:
        messages.error(request, 'Chat does not exist')
        return redirect('chats')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.user = request.user
            message.save()
            send_notification("Message Notification", "You received a new message", request.user.id)
            return redirect('chats', pk=pk)
        else:
            messages.error(request, 'An error occured while sending message')

    chats = Chat.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-created')
    messagesList = Message.objects.filter(Q(chat=chat)).order_by('created')
    context = {'chats': chats, 'chatCount': chats.count(), 'chat': chat, 'chatMessages':messagesList}
    return render(request, 'base/chats.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You cannot do that!')
    if request.method == 'POST':
        message.delete()
        return redirect('chats', pk=message.chat.id)
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def deleteNotification(request, pk):
    request.user.notifications.remove(pk)
    return redirect('home')

def chatBot(request):
    response = ""
    if request.method == 'POST':
        form = ChatbotMessageForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['body']
            rules_list = []
            default_responses = [
                "I am not sure, I understand you",
                ]
            for pattern, transforms in utils.rules.items():
                pattern = eliza.remove_punct(str(pattern.upper()))
                rules_list.append((pattern, transforms))
            response = eliza.respond(rules_list, query.upper(), default_responses)
    sleep(0.5)
    return JsonResponse({'result': response})

