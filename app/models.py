from django.conf import settings
from django.db import models

from versatileimagefield.fields import VersatileImageField

from app import generate_unique_slug, validate_phone_number

PUBLISH_STATUS_CHOICES = (
    (0, 'Draft'),
    (1, 'Pending'),
    (2, 'Published')
)


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        abstract = True


class Wedding(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)
    template = models.CharField(max_length=35)
    publish_status = models.PositiveSmallIntegerField(default=0, choices=PUBLISH_STATUS_CHOICES)
    private = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    date = models.DateField()
    quotes = models.CharField(max_length=255, null=True, blank=True)
    time = models.CharField(max_length=30, null=True, blank=True)
    youtube = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name = 'Pernikahan'
        verbose_name_plural = 'Pernikahan'

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            name = '{} {}'.format(self.bride.name, self.groom.name)
            self.slug = generate_unique_slug(self, Wedding, name)
        super(Wedding, self).save(*args, **kwargs)


class Groom(BaseModel):
    wedding = models.OneToOneField(Wedding, related_name='groom', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    photo = VersatileImageField(upload_to='groom_photo')
    about = models.TextField(blank=True)

    facebook = models.URLField(max_length=150, null=True, blank=True)
    twitter = models.URLField(max_length=150, null=True, blank=True)
    instagram = models.URLField(max_length=150, null=True, blank=True)

    class Meta:
        verbose_name = 'Mempelai Laki-laki'
        verbose_name_plural = 'Mempelai Laki-laki'

    def __str__(self):
        return self.name


class Bride(BaseModel):
    wedding = models.OneToOneField(Wedding, related_name='bride', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    photo = VersatileImageField(upload_to='bride_photo')
    about = models.TextField(blank=True)

    facebook = models.URLField(max_length=150, null=True, blank=True)
    twitter = models.URLField(max_length=150, null=True, blank=True)
    instagram = models.URLField(max_length=150, null=True, blank=True)

    class Meta:
        verbose_name = 'Mempelai Perempuan'
        verbose_name_plural = 'Mempelai Perempuan'

    def __str__(self):
        return self.name


class Invitation(BaseModel):
    wedding = models.ForeignKey(Wedding, null=True, blank=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=55)

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, null=True, blank=True, validators=[validate_phone_number])
    greeting = models.TextField(blank=True)
    attended = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Undangan'
        verbose_name_plural = 'Undangan'

    def __str__(self):
        return self.name


class InvitationText(BaseModel):
    wedding = models.OneToOneField(Wedding, related_name='invitation_text', on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        verbose_name = 'Kalimat Undangan'
        verbose_name_plural = 'Kalimat Undangan'

    def __str__(self):
        return self.wedding.slug


class Story(BaseModel):
    wedding = models.ForeignKey(Wedding, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()
    image = VersatileImageField(upload_to='story_image', null=True, blank=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'Kisah Perjalan Hubungan'
        verbose_name_plural = 'Kisah Perjalan Hubungan'

    def __str__(self):
        return self.wedding.slug


class Gallery(BaseModel):
    wedding = models.ForeignKey(Wedding, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Galeri'
        verbose_name_plural = 'Galeri'

    def __str__(self):
        return self.wedding.slug


class ImageGallery(BaseModel):
    gallery = models.ForeignKey(Gallery, null=True, blank=True, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255, null=True, blank=True)
    image = VersatileImageField(upload_to='gallery_image')

    class Meta:
        verbose_name = 'Foto Galeri'
        verbose_name_plural = 'Foto Galeri'

    def __str__(self):
        return self.gallery.title
