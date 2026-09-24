"""Punto de entrada para el empaquetado en Android.

Buildozer (Android) ejecuta este archivo como punto de entrada de la
aplicacion. Reutiliza la interfaz grafica Kivy que se ve en el escritorio
(src/view/gui/gui_main.py), de modo que el celular usa la misma interfaz
que el codigo local sin cambiar nada de la app original.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from view.gui.gui_main import CalculadoraAhorroApp  # noqa: E402


def main():
    CalculadoraAhorroApp().run()


if __name__ == "__main__":
    main()