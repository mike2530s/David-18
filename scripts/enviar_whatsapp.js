#!/usr/bin/env node
/**
 * Envío automático del video de recuerdos por WhatsApp
 * - Lee 'invitados_whatsapp.json' generado por crear_video.py.
 * - Muestra un código QR en la terminal para vincular el WhatsApp de David.
 * - Envía el video MP4 adjunto y un mensaje personalizado a cada invitado.
 * - Pausa de 5 segundos entre cada envío para evitar alertas de spam.
 * - Registra cada envío para permitir pausar y reanudar sin duplicados.
 */

import { makeWASocket, useMultiFileAuthState, DisconnectReason } from '@whiskeysockets/baileys';
import qrcode from 'qrcode-terminal';
import pino from 'pino';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const INVITADOS_FILE = path.join(__dirname, 'invitados_whatsapp.json');
const VIDEO_FILE = path.join(__dirname, 'recuerdos_david_18.mp4');
const AUTH_DIR = path.join(__dirname, '.wa_auth');

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function iniciarBot() {
  if (!fs.existsSync(VIDEO_FILE)) {
    console.error('❌ Error: No existe el video en ' + VIDEO_FILE);
    console.log('👉 Ejecuta primero: python3 crear_video.py');
    process.exit(1);
  }

  if (!fs.existsSync(INVITADOS_FILE)) {
    console.error('❌ Error: No se encontró la lista ' + INVITADOS_FILE);
    console.log('👉 Ejecuta primero: python3 crear_video.py');
    process.exit(1);
  }

  const rawData = fs.readFileSync(INVITADOS_FILE, 'utf-8');
  let invitados = JSON.parse(rawData);

  const pendientes = invitados.filter((i) => !i.enviado);
  console.log('============================================================');
  console.log('📱 ENVÍO DE RECUERDOS POR WHATSAPP - 18 AÑOS DE DAVID');
  console.log(`👥 Total invitados: ${invitados.length} | Pendientes por enviar: ${pendientes.length}`);
  console.log('============================================================\n');

  if (pendientes.length === 0) {
    console.log('🎉 ¡Todos los invitados ya tienen su video! No hay pendientes.');
    process.exit(0);
  }

  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);

  const sock = makeWASocket({
    auth: state,
    logger: pino({ level: 'silent' }),
    printQRInTerminal: false
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('connection.update', async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      console.log('\n📲 Escanea este código QR con el WhatsApp de David (Dispositivos vinculados):\n');
      qrcode.generate(qr, { small: true });
    }

    if (connection === 'close') {
      const statusCode = lastDisconnect?.error?.output?.statusCode;
      const shouldReconnect = statusCode !== DisconnectReason.loggedOut;
      console.log(`🔌 Conexión cerrada. Reconectando: ${shouldReconnect}`);
      if (shouldReconnect) {
        iniciarBot();
      }
    } else if (connection === 'open') {
      console.log('\n✅ ¡WhatsApp conectado exitosamente!\n');
      console.log('🚀 Iniciando envíos automáticos...');

      const videoBuffer = fs.readFileSync(VIDEO_FILE);

      for (let i = 0; i < invitados.length; i++) {
        const invitado = invitados[i];
        if (invitado.enviado) continue;

        const jid = `${invitado.telefono_wa}@s.whatsapp.net`;
        const mensaje = `¡Hola ${invitado.nombre}! 🎉\n\nMuchas gracias por haber venido a celebrar mis 18 años. Te comparto el video con todas las fotos y recuerdos de la noche. ¡Fue una noche inolvidable! 🥂`;

        console.log(`➡️ [${i + 1}/${invitados.length}] Enviando a ${invitado.nombre} (+${invitado.telefono_wa})...`);

        try {
          await sock.sendMessage(jid, {
            video: videoBuffer,
            caption: mensaje,
            mimetype: 'video/mp4'
          });

          invitado.enviado = true;
          invitado.fecha_envio = new Date().toISOString();
          fs.writeFileSync(INVITADOS_FILE, JSON.stringify(invitados, null, 2), 'utf-8');
          console.log(`   ✅ Enviado con éxito a ${invitado.nombre}`);
        } catch (err) {
          console.error(`   ❌ Error al enviar a ${invitado.nombre}: ${err.message}`);
        }

        // Pausa de 5 segundos entre envíos para seguridad
        console.log('   ⏳ Esperando 5 segundos antes del siguiente...');
        await delay(5000);
      }

      console.log('\n============================================================');
      console.log('🎉 ¡TODOS LOS MENSAJES FUERON ENVIADOS CON ÉXITO!');
      console.log('============================================================');
      process.exit(0);
    }
  });
}

iniciarBot();
