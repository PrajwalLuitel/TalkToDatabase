// components/DataTable.jsx
import React from "react";

const DataTable = ({ data }) => {
  if (typeof data === "object" && data !== null && !Array.isArray(data)) {
    data = Object.values(data);
  }

  if (!Array.isArray(data) || data.length === 0) {
    return <div>No data available</div>;
  }

  const headers = Object.keys(data[0]);

  return (
    <table className="w-full ">
      <thead>
        <tr>
          {headers.map((header) => (
            <th className="bg-emerald-800 px-8 text-lg rounded-md" key={header}>{header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, rowIndex) => (
          <tr key={rowIndex}>
            {headers.map((header) => (
              <td className="bg-emerald-100 text-slate-800 rounded-md" key={`${rowIndex}-${header}`}>{row[header]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default DataTable;
