"""
Author: Francois Oratile Kgatlhanye
Date: 2026-06-04
Description: Views for Oradio website.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Post, Comment, User, Message
from .forms import PostForm, UserForm, MyUserCreationForm


# ── Helpers ─────────────────────────────────────────────────────

def get_unread_count(user):
    """Return total unread messages for the navbar badge."""
    if user.is_authenticated:
        return Message.objects.filter(recipient=user, is_read=False).count()
    return 0


def get_conversations(user):
    """Return conversation list for the home page left sidebar."""
    if not user.is_authenticated:
        return []
    others = User.objects.filter(
        Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
    ).distinct().exclude(id=user.id)

    conv_data = []
    for other in others:
        msgs = Message.objects.filter(
            Q(sender=user, recipient=other) | Q(sender=other, recipient=user)
        ).order_by('-created')
        last_msg = msgs.first()
        unread = msgs.filter(recipient=user, is_read=False).count()
        conv_data.append({'user': other, 'last_msg': last_msg, 'unread': unread})

    conv_data.sort(key=lambda x: x['last_msg'].created if x['last_msg'] else 0, reverse=True)
    return conv_data


# ── Auth ─────────────────────────────────────────────────────────

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'theme/login.html', {})


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.strip().lower()
            user.first_name = user.first_name.strip().capitalize()
            user.last_name = user.last_name.strip().capitalize()
            user.email = user.email.strip().lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'theme/register.html', {'form': form})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'theme/update-profile.html', {'form': form})


# ── Feed / Posts ─────────────────────────────────────────────────

def home(request):
    q = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(host__first_name__icontains=q) |
        Q(host__last_name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(caption__icontains=q)
    )
    # Right sidebar shows 10 most recent posts
    recent_posts = Post.objects.all()[:10]
    context = {
        'posts': posts,
        'recent_posts': recent_posts,
        'conversations': get_conversations(request.user),
        'unread_count': get_unread_count(request.user),
    }
    return render(request, 'home.html', context)


def post(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.comment_set.filter(parent=None)  # top-level only
    if request.method == 'POST':
        Comment.objects.create(
            user=request.user,
            post=post,
            body=request.FILES['media']
        )
        return redirect('post', pk=post.id)
    context = {
        'post': post,
        'comments': comments,
        'unread_count': get_unread_count(request.user),
    }
    return render(request, 'theme/post.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    context = {
        'user': user,
        'posts': posts,
        'unread_count': get_unread_count(request.user),
    }
    return render(request, 'theme/profile.html', context)


@login_required(login_url='login')
def createPost(request):
    if request.method == 'POST':
        Post.objects.create(
            host=request.user,
            caption=request.POST.get('caption'),
            body=request.FILES['media'],
        )
        return redirect('home')
    return render(request, 'theme/create-post.html', {
        'unread_count': get_unread_count(request.user)
    })


@login_required(login_url='login')
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'theme/post_form.html', {'form': form, 'post': post})


@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.user != post.host:
        return HttpResponse('Not allowed.')
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'theme/delete.html', {'obj': post})


@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user != comment.user:
        return HttpResponse('Not allowed.')
    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'theme/delete.html', {'obj': comment})


@login_required(login_url='login')
def replyComment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method == 'POST':
        Comment.objects.create(
            user=request.user,
            post=comment.post,
            body=request.FILES['media'],
            parent=comment
        )
        return redirect('post', pk=comment.post.id)
    return redirect('post', pk=comment.post.id)


# ── Follow / React ───────────────────────────────────────────────

@login_required(login_url='login')
def followUser(request, pk):
    post = Post.objects.get(id=pk)
    if post.host != request.user:
        if post.host not in request.user.following.all():
            request.user.following.add(post.host)
            post.host.followers.add(request.user)
        else:
            request.user.following.remove(post.host)
            post.host.followers.remove(request.user)
    return redirect('home')


@login_required(login_url='login')
def unfollowUser(request, pk):
    post = Post.objects.get(id=pk)
    request.user.following.remove(post.host)
    post.host.followers.remove(request.user)
    return redirect('home')


@login_required(login_url='login')
def react(request, pk):
    post = Post.objects.get(id=pk)
    if request.user not in post.users_reacted.all():
        post.users_reacted.add(request.user)
    return redirect('home')


@login_required(login_url='login')
def unreact(request, pk):
    post = Post.objects.get(id=pk)
    if request.user in post.users_reacted.all():
        post.users_reacted.remove(request.user)
    return redirect('home')


# ── Messenger ────────────────────────────────────────────────────

@login_required(login_url='login')
def inbox(request):
    return render(request, 'theme/messenger.html', {
        'conversations': get_conversations(request.user),
        'unread_count': get_unread_count(request.user),
    })


@login_required(login_url='login')
def conversation(request, pk):
    other = get_object_or_404(User, id=pk)
    user = request.user

    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if body:
            Message.objects.create(sender=user, recipient=other, body=body)
        return redirect('conversation', pk=pk)

    # Mark messages from other as read
    Message.objects.filter(sender=other, recipient=user, is_read=False).update(is_read=True)

    messages_qs = Message.objects.filter(
        Q(sender=user, recipient=other) | Q(sender=other, recipient=user)
    ).order_by('created')

    all_users = User.objects.exclude(id=user.id).order_by('username')

    context = {
        'other': other,
        'messages': messages_qs,
        'all_users': all_users,
        'unread_count': get_unread_count(request.user),
    }
    return render(request, 'theme/conversation.html', context)


@login_required(login_url='login')
def newConversation(request, pk):
    return redirect('conversation', pk=pk)
