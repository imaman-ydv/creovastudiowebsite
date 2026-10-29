from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ContactInquiry,
    FAQItem,
    HeroBranding,
    HeroPanel,
    Insight,
    InsightImage,
    PageSection,
    Project,
    ProjectImage,
    Service,
    SitePage,
    SiteSectionVisibility,
    SiteSetting,
    Testimonial,
)

admin.site.site_header = 'Creova Studio — Website Manager'
admin.site.site_title = 'Creova Studio Admin'
admin.site.index_title = 'Manage website content'

PAGE_SECTION_LABELS = {
    'home-hero-heading': 'Homepage hero heading',
    'home-intro-label': 'Intro label',
    'home-intro-copy-one': 'First introduction paragraph',
    'home-intro-image-one': 'First introduction image',
    'home-intro-copy-two': 'Second introduction paragraph',
    'home-intro-image-two': 'Second introduction image',
    'home-intro-sticker': 'Introduction sticker image',
    'home-work-heading': 'Latest work heading',
    'home-featured-link': 'Featured work project link',
    'home-featured-image': 'Featured work image',
    'home-featured-title': 'Featured work title',
    'home-featured-summary': 'Featured work description',
    'home-work-button': 'View all work button',
    'home-client-heading': 'Client showcase heading',
    'home-client-sticker': 'Client showcase image',
    'home-services-heading': 'Homepage services heading',
    'home-services-intro': 'Homepage services introduction',
    'about-hero-image': 'Hero background image',
    'about-heading': 'Main heading',
    'about-tagline': 'Intro tagline',
    'about-intro': 'About introduction',
    'about-since': 'Crafting since label',
    'about-studio-image': 'Studio image',
    'about-studio-banner': 'Studio banner image',
    'about-approach': 'Our approach paragraph',
    'about-echo-banner': 'Echoes banner image',
    'about-help-heading': 'How we can help heading',
    'about-help-intro': 'How we can help introduction',
    'about-quote': 'Closing quote',
}
for service_number in range(1, 5):
    PAGE_SECTION_LABELS[f'about-principle-{service_number}-title'] = f'Approach principle {service_number} title'
    PAGE_SECTION_LABELS[f'about-principle-{service_number}-body'] = f'Approach principle {service_number} text'
    PAGE_SECTION_LABELS[f'about-service-{service_number}-title'] = f'Service {service_number} title'
    PAGE_SECTION_LABELS[f'about-service-{service_number}-body'] = f'Service {service_number} description'


class PageSectionInline(admin.StackedInline):
    model = PageSection
    extra = 0
    fields = ('section_label', 'section_type', 'heading', 'body', 'image', 'image_preview', 'image_alt', 'image_url', 'link_text', 'link_url', 'published', 'sort_order')
    readonly_fields = ('section_label', 'image_preview')

    @admin.display(description='Content area')
    def section_label(self, obj):
        return PAGE_SECTION_LABELS.get(obj.content_key, obj.content_key) if obj else 'New content area'

    @admin.display(description='Current image')
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" alt="" style="max-height:100px;max-width:160px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        if obj and obj.image_url:
            return format_html('<img src="{}" alt="" style="max-height:100px;max-width:160px;object-fit:cover;border-radius:6px;" />', obj.image_url)
        return 'No image selected'


@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published', 'sort_order', 'updated_at')
    list_filter = ('published',)
    search_fields = ('title', 'meta_title', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PageSectionInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'year', 'category', 'cover_preview', 'featured', 'published', 'sort_order')
    list_filter = ('published', 'featured', 'year', 'category')
    search_fields = ('title', 'client', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('sort_order', '-created_at')
    readonly_fields = ('cover_preview',)
    inlines = []
    fieldsets = (
        ('Project details', {'fields': ('title', 'slug', 'client', 'year', 'category', 'summary', 'body', 'website_url')}),
        ('Cover image', {'fields': ('cover_image', 'cover_preview', 'image_alt', 'cover_image_url')}),
        ('Website display', {'fields': ('featured', 'published', 'sort_order')}),
    )

    @admin.display(description='Cover image')
    def cover_preview(self, obj):
        if obj and obj.cover_image:
            return format_html('<img src="{}" alt="" style="max-height:80px;max-width:120px;object-fit:cover;border-radius:6px;" />', obj.cover_image.url)
        if obj and obj.cover_image_url:
            return format_html('<img src="{}" alt="" style="max-height:80px;max-width:120px;object-fit:cover;border-radius:6px;" />', obj.cover_image_url)
        return 'No image selected'


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 0
    fields = ('image', 'image_preview', 'alt_text', 'caption', 'sort_order')
    readonly_fields = ('image_preview',)

    @admin.display(description='Preview')
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" alt="" style="max-height:70px;max-width:100px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return 'Upload an image'


ProjectAdmin.inlines = [ProjectImageInline]


class InsightImageInline(admin.TabularInline):
    model = InsightImage
    extra = 0
    fields = ('image', 'image_preview', 'alt_text', 'caption', 'sort_order')
    readonly_fields = ('image_preview',)

    @admin.display(description='Preview')
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" alt="" style="max-height:70px;max-width:100px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return 'Upload an image'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'published', 'sort_order')
    list_editable = ('published', 'sort_order')
    list_filter = ('published',)
    search_fields = ('title', 'description', 'details')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('sort_order', 'title')
    readonly_fields = ('image_preview',)
    fieldsets = (
        ('Card content', {'fields': ('title', 'slug', 'description', 'details', 'read_more_content')}),
        ('Card image', {'fields': ('card_image', 'image_preview', 'image_alt')}),
        ('Optional link', {'fields': ('link_text', 'link_url')}),
        ('Website display', {'fields': ('published', 'sort_order')}),
    )

    @admin.display(description='Current image')
    def image_preview(self, obj):
        if obj and obj.card_image:
            return format_html('<img src="{}" alt="" style="max-height:100px;max-width:160px;object-fit:cover;border-radius:6px;" />', obj.card_image.url)
        if obj and obj.image_url:
            return format_html('<img src="{}" alt="" style="max-height:100px;max-width:160px;object-fit:cover;border-radius:6px;" />', obj.image_url)
        return 'No image selected'


