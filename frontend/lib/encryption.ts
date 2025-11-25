import crypto from 'crypto';

const ALGORITHM = 'aes-256-cbc';
const keyHex = process.env.ENCRYPTION_KEY;

if (!keyHex) {
  throw new Error('ENCRYPTION_KEY is not set');
}

const ENCRYPTION_KEY = Buffer.from(keyHex, 'hex');

if (ENCRYPTION_KEY.length !== 32) {
  throw new Error('ENCRYPTION_KEY must be 32 bytes (64 hex characters).');
}

export function encrypt(text: string): string {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, ENCRYPTION_KEY, iv);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return `${iv.toString('hex')}:${encrypted}`;
}

export function decrypt(text: string): string {
  const [ivHex, encryptedData] = text.split(':');
  const iv = Buffer.from(ivHex, 'hex');
  const decipher = crypto.createDecipheriv(ALGORITHM, ENCRYPTION_KEY, iv);
  let decrypted = decipher.update(encryptedData, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

