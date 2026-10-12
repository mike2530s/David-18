import { PUBLIC_CLOUDINARY_CLOUD_NAME, PUBLIC_CLOUDINARY_UPLOAD_PRESET } from '$env/static/public';

export async function uploadToCloudinary(file) {
  const form = new FormData();
  form.append('file', file);
  form.append('upload_preset', PUBLIC_CLOUDINARY_UPLOAD_PRESET);

  const res = await fetch(
    `https://api.cloudinary.com/v1_1/${PUBLIC_CLOUDINARY_CLOUD_NAME}/image/upload`,
    { method: 'POST', body: form }
  );
  if (!res.ok) throw new Error('Error al subir la imagen a Cloudinary');
  const data = await res.json();
  return data.secure_url;
}
