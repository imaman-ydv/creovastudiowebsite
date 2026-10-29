from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from urllib.parse import urlsplit


def validate_public_link(value):
    if not value or value == '#':
        return
    if value.startswith('/') and not value.startswith('//') and '\\' not in value:
        return
    parsed = urlsplit(value)
    if parsed.scheme in {'http', 'https'} and parsed.netloc:
        return
    raise ValidationError('Use a website link beginning with https:// or a local path beginning with /.')


def validate_image_size(image):
    if image.size > 8 * 1024 * 1024:
        raise ValidationError('Choose an image smaller than 8 MB.')


class SitePage(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    meta_title = models.CharField(max_length=180, blank=True)
    meta_description = models.CharField(max_length=320, blank=True)
    published = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'title']
        verbose_name = 'page'
        verbose_name_plural = 'pages'

    def __str__(self):
        return self.title


class PageSection(models.Model):
    SECTION_TYPES = [
        ('hero', 'Hero'),
        ('text', 'Text'),
        ('image', 'Image'),
        ('split_content', 'Split content'),
        ('project_grid', 'Project grid'),
        ('service_grid', 'Service grid'),
        ('insight_grid', 'Insight grid'),
        ('testimonials', 'Testimonials'),
        ('faq', 'FAQs'),
        ('cta', 'Call to action'),
        ('custom', 'Custom section'),
    ]

    page = models.ForeignKey(SitePage, related_name='sections', on_delete=models.CASCADE)
    content_key = models.SlugField(max_length=80, blank=True, help_text='Editor-friendly slot name, such as about-heading or about-hero-image.')
    section_type = models.CharField(max_length=32, choices=SECTION_TYPES, default='text')
    heading = models.CharField(max_length=240, blank=True)
    body = models.TextField(blank=True)
    image_url = models.CharField(max_length=500, blank=True, help_text='Optional image link or site path, such as /images/example.avif.')
    image = models.ImageField(
        upload_to='site/pages/', blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_image_size],
        verbose_name='Uploaded image',
        help_text='Upload a JPG, PNG, or WebP image (maximum 8 MB). Takes priority over the image link.',
    )
    image_alt = models.CharField(max_length=240, blank=True, verbose_name='Image description')
    link_text = models.CharField(max_length=100, blank=True)
    link_url = models.CharField(max_length=500, blank=True)
    data = models.JSONField(default=dict, blank=True, help_text='Extra editable fields for this section.')
    published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f'{self.page.title} — {self.get_section_type_display()}'


class Project(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    client = models.CharField(max_length=160, blank=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    cover_image_url = models.CharField(max_length=500, blank=True, help_text='Optional image link or site path. An uploaded image takes priority.')
    cover_image = models.ImageField(
        upload_to='site/projects/', blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_image_size],
        verbose_name='Uploaded cover image',
        help_text='Upload a JPG, PNG, or WebP image (maximum 8 MB). Takes priority over the image link.',
    )
    image_alt = models.CharField(max_length=240, blank=True, verbose_name='Image description')
    body = models.TextField(blank=True, help_text='Optional full project story. Leave empty to keep the original static page content.')
    website_url = models.URLField(max_length=500, blank=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='site/projects/gallery/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_image_size],
        help_text='Upload a JPG, PNG, or WebP image (maximum 8 MB).',
    )
    alt_text = models.CharField(max_length=240, blank=True, verbose_name='Image description')
    caption = models.CharField(max_length=240, blank=True)
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Image position')

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'project image'
        verbose_name_plural = 'project images'

    def __str__(self):
        return self.caption or f'{self.project.title} image'


class Service(models.Model):
    title = models.CharField(
        max_length=160,
        verbose_name='Card title',
        help_text='The large title shown at the top of the card.',
    )
    slug = models.SlugField(unique=True)
    short_heading = models.CharField(max_length=180, blank=True)
    description = models.TextField(
        blank=True,
        verbose_name='Main text',
        help_text='The larger paragraph below the card title.',
    )
    details = models.TextField(
        blank=True,
        verbose_name='Supporting text',
        help_text='The smaller paragraph below the main text.',
    )
    read_more_content = models.TextField(
        blank=True,
        verbose_name='More to read',
        help_text='Optional extra information shown when a visitor clicks [ Read ].',
    )
    card_image = models.ImageField(
        upload_to='site/services/',
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_image_size],
        verbose_name='Card image',
        help_text='Upload a JPG, PNG, or WebP image (maximum 8 MB).',
    )
    image_alt = models.CharField(
        max_length=240,
        blank=True,
        verbose_name='Image description',
        help_text='Short description for accessibility.',
    )
    image_url = models.CharField(
        max_length=500,
        blank=True,
        help_text='Existing image fallback. Upload a new image above to replace it.',
    )
    link_text = models.CharField(max_length=100, blank=True, default='[ Read ]', verbose_name='Link label')
    link_url = models.CharField(max_length=500, blank=True, validators=[validate_public_link], verbose_name='Link destination')
    published = models.BooleanField(default=False, verbose_name='Show this card')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Card position')

    class Meta:
        ordering = ['sort_order', 'title']
        verbose_name = 'homepage card'
        verbose_name_plural = 'homepage cards'

    def __str__(self):
        return self.title


