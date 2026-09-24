#!/usr/bin/env bash
# =====================================================================
#  Genera el .apk de la Calculadora de Ahorro para Android con Buildozer
#
#  REQUISITOS:
#   - Linux, WSL o macOS (Buildozer NO funciona en Windows nativo:
#     se necesita Linux o macOS, o el flujo de GitHub Actions).
#   - Python 3.10+ y las herramientas basicas del sistema.
#
#  USO:
#   bash build_android.sh            # compila el APK de depuracion
#   bash build_android.sh release    # compila un APK liberado (firmado)
# =====================================================================
set -euo pipefail

SISTEMA="$(uname)"
ANDROID_CMD="android debug"

if [ "${1:-}" = "release" ]; then
    ANDROID_CMD="android release"
    echo ">>> Modo RELEASE activado."
fi

if [ "$SISTEMA" = "MINGW"* ] || [ "$SISTEMA" = "MSYS"* ] || [ "$SISTEMA" = "CYGWIN"* ]; then
    echo "[ERROR] Buildozer no soporta Windows nativo."
    echo "   Usa WSL (Ubuntu) o el flujo de GitHub Actions (.github/workflows)."
    exit 1
fi

if ! python3 -c "import buildozer" 2>/dev/null; then
    echo ">>> Instalando buildozer..."
    python3 -m pip install --user buildozer
fi

echo ">>> Compilando APK (buildozer $ANDROID_CMD)..."
buildozer -v $ANDROID_CMD

echo ""
echo "====================================================================="
echo " LISTO! Tu APK de Android esta en la carpeta:  bin/"
echo "   Puedes instalarlo en tu celular con:"
echo "   adb install bin/calculadoraahorro-*.apk"
echo "====================================================================="