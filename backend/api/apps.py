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
            global_graph.add_connection(str(connection.user1.username), str(connection.user2.username))
        
        # print("graph:")
        # print(global_graph)
        global_graph.save_to_neo4j()
        import api.signals
    