META_MINIMA = 0
TASA_INTERES_MINIMA = 0
MINIMO_PERIODOS = 0
ABONO_EXTRA_MINIMO = 0


class MetaInvalida(Exception):
    """Excepcion que se dispara cuando la meta es menor o igual que cero."""

    def __init__(self):
        super().__init__("La meta de ahorro debe ser mayor que cero")


class TasaInteresInvalida(Exception):
    """Excepcion que se dispara cuando la tasa de interes es menor o igual a cero."""

    def __init__(self):
        super().__init__("La tasa de interés debe ser mayor que cero")


class PeriodosInvalidos(Exception):
    """Excepcion que se dispara cuando los periodos es menor o igual a cero."""

    def __init__(self):
        super().__init__("El número de periodos debe ser un entero positivo")


class AbonoExtraInvalido(Exception):
    """Excepcion que se dispara cuando el abono extra es menor a cero."""

    def __init__(self):
        super().__init__("El abono extra debe ser menor que la meta de ahorro")


class CalculadoraAhorro:
    """Calcula la cuota periódica constante necesaria para alcanzar una meta
    de ahorro programada, dada una tasa de interés y un número de periodos,
    con un abono extra opcional en el último periodo."""

    def __init__(self, meta: float, tasa_interes: float, periodos: float, abono_extra: float = 0):
        self.meta: float = meta
        self.tasa_interes: float = tasa_interes
        self.periodos: float = periodos
        self.abono_extra: float = abono_extra

    def verificar_meta(self):
        if self.meta <= META_MINIMA:
            raise MetaInvalida()

    def verificar_tasa_interes(self):
        if self.tasa_interes <= TASA_INTERES_MINIMA:
            raise TasaInteresInvalida()

    def verificar_periodos(self):
        if self.periodos <= MINIMO_PERIODOS or self.periodos != int(self.periodos):
            raise PeriodosInvalidos()

    def verificar_abono_extra(self):
        if self.abono_extra < ABONO_EXTRA_MINIMO or self.abono_extra >= self.meta:
            raise AbonoExtraInvalido()

    def calcular_cuota(self) -> float:
        self.verificar_meta()
        self.verificar_tasa_interes()
        self.verificar_periodos()
        self.verificar_abono_extra()
        periodos = int(self.periodos)
        return (self.meta - self.abono_extra) * self.tasa_interes / ((1 + self.tasa_interes) ** periodos - 1)


def calcular_cuota(meta: float, tasa_interes: float, periodos: float, abono_extra: float = 0) -> float:
    """Función compartida por la consola y la GUI (Kivy). Delega en CalculadoraAhorro.

    Permite calcular la cuota sin construir la clase directamente y mantiene
    una única fuente de verdad para la lógica de cálculo.
    """
    return CalculadoraAhorro(meta, tasa_interes, periodos, abono_extra).calcular_cuota()


def generar_tabla_acumulacion(meta: float, tasa_interes: float, periodos: float, abono_extra: float = 0) -> list:
    """Genera la tabla de acumulación periodo a periodo.

    El abono extra solo se suma en el último periodo.
    """
    cuota = CalculadoraAhorro(meta, tasa_interes, periodos, abono_extra).calcular_cuota()
    periodos = int(periodos)

    tabla = []
    saldo_inicial = 0.0
    for periodo in range(1, periodos + 1):
        interes = saldo_inicial * tasa_interes
        abono_extra_periodo = abono_extra if periodo == periodos else 0.0
        saldo_final = saldo_inicial + cuota + interes + abono_extra_periodo

        tabla.append({
            "periodo": periodo,
            "saldo_inicial": saldo_inicial,
            "cuota": cuota,
            "interes_ganado": interes,
            "abono_extra": abono_extra_periodo,
            "saldo_final": saldo_final,
        })

        saldo_inicial = saldo_final

    return tabla


def calcular_totales(tabla: list) -> dict:
    total_cuotas = sum(fila["cuota"] for fila in tabla)
    total_interes = sum(fila["interes_ganado"] for fila in tabla)
    total_abono_extra = sum(fila["abono_extra"] for fila in tabla)
    saldo_final = tabla[-1]["saldo_final"] if tabla else 0.0

    return {
        "total_cuotas": total_cuotas,
        "total_interes": total_interes,
        "total_abono_extra": total_abono_extra,
        "total_aportado": total_cuotas + total_abono_extra,
        "saldo_final": saldo_final,
    }