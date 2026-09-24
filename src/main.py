"""Punto de entrada para el empaquetado en Android.

Buildozer (Android) ejecuta este archivo como punto de entrada de la
aplicacion. Reutiliza la interfaz grafica Kivy existente del proyecto
(src/view/gui/main.py), de modo que el celular usa la misma interfaz
que el escritorio sin cambiar el codigo de la app.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from view.gui.main import CalculadoraAhorroApp  # noqa: E402


def main():
    CalculadoraAhorroApp().run()


if __name__ == "__main__":
    main()