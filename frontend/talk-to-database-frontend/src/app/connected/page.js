"use client";

import React, { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";

const Connected = () => {
  const [sessionId, setSessionId] = useState(null);
  const searchParams = useSearchParams();

  useEffect(() => {
    try {
      setSessionId(searchParams.get("sessionId"));
    } catch {
      alert("Error getting session id !!!!!");
    }
  }, []);

  return (
    <div>
      {sessionId ? (
        <p>Connected with sessionId: {sessionId}</p>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Connected;
