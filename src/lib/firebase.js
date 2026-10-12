import { initializeApp, getApps, getApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { env } from '$env/dynamic/public';

const config = {
  apiKey: env.PUBLIC_FIREBASE_API_KEY || env.PUBLI_FIREBASE_API_KEY || 'demo-api-key',
  authDomain: env.PUBLIC_FIREBASE_AUTH_DOMAIN || env.PUBLI_FIREBASE_AUTH_DOMAIN || 'davi-18.firebaseapp.com',
  projectId: env.PUBLIC_FIREBASE_PROJECT_ID || env.PUBLI_FIREBASE_PROJECT_ID || 'davi-18',
  storageBucket: env.PUBLIC_FIREBASE_STORAGE_BUCKET || env.PUBLI_FIREBASE_STORAGE_BUCKET || 'davi-18.appspot.com',
  messagingSenderId: env.PUBLIC_FIREBASE_MESSAGING_SENDER_ID || env.PUBLI_FIREBASE_MESSAGING_SENDER_ID || '1234567890',
  appId: env.PUBLIC_FIREBASE_APP_ID || env.PUBLI_FIREBASE_APP_ID || '1:1234567890:web:abcdef'
};

const app = getApps().length ? getApp() : initializeApp(config);
export const db = getFirestore(app);
