// utils/index.js


export const connectToDatabase = async (formData) => {
  try {
    console.log("Form data being sent:", JSON.stringify(formData));
    const response = await fetch("http://0.0.0.0:9999/database/connect/", {
      method: "POST",
      headers:{"Content-Type": "application/json"},
      body: JSON.stringify(formData)
    });
    console.log("Response status:", response.status);
    const result = await response.json();
    console.log("API result:", result);

    if (response.ok) {
      return result.session_id;
    }
  } catch (error) {
    console.error("Error connecting to database:", error);
    return null;
  }
};



export const uploadFile = async (fileData) => {
  try {
    const response = await fetch("0.0.0.0:9999/audio/upload", {
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

export const fetchText = async (session_id) => {
  try {
    const response = await fetch(`http://0.0.0.0:9999/audio/convert`, {
      method: "GET",
      body: JSON.stringify({ session_id }),
    });
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

export const processAudio = async (session_id, question) => {
  try {
    const max_seq_len = 10;
    const response = await fetch("0.0.0.0:9999/database/execute_query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ session_id, question, max_seq_len }),
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