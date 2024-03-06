from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import Post, ChatRoom, Message
from PIL import Image
import ffmpeg
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .templatetags.custom_filters import add_class


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}!')
           # return redirect('login')  # Redirect to login page after successful registration
            return redirect('post_list')  # Redirect to the list page after registration 
    else:
        form = UserRegistrationForm()
    #return render(request, 'report/register.html', {'form': form})
    return render(request, 'report/register.html', {'add_class': add_class})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'report/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'report/post_detail.html', {'post': post})


def resize_image(image_path, output_width, output_height):
    img = Image.open(image_path)
    img.thumbnail((output_width, output_height))
    img.save(image_path)

def resize_video(video_path, output_width, output_height):
    ffmpeg.input(video_path).output(video_path, s=f'{output_width}x{output_height}').run()

from django.shortcuts import render
from .models import Post

def view_media(request):
    posts = Post.objects.all()
    return render(request, 'report/view_media.html', {'posts': posts})


def serve_media(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.file:
        return FileResponse(open(post.file.path, 'rb'))
    else:
        return render(request, 'report/file_not_found.html')
    


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if a chat room already exists for the post
    chat_room, created = ChatRoom.objects.get_or_create(post=post)
    
    if created:
        # Perform any additional initialization for the newly created chat room
        # For example: You can set initial messages, configure chat settings, etc.
        pass
    
    # Retrieve messages associated with the chat room
    messages = chat_room.message_set.all()
    
    return render(request, 'report/post_detail.html', {'post': post, 'messages': messages})


def send_message(request):
    if request.method == 'POST':
        # Create a new message
        message_content = request.POST.get('message')
        post_id = request.POST.get('post_id')
        # Assuming you have authentication set up, you can get the current user
        user = request.user
        # Save the message
        message = Message.objects.create(user=user, post_id=post_id, content=message_content)
        message.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def get_messages(request, post_id):
    # Retrieve messages for the given post_id
    messages = Message.objects.filter(post_id=post_id).order_by('created_at')
    # Format messages as JSON
    data = [{'user': message.user.username, 'content': message.content} for message in messages]
    return JsonResponse(data, safe=False)

def chat_room_view(request, chat_room_id):
    chat_room = ChatRoom.objects.get(id=chat_room_id)
    messages = Message.objects.filter(chat_room=chat_room).order_by('timestamp')
    return render(request, 'chat_room.html', {'chat_room': chat_room, 'messages': messages})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')