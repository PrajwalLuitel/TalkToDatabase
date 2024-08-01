"use client";
import { useState } from "react";
import { connectToDatabase } from "@/utils/index.js";
import { Montserrat_Alternates } from "next/font/google";
import { useRouter } from "next/navigation";

const montserrat = Montserrat_Alternates({
  subsets: ["latin"],
  weight: ["700"],
});

const DatabaseForm = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    host_name: "",
    database_name: "",
    port: "",
    database_type: "",
  });
  const [sessionId, setSessionId] = useState(null);
  const router = useRouter();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const getSessionId = async (e) => {
    e.preventDefault();
    try {
      const session = await connectToDatabase(formData);
      setSessionId(session);

      if (session == null) {
        alert("Couldn't connect to database. Please try again.");
      } else {
        router.push(`/connected?sessionId=${session}`);
      }
    } catch (error) {
      console.error("Error connecting to database:", error);
      alert("An error occurred. Please check the console for details.");
    }
  };

  return (
    <div className="w-full mt-10 mx-auto rounded-xl p-4 bg-fixed bg-form-background shadow-lg shadow-emerald-400 mb-14 pb-14 pt-12 ">
      <h1
        className={`mx-auto w-fit text-center text-emerald-100 text-[1.5rem] ${montserrat.className} backdrop-blur-lg`}
      >
        Please Enter the Details to Connect to Your Database:
      </h1>
      <form
        className="flex flex-col gap-4 max-w-[65%] max-md:max-w-[90%] mt-14 max-md:mt-0 mx-auto p-8 bg-emerald-50 shadow-xl shadow-emerald-200 rounded-xl text-black"
        onSubmit={getSessionId}
      >
        <div className="flex flex-col gap-1 w-full ">
          <p className="p-2 max-md:py-0">Enter the Name of the Database:</p>
          <input
            type="text"
            name="database_name"
            value={formData.database_name}
            onChange={handleChange}
            placeholder="Database Name"
            className="p-2 border border-gray-300 rounded text-black w-full"
            required
          />
        </div>

        <div className="flex flex-col gap-1 w-full ">
          <p className="p-2 max-md:py-0">Enter Your Username:</p>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="Username"
            className="p-2 border border-gray-300 rounded w-full"
            required
          />
        </div>

        <div className="flex flex-col gap-1 w-full ">
          <p className="p-2 max-md:py-0">Enter your Password:</p>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Password"
            className="p-2 border border-gray-300 rounded"
          />
        </div>

        <div className="flex flex-col gap-1 w-full ">
          <p className="p-2 max-md:py-0">Enter your Hostname:</p>
          <input
            type="text"
            name="host_name"
            value={formData.host_name}
            onChange={handleChange}
            placeholder="Hostname"
            className="p-2 border border-gray-300 rounded"
            required
          />
        </div>

        <div className="flex flex-col gap-1 w-full ">
          <p className="p-2 max-md:py-0">Enter the Port of your Database:</p>
          <input
            type="number"
            name="port"
            value={formData.port}
            onChange={handleChange}
            placeholder="Port"
            className="p-2 border border-gray-300 rounded"
            required
          />
        </div>

        <div className="flex flex-col gap-1 w-full ">
          <p className="p-2 max-md:py-0">Select the type of your database:</p>
          <select
            name="database_type"
            value={formData.database_type}
            onChange={handleChange}
            placeholder="Database Type"
            className="p-2 border border-gray-300 rounded"
            required
          >
            <option value="">Select Database Type</option>
            <option value="MySQL">MySQL</option>
            <option value="PostgreSQL">PostgreSQL</option>
            <option value="MariaDB">MariaDB</option>
            <option value="SQLite">SQLite</option>
            <option value="OracleSQL">OracleSQL</option>
          </select>
        </div>
        <button
          type="submit"
          className="p-3 text-lg font-semibold bg-gradient-to-r from-teal-600 to-emerald-500 text-white rounded hover:from-emerald-500 hover:to-teal-600 mt-7"
        >
          Connect
        </button>

        {sessionId && (
          <div>
            <p>Connected Successfully !!! </p>
          </div>
        )}
      </form>
    </div>
  );
};

export default DatabaseForm;
