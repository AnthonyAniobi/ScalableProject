# PhotoShare - Django Photo Sharing Platform

A simple Instagram-like photo sharing platform built with Django and styled with Tailwind CSS.

## Features

### For All Users:
- View all uploaded photos in a feed format
- Browse user profiles
- View photo details with comments and likes

### For Authenticated Users:
- Upload photos with captions
- Like photos
- Comment on photos
- Custom user profiles with:
  - Profile photo upload
  - Bio
  - Website link
  - First and Last name
- Edit profile information
- Delete own photos and comments

## Setup Instructions

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd video_upload
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser and go to:**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
video_upload/
├── accounts/          # User authentication and profiles
├── photos/            # Photo sharing functionality
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS, images)
├── media/             # User uploaded files
└── core/              # Django project settings
```

## Key Components

### Custom User Model
- Extended Django's AbstractUser
- Added profile photo, bio, and website fields
- Automatic image resizing for profile photos

### Photo Model
- Image upload with automatic resizing
- Caption support
- Like and comment functionality
- User ownership tracking

### Instagram-like Design
- Clean, modern interface using Tailwind CSS
- Responsive design for mobile and desktop
- Interactive elements (like buttons, hover effects)
- Grid layout for photo browsing

## Security Features

- CSRF protection on all forms
- User authentication required for uploads and comments
- Users can only delete their own content
- Secure file upload handling

## Technologies Used

- **Backend:** Django 4.2.23
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Database:** SQLite (development)
- **Image Processing:** Pillow
- **Icons:** Font Awesome

## Usage

1. **Register an account** or log in if you already have one
2. **Upload photos** by clicking the upload button in the navigation
3. **Explore** photos from other users in the main feed
4. **Interact** by liking and commenting on photos
5. **Customize** your profile by adding a bio, profile photo, and website

## Admin Panel

Access the Django admin panel at `/admin/` to manage:
- Users and their profiles
- Photos and their metadata
- Comments and likes
- Site administration

## Development Notes

- The project uses a custom user model, so migrations were created from the start
- Media files are served during development through Django's static file handling
- Profile photos and uploaded images are automatically resized to optimize storage
- The design is responsive and works well on both desktop and mobile devices