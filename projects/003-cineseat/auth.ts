import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";
import Google from "next-auth/providers/google";

/**
 * Auth with a fallback.
 *
 * If AUTH_GOOGLE_ID / AUTH_GOOGLE_SECRET are set, CineSeat uses real Google
 * OAuth - Session 4's exact flow. If they are not (which is most laptops in a
 * classroom), it falls back to a one-click demo provider so nothing further
 * down the session is blocked on a Google Cloud Console account.
 *
 * That fallback is development scaffolding, not a feature. It is announced
 * loudly in the console and it is the first thing you rip out for real users.
 */
const googleConfigured = Boolean(
  process.env.AUTH_GOOGLE_ID && process.env.AUTH_GOOGLE_SECRET,
);

export const AUTH_PROVIDER_ID = googleConfigured ? "google" : "demo";

if (!googleConfigured) {
  console.warn(
    "[auth] No Google credentials found - using the demo sign-in provider. " +
      "Never deploy this to real customers.",
  );
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  // A dev default so a forgotten `npx auth secret` does not stop the class.
  secret: process.env.AUTH_SECRET ?? "cineseat-dev-only-secret-change-me",
  trustHost: true,
  session: { strategy: "jwt" },
  providers: googleConfigured
    ? [Google]
    : [
        Credentials({
          id: "demo",
          name: "Demo sign-in",
          credentials: {},
          authorize: async () => ({
            id: "demo-user",
            name: "Demo Customer",
            email: "demo@cineseat.test",
          }),
        }),
      ],
});
