from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import os

from .models import Section, MediaItem
from .forms import SectionForm, MediaUploadForm, MediaEditForm


# ─── Public Views ───────────────────────────────────────────────────────────

def home(request):
    sections = Section.objects.prefetch_related('media').all()
    query = request.GET.get('q', '')
    if query:
        sections = sections.filter(name__icontains=query)
    return render(request, 'home.html', {'sections': sections, 'query': query})


def section_detail(request, pk):
    section = get_object_or_404(Section, pk=pk)
    media_items = section.media.all()
    media_type = request.GET.get('type', '')
    if media_type in ['image', 'video']:
        media_items = media_items.filter(media_type=media_type)
    all_sections = Section.objects.all()
    return render(request, 'section_detail.html', {
        'section': section,
        'media_items': media_items,
        'media_type': media_type,
        'all_sections': all_sections,
    })


# ─── Auth Views ──────────────────────────────────────────────────────────────

def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'dashboard/login.html')


@login_required
def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')


# ─── Dashboard Views ─────────────────────────────────────────────────────────

@login_required
def dashboard_home(request):
    sections = Section.objects.all()
    total_media = MediaItem.objects.count()
    total_images = MediaItem.objects.filter(media_type='image').count()
    total_videos = MediaItem.objects.filter(media_type='video').count()
    return render(request, 'dashboard/home.html', {
        'sections': sections,
        'total_media': total_media,
        'total_images': total_images,
        'total_videos': total_videos,
    })


@login_required
def dashboard_sections(request):
    sections = Section.objects.all()
    return render(request, 'dashboard/sections.html', {'sections': sections})


@login_required
def section_create(request):
    if request.method == 'POST':
        form = SectionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Section created successfully!')
            return redirect('dashboard_sections')
    else:
        form = SectionForm()
    return render(request, 'dashboard/section_form.html', {'form': form, 'action': 'Create'})


@login_required
def section_edit(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        form = SectionForm(request.POST, request.FILES, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, 'Section updated successfully!')
            return redirect('dashboard_sections')
    else:
        form = SectionForm(instance=section)
    return render(request, 'dashboard/section_form.html', {'form': form, 'action': 'Edit', 'section': section})


@login_required
@require_POST
def section_delete(request, pk):
    section = get_object_or_404(Section, pk=pk)
    # Delete associated media files
    for item in section.media.all():
        if item.file and os.path.exists(item.file.path):
            os.remove(item.file.path)
    if section.cover_image and os.path.exists(section.cover_image.path):
        os.remove(section.cover_image.path)
    section.delete()
    messages.success(request, 'Section deleted.')
    return redirect('dashboard_sections')


@login_required
@require_POST
def section_reorder(request):
    try:
        data = json.loads(request.body)
        for item in data:
            Section.objects.filter(pk=item['id']).update(order=item['order'])
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
@require_POST
def media_reorder(request):
    try:
        data = json.loads(request.body)
        for item in data:
            MediaItem.objects.filter(pk=item['id']).update(order=item['order'])
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
@require_POST
def media_bulk_delete(request):
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        deleted = 0
        for item in MediaItem.objects.filter(pk__in=ids):
            if item.file and os.path.exists(item.file.path):
                os.remove(item.file.path)
            item.delete()
            deleted += 1
        return JsonResponse({'status': 'ok', 'deleted': deleted})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def media_upload(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        caption = request.POST.get('caption', '')
        files = request.FILES.getlist('files')
        if not files:
            # fallback for single file
            f = request.FILES.get('files')
            files = [f] if f else []
        uploaded = 0
        for f in files:
            ext = os.path.splitext(f.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                mtype = 'image'
            elif ext in ['.mp4', '.mov', '.avi', '.webm']:
                mtype = 'video'
            else:
                continue
            MediaItem.objects.create(
                section=section,
                file=f,
                media_type=mtype,
                caption=caption
            )
            uploaded += 1
        messages.success(request, f'{uploaded} file(s) uploaded successfully!')
        return redirect('media_upload', pk=pk)
    form = MediaUploadForm()
    recent_media = section.media.all()
    return render(request, 'dashboard/upload.html', {
        'section': section,
        'form': form,
        'recent_media': recent_media,
    })


@login_required
@require_POST
def media_delete(request, pk):
    item = get_object_or_404(MediaItem, pk=pk)
    section_pk = item.section.pk
    if item.file and os.path.exists(item.file.path):
        os.remove(item.file.path)
    item.delete()
    messages.success(request, 'Media deleted.')
    return redirect('media_upload', pk=section_pk)


@login_required
def media_edit(request, pk):
    item = get_object_or_404(MediaItem, pk=pk)
    old_section_pk = item.section.pk
    if request.method == 'POST':
        form = MediaEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Media updated.')
            return redirect('media_upload', pk=item.section.pk)
    else:
        form = MediaEditForm(instance=item)
    return render(request, 'dashboard/media_edit.html', {'form': form, 'item': item})


@login_required
@require_POST
def set_cover(request, section_pk, media_pk):
    section = get_object_or_404(Section, pk=section_pk)
    item = get_object_or_404(MediaItem, pk=media_pk, section=section, media_type='image')
    # Copy image to covers folder or just update reference
    from django.core.files import File
    import shutil
    section.cover_image = item.file
    section.save()
    messages.success(request, 'Cover image updated!')
    return redirect('media_upload', pk=section_pk)


# ─── Error Handlers ──────────────────────────────────────────────────────────

def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    return render(request, 'errors/500.html', status=500)
