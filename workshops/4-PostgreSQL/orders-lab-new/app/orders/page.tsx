// app/orders/page.tsx
import { auth, signOut } from "@/auth";
import { redirect } from "next/navigation";
import { OrdersList } from "./orders-list";

export default async function OrdersPage() {
  const session = await auth();
  if (!session?.user) redirect("/login");

  return (
    <>
      <header className="app-header">
        <span className="wordmark">
          <span className="wordmark-mark" />
          <span className="wordmark-text">Orders</span>
        </span>
        <div className="app-header-right">
          <span className="user-email">{session.user.email}</span>
          <form
            action={async () => {
              "use server";
              await signOut({ redirectTo: "/login" });
            }}
          >
            <button type="submit" className="sign-out-link">Sign out</button>
          </form>
        </div>
      </header>

      <main className="orders-main">
        <h1 className="orders-heading">Your orders</h1>
        <p className="orders-subheading">Everything you&apos;ve ordered, most recent first.</p>
        <OrdersList userId={session.user.id} />
      </main>
    </>
  );
}
