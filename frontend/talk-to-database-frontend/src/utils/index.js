const connectToDatabase = async (formData) => {
  try {
    const response = await fetch("http://0.0.0.0:9999/database/connect", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });
    const result = await response.json();
    if (response.ok) {
      return result.sessionId;
    }
  } catch {
    return null;
  }
};

export default connectToDatabase;
