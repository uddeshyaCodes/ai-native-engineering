"use client";

import { useState } from "react";

/**
 * Flips the order list between compact and comfortable spacing.
 * Used as the "test a click, not just a render" example.
 */
export function ViewToggle() {
  const [compact, setCompact] = useState(false);

  return (
    <button type="button" onClick={() => setCompact(!compact)}>
      {compact ? "Switch to comfortable" : "Switch to compact"}
    </button>
  );
}
