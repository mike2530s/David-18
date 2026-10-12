#!/usr/bin/env python3
"""
Generador automático de video de recuerdos - 18 Años de David
- Descarga fotos desde Firestore (invitados_fotos).
- Genera video vertical 1080x1920 (4 segundos por foto) con fondo blur y autor.
- Incluye Intro ("18 Años de David") y Outro de agradecimiento.
- Mezcla con la música 'Young Dumb & Broke' (musica.mp3) con fade out suave.
- Guarda la lista de teléfonos únicos en 'invitados_whatsapp.json' para el envío masivo.
"""

import os
import sys
import json
import urllib.request
import subprocess
from pathlib import Path

# --- CONFIGURACIÓN ---
SEGUNDOS_POR_FOTO = 4
INTRO_SEGUNDOS = 3
OUTRO_SEGUNDOS = 3
ANCHO = 1080
ALTO = 1920
FPS = 30

BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "temp_fotos"
TEMP_CLIPS_DIR = BASE_DIR / "temp_clips"
OUTPUT_VIDEO = BASE_DIR / "recuerdos_david_18.mp4"
MUSICA_FILE = BASE_DIR / "musica.mp3"
INVITADOS_JSON = BASE_DIR / "invitados_whatsapp.json"
FONT_BOLD = "/usr/share/fonts/google-noto/NotoSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/google-noto/NotoSans-Regular.ttf"

PROJECT_ID = "invitacion-18-abf45"
FIRESTORE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/invitados_fotos"


def obtener_fotos_firestore():
    """Consulta Firestore REST API para traer fotos y datos de invitados"""
    print("📡 Consultando fotos en Firestore...")
    req = urllib.request.Request(FIRESTORE_URL, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"❌ Error al consultar Firestore: {e}")
        return []

    documents = data.get("documents", [])
    fotos = []

    for doc in documents:
        fields = doc.get("fields", {})
        url_foto = fields.get("url_foto", {}).get("stringValue", "")
        nombre = fields.get("nombre", {}).get("stringValue", "Invitado")
        telefono = fields.get("telefono", {}).get("stringValue", "")
        timestamp = fields.get("timestamp", {}).get("timestampValue", "")

        if url_foto:
            fotos.append({
                "url": url_foto,
                "nombre": nombre.strip() or "Invitado",
                "telefono": telefono.strip(),
                "timestamp": timestamp
            })

    print(f"✅ Se encontraron {len(fotos)} fotos en Firestore.")
    return fotos


def guardar_lista_whatsapp(fotos):
    """Genera lista única de contactos para envío de WhatsApp"""
    contactos = {}
    for f in fotos:
        tel = f["telefono"]
        if not tel:
            continue
        # Normalizar a formato WhatsApp México (+52)
        clean_tel = "".join(filter(str.isdigit, tel))
        if len(clean_tel) == 10:
            wa_num = f"52{clean_tel}"
        elif len(clean_tel) == 12 and clean_tel.startswith("52"):
            wa_num = clean_tel
        else:
            wa_num = clean_tel

        if wa_num not in contactos:
            contactos[wa_num] = {
                "nombre": f["nombre"],
                "telefono_wa": wa_num,
                "telefono_original": tel,
                "enviado": False
            }

    lista = list(contactos.values())
    with open(INVITADOS_JSON, "w", encoding="utf-8") as out:
        json.dump(lista, out, ensure_ascii=False, indent=2)

    print(f"📋 Guardados {len(lista)} números únicos en {INVITADOS_JSON.name}")


def descargar_foto(url, ruta_destino):
    """Descarga una foto de Cloudinary a disco"""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(ruta_destino, "wb") as f:
        f.write(resp.read())


def sanitizar_texto(texto):
    """Limpia caracteres especiales para ffmpeg drawtext"""
    return texto.replace(":", "\\:").replace("'", "").replace("%", "\\%")


