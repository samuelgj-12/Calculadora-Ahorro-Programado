import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from model import logica_calculadora

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

COLOR_TITULO = (0.04, 0.32, 0.54, 1)
COLOR_DESTACADO = (0.04, 0.46, 0.28, 1)
COLOR_ERROR = (0.82, 0.12, 0.12, 1)
COLOR_ENCABEZADO = (0.28, 0.52, 0.74, 1)
COLOR_TEXTO = (0.13, 0.16, 0.19, 1)
BLANCO = (1, 1, 1, 1)

ENCABEZADOS_TABLA = [
    "Periodo",
    "Saldo inicial",
    "Cuota",
    "Interés",
    "Abono extra",
    "Saldo final",
]


class Etiqueta(Label):
    """Etiqueta que ajusta su texto al ancho disponible y lo centra verticalmente."""

    def __init__(self, texto, color=COLOR_TEXTO, tamano=14, negrita=False, centrada=False, **kwargs):
        super().__init__(**kwargs)
        self.text = texto
        self.color = color
        self.font_size = dp(tamano)
        self.bold = negrita
        self.halign = "center" if centrada else "left"
        self.valign = "middle"
        self.bind(size=self._ajustar_texto)

    def _ajustar_texto(self, *_):
        self.text_size = (self.width, self.height)


def _fila_campo(texto_campo, campo):
    fila = BoxLayout(
        orientation="horizontal",
        size_hint_y=None,
        height=dp(40),
        spacing=dp(8),
    )
    etiqueta = Etiqueta(texto_campo, tamano=14, centrada=True)
    etiqueta.size_hint_x = 0.55
    fila.add_widget(etiqueta)
    campo.size_hint_x = 0.45
    fila.add_widget(campo)
    return fila


def _campo_numerico(tipo_filtro):
    return TextInput(
        multiline=False,
        input_filter=tipo_filtro,
        font_size=dp(15),
        halign="right",
        size_hint_y=None,
        height=dp(40),
    )


