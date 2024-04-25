from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Thread, Topic, Comment, SocialPage, User, Room, Reservation, Chat, Message
from .forms import ThreadForm, SocialPageForm, UserForm, MyUserCreationForm, ReservationForm, MessageForm, ChatbotMessageForm
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


def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    threads = Thread.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )#[0:5]
    thread_count = threads.count()
#############################################################################################3333
    paginator = Paginator(threads, 5)  # Show 5 threads per page

    page_number = request.GET.get('page')
    try:
        threads = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        threads = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        threads = paginator.page(paginator.num_pages)

#####################################################################################################
    topics = Topic.objects.all() #[0:5]
    
    thread_comments = Comment.objects.filter(Q(thread__topic__name__icontains=q))[0:5]
    context = {'threads': threads, 'topics': topics, 'thread_comments': thread_comments, 'thread_count': thread_count, 'q': q}
    return render(request, 'base/home.html', context )

 
def thread(request, pk):
     
     thread = Thread.objects.get(id=pk)
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
    if user.username == 'admin_ecu':#or user.username == 'user2' or user.username == 'user3':
        # Grant admin-like access to user1
        return True
    # For other users, restrict posting in Main Topic 1
    return topic.name != 'General Announcements' #and topic.name != 'Main Topic 2'




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
    posts = SocialPage.objects.all().order_by('-timestamp')
    context = {'posts': posts}
    return render(request, 'base/social_page.html', context)

@login_required(login_url='login')
def createSocialPost(request):
    # Create a new social page post
    if request.method == 'POST':
        form = SocialPageForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
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
     return render(request, 'base/unimap.html')




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