def crear_clip_intro(ruta_salida):
    """Genera clip de intro elegante con animación sutil"""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c=#0B1528:s={ANCHO}x{ALTO}:d={INTRO_SEGUNDOS}:r={FPS}",
        "-vf", (
            f"drawtext=fontfile={FONT_BOLD}:text='18 AÑOS DE DAVID':fontcolor=#93C5FD:"
            f"fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2-80:shadowcolor=black@0.6:shadowx=3:shadowy=3,"
            f"drawtext=fontfile={FONT_REGULAR}:text='Recuerdos de una noche inolvidable':fontcolor=#CBD5E1:"
            f"fontsize=36:x=(w-text_w)/2:y=(h-text_h)/2+20:shadowcolor=black@0.6:shadowx=2:shadowy=2"
        ),
        "-c:v", "libopenh264", "-pix_fmt", "yuv420p", str(ruta_salida)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def crear_clip_outro(ruta_salida):
    """Genera clip de despedida y agradecimiento"""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c=#0B1528:s={ANCHO}x{ALTO}:d={OUTRO_SEGUNDOS}:r={FPS}",
        "-vf", (
            f"drawtext=fontfile={FONT_BOLD}:text='¡GRACIAS POR VENIR!':fontcolor=#93C5FD:"
            f"fontsize=62:x=(w-text_w)/2:y=(h-text_h)/2-60:shadowcolor=black@0.6:shadowx=3:shadowy=3,"
            f"drawtext=fontfile={FONT_REGULAR}:text='Fue una noche increíble 🎉':fontcolor=#CBD5E1:"
            f"fontsize=38:x=(w-text_w)/2:y=(h-text_h)/2+30:shadowcolor=black@0.6:shadowx=2:shadowy=2"
        ),
        "-c:v", "libopenh264", "-pix_fmt", "yuv420p", str(ruta_salida)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def crear_clip_foto(ruta_img, nombre_autor, ruta_salida):
    """Crea clip vertical 1080x1920 con fondo blur y autor"""
    autor_seguro = sanitizar_texto(nombre_autor)
    # Fondo con blur gaussiano + imagen nítida centrada + badge de autor
    filtro = (
        f"[0:v]scale={ANCHO}:{ALTO}:force_original_aspect_ratio=increase,crop={ANCHO}:{ALTO},boxblur=25:5[bg];"
        f"[0:v]scale={ANCHO}:{ALTO}:force_original_aspect_ratio=decrease[fg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2[base];"
        f"[base]drawtext=fontfile={FONT_BOLD}:text='📸 {autor_seguro}':"
        f"fontcolor=white:fontsize=40:x=(w-text_w)/2:y=h-180:"
        f"box=1:boxcolor=black@0.55:boxborderw=18:shadowcolor=black@0.7:shadowx=2:shadowy=2[v]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(SEGUNDOS_POR_FOTO),
        "-i", str(ruta_img),
        "-filter_complex", filtro,
        "-map", "[v]",
        "-c:v", "libopenh264", "-pix_fmt", "yuv420p", "-r", str(FPS),
        str(ruta_salida)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def main():
    print("=" * 60)
    print("🎬 GENERADOR DE VIDEO - 18 AÑOS DE DAVID")
    print(f"⚙️ Configuración: {SEGUNDOS_POR_FOTO}s por foto | Vertical 1080x1920")
    print("=" * 60)

    TEMP_DIR.mkdir(exist_ok=True)
    TEMP_CLIPS_DIR.mkdir(exist_ok=True)

    fotos = obtener_fotos_firestore()

    if not fotos:
        print("\n⚠️ No se encontraron fotos en Firestore.")
        print("💡 Si tienes fotos descargadas manualmente, colócalas en 'temp_fotos/'")
        archivos_locales = list(TEMP_DIR.glob("*.jpg")) + list(TEMP_DIR.glob("*.png"))
        if archivos_locales:
            print(f"📁 Se encontraron {len(archivos_locales)} fotos locales. Usando esas...")
            fotos = [{"local": str(p), "nombre": p.stem.replace("_", " "), "telefono": ""} for p in archivos_locales]
        else:
            print("❌ No hay fotos para procesar. Salida.")
            return

    guardar_lista_whatsapp(fotos)

    clips = []

    # 1. Intro
    print("\n🎬 Generando Intro...")
    intro_clip = TEMP_CLIPS_DIR / "000_intro.mp4"
    crear_clip_intro(intro_clip)
    clips.append(intro_clip)

    # 2. Clips de fotos
    print(f"\n🖼️ Procesando {len(fotos)} fotos ({SEGUNDOS_POR_FOTO}s cada una)...")
    for idx, f in enumerate(fotos, start=1):
        nombre = f.get("nombre", f"Invitado {idx}")
        print(f"  [{idx}/{len(fotos)}] Procesando foto de {nombre}...")

        if "local" in f:
            img_path = Path(f["local"])
        else:
            img_path = TEMP_DIR / f"foto_{idx:03d}.jpg"
            try:
                descargar_foto(f["url"], img_path)
            except Exception as e:
                print(f"    ⚠️ Error descargando foto: {e}")
                continue

        clip_path = TEMP_CLIPS_DIR / f"clip_{idx:03d}.mp4"
        try:
            crear_clip_foto(img_path, nombre, clip_path)
            clips.append(clip_path)
        except Exception as e:
            print(f"    ⚠️ Error generando clip: {e}")

    # 3. Outro
    print("\n🎬 Generando Outro...")
    outro_clip = TEMP_CLIPS_DIR / "999_outro.mp4"
    crear_clip_outro(outro_clip)
    clips.append(outro_clip)

    # 4. Concatenar clips
    print(f"\n🎞️ Concatenando {len(clips)} partes...")
    concat_list = TEMP_CLIPS_DIR / "clips.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for c in clips:
            f.write(f"file '{c.resolve()}'\n")

    video_sin_audio = TEMP_CLIPS_DIR / "video_raw.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c", "copy", str(video_sin_audio)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    duracion_total = INTRO_SEGUNDOS + (len(fotos) * SEGUNDOS_POR_FOTO) + OUTRO_SEGUNDOS
    print(f"⏱️ Duración total del video: {duracion_total} segundos (~{duracion_total // 60}:{duracion_total % 60:02d} min)")

    # 5. Agregar música
    if MUSICA_FILE.exists():
        print(f"\n🎵 Agregando canción: {MUSICA_FILE.name} (fade out al segundo {duracion_total - 3})...")
        fade_start = max(0, duracion_total - 3)
        audio_filter = f"[1:a]aloop=loop=-1:size=2e+09,atrim=0:{duracion_total},afade=t=out:st={fade_start}:d=3[a]"

        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(video_sin_audio),
            "-i", str(MUSICA_FILE),
            "-filter_complex", audio_filter,
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            str(OUTPUT_VIDEO)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    else:
        print(f"\n⚠️ No se encontró '{MUSICA_FILE.name}'. Guardando video sin audio.")
        print(f"💡 Para incluir música, coloca el archivo MP3 en: {MUSICA_FILE}")
        import shutil
        shutil.copy(video_sin_audio, OUTPUT_VIDEO)

    print("\n" + "=" * 60)
    print(f"🎉 ¡VIDEO COMPLETADO CON ÉXITO!")
    print(f"📁 Archivo final: {OUTPUT_VIDEO}")
    print(f"📱 Lista para WhatsApp: {INVITADOS_JSON}")
    print("=" * 60)


if __name__ == "__main__":
    main()
