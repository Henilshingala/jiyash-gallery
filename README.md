# JIYA & SHAILESH Gallery

A personal media gallery and video sharing website built with Django.

## Features
- 5+ dynamic sections with custom order, name, and cover image
- Photo & video gallery with lightbox viewer
- Admin dashboard to manage sections and upload media
- Drag-and-drop section reordering
- Newest media always appears first
- Fully responsive dark luxury design

---

## Quick Start

```bash
# 1. Enter project folder
cd mediagallery

# 2. Run the setup script (creates venv, migrates DB, creates admin account)
chmod +x setup.sh
./setup.sh

# 3. Start the server
source venv/bin/activate
python manage.py runserver
```

### Manual setup (if you prefer)
```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations gallery
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## URLs

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Public gallery homepage |
| `http://127.0.0.1:8000/section/<id>/` | Individual section page |
| `http://127.0.0.1:8000/dashboard/` | Admin dashboard |
| `http://127.0.0.1:8000/dashboard/login/` | Admin login |
| `http://127.0.0.1:8000/dashboard/sections/` | Manage & reorder sections |
| `http://127.0.0.1:8000/dashboard/upload/<id>/` | Upload media to section |
| `http://127.0.0.1:8000/admin/` | Django built-in admin |

---

## Project Structure

```
mediagallery/
├── manage.py
├── requirements.txt
├── setup.sh
├── mediagallery/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── gallery/               # Main app
│   ├── models.py          # Section, MediaItem
│   ├── views.py           # All views
│   ├── urls.py            # URL routing
│   ├── forms.py           # Forms
│   └── admin.py
├── templates/
│   ├── base.html          # Public base layout
│   ├── home.html          # Homepage
│   ├── section_detail.html
│   ├── dashboard/
│   │   ├── base_dashboard.html
│   │   ├── login.html
│   │   ├── home.html
│   │   ├── sections.html
│   │   ├── section_form.html
│   │   ├── upload.html
│   │   └── media_edit.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
├── static/
│   ├── css/
│   │   ├── style.css      # Public site styles
│   │   └── dashboard.css  # Dashboard styles
│   └── js/
│       ├── main.js
│       └── dashboard.js
└── media/                 # Uploaded files (auto-created)
```

---

## Admin Panel Guide

### Creating Sections
1. Go to `/dashboard/sections/` → click **+ New Section**
2. Set a name, description, and order number (1 = first on homepage)
3. Optionally upload a cover image

### Uploading Media
1. Go to `/dashboard/sections/` → click **Upload** next to a section
2. Drag & drop or browse to select multiple files
3. Optionally add a shared caption
4. New media always appears first in the section

### Reordering Sections
- **Drag rows** in the sections table to reorder visually
- Or **edit the number** in the Order column
- Click **Save Order** to apply — sections refresh in ascending number order

### Setting Cover Images
- In the Upload page, any photo has a **Cover** button
- Click it to set that photo as the section's cover thumbnail

---

## Deployment Notes

For production, update `settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = 'your-strong-secret-key'
```

Use Gunicorn + Nginx for serving.
