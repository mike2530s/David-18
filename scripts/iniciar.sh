#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "============================================================"
echo "🎉 18 AÑOS DE DAVID - SISTEMA DE RECUERDOS Y WHATSAPP"
echo "============================================================"
echo ""

echo "▶️ PASO 1: Generando video con todas las fotos de la fiesta..."
python3 crear_video.py

if [ ! -f "recuerdos_david_18.mp4" ]; then
  echo ""
  echo "⚠️ No se generó el video (posiblemente aún no hay fotos subidas)."
  exit 1
fi

echo ""
echo "------------------------------------------------------------"
read -p "👀 ¿Deseas abrir el video para revisarlo antes de enviar? (s/N): " VER_VIDEO
if [[ "$VER_VIDEO" =~ ^[sS]$ ]]; then
  if command -v xdg-open &> /dev/null; then
    xdg-open recuerdos_david_18.mp4 &
  elif command -v mpv &> /dev/null; then
    mpv recuerdos_david_18.mp4 &
  elif command -v vlc &> /dev/null; then
    vlc recuerdos_david_18.mp4 &
  else
    echo "💡 Puedes abrir 'scripts/recuerdos_david_18.mp4' con tu reproductor favorito."
  fi
fi

echo ""
echo "------------------------------------------------------------"
read -p "🚀 ¿Iniciar el envío automático por WhatsApp a los invitados? (s/N): " CONFIRMAR
if [[ "$CONFIRMAR" =~ ^[sS]$ ]]; then
  echo ""
  echo "▶️ PASO 2: Iniciando bot de WhatsApp..."
  node enviar_whatsapp.js
else
  echo ""
  echo "⏸️ Envío pausado. Puedes enviarlo más tarde ejecutando:"
  echo "   node scripts/enviar_whatsapp.js"
fi
