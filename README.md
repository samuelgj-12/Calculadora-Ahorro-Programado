# Calculadora de Ahorro Programado

Aplicación que calcula el valor de la cuota mensual constante que debe depositar una
persona en una entidad financiera para alcanzar una meta de ahorro al final de un
plazo pactado, dada una tasa de interés fija. Permite además incluir un abono extra
en la última cuota.

1. # Entradas

M	Meta de ahorro (valor futuro deseado)	M > 0
i	Tasa de interés periódica (mensual, en decimal)	i > 0
n	Número de periodos (meses) del plan	entero > 0
AE	Abono extra en la última cuota (opcional, por defecto 0)	AE ≥ 0 y AE < M

Si la tasa se entrega en forma nominal anual (j) o efectiva anual (EA), debe
convertirse a periódica mensual antes de ingresarla:

Nominal: i = j / 12
Efectiva anual: i = (1 + EA)^(1/12) - 1
2. # Proceso

Validación de entradas (en este orden):

M <= 0 → Error: La meta de ahorro (M) debe ser mayor que cero
i <= 0 → Error: La tasa de interés (i) debe ser mayor que cero
n no entero o n <= 0 → Error: El número de periodos (n) debe ser un entero positivo
AE >= M (o AE < 0) → Error: El abono extra (AE) debe ser menor que la meta de ahorro (M)

Cálculo de la cuota mensual (A):

A = (M - AE) * i / [ (1+i)^n - 1 ]

Cálculo de la tabla de acumulación, periodo a periodo (k = 1 … n):

Interes_k = Saldo_(k-1) * i

Saldo_k = Saldo_(k-1) * (1+i) + A                   para k = 1 … n-1
Saldo_n = Saldo_(n-1) * (1+i) + A + AE              (último periodo, incluye el abono extra)

Cálculo de totales, sumando toda la tabla:

Total cuotas       = Σ A
Total interés       = Σ Interes_k
Total abono extra   = AE
Total aportado      = Total cuotas + Total abono extra
Saldo final          = Saldo_n   (debe ser ≈ M)
3. # Salidas
Cuota mensual de ahorro requerida (A), o el mensaje de error correspondiente.

Totales:
cuota mensual
Total aportado
Total de interés ganados

Casos de prueba

El proyecto incluye 10 casos de prueba en Excel, para las entradas y salidas esperadas del código:

3 normales: cálculo estándar de la cuota, con y sin abono extra.
3 excepcionales: plazo de un solo periodo, abono extra casi igual a la meta,
plazo muy largo (360 meses). Son válidos y no deben lanzar error.
4 de error: meta inválida, tasa inválida, número de periodos inválido, abono
extra igual o mayor a la meta.

4. # Que se hace en cada carpeta?

# .vscode/ 
Esta carpeta contiene configuraciones específicas para Visual Studio Code.

settings.json: contiene configuraciones del entorno de desarrollo utilizadas por Visual Studio Code.
No contiene la lógica de la aplicación.
Es una carpeta útil para facilitar que diferentes desarrolladores trabajen con una configuración similar del editor.

# src/

Es la carpeta principal que contiene el código fuente de la aplicación.

Dentro de src se separan las responsabilidades del programa en diferentes módulos:

model/: contiene la lógica de negocio y los cálculos financieros.
view/console/: contiene la interfaz de usuario por consola.
view/gui/: contiene la interfaz de usuario gráfica (Kivy).
Esta separación permite modificar la lógica de cálculo sin tener que modificar directamente la forma en que el usuario interactúa con la aplicación. La consola y la interfaz gráfica comparten la misma lógica (model).

# src/model/

Esta carpeta contiene la lógica principal de la calculadora.

logica_calculadora.py
Es el módulo encargado de realizar los cálculos del ahorro programado.

Contiene la clase CalculadoraAhorro, que recibe:

meta: valor que se desea alcanzar al finalizar el plan de ahorro.
tasa_interes: tasa de interés periódica expresada en decimal.
periodos: número de meses o períodos del plan.
abono_extra: valor opcional que se agrega en la última cuota.
La función calcular_cuota() valida los datos recibidos y calcula la cuota periódica necesaria para alcanzar la meta. También existe la función calcular_cuota() a nivel de módulo, que delega en la clase CalculadoraAhorro y es usada tanto por la consola como por la interfaz gráfica.

La fórmula utilizada es:

A = (M - AE) * i / ((1 + i)^n - 1)

Donde:

A = cuota periódica de ahorro.
M = meta de ahorro.
AE = abono extra realizado en el último período.
i = tasa de interés periódica.
n = número de períodos.
El módulo también contiene:

generar_tabla_acumulacion(): genera el comportamiento del ahorro período por período.
calcular_totales(): calcula los totales de cuotas, intereses, abonos adicionales, total aportado y saldo final.
La lógica también contempla validaciones para evitar valores inválidos, como una meta menor o igual a cero, una tasa no positiva, un número de períodos no entero o un abono extra mayor o igual a la meta.

# src/view/console/

Esta carpeta contiene la interfaz de usuario de la aplicación mediante consola.

main.py
Es el punto de entrada de la aplicación.

Su función es:

Mostrar información al usuario.
Solicitar la meta de ahorro.
Solicitar la tasa de interés mensual.
Solicitar el número de cuotas o meses.
Solicitar opcionalmente un abono adicional para la última cuota.
Ejecutar los cálculos.
Mostrar la cuota mensual requerida.
Mostrar la tabla de acumulación.
Mostrar el total aportado.
Mostrar el total de intereses generados.
Mostrar el saldo final esperado.
El archivo también captura excepciones para mostrar mensajes de error cuando los datos ingresados no cumplen las validaciones.

