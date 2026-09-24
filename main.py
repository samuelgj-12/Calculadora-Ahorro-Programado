"""Punto de entrada para Android (exigido por Buildozer en la raiz).

Buildozer/Python-for-Android requieren un archivo main.py en el directorio
raiz de la aplicacion (la opcion source.main no es compatible con p4a 2024.1.21).
Este archivo solo reutiliza el punto de entrada real definido en src/main.py.
"""

from src.main import main


if __name__ == "__main__":
    main()