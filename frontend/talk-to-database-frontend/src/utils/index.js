const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch("0.0.0.0:9999/database/connect", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });
    const result = await response.json();
    if (response.ok) {
      onSubmit(result.sessionId);
    } else {
      alert("Failed to connect to the database");
    }
};
  


export default {handleSubmit}