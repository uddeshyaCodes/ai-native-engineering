"use client";

// app/providers.tsx
// Wrap the root layout's children with this so useQuery works anywhere
// in the app. Slides skip this plumbing — it's one-time setup, not
// something you touch per-feature.

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}