class HeroPanelInline(admin.TabularInline):
    model = HeroPanel
    extra = 0
    max_num = 11
    can_delete = False
    fields = ('slot', 'team_photo', 'image_preview', 'image_alt', 'visible')
    readonly_fields = ('image_preview',)
    ordering = ('slot',)

    @admin.display(description='Current photo')
    def image_preview(self, obj):
        if obj and obj.team_photo:
            return format_html(
                '<img src="{}" alt="" style="max-height:90px;max-width:120px;object-fit:cover;border-radius:6px;" />',
                obj.team_photo.url,
            )
        return 'White reverse side (no photo uploaded)'


@admin.register(HeroBranding)
class HeroBrandingAdmin(admin.ModelAdmin):
    fields = ('logo_image', 'image_preview', 'image_alt', 'size_percent')
    readonly_fields = ('image_preview',)
    inlines = [HeroPanelInline]

    @admin.display(description='Current logo preview')
    def image_preview(self, obj):
        if obj and obj.logo_image:
            return format_html('<img src="{}" alt="" style="max-height:180px;max-width:320px;object-fit:contain;background:#111;padding:12px;border-radius:6px;" />', obj.logo_image.url)
        return format_html(
            '<img src="{}" alt="" style="max-height:180px;max-width:320px;object-fit:contain;background:#111;padding:12px;border-radius:6px;" />',
            '/images/Logo.avif',
        )

    def has_add_permission(self, request):
        return not HeroBranding.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSectionVisibility)
class SiteSectionVisibilityAdmin(admin.ModelAdmin):
    list_display = ('label', 'page', 'visible')
    list_editable = ('visible',)
    list_filter = ('page', 'visible')
    ordering = ('sort_order', 'label')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ('title', 'cover_preview', 'published', 'published_at', 'sort_order')
    list_filter = ('published',)
    search_fields = ('title', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('sort_order', '-published_at')
    inlines = [InsightImageInline]
    readonly_fields = ('cover_preview',)
    fieldsets = (
        ('Article content', {'fields': ('title', 'slug', 'excerpt', 'body')}),
        ('Cover image', {'fields': ('cover_image', 'cover_preview', 'image_alt', 'cover_image_url')}),
        ('Website display', {'fields': ('published', 'published_at', 'sort_order')}),
    )

    @admin.display(description='Cover image')
    def cover_preview(self, obj):
        if obj and obj.cover_image:
            return format_html('<img src="{}" alt="" style="max-height:80px;max-width:120px;object-fit:cover;border-radius:6px;" />', obj.cover_image.url)
        if obj and obj.cover_image_url:
            return format_html('<img src="{}" alt="" style="max-height:80px;max-width:120px;object-fit:cover;border-radius:6px;" />', obj.cover_image_url)
        return 'No image selected'


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('label', 'key', 'group', 'updated_at')
    list_filter = ('group',)
    search_fields = ('label', 'key', 'value')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'published', 'sort_order')
    list_filter = ('published',)
    search_fields = ('name', 'company', 'role', 'quote')


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'published', 'sort_order')
    list_filter = ('published',)
    search_fields = ('question', 'answer')


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company_brand', 'project_type', 'status', 'follow_up_at', 'notification_sent', 'created_at', 'is_read')
    list_editable = ('status', 'follow_up_at', 'is_read')
    list_filter = ('status', 'project_type', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'company_brand', 'project_type', 'message', 'internal_notes')
    readonly_fields = ('name', 'email', 'company_brand', 'project_type', 'budget_range', 'message', 'created_at')
    date_hierarchy = 'created_at'
    actions = ('mark_new', 'mark_in_progress', 'mark_won', 'mark_lost')
    fieldsets = (
        ('Contact details', {'fields': ('name', 'email', 'company_brand')}),
        ('Project brief', {'fields': ('project_type', 'budget_range', 'message')}),
        ('Lead tracking', {'fields': ('status', 'internal_notes', 'follow_up_at', 'notification_sent', 'is_read', 'created_at')}),
    )
    readonly_fields = (*readonly_fields, 'notification_sent')

    @admin.action(description='Mark selected inquiries as new')
    def mark_new(self, request, queryset):
        queryset.update(status=ContactInquiry.STATUS_NEW)

    @admin.action(description='Mark selected inquiries as in progress')
    def mark_in_progress(self, request, queryset):
        queryset.update(status=ContactInquiry.STATUS_IN_PROGRESS)

    @admin.action(description='Mark selected inquiries as won')
    def mark_won(self, request, queryset):
        queryset.update(status=ContactInquiry.STATUS_WON)

    @admin.action(description='Mark selected inquiries as lost')
    def mark_lost(self, request, queryset):
        queryset.update(status=ContactInquiry.STATUS_LOST)
