"use client";

// app/orders/orders-list.tsx
import { useQuery } from "@tanstack/react-query";

type Order = {
  id: string;
  total: string;
  status: "PENDING" | "PAID" | "SHIPPED" | "CANCELLED";
  createdAt: string;
};

const STATUS_CLASS: Record<Order["status"], string> = {
  PENDING: "status-pending",
  PAID: "status-paid",
  SHIPPED: "status-shipped",
  CANCELLED: "status-cancelled",
};

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function OrdersList({ userId }: { userId: string }) {
  const { data, isLoading, isError } = useQuery<Order[]>({
    // userId in the key keeps the cache scoped per user, even though the
    // API route itself derives identity from the session, not this param
    queryKey: ["orders", userId],
    queryFn: () =>
      fetch("/api/orders").then((r) => {
        if (!r.ok) throw new Error("Failed to load orders");
        return r.json();
      }),
    staleTime: 30_000,
  });

  if (isLoading) {
    return (
      <div className="skeleton-list">
        <div className="skeleton-row" />
        <div className="skeleton-row" />
        <div className="skeleton-row" />
      </div>
    );
  }

  if (isError) {
    return <div className="state-block">Couldn&apos;t load your orders. Try refreshing.</div>;
  }

  if (!data?.length) {
    return <div className="state-block">No orders yet.</div>;
  }

  return (
    <ul className="order-list">
      {data.map((o) => (
        <li key={o.id} className="order-row">
          <div className="order-row-left">
            <span className="order-id">#{o.id.slice(0, 6)}</span>
            <span className="order-date">{formatDate(o.createdAt)}</span>
          </div>
          <div className="order-row-right">
            <span className={`status-pill ${STATUS_CLASS[o.status]}`}>{o.status}</span>
            <span className="order-total">${o.total}</span>
          </div>
        </li>
      ))}
    </ul>
  );
}
