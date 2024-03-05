from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import Post, ChatRoom, Message
from PIL import Image
import ffmpeg
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}!')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'report/register.html', {'form': form})

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

def view_media(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.file:
        file_path = post.file.path
        file_extension = file_path.split('.')[-1].lower()
        if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
            # Resize image
            resize_image(file_path, 640, 480)  # Adjust dimensions as needed
            return render(request, 'report/view_picture.html', {'post': post})
        elif file_extension in ['mp4', 'webm', 'ogg']:
            # Resize video
            #resize_video(file_path, 640, 480)  # Adjust dimensions as needed
            return render(request, 'report/view_video.html', {'post': post})
        elif file_extension in ['mp3', 'wav', 'ogg']:
            # Audio file
            return render(request, 'report/view_audio.html', {'post': post})
        elif file_extension in ['pdf', 'doc', 'docx', 'txt']:
            # Document file
            return render(request, 'report/view_document.html', {'post': post})
        else:
            return render(request, 'report/unsupported_file.html', {'post': post})
    else:
        return render(request, 'report/file_not_found.html')

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