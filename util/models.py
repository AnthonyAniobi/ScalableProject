from django.db import models
from PIL import Image
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def get_image_upload_path(instance, filename):
    return os.path.join('images', instance.path, filename)


class ImageModel(models.Model):
    title = models.CharField(max_length=100, blank=True)
    path = models.CharField(max_length=100, default='default', help_text="Subfolder within images/ to store the image")
    file = models.ImageField()#upload_to=get_image_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_image_url(self):
        """Get the full URL for the image"""
        if self.file:
            return self.file.url
        return None

    def __str__(self):
        return self.title or f"Image {self.id}"
    
    def save(self, *args, **kwargs):
        # If updating an existing instance with a new image
        if self.pk:
            try:
                old_instance = ImageModel.objects.get(pk=self.pk)
                if old_instance.file and self.file != old_instance.file:
                    # Delete the old image file
                    if os.path.isfile(old_instance.file.path):
                        os.remove(old_instance.file.path)
            except ImageModel.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
        
        # Resize image after saving
        self.resize_image()

    def resize_image(self):
        """Resize the image to appropriate dimensions"""
        if not self.file:
            return
        
        try:
            image = Image.open(self.file)

            max_size = (800, 800)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            # save to Bytes IO
            output = BytesIO()
            image_format = image.format or 'JPEG'
            image.save(output, format=image_format, quality=85)
            output.seek(0)
            
            # Replace the file with resized version
            self.file = InMemoryUploadedFile(
                output,
                'ImageField',
                f"{self.file.name.split('.')[0]}_resized.{image_format.lower()}",
                f'image/{image_format.lower()}',
                output.getbuffer().nbytes,
                None
            )
        except:
            print(f"Error processing image {self.file.name}")
        # if self.file and hasattr(self.file, 'path'):
        #     try:
        #         with Image.open(self.file.path) as img:
        #             # Determine max size based on path/usage
        #             if self.path == 'profile_photos':
        #                 max_size = (300, 300)  # Profile photos
        #             else:
        #                 max_size = (800, 800)  # Regular photos
                    
        #             # Only resize if image is larger than max size
        #             if img.height > max_size[1] or img.width > max_size[0]:
        #                 img.thumbnail(max_size, Image.Resampling.LANCZOS)
        #                 img.save(self.file.path, optimize=True, quality=85)
        #     except Exception as e:
        #         print(f"Error resizing image: {e}")


@receiver(pre_delete, sender=ImageModel)
def delete_image_file(sender, instance, **kwargs):
    """Delete image file when the model instance is deleted"""
    if instance.file:
        instance.file.delete(save=False)
        # try:
        #     if os.path.isfile(instance.file.path):
        #         os.remove(instance.file.path)
        # except Exception:
        #     pass


