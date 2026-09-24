# Empaquetado para Android (.apk)

Guía para generar el **APK** de Android de la Calculadora de Ahorro Programado.
Estos archivos fueron **solo agregados** al proyecto; el código de la app no se modificó:

| Archivo                    | Para qué sirve                                              |
|----------------------------|-------------------------------------------------------------|
| `buildozer.spec`           | Configuración de Buildozer (nombre, arquitectura, versión). |
| `src/main.py`              | Punto de entrada que usa la GUI existente (`view.gui.main`).|
| `build_android.sh`         | Genera el APK en Linux/WSL/macOS con un solo comando.        |
| `.github/workflows/build-android.yml` | Compila el APK en la nube con GitHub Actions.    |

---

## Opción A: Compilar en la nube con GitHub Actions (recomendada desde Windows)

1. En el repositorio (en GitHub), ve a la pestaña **Actions**.
2. Selecciona el flujo **"Compilar APK Android"** y pulsa **Run workflow**.
3. Cuando termine, abre el resumen del job **"APK de Android"** y descarga el artefacto
   `calculadora-ahorro-android-apk`.
4. Descomprime y copia el archivo `.apk` a tu celular (o instálalo con `adb install bin/*.apk`).

## Opción B: Compilar localmente en Linux / WSL / macOS

Requisitos: Python 3.10+ y herramientas base (`git`, `zip`, `unzip`, `autoconf`, `libtool`,
`pkg-config`, `zlib1g-dev`, `openjdk`). La primera compilación descarga Android SDK/NDK (tarda bastante).

```bash
# 1. Instalar buildozer
python3 -m pip install --user buildozer

# 2. Compilar el APK (usa el buildozer.spec del proyecto)
bash build_android.sh

# 3. El APK queda en la carpeta bin/; se instala en el celular con:
adb install bin/calculadoraahorro-*.apk
```

## Instalar en el celular

1. Pasa el archivo `.apk` al teléfono (USB, Drive, WhatsApp, etc.).
2. En el teléfono toca el `.apk` y acepta **Instalar aplicaciones de orígenes desconocidos**.
3. Al terminar, abre la app **"Calculadora Ahorro"**.