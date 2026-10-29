from django.urls import path

from . import views

urlpatterns = [
    path('pages/', views.page_list, name='page-list'),
    path('pages/<slug:slug>/', views.page_detail, name='page-detail'),
    path('projects/', views.project_list, name='project-list'),
    path('projects/<slug:slug>/', views.project_detail, name='project-detail'),
    path('insights/', views.insight_list, name='insight-list'),
    path('insights/<slug:slug>/', views.insight_detail, name='insight-detail'),
    path('services/', views.service_list, name='service-list'),
    path('sections/', views.section_visibility_list, name='section-visibility-list'),
    path('branding/', views.hero_branding, name='hero-branding'),
    path('hero-panels/', views.hero_panel_list, name='hero-panel-list'),
    path('settings/', views.site_settings, name='site-settings'),
    path('testimonials/', views.testimonial_list, name='testimonial-list'),
    path('faqs/', views.faq_list, name='faq-list'),
    path('contact/', views.contact_inquiry, name='contact-inquiry'),
]
