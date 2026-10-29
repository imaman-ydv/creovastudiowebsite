import json

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from django.shortcuts import get_object_or_404

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
from .notifications import notify_contact_inquiry


def _section_data(section: PageSection):
    return {
        'type': section.section_type,
        'heading': section.heading,
        'body': section.body,
        'key': section.content_key,
        'image_url': section.image.url if section.image else _content_image_url(None, section.image_url),
        'image_alt': section.image_alt,
        'link_text': section.link_text,
        'link_url': section.link_url,
        'data': section.data,
    }


def _page_data(page: SitePage):
    return {
        'title': page.title,
        'slug': page.slug,
        'meta_title': page.meta_title,
        'meta_description': page.meta_description,
        'sections': [_section_data(section) for section in page.sections.filter(published=True)],
    }


@require_GET
def page_list(request):
    return JsonResponse({'results': [_page_data(page) for page in SitePage.objects.filter(published=True)]})


@require_GET
def page_detail(request, slug):
    page = get_object_or_404(SitePage.objects.prefetch_related('sections'), slug=slug, published=True)
    return JsonResponse(_page_data(page))


@require_GET
def project_list(request):
    projects = Project.objects.filter(published=True)
    return JsonResponse({'results': [
        {
            'id': project.pk,
            'title': project.title,
            'slug': project.slug,
            'client': project.client,
            'year': project.year,
            'category': project.category,
            'summary': project.summary,
            'cover_image_url': _content_image_url(project.cover_image, project.cover_image_url),
            'image_alt': project.image_alt,
            'website_url': project.website_url,
            'featured': project.featured,
        }
        for project in projects
    ]})


@require_GET
def project_detail(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related('images'), slug=slug, published=True)
    return JsonResponse({
        'id': project.pk,
        'title': project.title,
        'slug': project.slug,
        'client': project.client,
        'year': project.year,
        'category': project.category,
        'summary': project.summary,
        'body': project.body,
        'cover_image_url': _content_image_url(project.cover_image, project.cover_image_url),
        'image_alt': project.image_alt,
        'website_url': project.website_url,
        'images': [
            {'image_url': image.image.url, 'image_alt': image.alt_text, 'caption': image.caption}
            for image in project.images.all()
        ],
    })


@require_GET
def insight_list(request):
    insights = Insight.objects.filter(published=True)
    return JsonResponse({'results': [
        {
            'id': insight.pk,
            'title': insight.title,
            'slug': insight.slug,
            'excerpt': insight.excerpt,
            'cover_image_url': _content_image_url(insight.cover_image, insight.cover_image_url),
            'image_alt': insight.image_alt,
            'body': insight.body,
            'published_at': insight.published_at.isoformat() if insight.published_at else None,
        }
        for insight in insights
    ]})


@require_GET
def insight_detail(request, slug):
    insight = get_object_or_404(Insight.objects.prefetch_related('images'), slug=slug, published=True)
    return JsonResponse({
        'id': insight.pk,
        'title': insight.title,
        'slug': insight.slug,
        'excerpt': insight.excerpt,
        'cover_image_url': _content_image_url(insight.cover_image, insight.cover_image_url),
        'image_alt': insight.image_alt,
        'body': insight.body,
        'published_at': insight.published_at.isoformat() if insight.published_at else None,
        'images': [
            {'image_url': image.image.url, 'image_alt': image.alt_text, 'caption': image.caption}
            for image in insight.images.all()
        ],
    })


def _content_image_url(upload, fallback):
    if upload:
        return upload.url
    fallback = fallback.strip()
    if fallback.startswith(('https://', 'http://', '/')):
        return fallback
    return f'/{fallback.removeprefix("./")}' if fallback else ''


@require_GET
def service_list(request):
    services = Service.objects.filter(published=True)
    return JsonResponse({'results': [
        {
            'title': service.title,
            'slug': service.slug,
            'short_heading': service.short_heading,
            'description': service.description,
            'details': service.details,
            'read_more_content': service.read_more_content,
            'image_url': _service_image_url(service),
            'image_alt': service.image_alt,
            'link_text': service.link_text,
            'link_url': service.link_url,
        }
        for service in services
    ]})


