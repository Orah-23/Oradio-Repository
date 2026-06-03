# 🎙️ Oradio

> **Listen to the world.** A voice-first social platform where every post, comment, and reply is an audio recording.

---

## Overview

Oradio is a Django-based audio social network. Instead of typing posts and comments, users record voice notes directly in the browser. Think Twitter, but everything is spoken.

**Core idea:** microphone → record → post. No text required.

---

## Features

- **Voice posts** — record and upload audio posts from the browser
- **Voice comments** — comment on posts with audio recordings
- **Threaded replies** — reply to comments with nested audio threads
- **Reactions** — like/unlike posts with a heart button
- **Follow system** — follow and unfollow other users
- **Messenger** — direct text messaging between users
- **Online presence** — green dot shows who's currently active (5 min window)
- **Search** — search posts by caption or author name
- **User profiles** — avatar, bio, follower/following counts
- **Auth** — register, login, logout with Django's auth system
- **Ownership guards** — only post/comment owners can delete their content

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0.3 |
| API | Django REST Framework 3.17.1 |
| CORS | django-cors-headers 4.9.0 |
| Image handling | Pillow 12.2.0 |
| Database | SQLite (development) |
| Frontend | Vanilla HTML/CSS/JS |
| Fonts | Playfair Display, DM Sans, DM Mono (Google Fonts) |

---

## Project Structure

```
oradio/
├── base/                        # Main Django app
│   ├── migrations/
│   ├── api/                     # REST API (DRF)
│   ├── admin.py                 # Admin registrations
│   ├── apps.py
│   ├── forms.py                 # UserCreationForm, UserForm, PostForm
│   ├── middleware.py            # LastSeenMiddleware (online presence)
│   ├── models.py                # User, Post, Comment, Message
│   ├── urls.py                  # App URL patterns
│   └── views.py                 # All views
├── oradio/                      # Django project config
│   ├── settings.py
│   ├── urls.py                  # Root URL config
│   ├── asgi.py
│   └── wsgi.py
├── static/
│   ├── js/script.js             # Dropdown, avatar preview, audio exclusivity
│   ├── media/                   # Default avatar, icons, logo
│   └── styles/style.css         # Main stylesheet
├── templates/
│   ├── home.html
│   ├── navbar.html
│   └── theme/
│       ├── create-post.html
│       ├── conversation.html
│       ├── delete.html
│       ├── feed.html
│       ├── login.html
│       ├── messenger.html
│       ├── post.html
│       ├── profile.html
│       ├── register.html
│       └── update-profile.html
├── db.sqlite3
└── manage.py
```

---

## Data Models

### `User` (extends AbstractUser)
| Field | Type | Notes |
|---|---|---|
| first_name | CharField | |
| last_name | CharField | |
| email | EmailField | unique |
| bio | TextField | optional |
| avatar | ImageField | defaults to avatar.svg |
| last_seen | DateTimeField | updated by middleware |
| followers | ManyToManyField(self) | symmetrical=False |

**Properties:** `is_online` (active within last 5 minutes), `total_followers()`, `total_following()`

### `Post`
| Field | Type | Notes |
|---|---|---|
| host | ForeignKey(User) | |
| caption | TextField | optional |
| body | FileField | audio file, uploads to `posts/` |
| users_reacted | ManyToManyField(User) | |
| created / updated | DateTimeField | |

### `Comment`
| Field | Type | Notes |
|---|---|---|
| user | ForeignKey(User) | |
| post | ForeignKey(Post) | |
| body | FileField | audio file, uploads to `comments/` |
| parent | ForeignKey(self) | null = top-level comment, set = reply |
| created / updated | DateTimeField | |

### `Message`
| Field | Type | Notes |
|---|---|---|
| sender | ForeignKey(User) | related_name: sent_messages |
| recipient | ForeignKey(User) | related_name: received_messages |
| body | TextField | |
| is_read | BooleanField | default False |
| created | DateTimeField | |

---

## URL Reference

| URL | Name | View | Auth required |
|---|---|---|---|
| `/` | `home` | Home feed | No |
| `/login/` | `login` | Login | No |
| `/logout/` | `logout` | Logout | No |
| `/register/` | `register` | Register | No |
| `/post/<pk>/` | `post` | Post detail + comments | No |
| `/profile/<pk>/` | `user-profile` | User profile | No |
| `/create-post/` | `create-post` | Create post | ✅ |
| `/delete-post/<pk>/` | `delete-post` | Delete post | ✅ |
| `/delete-comment/<pk>/` | `delete-comment` | Delete comment | ✅ |
| `/reply-comment/<pk>/` | `reply-comment` | Reply to comment | ✅ |
| `/update-user/` | `update-user` | Edit profile | ✅ |
| `/follow-user/<pk>/` | `follow-user` | Follow user | ✅ |
| `/unfollow-user/<pk>/` | `unfollow-user` | Unfollow user | ✅ |
| `/react/<pk>/` | `react` | React to post | ✅ |
| `/unreact/<pk>/` | `unreact` | Remove reaction | ✅ |
| `/inbox/` | `inbox` | Message inbox | ✅ |
| `/conversation/<pk>/` | `conversation` | Chat with user | ✅ |
| `/new-conversation/<pk>/` | `new-conversation` | Start conversation | ✅ |

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd oradio

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install django==6.0.3 djangorestframework django-cors-headers pillow

# 4. Apply migrations
python manage.py migrate

# 5. Create a superuser (optional)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Configuration Notes

**`settings.py` — important settings:**

```python
AUTH_USER_MODEL = 'base.User'   # Custom user model
MEDIA_ROOT = BASE_DIR / 'static/media'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [BASE_DIR / 'static']
CORS_ALLOW_ALL_ORIGINS = True   # Restrict in production
```

**Middleware order matters** — `LastSeenMiddleware` must come after `AuthenticationMiddleware`:

```python
MIDDLEWARE = [
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
    'base.middleware.LastSeenMiddleware',  # ← last
]
```

---

## Key Frontend Behaviours

**Exclusive audio playback** — only one voice note plays at a time. When a new one starts, all others pause automatically via the `onplay="pauseOthers(this)"` inline handler on every `<audio>` element.

**Animated waveform** — the recording UI shows 12 animated bars that bounce while recording, with a pulsing red REC indicator.

**Live chat refresh** — the conversation page polls for new messages every 5 seconds using `fetch()` and replaces the messages container without a full page reload.

**Avatar preview** — on the update profile page, selecting a new avatar image shows a live preview before saving.

---

## Admin

Register at `/admin/` using your superuser credentials. The following models are registered:

- `User` (with full UserAdmin interface)
- `Post`
- `Comment`

---

## Known Limitations

- Audio is stored as raw files (WebM/WAV) — no transcoding or compression
- Messages refresh via polling (every 5s), not WebSockets — not suitable for high-traffic production use
- `CORS_ALLOW_ALL_ORIGINS = True` should be restricted before deploying
- SQLite is used for development — switch to PostgreSQL for production
- `SECRET_KEY` in `settings.py` must be rotated and moved to environment variables before deployment

---

## License

All rights reserved. This project and its source code are the intellectual property of the author. No part of this codebase may be copied, reproduced, distributed, or used in any form without explicit written permission from the author. This project may be commercialised and made into an official product in the future.

---

*Built with Django by Oratile*
