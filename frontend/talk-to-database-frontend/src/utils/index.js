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

export const uploadFile = async (fileData) => {
  try {
    const response = await fetch("http://0.0.0.0:9999/files/upload", {
      method: "POST",
      body: fileData,
    });
    if (response.ok) {
      return await response.json();
    } else {
      return null;
    }
  } catch (error) {
    console.error("Error uploading file:", error);
    return null;
  }
};

export const fetchText = async (sessionId) => {
  try {
    const response = await fetch(
      `http://0.0.0.0:9999/fetchtext?sessionId=${sessionId}`,
      {
        method: "GET",
      }
    );
    if (response.ok) {
      const data = await response.json();
      return data.text;
    } else {
      return "";
    }
  } catch (error) {
    console.error("Error fetching text:", error);
    return "";
  }
};

export const processAudio = async (sessionId, text) => {
  try {
    const response = await fetch("http://0.0.0.0:9999/audio/process", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ sessionId, text }),
    });
    if (response.ok) {
      return await response.json();
    } else {
      return null;
    }
  } catch (error) {
    console.error("Error processing audio:", error);
    return null;
  }
};

export default { connectToDatabase, uploadFile, fetchText, processAudio };