def _service_image_url(service):
    if service.card_image:
        return service.card_image.url
    image_url = service.image_url.strip()
    if not image_url:
        return ''
    if image_url.startswith(('https://', 'http://')):
        return image_url
    if image_url.startswith('./'):
        image_url = image_url[2:]
    if not image_url.startswith('/'):
        image_url = f'/{image_url}'
    return image_url


@require_GET
def section_visibility_list(request):
    return JsonResponse({'results': [
        {
            'key': section.key,
            'label': section.label,
            'visible': section.visible,
        }
        for section in SiteSectionVisibility.objects.all()
    ]})


@require_GET
def hero_branding(request):
    branding = HeroBranding.objects.first()
    return JsonResponse({
        'logo_url': branding.logo_image.url if branding and branding.logo_image else '/images/Logo.avif',
        'image_alt': branding.image_alt if branding else "CreovaStudio's Logo",
        'size_percent': branding.size_percent if branding else 86,
    })


@require_GET
def hero_panel_list(request):
    branding = HeroBranding.objects.first()
    panels = HeroPanel.objects.select_related('branding').all()
    if branding:
        panels = panels.filter(branding=branding)
    return JsonResponse({'results': [
        {
            'slot': panel.slot,
            'visible': panel.visible,
            'image_url': panel.team_photo.url if panel.team_photo else '',
            'image_alt': panel.image_alt,
        }
        for panel in panels
    ]})


@require_GET
def site_settings(request):
    return JsonResponse({item.key: item.value for item in SiteSetting.objects.all()})


@require_GET
def testimonial_list(request):
    testimonials = Testimonial.objects.filter(published=True)
    return JsonResponse({'results': [
        {
            'name': item.name,
            'role': item.role,
            'company': item.company,
            'quote': item.quote,
            'image_url': item.image_url,
        }
        for item in testimonials
    ]})


@require_GET
def faq_list(request):
    items = FAQItem.objects.filter(published=True)
    return JsonResponse({'results': [
        {'question': item.question, 'answer': item.answer}
        for item in items
    ]})


@csrf_exempt
@require_POST
def contact_inquiry(request):
    if request.content_type != 'application/json':
        return JsonResponse({'error': 'Content-Type must be application/json.'}, status=415)
    if len(request.body) > 12_000:
        return JsonResponse({'error': 'Request body is too large.'}, status=413)
    try:
        data = json.loads(request.body or b'{}')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Request body must be valid JSON.'}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({'error': 'Request body must be a JSON object.'}, status=400)
    # Quietly accept automated honeypot submissions without storing them.
    if str(data.get('website', '')).strip():
        return JsonResponse({'ok': True, 'id': None}, status=201)

    name = str(data.get('name', '')).strip()
    email = str(data.get('email', '')).strip()
    message = str(data.get('details', data.get('message', ''))).strip()
    company_brand = str(data.get('company_brand', '')).strip()
    project_type = str(data.get('project_type', '')).strip()
    budget_range = str(data.get('budget_range', '')).strip()
    if not name or not email or not message:
        return JsonResponse({'error': 'Name, email, and project details are required.'}, status=400)
    if len(name) > 120 or len(email) > 254 or len(message) > 5000 or len(company_brand) > 160 or len(project_type) > 80 or len(budget_range) > 80:
        return JsonResponse({'error': 'One or more fields are too long.'}, status=400)
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'error': 'Enter a valid email address.'}, status=400)

    inquiry = ContactInquiry.objects.create(
        name=name,
        email=email,
        company_brand=company_brand,
        project_type=project_type,
        budget_range=budget_range,
        message=message,
    )
    inquiry.notification_sent = notify_contact_inquiry(inquiry)
    inquiry.save(update_fields=['notification_sent'])
    return JsonResponse({'ok': True, 'id': inquiry.pk}, status=201)
