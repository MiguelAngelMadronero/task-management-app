import os
import django
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')  # Reemplaza 'tu_proyecto' por el nombre de tu proyecto Django
django.setup()

# Datos del nuevo superusuario
username = 'miguel1'
email = 'mams2208@outlook.com'
password = 'miguel@ngel2208.123'

# Verifica si el superusuario ya existe
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superusuario '{username}' creado con éxito.")
else:
    print(f"El superusuario '{username}' ya existe.")
