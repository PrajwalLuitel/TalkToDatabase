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
  <div>      <p>Connected with sessionId: {sessionId}</p>
          <p>This part allows the user to provide voice command</p>
          
          <p>Space for the user voice converted to text</p>

          <p>Space for data fetched from the database.</p>
        </div>

  

      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Connected;
