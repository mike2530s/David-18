import { env } from '$env/dynamic/public';

export async function uploadToCloudinary(file) {
  const cloudName = env.PUBLIC_CLOUDINARY_CLOUD_NAME || env.PUBLI_CLOUDINARY_CLOUD_NAME;
  const uploadPreset = env.PUBLIC_CLOUDINARY_UPLOAD_PRESET || env.PUBLI_CLOUDINARY_UPLOAD_PRESET;

  if (!cloudName || !uploadPreset) {
    throw new Error('Faltan variables de entorno de Cloudinary (CLOUD_NAME o UPLOAD_PRESET)');
  }

  const form = new FormData();
  form.append('file', file);
  form.append('upload_preset', uploadPreset);

  const res = await fetch(
    `https://api.cloudinary.com/v1_1/${cloudName}/image/upload`,
    { method: 'POST', body: form }
  );
  if (!res.ok) throw new Error('Error al subir la imagen a Cloudinary');
  const data = await res.json();
  return data.secure_url;
}
