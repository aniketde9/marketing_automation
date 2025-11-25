import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';
import { sql } from '@/lib/db';

// Validate required environment variables
const GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID;
const GOOGLE_CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET;
const NEXTAUTH_SECRET = process.env.NEXTAUTH_SECRET;

if (!GOOGLE_CLIENT_ID) {
  throw new Error('GOOGLE_CLIENT_ID is not set');
}

if (!GOOGLE_CLIENT_SECRET) {
  throw new Error('GOOGLE_CLIENT_SECRET is not set');
}

if (!NEXTAUTH_SECRET) {
  throw new Error('NEXTAUTH_SECRET is not set');
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    GoogleProvider({
      clientId: GOOGLE_CLIENT_ID,
      clientSecret: GOOGLE_CLIENT_SECRET,
    }),
  ],
  callbacks: {
    async signIn({ user, account }) {
      if (account?.provider === 'google' && user.email && account.providerAccountId) {
        try {
          // Upsert user (create or update)
          await sql`
            INSERT INTO users (email, google_id, name, created_at)
            VALUES (${user.email}, ${account.providerAccountId}, ${user.name || null}, NOW())
            ON CONFLICT (google_id)
            DO UPDATE SET
              email = EXCLUDED.email,
              name = EXCLUDED.name,
              updated_at = NOW()
          `;
          
          return true;
        } catch (error) {
          console.error('Sign in error:', error);
          return false;
        }
      }
      return false;
    },
    async jwt({ token, user }) {
      if (user?.email) {
        const dbUser = await sql`
          SELECT id, gemini_api_key_encrypted FROM users WHERE email = ${user.email}
        `;
        if (dbUser.length > 0) {
          token.id = dbUser[0].id;
          token.hasApiKey = Boolean(dbUser[0].gemini_api_key_encrypted);
        }
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        session.user.hasApiKey = Boolean(token.hasApiKey);
      }
      return session;
    },
  },
  pages: {
    signIn: '/login',
    error: '/login',
  },
  secret: NEXTAUTH_SECRET,
});