class HeroBranding(models.Model):
    logo_image = models.ImageField(
        upload_to='site/branding/',
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_image_size],
        verbose_name='Large homepage logo',
        help_text='Upload a JPG, PNG, or WebP logo (maximum 8 MB). Leave empty to use the original logo.',
    )
    image_alt = models.CharField(
        max_length=240,
        default="CreovaStudio's Logo",
        verbose_name='Image description',
    )
    size_percent = models.PositiveSmallIntegerField(
        default=86,
        validators=[MinValueValidator(30), MaxValueValidator(100)],
        verbose_name='Logo size (%)',
        help_text='Choose 30–100% of the hero area. The default 86% leaves space around the logo; it stays centered.',
    )

    class Meta:
        verbose_name = 'homepage hero logo'
        verbose_name_plural = 'homepage hero logo'

    def __str__(self):
        return 'Homepage hero logo'


class HeroPanel(models.Model):
    PANEL_SLOTS = [(slot, f'Strip {slot}') for slot in range(1, 12)]

    branding = models.ForeignKey(HeroBranding, related_name='panels', on_delete=models.CASCADE)
    slot = models.PositiveSmallIntegerField(choices=PANEL_SLOTS, verbose_name='Strip position')
    team_photo = models.ImageField(
        upload_to='site/hero-panels/',
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_image_size],
        verbose_name='Team photo (optional)',
        help_text='Upload a JPG, PNG, or WebP image (maximum 8 MB). Leave empty for a plain white reverse side.',
    )
    image_alt = models.CharField(max_length=240, blank=True, verbose_name='Photo description')
    visible = models.BooleanField(default=True, verbose_name='Show this strip')

    class Meta:
        ordering = ['slot']
        constraints = [
            models.UniqueConstraint(fields=['branding', 'slot'], name='unique_hero_panel_slot'),
        ]
        verbose_name = 'homepage hero strip'
        verbose_name_plural = 'homepage hero strips'

    def __str__(self):
        return f'Hero strip {self.slot}'


class SiteSectionVisibility(models.Model):
    key = models.SlugField(max_length=80, unique=True, editable=False)
    label = models.CharField(max_length=120, editable=False, verbose_name='Website section')
    page = models.CharField(max_length=80, default='Homepage', editable=False)
    visible = models.BooleanField(default=True, verbose_name='Show on website')
    sort_order = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ['sort_order', 'label']
        verbose_name = 'website section'
        verbose_name_plural = 'website sections'

    def __str__(self):
        return f'{self.page} — {self.label}'


class Insight(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(blank=True)
    cover_image_url = models.CharField(max_length=500, blank=True, help_text='Optional image link or site path. An uploaded image takes priority.')
    cover_image = models.ImageField(
        upload_to='site/insights/', blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_image_size],
        verbose_name='Uploaded cover image',
        help_text='Upload a JPG, PNG, or WebP image (maximum 8 MB). Takes priority over the image link.',
    )
    image_alt = models.CharField(max_length=240, blank=True, verbose_name='Image description')
    body = models.TextField(blank=True, help_text='Article content in Markdown or plain text.')
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', '-published_at', '-created_at']

    def __str__(self):
        return self.title


class InsightImage(models.Model):
    insight = models.ForeignKey(Insight, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='site/insights/gallery/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_image_size],
        help_text='Upload a JPG, PNG, or WebP image (maximum 8 MB).',
    )
    alt_text = models.CharField(max_length=240, blank=True, verbose_name='Image description')
    caption = models.CharField(max_length=240, blank=True)
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Image position')

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'insight image'
        verbose_name_plural = 'insight images'

    def __str__(self):
        return self.caption or f'{self.insight.title} image'


class SiteSetting(models.Model):
    key = models.SlugField(unique=True, help_text='For example: contact-email or instagram-url.')
    label = models.CharField(max_length=120)
    value = models.TextField(blank=True)
    group = models.CharField(max_length=80, default='General')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['group', 'label']
        verbose_name = 'site setting'
        verbose_name_plural = 'site settings'

    def __str__(self):
        return f'{self.group}: {self.label}'


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=160, blank=True)
    company = models.CharField(max_length=160, blank=True)
    quote = models.TextField()
    image_url = models.URLField(max_length=500, blank=True)
    published = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return f'{self.name} — {self.company}' if self.company else self.name


class FAQItem(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    published = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'FAQ item'
        verbose_name_plural = 'FAQ items'

    def __str__(self):
        return self.question


class ContactInquiry(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_WON = 'won'
    STATUS_LOST = 'lost'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_WON, 'Won'),
        (STATUS_LOST, 'Lost'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    company_brand = models.CharField(max_length=160, blank=True, verbose_name='Company / brand')
    project_type = models.CharField(max_length=80, blank=True)
    budget_range = models.CharField(max_length=80, blank=True)
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name='Reviewed')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    internal_notes = models.TextField(blank=True)
    follow_up_at = models.DateField(null=True, blank=True, verbose_name='Follow-up date')
    notification_sent = models.BooleanField(default=False, verbose_name='Notification accepted by SMTP')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'form submission'
        verbose_name_plural = 'form submissions'

    def __str__(self):
        return f'{self.name} — {self.created_at:%Y-%m-%d}'