class PantallaPrincipal(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(12), spacing=dp(8), **kwargs)
        self._construir_encabezado()
        self._construir_formulario()
        self._construir_resultados()
        self._construir_tabla()

    def _construir_encabezado(self):
        titulo = Etiqueta(
            "Calculadora de Ahorro Programado",
            color=COLOR_TITULO,
            tamano=22,
            negrita=True,
            centrada=True,
        )
        titulo.size_hint_y = None
        titulo.height = dp(44)
        self.add_widget(titulo)

        subtitulo = Etiqueta(
            "Calcule la cuota mensual necesaria para alcanzar su meta de ahorro.",
            tamano=13,
            centrada=True,
        )
        subtitulo.size_hint_y = None
        subtitulo.height = dp(24)
        self.add_widget(subtitulo)

    def _construir_formulario(self):
        formulario = GridLayout(cols=2, spacing=(dp(8), dp(8)), size_hint_y=None, height=dp(200))

        self.campo_meta = _campo_numerico("float")
        formulario.add_widget(_fila_campo("Meta de ahorro:", self.campo_meta))

        self.campo_tasa = _campo_numerico("float")
        formulario.add_widget(_fila_campo("Tasa de interés periódica (%):", self.campo_tasa))

        self.campo_periodos = _campo_numerico("int")
        formulario.add_widget(_fila_campo("Número de periodos (meses):", self.campo_periodos))

        self.campo_abono = _campo_numerico("float")
        formulario.add_widget(_fila_campo("Abono extra en la última cuota:", self.campo_abono))

        self.add_widget(formulario)

        self.etiqueta_error = Etiqueta("", color=COLOR_ERROR, tamano=13, centrada=True)
        self.etiqueta_error.size_hint_y = None
        self.etiqueta_error.height = dp(24)
        self.add_widget(self.etiqueta_error)

        botones = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(46), spacing=dp(10))
        boton_calcular = Button(text="Calcular", font_size=dp(16), bold=True)
        boton_calcular.bind(on_release=self._calcular)
        boton_limpiar = Button(text="Limpiar", font_size=dp(16))
        boton_limpiar.bind(on_release=self._limpiar)
        botones.add_widget(boton_calcular)
        botones.add_widget(boton_limpiar)
        self.add_widget(botones)

    def _construir_resultados(self):
        resumen = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(96),
            spacing=dp(2),
            padding=(dp(6), dp(4)),
        )

        self.etiqueta_cuota = Etiqueta(
            "",
            color=COLOR_DESTACADO,
            tamano=20,
            negrita=True,
            centrada=True,
        )
        self.etiqueta_cuota.size_hint_y = None
        self.etiqueta_cuota.height = dp(38)
        resumen.add_widget(self.etiqueta_cuota)

        self.etiqueta_totales = Etiqueta("", tamano=13, centrada=True)
        self.etiqueta_totales.size_hint_y = None
        self.etiqueta_totales.height = dp(30)
        resumen.add_widget(self.etiqueta_totales)

        self.add_widget(resumen)

    def _construir_tabla(self):
        contenedor_tabla = BoxLayout(orientation="vertical", size_hint=(1, 1), spacing=dp(2))

        fila_encabezado = GridLayout(cols=6, size_hint_y=None, height=dp(30))
        for texto in ENCABEZADOS_TABLA:
            etiqueta = Etiqueta(texto, color=BLANCO, tamano=12, negrita=True, centrada=True)
            etiqueta.background_color = COLOR_ENCABEZADO
            fila_encabezado.add_widget(etiqueta)
        contenedor_tabla.add_widget(fila_encabezado)

        self.scroll_tabla = ScrollView(size_hint=(1, 1), do_scroll_y=True, do_scroll_x=True)
        contenedor_tabla.add_widget(self.scroll_tabla)

        self.add_widget(contenedor_tabla)

    def _leer_campos(self):
        meta = float(self.campo_meta.text)
        tasa = float(self.campo_tasa.text) / 100.0
        periodos = float(self.campo_periodos.text)
        abono_texto = self.campo_abono.text.strip()
        abono = float(abono_texto) if abono_texto else 0.0
        return meta, tasa, periodos, abono

    def _limpiar_tabla(self):
        self.scroll_tabla.clear_widgets()

    def _mostrar_error(self, mensaje):
        self.etiqueta_error.text = mensaje
        self.etiqueta_cuota.text = ""
        self.etiqueta_totales.text = ""
        self._limpiar_tabla()

    def _calcular(self, _boton=None):
        self.etiqueta_error.text = ""

        try:
            meta, tasa, periodos, abono = self._leer_campos()
        except ValueError:
            self._mostrar_error("Complete todos los campos con valores numéricos válidos.")
            return

        try:
            cuota = logica_calculadora.calcular_cuota(meta, tasa, periodos, abono)
            tabla = logica_calculadora.generar_tabla_acumulacion(meta, tasa, periodos, abono)
            totales = logica_calculadora.calcular_totales(tabla)
        except (
            logica_calculadora.MetaInvalida,
            logica_calculadora.TasaInteresInvalida,
            logica_calculadora.PeriodosInvalidos,
            logica_calculadora.AbonoExtraInvalido,
        ) as error:
            self._mostrar_error(str(error))
            return
        except Exception as error:
            self._mostrar_error(f"No se pudo calcular la cuota: {error}")
            return

        self._mostrar_resultados(cuota, totales)
        self._mostrar_tabla(tabla)

    @staticmethod
    def _formatear_dinero(valor):
        return "{:,.2f}".format(valor)

    def _mostrar_resultados(self, cuota, totales):
        self.etiqueta_cuota.text = "Cuota mensual requerida: $" + self._formatear_dinero(cuota)
        self.etiqueta_totales.text = (
            "Total aportado: $"
            + self._formatear_dinero(totales["total_aportado"])
            + "    Total de interés generado: $"
            + self._formatear_dinero(totales["total_interes"])
            + "    Saldo final: $"
            + self._formatear_dinero(totales["saldo_final"])
        )

    def _mostrar_tabla(self, tabla):
        self._limpiar_tabla()

        filas = GridLayout(cols=6, spacing=(dp(2), dp(2)), size_hint_y=None)
        filas.bind(minimum_height=filas.setter("height"))

        for fila in tabla:
            filas.add_widget(Etiqueta(str(fila["periodo"]), tamano=11, centrada=True))
            filas.add_widget(Etiqueta(self._formatear_dinero(fila["saldo_inicial"]), tamano=11, centrada=True))
            filas.add_widget(Etiqueta(self._formatear_dinero(fila["cuota"]), tamano=11, centrada=True))
            filas.add_widget(Etiqueta(self._formatear_dinero(fila["interes_ganado"]), tamano=11, centrada=True))
            filas.add_widget(Etiqueta(self._formatear_dinero(fila["abono_extra"]), tamano=11, centrada=True))
            filas.add_widget(Etiqueta(self._formatear_dinero(fila["saldo_final"]), tamano=11, centrada=True))

        self.scroll_tabla.add_widget(filas)

    def _limpiar(self, _boton=None):
        self.campo_meta.text = ""
        self.campo_tasa.text = ""
        self.campo_periodos.text = ""
        self.campo_abono.text = ""
        self.etiqueta_error.text = ""
        self.etiqueta_cuota.text = ""
        self.etiqueta_totales.text = ""
        self._limpiar_tabla()


class CalculadoraAhorroApp(App):

    def build(self):
        Window.size = (680, 780)
        self.title = "Calculadora de Ahorro Programado"
        return PantallaPrincipal()


def main():
    CalculadoraAhorroApp().run()


if __name__ == "__main__":
    main()