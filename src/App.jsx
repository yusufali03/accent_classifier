import React, { useState, useEffect } from "react";
import { analyzeVideo, analyzeFile } from "./api";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [progress, setProgress] = useState(0);
  const [isUploadMode, setIsUploadMode] = useState(false);
  const [videoLink, setVideoLink] = useState("");
  const [videoFile, setVideoFile] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    setProgress(0);
  
    let interval = setInterval(() => {
      setProgress((prev) => (prev < 90 ? prev + 5 : prev));
    }, 500);
  
    try {
      let res;
      if (isUploadMode) {
        if (!videoFile) {
          throw new Error("Please select a video file.");
        }
        res = await analyzeFile(videoFile);  // ✅ Upload file to backend
        setVideoFile(null);                  // ✅ Clear input
      } else {
        if (!url.trim()) {
          throw new Error("Please enter a video URL.");
        }
        res = await analyzeVideo(url);       // ✅ Submit URL to backend
        setUrl("");                          // ✅ Clear input
      }
  
      setResult(res);
      setProgress(100);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
      clearInterval(interval);
    }
  };
  
  // Disable button if loading or no URL
  const isDisabled = loading || (!isUploadMode && !url.trim()) || (isUploadMode && !videoFile);


  const handleToggle = () => {
    setIsUploadMode(!isUploadMode);
    setUrl("");
    setVideoFile(null);
    setResult(null);
    setError("");
  };

  return (
    <div className="container">
      <h1>Accent Analyzer</h1>

       {/* Toggle Switch */}
       <div className="toggle-wrapper">
        <span>Paste URL</span>
        <label className="switch">
          <input type="checkbox" checked={isUploadMode} onChange={handleToggle} />
          <span className="slider round"></span>
        </label>
        <span>Upload File</span>
      </div>
      
      {/* Input: URL or File */}
      {!isUploadMode ? (
        <input
          type="text"
          placeholder="Paste video URL (YouTube, Loom, etc.)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
      ) : (
        <input
          type="file"
          accept="video/*"
          onChange={(e) => setVideoFile(e.target.files[0])}
          key={isUploadMode}
        />
      )}
      <button onClick={handleAnalyze} disabled={isDisabled}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {loading && <div className="loader">Analyzing... Please wait ⏳, <i>(If your video is bigger you will wait much longer)</i>
      <div style={{ width: "100%", marginTop: "20px" }}>
      <div style={{
          height: "10px",
          width: `${progress}%`,
          backgroundColor: "#4caf50",
          transition: "width 0.3s"
         }} />
        <p style={{ textAlign: "center" }}>{progress}%</p>
      </div>
      </div>}

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result">
          <p><strong>Accent:</strong> {result.accent}</p>
          <p><strong>Confidence:</strong> {result.confidence}%</p>
          <p><strong>Summary:</strong> {result.summary}</p>
        </div>
      )}
    </div>
  );
}

export default App;

// import React, { useState } from "react";
// import { analyzeVideo, analyzeFile } from "./api";
// import "./App.css";

// function App() {
//   const [isUploadMode, setIsUploadMode] = useState(false);
//   const [videoLink, setVideoLink] = useState("");
//   const [videoFile, setVideoFile] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [result, setResult] = useState(null);

//   const handleToggle = () => {
//     setIsUploadMode(!isUploadMode);
//     setVideoLink("");
//     setVideoFile(null);
//     setResult(null);
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setLoading(true);
//     setResult(null);

//     try {
//       const response = isUploadMode
//         ? await analyzeFile(videoFile)
//         : await analyzeVideo(videoLink);

//       setResult(response);
//       setVideoLink("");
//       setVideoFile(null);
//     } catch (err) {
//       alert("Error: " + err.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="app-container">
//       <h1>Accent Analyzer</h1>

//       <div className="toggle-wrapper">
//         <span>Paste Link</span>
//         <label className="toggle-switch">
//           <input type="checkbox" checked={isUploadMode} onChange={handleToggle} />
//           <span className="slider"></span>
//         </label>
//         <span>Upload Video</span>
//       </div>

//       <form onSubmit={handleSubmit} className="form-section">
//         {!isUploadMode ? (
//           <input
//             type="text"
//             placeholder="Paste YouTube / Loom / MP4 URL"
//             value={videoLink}
//             onChange={(e) => setVideoLink(e.target.value)}
//             disabled={loading}
//             required
//           />
//         ) : (
//           <input
//             type="file"
//             accept="video/*"
//             onChange={(e) => setVideoFile(e.target.files[0])}
//             disabled={loading}
//             required
//           />
//         )}

//         <button
//           type="submit"
//           disabled={
//             loading ||
//             (!isUploadMode && !videoLink) ||
//             (isUploadMode && !videoFile)
//           }
//         >
//           {loading ? "Analyzing..." : "Analyze"}
//         </button>
//       </form>

//       {loading && (
//         <div className="loader-container">
//           <div className="loader"></div>
//           <p>Processing video, please wait...</p>
//         </div>
//       )}

//       {result && (
//         <div className="result-section">
//           <h3>Detected Accent: {result.accent}</h3>
//           <p>Confidence: {Math.round(result.confidence * 100)}%</p>
//           <p><strong>Summary:</strong> {result.summary}</p>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

