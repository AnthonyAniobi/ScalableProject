from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import ImageModel, Photo, Like, Comment
from .forms import PhotoUploadForm, CommentForm


def home_view(request):
    """Display all photos in a feed format"""
    photos_list = Photo.objects.select_related('user').prefetch_related('likes', 'comments').all()
    # paginator = Paginator(photos_list, 10)  # Show 10 photos per page
    
    # page_number = request.GET.get('page')
    # photos = paginator.get_page(page_number)
    
    context = {
        'photos': photos_list,
        'comment_form': CommentForm() if request.user.is_authenticated else None,
    }
    return render(request, 'photos/home.html', context)


@login_required
def upload_photo(request):
    """Upload a new photo"""
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            caption = form.cleaned_data['caption']
            
            # Create ImageModel instance
            image_instance = ImageModel.objects.create(
                title=f"Photo by {request.user.username}",
                path='uploaded_photos',
                file=image_file
            )
            
            # Create Photo instance
            Photo.objects.create(
                user=request.user,
                image=image_instance,
                caption=caption
            )
            
            messages.success(request, 'Photo uploaded successfully!')
            return redirect('photos:home')
        else:
            messages.error(request, 'Error uploading photo. Please check the form.')
    else:
        form = PhotoUploadForm()
    
    return render(request, 'photos/upload.html', {'form': form})


def photo_detail(request, photo_id):
    """Display a single photo with comments"""
    photo = get_object_or_404(Photo, id=photo_id)
    comments = photo.comments.select_related('user').all()
    
    context = {
        'photo': photo,
        'comments': comments,
        'comment_form': CommentForm() if request.user.is_authenticated else None,
        'is_liked': photo.likes.filter(user=request.user).exists() if request.user.is_authenticated else False,
    }
    return render(request, 'photos/detail.html', context)


@login_required
@require_POST
def toggle_like(request, photo_id):
    """Toggle like status for a photo"""
    photo = get_object_or_404(Photo, id=photo_id)
    like, created = Like.objects.get_or_create(user=request.user, photo=photo)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'like_count': photo.like_count,
    })


@login_required
def add_comment(request, photo_id):
    """Add a comment to a photo"""
    photo = get_object_or_404(Photo, id=photo_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.photo = photo
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment.')
    
    return redirect('photos:detail', photo_id=photo_id)


@login_required
def delete_comment(request, comment_id):
    """Delete a comment (only by the comment author)"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.user != request.user:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('photos:detail', photo_id=comment.photo.id)
    
    if request.method == 'POST':
        photo_id = comment.photo.id
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('photos:detail', photo_id=photo_id)
    
    return render(request, 'photos/delete_comment.html', {'comment': comment})


@login_required
def delete_photo(request, photo_id):
    """Delete a photo (only by the photo owner)"""
    photo = get_object_or_404(Photo, id=photo_id)
    
    if photo.user != request.user:
        messages.error(request, 'You can only delete your own photos.')
        return redirect('photos:detail', photo_id=photo_id)
    
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Photo deleted successfully!')
        return redirect('photos:home')
    
    return render(request, 'photos/delete_photo.html', {'photo': photo})
