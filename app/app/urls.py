from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


from user.views import goto
from events.views import FeedbackView


urlpatterns = [
    path('', goto, name='goto'),
    path('ad/', admin.site.urls),
    path('accounts/', include('user.urls')),
    path('app/', include('events.urls')),

    path('info/about/', TemplateView.as_view(template_name='events/info/about.html'), name='about'),
    path('info/contact/', TemplateView.as_view(template_name='events/info/contact.html'), name='contact'),
    path('info/leave-feedback/', FeedbackView.as_view(), name='feedback'),
]



