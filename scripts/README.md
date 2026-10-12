# 🎬 Generador de Video y Bot de WhatsApp - 18 Años de David

Este módulo automatiza la creación del video con todas las fotos de los invitados y su envío masivo por WhatsApp.

---

## 📋 Requisitos previos
1. **Colocar la canción**:
   - Guarda el archivo de audio de **Young Dumb & Broke** con el nombre exacto:
     `scripts/musica.mp3`
   - El script ajustará automáticamente el volumen, la duración y aplicará fade-out suave al final.

---

## 🚀 Pasos de uso (al finalizar la fiesta)

### Paso 1: Generar el video
Ejecuta en la terminal:
```bash
python3 scripts/crear_video.py
```

**¿Qué hace automáticamente?**
- Descarga todas las fotos de Firestore (`invitados_fotos`).
- Asigna **4 segundos por foto** con formato vertical (1080x1920) y fondo desenfocado (blur).
- Incluye el nombre de cada invitado abajo (`📸 Foto de [Nombre]`).
- Crea una Intro elegante (*"18 Años de David"*) y un Outro (*"¡Gracias por venir!"*).
- Agrega la canción con fade-out al terminar.
- Genera el video final: `scripts/recuerdos_david_18.mp4`.
- Exporta la lista de números limpios en: `scripts/invitados_whatsapp.json`.

---

### Paso 2: Enviar por WhatsApp a todos los invitados
Ejecuta:
```bash
node scripts/enviar_whatsapp.js
```

**¿Cómo funciona?**
1. Aparecerá un código QR en la terminal.
2. Abre WhatsApp en el celular de David ➡️ **Dispositivos vinculados** ➡️ **Vincular dispositivo** y escanea el QR.
3. El bot enviará automáticamente a cada contacto:
   - El video MP4 adjunto.
   - El mensaje de agradecimiento personalizado con su nombre.
   - Pausa de 5 segundos entre cada mensaje para proteger la cuenta contra spam.
