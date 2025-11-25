import os
import django
import sys

def setup_django_environment():
    
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 
    sys.path.append(project_path)
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KVBerlinParser_project.settings")

    django.setup()


setup_django_environment()