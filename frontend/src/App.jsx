import { useState, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [history, setHistory] = useState([]);
  const [keyword, setKeyword] = useState("");
  const API_BASE = "http://127.0.0.1:8000";

  const fetchHistory = async (filter = "") => {
    try {
      const url = filter
        ? `${API_BASE}/history?keyword=${filter}`
        : `${API_BASE}/history`;
      const res = await axios.get(url);
      setHistory(res.data);
    } catch (err) {
      console.error("Error fetching history:", err);
    }
  };

  const analyzeSymptoms = async () => {
    if (!text.trim()) return;
    try {
      const res = await axios.post(`${API_BASE}/analyze`, { text });
      setResult(res.data.result);
      fetchHistory();
    } catch (err) {
      console.error(err);
      setResult("⚠️ Error analyzing symptoms.");
    }
  };

  // 🗑️ delete one entry
  const deleteEntry = async (id) => {
    try {
      await axios.delete(`${API_BASE}/history/${id}`);
      fetchHistory();
    } catch (err) {
      console.error("Error deleting entry:", err);
    }
  };

  // 🧹 delete all entries
  const clearAllHistory = async () => {
    try {
      await axios.delete(`${API_BASE}/history`);
      fetchHistory();
    } catch (err) {
      console.error("Error clearing history:", err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="container">
      <h1>🩺 Healthcare Symptom Checker</h1>

      <textarea
        placeholder="Describe your symptoms..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      ></textarea>

      <button onClick={analyzeSymptoms}>Analyze</button>

      {result && (
        <div className="result">
          <h3>AI Diagnosis:</h3>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{result}</ReactMarkdown>
        </div>
      )}

      <h2>History</h2>

      <div className="history-controls">
        <button className="clear-btn" onClick={clearAllHistory}>
          🗑️ Clear All
        </button>
      </div>

      <input
        placeholder="Search keyword (e.g., fever)"
        value={keyword}
        onChange={(e) => {
          setKeyword(e.target.value);
          fetchHistory(e.target.value);
        }}
      />

      <ul className="history">
        {history.map((item) => (
          <li key={item.id}>
            <strong>{item.symptoms}</strong>
            <br />
            <em>
              {new Date(item.timestamp + "Z").toLocaleString("en-IN", {
              timeZone: "Asia/Kolkata",
              })}
            </em>

            <br />
            <small>{item.model}</small>
            <button
              className="delete-btn"
              onClick={() => deleteEntry(item.id)}
            >
              ❌
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
