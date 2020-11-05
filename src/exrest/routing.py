"""Роутинг для Channels."""

from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from exrest.apps.sockets.auth_middleware import TokenAuthMiddlewareStack
from exrest.apps.sockets.crew_consumer import CrewConsumer
from exrest.apps.sockets.logistician_consumer import LogisticianConsumer
from exrest.apps.sockets.notifications_consumer import NotificationConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': TokenAuthMiddlewareStack(
        URLRouter([
            url('ws/logistician/', LogisticianConsumer),
            url('ws/crew/', CrewConsumer),
            url('ws/notifications/', NotificationConsumer)
        ])
    )
})
