from django.db.models.signals import post_save, post_delete, post_migrate
from django.dispatch import receiver
from .models import Connection
from .apps import ApiConfig
from django.apps import AppConfig
from .graph import Graph

@receiver(post_save, sender=Connection)
def update_global_graph_on_connection_create(sender, instance, created, **kwargs):
    if created:
        global_graph = ApiConfig.global_graph
        global_graph.add_connection(instance.user1.id, instance.user2.id)

@receiver(post_delete, sender=Connection)
def update_global_graph_on_connection_delete(sender, instance, **kwargs):
    global_graph = ApiConfig.global_graph
    global_graph.remove_connection(instance.user1.id, instance.user2.id)

@receiver(post_migrate, sender=ApiConfig)
def build_global_graph(sender, **kwargs):
    from .models import Connection
    global_graph = ApiConfig.global_graph
    global_graph = Graph()
    all_connections = Connection.objects.all()

    for connection in all_connections:
        global_graph.add_connection(connection.user1.username, connection.user2.username)