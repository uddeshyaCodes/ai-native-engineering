import { AUTH_PROVIDER_ID, auth, signIn, signOut } from "@/auth";

export async function AuthButtons() {
  const session = await auth();
  const email = session?.user?.email;

  if (!email) {
    return (
      <form
        action={async () => {
          "use server";
          await signIn(AUTH_PROVIDER_ID, { redirectTo: "/" });
        }}
      >
        <button type="submit" className="button">
          {AUTH_PROVIDER_ID === "google" ? "Sign in with Google" : "Demo sign-in"}
        </button>
      </form>
    );
  }

  return (
    <div className="auth-row">
      <span className="muted">Signed in as {email}</span>
      <form
        action={async () => {
          "use server";
          await signOut({ redirectTo: "/" });
        }}
      >
        <button type="submit" className="button button--quiet">
          Sign out
        </button>
      </form>
    </div>
  );
}
