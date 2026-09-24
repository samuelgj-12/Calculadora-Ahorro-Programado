"""Interfaz gráfica (Kivy) de la Calculadora de Ahorro Programado.

Esta vista NO contiene lógica de negocio propia: reutiliza exactamente el
mismo módulo model.logica_calculadora que usa la interfaz de consola
(src/view/console/main.py), a través de la función compartida
calcular_resultado_completo(). Así se garantiza que ambas interfaces
siempre calculen lo mismo, y que las pruebas unitarias (que validan el
módulo model) sigan siendo la fuente de verdad de la lógica.
"""

import os
import sys

# Se calcula la ruta a "src" a partir de la ubicación real de este archivo
# (y no del directorio actual de trabajo), para que la aplicación funcione
# sin importar desde qué carpeta se ejecute o en qué computador se instale.
_SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_SRC_DIR = os.path.join(_SRC_DIR, "src")
if _SRC_DIR not in sys.path:
    sys.path.append(_SRC_DIR)

from model import logica_calculadora  # noqa: E402

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import platform

# En Android la ventana ocupa toda la pantalla del dispositivo, por lo que
# no se fuerza un tamano. En el escritorio (Windows/Linux/macOS) se usa una
# ventana con tamano fijo y el teclado movil no interfiere con los campos.
_ES_MOVIL = platform in ("android",)
if not _ES_MOVIL:
    Window.size = (760, 640)
    Window.minimum_width, Window.minimum_height = (620, 480)
else:
    Window.softinput_mode = "below_target"

Window.clearcolor = (0.96, 0.96, 0.97, 1)  # fondo claro para buen contraste con texto oscuro

COLOR_ERROR = (0.85, 0.2, 0.2, 1)
COLOR_OK = (0.15, 0.55, 0.2, 1)
COLOR_TEXTO = (0.1, 0.1, 0.1, 1)
COLOR_ENCABEZADO = (0.92, 0.92, 0.95, 1)


def formatear_numero(valor: float) -> str:
    """Formatea un número en estilo latinoamericano: punto para miles,
    coma para decimales (ej: 1.234.567,89). Si el valor no se puede
    formatear por alguna razón inesperada, devuelve su representación
    simple para que la aplicación no se rompa."""

    try:
        texto = f"{valor:,.2f}"
        return texto.translate(str.maketrans(",.", ".,"))
    except (ValueError, TypeError):
        return str(valor)


def parsear_numero(texto: str, permitir_vacio: bool = False) -> float:
    """Convierte texto ingresado por el usuario a float de forma tolerante:
    acepta coma o punto como separador decimal y espacios sobrantes.
    Lanza ValueError con un mensaje amigable si el texto no es un número."""

    texto = (texto or "").strip()

    if texto == "":
        if permitir_vacio:
            return 0.0
        raise ValueError("Este campo es obligatorio.")

    texto_normalizado = texto.replace(" ", "").replace(",", ".")

    try:
        return float(texto_normalizado)
    except ValueError:
        raise ValueError(f"'{texto}' no es un número válido.")


class CampoEntrada(BoxLayout):
    """Fila reutilizable: etiqueta + campo de texto numérico."""

    def __init__(self, etiqueta: str, placeholder: str = "", **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=dp(44), spacing=dp(10), **kwargs)

        self.label = Label(
            text=etiqueta,
            size_hint_x=0.45,
            halign="right",
            valign="middle",
            color=COLOR_TEXTO,
        )
        self.label.bind(size=self._actualizar_text_size)

        self.input = TextInput(
            hint_text=placeholder,
            multiline=False,
            input_filter=None,  # se valida manualmente para aceptar coma o punto
            size_hint_x=0.55,
            padding=[dp(10), dp(10), dp(10), dp(10)],
        )

        self.add_widget(self.label)
        self.add_widget(self.input)

    def _actualizar_text_size(self, instance, value):
        instance.text_size = (instance.width, instance.height)

    @property
    def texto(self) -> str:
        return self.input.text

    def limpiar(self):
        self.input.text = ""


class FilaTabla(GridLayout):
    """Una fila de la tabla de acumulación (o de encabezado)."""

    def __init__(self, valores, es_encabezado=False, **kwargs):
        super().__init__(
            cols=6,
            size_hint_y=None,
            height=dp(30),
            **kwargs,
        )

        color_fondo = COLOR_ENCABEZADO if es_encabezado else (1, 1, 1, 1)

        with self.canvas.before:
            Color(*color_fondo)
            self._rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._actualizar_fondo, size=self._actualizar_fondo)

        for valor in valores:
            lbl = Label(
                text=str(valor),
                color=COLOR_TEXTO,
                bold=es_encabezado,
                font_size=dp(13),
            )
            self.add_widget(lbl)

    def _actualizar_fondo(self, instance, value):
        self._rect.pos = instance.pos
        self._rect.size = instance.size


class CalculadoraAhorroGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(16), spacing=dp(10), **kwargs)

        titulo = Label(
            text="Calculadora de Ahorro Programado",
            size_hint_y=None,
            height=dp(40),
            font_size=dp(20),
            bold=True,
            color=COLOR_TEXTO,
        )
        self.add_widget(titulo)

        # --- Formulario ---
        self.campo_meta = CampoEntrada("Meta de ahorro:", "Ej: 10000000")
        self.campo_tasa = CampoEntrada("Tasa de interés periódica (%):", "Ej: 1.5")
        self.campo_periodos = CampoEntrada("Número de periodos:", "Ej: 12")
        self.campo_abono = CampoEntrada("Abono extra última cuota (opcional):", "Ej: 0")

        self.add_widget(self.campo_meta)
        self.add_widget(self.campo_tasa)
        self.add_widget(self.campo_periodos)
        self.add_widget(self.campo_abono)

        # --- Botones ---
        fila_botones = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(10))
        boton_calcular = Button(text="Calcular", bold=True)
        boton_calcular.bind(on_release=self.calcular)
        boton_limpiar = Button(text="Limpiar")
        boton_limpiar.bind(on_release=self.limpiar)
        fila_botones.add_widget(boton_calcular)
        fila_botones.add_widget(boton_limpiar)
        self.add_widget(fila_botones)

        # --- Mensaje de estado / error ---
        self.label_estado = Label(
            text="",
            size_hint_y=None,
            height=dp(30),
            color=COLOR_ERROR,
        )
        self.add_widget(self.label_estado)

        # --- Resultado principal ---
        self.label_cuota = Label(
            text="",
            size_hint_y=None,
            height=dp(34),
            font_size=dp(17),
            bold=True,
            color=COLOR_OK,
        )
        self.add_widget(self.label_cuota)

        # --- Tabla de acumulación (con scroll, soporta cientos de filas) ---
        self.scroll = ScrollView(size_hint=(1, 1))
        self.tabla_contenedor = GridLayout(cols=1, size_hint_y=None, spacing=dp(1))
        self.tabla_contenedor.bind(minimum_height=self.tabla_contenedor.setter("height"))
        self.scroll.add_widget(self.tabla_contenedor)
        self.add_widget(self.scroll)

        # --- Totales ---
        self.label_totales = Label(
            text="",
            size_hint_y=None,
            height=dp(70),
            color=COLOR_TEXTO,
            halign="left",
            valign="top",
        )
        self.label_totales.bind(size=self._actualizar_text_size_totales)
        self.add_widget(self.label_totales)

    def _actualizar_text_size_totales(self, instance, value):
        instance.text_size = (instance.width, None)

    def limpiar(self, *_args):
        self.campo_meta.limpiar()
        self.campo_tasa.limpiar()
        self.campo_periodos.limpiar()
        self.campo_abono.limpiar()
        self.label_estado.text = ""
        self.label_cuota.text = ""
        self.label_totales.text = ""
        self.tabla_contenedor.clear_widgets()

    def calcular(self, *_args):
        self.label_estado.text = ""
        self.label_cuota.text = ""
        self.label_totales.text = ""
        self.tabla_contenedor.clear_widgets()

        try:
            meta = parsear_numero(self.campo_meta.texto)
            tasa_pct = parsear_numero(self.campo_tasa.texto)
            periodos = parsear_numero(self.campo_periodos.texto)
            abono_extra = parsear_numero(self.campo_abono.texto, permitir_vacio=True)

            # Se prefiere la funcion envoltorio cuando el modelo la tiene;
            # si no (versiones del modelo sin ella), se componen las tres
            # funciones individuales con el mismo resultado.
            if hasattr(logica_calculadora, "calcular_resultado_completo"):
                resultado = logica_calculadora.calcular_resultado_completo(
                    meta,
                    tasa_pct / 100,
                    periodos,
                    abono_extra,
                )
            else:
                cuota = logica_calculadora.calcular_cuota(
                    meta, tasa_pct / 100, periodos, abono_extra
                )
                tabla = logica_calculadora.generar_tabla_acumulacion(
                    meta, tasa_pct / 100, periodos, abono_extra
                )
                resultado = {
                    "cuota": cuota,
                    "tabla": tabla,
                    "totales": logica_calculadora.calcular_totales(tabla),
                }

        except ValueError as error:
            # Errores de formato de entrada del usuario (texto no numérico, campo vacío)
            self._mostrar_error(str(error))
            return
        except (
            logica_calculadora.MetaInvalida,
            logica_calculadora.TasaInteresInvalida,
            logica_calculadora.PeriodosInvalidos,
            logica_calculadora.AbonoExtraInvalido,
        ) as error:
            # Errores de reglas de negocio, validados en el módulo compartido
            self._mostrar_error(str(error))
            return
        except Exception as error:
            # Última barrera de resiliencia: nunca debe cerrarse la app de forma abrupta
            self._mostrar_error(f"Ocurrió un error inesperado: {error}")
            return

        self._mostrar_resultado(resultado)

    def _mostrar_error(self, mensaje: str):
        self.label_estado.color = COLOR_ERROR
        self.label_estado.text = mensaje

    def _mostrar_resultado(self, resultado: dict):
        cuota = resultado["cuota"]
        tabla = resultado["tabla"]
        totales = resultado["totales"]

        self.label_estado.color = COLOR_OK
        self.label_estado.text = "Cálculo realizado con éxito."
        self.label_cuota.text = f"Cuota periódica requerida: {formatear_numero(cuota)}"

        encabezados = ["Periodo", "Saldo inicial", "Cuota", "Interés", "Abono extra", "Saldo final"]
        self.tabla_contenedor.add_widget(FilaTabla(encabezados, es_encabezado=True))

        for fila in tabla:
            valores = [
                fila["periodo"],
                formatear_numero(fila["saldo_inicial"]),
                formatear_numero(fila["cuota"]),
                formatear_numero(fila["interes_ganado"]),
                formatear_numero(fila["abono_extra"]),
                formatear_numero(fila["saldo_final"]),
            ]
            self.tabla_contenedor.add_widget(FilaTabla(valores))

        self.label_totales.text = (
            f"Total aportado: {formatear_numero(totales['total_aportado'])}\n"
            f"Total de interés generado: {formatear_numero(totales['total_interes'])}\n"
            f"Saldo final: {formatear_numero(totales['saldo_final'])}"
        )


class CalculadoraAhorroApp(App):
    title = "Calculadora de Ahorro Programado"

    def build(self):
        return CalculadoraAhorroGUI()


def main():
    CalculadoraAhorroApp().run()


if __name__ == "__main__":
    main()
