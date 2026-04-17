#!/usr/bin/env bash
# Renderiza todas as cenas de media_vetorial.py e concatena em reports/media_vetorial_final.mp4
#
# Uso:
#   bash references/manim_media_vetorial/render_all.sh         # qualidade -qm (720p30) padrão
#   bash references/manim_media_vetorial/render_all.sh --hq    # qualidade -qh (1080p60)
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
VENV_ACTIVATE="${PROJECT_ROOT}/.venv/bin/activate"
REPORTS_DIR="${PROJECT_ROOT}/reports"
OUTPUT_FINAL="${REPORTS_DIR}/media_vetorial_final.mp4"

QUALITY_FLAG="-qm"
QUALITY_DIR="720p30"
if [[ "${1:-}" == "--hq" ]]; then
    QUALITY_FLAG="-qh"
    QUALITY_DIR="1080p60"
fi

if [[ ! -f "${VENV_ACTIVATE}" ]]; then
    echo "ERRO: .venv não encontrado em ${PROJECT_ROOT}/.venv" >&2
    exit 1
fi
# shellcheck disable=SC1090
source "${VENV_ACTIVATE}"

if ! command -v manim >/dev/null 2>&1; then
    echo "ERRO: comando 'manim' não disponível mesmo após ativar .venv" >&2
    exit 1
fi
if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "ERRO: ffmpeg não encontrado no PATH" >&2
    exit 1
fi

mkdir -p "${REPORTS_DIR}"
cd "${SCRIPT_DIR}"

CENAS=(
    "Cena0_Abertura"
    "Cena1_RosaDosVentos"
    "Cena2_Paradoxo350_10"
    "Cena3_AngulosNotaveis"
    "Cena4_AngulosQuebrados"
    "Cena5_Magnitude"
    "Cena6_Ponderacao"
    "Cena7_Resumo"
)

echo "========================================="
echo "Renderizando em qualidade ${QUALITY_FLAG} (${QUALITY_DIR})"
echo "Saída Manim: ${SCRIPT_DIR}/media/"
echo "Saída final: ${OUTPUT_FINAL}"
echo "========================================="

for cena in "${CENAS[@]}"; do
    echo ">>> Renderizando ${cena}..."
    manim "${QUALITY_FLAG}" media_vetorial.py "${cena}"
done

MEDIA_DIR="${SCRIPT_DIR}/media/videos/media_vetorial/${QUALITY_DIR}"
if [[ ! -d "${MEDIA_DIR}" ]]; then
    echo "ERRO: diretório de saída não encontrado: ${MEDIA_DIR}" >&2
    exit 1
fi

CONCAT_LIST="$(mktemp)"
trap 'rm -f "${CONCAT_LIST}"' EXIT

for cena in "${CENAS[@]}"; do
    mp4="${MEDIA_DIR}/${cena}.mp4"
    if [[ ! -f "${mp4}" ]]; then
        echo "ERRO: arquivo esperado não foi gerado: ${mp4}" >&2
        exit 1
    fi
    printf "file '%s'\n" "${mp4}" >> "${CONCAT_LIST}"
done

echo ">>> Concatenando em ${OUTPUT_FINAL}..."
ffmpeg -y -f concat -safe 0 -i "${CONCAT_LIST}" -c copy "${OUTPUT_FINAL}"

echo "========================================="
echo "OK. Vídeo final: ${OUTPUT_FINAL}"
echo "========================================="
