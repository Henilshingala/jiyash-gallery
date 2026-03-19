from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from .models import Section, MediaItem
from .forms import MediaItemBulkUploadForm

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'media_count', 'created_at']
    list_editable = ['order']
    ordering = ['order']

@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ['caption', 'section', 'media_type', 'uploaded_at']
    list_filter = ['media_type', 'section']
    ordering = ['-uploaded_at']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.admin_site.admin_view(self.bulk_upload_view), name='gallery_mediaitem_bulk_upload'),
        ]
        return custom_urls + urls

    def bulk_upload_view(self, request):
        if request.method == 'POST':
            form = MediaItemBulkUploadForm(request.POST, request.FILES)
            files = request.FILES.getlist('files')
            if form.is_valid():
                section = form.cleaned_data['section']
                media_type = form.cleaned_data['media_type']
                caption = form.cleaned_data['caption']
                for f in files:
                    MediaItem.objects.create(
                        section=section,
                        media_type=media_type,
                        caption=caption,
                        file=f
                    )
                self.message_user(request, f"Uploaded {len(files)} files successfully.")
                return redirect('admin:gallery_mediaitem_changelist')
        else:
            form = MediaItemBulkUploadForm()
        return render(request, 'admin/gallery/mediaitem_bulk_upload.html', {'form': form})

    def add_view(self, request, form_url='', extra_context=None):
        # Redirect default add page to bulk upload
        from django.shortcuts import redirect
        return redirect('admin:gallery_mediaitem_bulk_upload')
