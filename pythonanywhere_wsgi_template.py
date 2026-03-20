import os
import sys

path = "/home/yourusername/your-repo/Lecture 2/Practical/Code/Practical2_code_pythonanywhere"
if path not in sys.path:
    sys.path.append(path)

os.environ["DJANGO_SETTINGS_MODULE"] = "shopsite.settings"

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
