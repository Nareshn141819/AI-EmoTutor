import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const uploadAudio = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("https://ai-emotutor.onrender.com", formData);

    setResult(res.data);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Emotion Aware AI Tutor</h1>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />

      <button onClick={uploadAudio}>Submit</button>

      {result && (
        <div>
          <p><b>Text:</b> {result.text}</p>
          <p><b>Emotion:</b> {result.emotion}</p>
          <p><b>Mode:</b> {result.mode}</p>
          <p><b>Response:</b> {result.response}</p>

          <audio controls src={`http://127.0.0.1:8000/${result.audio}`} />
        </div>
      )}
    </div>
  );
}

export default App;
