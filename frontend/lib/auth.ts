import NextAuth from "next-auth";
import Google from "next-auth/providers/google";

import { sql } from "@/lib/db";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  callbacks: {
    async signIn({ user, account }) {
      if (!user.email || !account?.providerAccountId) {
        return false;
      }

      await sql`
        INSERT INTO users (email, google_id, name)
        VALUES (${user.email}, ${account.providerAccountId}, ${user.name ?? null})
        ON CONFLICT (google_id)
        DO UPDATE SET
          email = EXCLUDED.email,
          name = EXCLUDED.name,
          updated_at = NOW()
      `;

      return true;
    },
    async session({ session }) {
      if (!session.user?.email) {
        return session;
      }

      const result = await sql`
        SELECT id, gemini_api_key_encrypted
        FROM users
        WHERE email = ${session.user.email}
      `;

      const dbUser = result[0];
      if (dbUser) {
        session.user.id = dbUser.id;
        session.user.hasApiKey = Boolean(dbUser.gemini_api_key_encrypted);
      }

      return session;
    },
  },
  pages: {
    signIn: "/login",
  },
});