import sys
sys.path.append("src")


from model import logica_calculadora


def leer_datos_usuario():
    print("Este programa le permite calcular la cuota mensual a ahorrar")
    print("para alcanzar una meta de ahorro programado\n")

    meta = float(input("Meta de ahorro: "))
    tasa = float(input("Tasa de interés periódica: ")) / 100
    periodos = float(input("Número de periodos del plan de ahorro: "))
    abono_extra_txt = input(
        "Abono extra en la última cuota (Enter para omitir): "
    )

    abono_extra = (
        float(abono_extra_txt)
        if abono_extra_txt.strip() != ""
        else 0.0
    )

    return meta, tasa, periodos, abono_extra


def calcular_resultado(datos):
    meta, tasa, periodos, abono_extra = datos

    cuota = round(
        logica_calculadora.calcular_cuota(
            meta,
            tasa,
            periodos,
            abono_extra
        ),
        2
    )

    tabla = logica_calculadora.generar_tabla_acumulacion(
        meta,
        tasa,
        periodos,
        abono_extra
    )

    totales = logica_calculadora.calcular_totales(tabla)

    return cuota, tabla, totales


def imprimir_tabla(tabla):
    print("\nPeriodo\tSaldo Inicial\tCuota\t\tInterés\t\tAbono Extra\tSaldo Final")

    for fila in tabla:
        print(
            f"{fila['periodo']}\t"
            f"{round(fila['saldo_inicial'], 2)}\t"
            f"{round(fila['cuota'], 2)}\t"
            f"{round(fila['interes_ganado'], 2)}\t"
            f"{round(fila['abono_extra'], 2)}\t\t"
            f"{round(fila['saldo_final'], 2)}"
        )


def imprimir_totales(totales):
    print(f"\nTotal aportado: {round(totales['total_aportado'], 2)}")
    print(f"Total de interés generado: {round(totales['total_interes'], 2)}")
    print(f"Saldo final: {round(totales['saldo_final'], 2)}")


def main():
    try:
        datos = leer_datos_usuario()
    except ValueError as error:
        print("\nDato inválido: ingrese valores numéricos válidos.")
        print(str(error))
        return

    try:
        cuota, tabla, totales = calcular_resultado(datos)
    except (
        logica_calculadora.MetaInvalida,
        logica_calculadora.TasaInteresInvalida,
        logica_calculadora.PeriodosInvalidos,
        logica_calculadora.AbonoExtraInvalido,
    ) as error:
        print(f"\n{error}")
        return
    except Exception as error:
        print(f"\nNo se pudo calcular la cuota: {error}")
        return

    print(f"\nLa cuota mensual de ahorro requerida es de: {cuota}")

    imprimir_tabla(tabla)
    imprimir_totales(totales)


if __name__ == "__main__":
    main()