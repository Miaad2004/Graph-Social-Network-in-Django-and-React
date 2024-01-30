from django.apps import AppConfig
from .graph import Graph

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    global_graph = Graph()
    
    def ready(self):
        from .models import Connection
        
        global_graph = ApiConfig.global_graph
        all_connections = Connection.objects.all()

        for connection in all_connections:
            global_graph.add_connection(str(connection.user1.id), str(connection.user2.id))
        
        print("graph:")
        print(global_graph)
        import api.signals
    