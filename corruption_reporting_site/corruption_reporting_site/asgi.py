"""
ASGI config for corruption_reporting_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# corruption_reporting_site/asgi.py
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from reports.routing import websocket_urlpatterns  # Import the `reports` app routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'corruption_reporting_site.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Use your `reports` app WebSocket routes
        )
    ),
})