# src/view/gui/

Esta carpeta contiene la interfaz de usuario gráfica de la aplicación desarrollada con Kivy.

main.py
Es el punto de entrada de la interfaz gráfica.

Su función es:

Mostrar un formulario con la meta de ahorro, la tasa de interés periódica (en %), el número de periodos y el abono extra opcional.
Ejecutar los cálculos usando la misma lógica de src/model/logica_calculadora.py.
Mostrar la cuota mensual requerida, el total aportado, el total de intereses generados y el saldo final.
Mostrar la tabla de acumulación periodo a periodo.
Mostrar mensajes de error amigables cuando los datos no cumplen las validaciones.
Usa la misma lógica que la consola, por lo que ambas interfaces comparten el modelo.

# test/

Esta carpeta contiene las pruebas automatizadas del proyecto.

test_calculadora.py
Contiene pruebas utilizando el módulo unittest de Python.

Actualmente se contemplan 10 casos:

3 casos normales de cálculo.
3 casos excepcionales o de límite.
4 casos donde se espera que el programa genere un error.
Entre las validaciones probadas se encuentran:

Meta de ahorro inválida.
Tasa de interés inválida.
Número de períodos inválido.
Abono extra inválido.
Plan de ahorro de un solo período.
Plan de ahorro de 360 meses.
Abono extra cercano al valor de la meta.
Las pruebas permiten comprobar que la lógica matemática y las validaciones se comporten de acuerdo con los resultados esperados.

__init__.py
Los archivos __init__.py permiten identificar las carpetas como paquetes de Python y facilitan la importación de los módulos del proyecto.

En este proyecto se encuentran en:

src/model/__init__.py
src/view/console/__init__.py
src/view/gui/__init__.py
test/__init__.py

# .gitignore

Este archivo indica qué archivos o carpetas deben ser ignorados por Git y, por lo tanto, no deben ser incluidos en el control de versiones.

Es especialmente útil para evitar subir archivos generados automáticamente por Python, el entorno de desarrollo u otros archivos locales.

# LICENSE

Contiene la licencia bajo la cual se distribuye el proyecto.

# README.md

Es el archivo de documentación principal del proyecto. Contiene la descripción de la aplicación, su funcionamiento, estructura, instrucciones de instalación, ejecución y pruebas.

5. # Como correr la aplicacion?

    # correr en interfaz por consola

    Requisitos para ejecutar la aplicación
Para ejecutar el proyecto desde otro equipo es necesario contar con:

Python 3 instalado.
Git instalado, si se desea clonar el proyecto directamente desde GitHub.
Una terminal o consola de comandos.
Opcionalmente, Visual Studio Code u otro editor de código.
El proyecto no utiliza una base de datos ni requiere servicios externos para realizar los cálculos.

Clonar el repositorio:

git clone https://github.com/JoseBerrioC/Calculadora-Ahorro-Programado.git

Entrar a la carpeta del proyecto:

cd Calculadora-Ahorro-Programado

Ejecutar la aplicación desde la terminal:

python src/view/console/main.py

La aplicación solicitará los datos necesarios y mostrará los resultados del cálculo.

En resumen: cualquier equipo con Python instalado puede descargar el repositorio, ingresar a la carpeta del proyecto y ejecutar main.py. La interfaz de consola no requiere instalar dependencias externas.

# correr en interfaz grafica (Kivy)

La interfaz gráfica requiere instalar Kivy (compatible con Python 3.8 a 3.13).

Instalar la dependencia (desde la carpeta raíz del proyecto):

python -m pip install -r requirements.txt

Ejecutar la aplicación:

python src/view/gui/main.py

La ventana solicita la meta de ahorro, la tasa de interés periódica (en %), el
número de periodos y, opcionalmente, un abono extra en la última cuota. Al
presionar Calcular muestra la cuota mensual, los totales y la tabla de acumulación.

En resumen: cualquier equipo con Python y Kivy instalados puede ejecutar la
interfaz gráfica con el mismo comando, desde cualquier carpeta.


# correr pruebas unitarias

Instalar y verificar Python
En una terminal:

Windows

python --version

Linux/macOS

python3 --version

Debe aparecer una versión de Python 3.

2. Descargar el proyecto
Si tienes Git instalado:

git clone https://github.com/JoseBerrioC/Calculadora-Ahorro-Programado.git
cd Calculadora-Ahorro-Programado

3. Ejecutar las pruebas
Desde la carpeta raíz del proyecto, ejecutar:

Windows

python -m unittest discover -s test -v

Linux/macOS

python3 -m unittest discover -s test -v

Este comando busca automáticamente las pruebas dentro de la carpeta test y las ejecuta mostrando el resultado de cada una.

4. Ejecutar las pruebas directamente
También se pueden ejecutar con:

python test/test_calculadora.py

En Linux/macOS:

python3 test/test_calculadora.py

Es importante ejecutarlo desde la carpeta principal del proyecto, porque las pruebas utilizan la carpeta src.

Comando principal
En resumen, después de clonar el proyecto:

cd Calculadora-Ahorro-Programado
python -m unittest discover -s test -v

6. # Casos de prueba en excel

 [Casos Prueba Ahorro Programado.xlsx](https://github.com/user-attachments/files/31009149/Casos.Prueba.Ahorro.Programado.xlsx)

7. # entrevista a experto
  

https://github.com/user-attachments/assets/5cab3eb8-5e3b-4e5b-8952-a8fa483446e5





