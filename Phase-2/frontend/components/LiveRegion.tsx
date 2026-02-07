/**
 * Aria-live region for announcing dynamic updates to screen readers.
 *
 * Features:
 * - Announces task creation, updates, and deletion
 * - Polite announcements (don't interrupt)
 * - Auto-clear after announcement
 */
"use client";

import { createContext, useContext, useState, useCallback, ReactNode } from "react";

interface LiveRegionContextType {
  announce: (message: string) => void;
}

const LiveRegionContext = createContext<LiveRegionContextType | undefined>(undefined);

export function useLiveRegion() {
  const context = useContext(LiveRegionContext);
  if (!context) {
    throw new Error("useLiveRegion must be used within LiveRegionProvider");
  }
  return context;
}

interface LiveRegionProviderProps {
  children: ReactNode;
}

export function LiveRegionProvider({ children }: LiveRegionProviderProps) {
  const [message, setMessage] = useState("");

  const announce = useCallback((newMessage: string) => {
    setMessage(newMessage);
    // Clear message after a short delay to allow for new announcements
    setTimeout(() => setMessage(""), 1000);
  }, []);

  return (
    <LiveRegionContext.Provider value={{ announce }}>
      {children}
      {/* Aria-live region for screen readers */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {message}
      </div>
    </LiveRegionContext.Provider>
  );
}
