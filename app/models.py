from django.conf import settings
from django.db import models

from app import generate_unique_slug

PUBLISH_STATUS_CHOICES = (
    (0, 'Draft'),
    (1, 'Review'),
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
    template = models.CharField(max_length=255)
    publish_status = models.PositiveSmallIntegerField(default=0, choices=PUBLISH_STATUS_CHOICES)
    private = models.BooleanField(default=False)

    bride = models.CharField(max_length=50)
    groom = models.CharField(max_length=50)
    date = models.DateField()
    about_bride = models.CharField(max_length=255, null=True, blank=True)
    about_groom = models.CharField(max_length=255, null=True, blank=True)
    quotes = models.CharField(max_length=255, null=True, blank=True)

    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            name = "{} {}".format(self.bride, self.groom)
            self.slug = generate_unique_slug(self, Wedding, name)
        super(Wedding, self).save(*args, **kwargs)


class Invitation(BaseModel):
    wedding = models.ForeignKey(Wedding, null=True, blank=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=55)

    name = models.CharField(max_length=255)
    greeting = models.TextField(blank=True)
    attended = models.BooleanField(default=False)

    def __str__(self):
        return self.wedding.slug


class Story(BaseModel):
    wedding = models.ForeignKey(Wedding, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()

    def __str__(self):
        return self.wedding.slug


class Gallery(BaseModel):
    wedding = models.ForeignKey(Wedding, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.wedding.slug


class ImageGallery(BaseModel):
    gallery = models.ForeignKey(Gallery, null=True, blank=True, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='galley_image')

    def __str__(self):
        return self.galley.title
