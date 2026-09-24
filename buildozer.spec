[app]

# (str) Nombre que se muestra bajo el icono en el dispositivo Android
title = Calculadora Ahorro

# (str) Nombre interno del paquete (se usa en el archivo .apk)
package.name = calculadoraahorro

# (str) Dominio del paquete (empresa/organizacion, se usa como identificador inverso)
package.domain = org.calculadora

# (str) Directorio raiz del codigo fuente que se empaqueta
source.dir = .

# (list) Extensiones de archivos que se incluyen en el APK
source.include_exts = py,png,jpg,jpeg,kv,atlas

# (list) Carpetas excluidas del APK.
# No se modifica el codigo existente de la app: solo se agrego el empaquetado.
source.exclude_dirs = test, .vscode, .git, venv, .venv, build, dist
source.exclude_patterns = __pycache__/**

# El punto de entrada es main.py en la raiz (ver main.py).
# La opcion source.main no es compatible con Python-for-Android 2024.1.21,
# por eso se deja sin definir.

# (str) Version de la aplicacion
version = 1.0.0

# (list) Recetas de Python que se compilan dentro del APK.
# La version de Python se fija para que Python-for-Android no elija
# una version nueva (p.ej. 3.14) que rompa el build de forma impredecible.
requirements = python3==3.11.9,kivy

# (str) Version (etiqueta git) de Python-for-Android que usa Buildozer.
# Debe coincidir con la que se instala en el workflow (python-for-android 2024.1.21)
# y con la version de Python fijada arriba, para que python3 y hostpython3
# no queden desincronizados (3.11.9 != 3.14.2).
p4a.branch = v2024.01.21

# (str) Orientacion de la aplicacion: portrait, landscape o sensor
orientation = portrait

# (bool) Si es 1 la app ocupa toda la pantalla (sin barra de sistema)
fullscreen = 0

# ---------------------------------- Android ---------------------------------
# (list) Arquitecturas del APK
android.archs = arm64-v8a

# (bool) Acepta automaticamente las licencias del SDK de Android
# (necesario en CI / GitHub Actions, donde no hay nadie para responder "y")
android.accept_sdk_license = True

# (int) Nivel de API de Android con el que se compila
android.api = 33

# (int) Nivel minimo de Android soportado
android.min_sdk_version = 21

# (list) Permisos de Android que pide la app (ninguno para esta calculadora)
android.permissions =

# (bool) Permite que el sistema respalde los datos de la app
android.allow_backup = True

# (bool) Mantiene la sesion activa evitando que se detenga en segundo plano
android.keep_alive = True

[buildozer]

# (int) Nivel de detalle de los registros (0 = NADA, 1 = ERROR, 2 = WARNING, 3 = INFO)
log_level = 2

# (int) Numero maximo de intentos al descargar dependencias
max_retries = 3