from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ContactInquiry,
    FAQItem,
    HeroBranding,
    HeroPanel,
    Insight,
    PageSection,
    Project,
    Service,
    SitePage,
    SiteSectionVisibility,
    SiteSetting,
    Testimonial,
)

admin.site.site_header = 'Creova Studio — Website Manager'
admin.site.site_title = 'Creova Studio Admin'
admin.site.index_title = 'Manage website content'


class PageSectionInline(admin.StackedInline):
    model = PageSection
    extra = 0
    fields = ('section_type', 'heading', 'body', 'image_url', 'link_text', 'link_url', 'data', 'published', 'sort_order')


@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published', 'sort_order', 'updated_at')
    list_filter = ('published',)
    search_fields = ('title', 'meta_title', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PageSectionInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'year', 'category', 'featured', 'published', 'sort_order')
    list_filter = ('published', 'featured', 'year', 'category')
    search_fields = ('title', 'client', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('sort_order', '-created_at')


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
    list_display = ('title', 'published', 'published_at', 'sort_order')
    list_filter = ('published',)
    search_fields = ('title', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('sort_order', '-published_at')


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
    list_display = ('name', 'email', 'company_brand', 'project_type', 'created_at', 'is_read')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'company_brand', 'project_type', 'message')
    readonly_fields = ('name', 'email', 'company_brand', 'project_type', 'budget_range', 'message', 'created_at')
    fieldsets = (
        ('Contact details', {'fields': ('name', 'email', 'company_brand')}),
        ('Project brief', {'fields': ('project_type', 'budget_range', 'message')}),
        ('Review', {'fields': ('created_at', 'is_read')}),
    )
