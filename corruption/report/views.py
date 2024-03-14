import io
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import Post, ChatRoom, Message, UserAuthentication
from PIL import Image
import ffmpeg
from moviepy.editor import VideoFileClip
import PyPDF2
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .templatetags.custom_filters import add_class
from .forms import PostForm
from django.utils import timezone
from django.template.defaultfilters import truncatechars


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
    for post in posts:
        post.short_description = truncatechars(post.description, 100)
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
        # Get the message content and post ID from the POST data
        message_content = request.POST.get('message')
        post_id = request.POST.get('post_id')
        
        # Assuming you have authentication set up, you can get the current user
        user = request.user
        
        # Create a new message object and save it to the database
        message = Message.objects.create(
            user=user,
            content=message_content,
            post_id=post_id,
            created_at=timezone.now()
        )
        
        # Return a JSON response indicating success
        return JsonResponse({'status': 'success'})
    else:
        # If the request method is not POST, return an error response
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})

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
            return redirect('view_media')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'report/login.html')
    

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Resize each uploaded file before saving
            for field_name, file_obj in request.FILES.items():
                resize_file(file_obj)  # Resize the file
            form.save()
            return redirect('view_media')  # Redirect to a page displaying all posts
    else:
        form = PostForm()
    return render(request, 'report/create_post.html', {'form': form})



def landing_page(request):
    # Fetch data for statistics
    registered_users_over_time = get_registered_users_over_time()
    posted_cases_over_time = get_posted_cases_over_time()
    cases_attracting_users = get_cases_attracting_users()

    # Pass data to the template
    return render(request, 'landing.html', {
        'registered_users_over_time': registered_users_over_time,
        'posted_cases_over_time': posted_cases_over_time,
        'cases_attracting_users': cases_attracting_users,
    })

def get_registered_users_over_time():
    # Query the database for registered users over time
    registered_users_over_time = UserAuthentication.objects.all()  # Example queryset, replace with your actual queryset
    return registered_users_over_time

def get_posted_cases_over_time():
    # Query the database for posted cases over time
    posted_cases_over_time = Post.objects.all()  # Example queryset, replace with your actual queryset
    return posted_cases_over_time

def get_cases_attracting_users():
    # Query the database for cases attracting users
    cases_attracting_users = Message.objects.all()  # Example queryset, replace with your actual queryset
    return cases_attracting_users


def logout_view(request):
    logout(request)
    # Redirect to a specific page after logout, or wherever you want
    return redirect('landing_page')


#resizing
def resize_file(file_content, target_size=(640, 480)):
    # Get the file extension from the content type
    content_type = file_content.content_type
    file_extension = None
    if content_type.startswith('image'):
        file_extension = '.jpg'
    elif content_type.startswith('video'):
        file_extension = '.mp4'
    elif content_type == 'application/pdf':
        file_extension = '.pdf'
    elif content_type == 'image/svg+xml':
        # Handle SVG files separately
        # You can skip resizing or handle them using a different approach
        return file_content

    # Resize based on file type
    if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
        # Resize image
        with Image.open(file_content) as img:
            if img.size != target_size:
                img_resized = img.resize(target_size)
                return img_resized
            else:
                return img
    elif file_extension in ['.mp4', '.avi', '.mov']:
        # Resize video
        clip = VideoFileClip(file_content)
        if clip.size != target_size:
            resized_clip = clip.resize(target_size)
            return resized_clip
        else:
            return clip
    elif file_extension == '.pdf':
        # Compress PDF
        pdf_reader = PyPDF2.PdfFileReader(file_content)
        pdf_writer = PyPDF2.PdfFileWriter()
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            page.compressContentStreams()  # Compress page content
            pdf_writer.addPage(page)
        
        # Write compressed PDF content to a BytesIO object
        output_file = io.BytesIO()
        pdf_writer.write(output_file)
        output_file.seek(0)
        return output_file