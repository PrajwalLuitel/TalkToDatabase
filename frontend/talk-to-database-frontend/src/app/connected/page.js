"use client";

import React, { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { uploadFile, fetchText, processAudio } from "@/utils";
import Image from "next/image";
import DataTable from "@/components/DataTable";
import LoadingAnimation from "@/components/LoadingAnimation";

const Connected = () => {
  const [sessionId, setSessionId] = useState(null);
  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [convertedText, setConvertedText] = useState("");
  const [processedData, setProcessedData] = useState(null);
  const searchParams = useSearchParams();
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);
  const [uploaded, setUploaded] = useState(false);
  const [textIsLoading, setTextIsLoading] = useState(false);
  const [tableIsLoading, setTableIsLoading] = useState(false);

  useEffect(() => {
    try {
      setSessionId(searchParams.get("sessionId"));
    } catch {
      alert("Error getting session id!");
    }
  }, [searchParams]);

  const handleRecording = () => {
    if (!recording) {
      startRecording();
    } else {
      stopRecording();
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setRecording(false);
    }
  };

  const startRecording = () => {
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
      const newMediaRecorder = new MediaRecorder(stream);
      const newAudioChunks = [];

      newMediaRecorder.ondataavailable = (event) => {
        newAudioChunks.push(event.data);
      };

      newMediaRecorder.onstop = () => {
        const blob = new Blob(newAudioChunks, { type: "audio/wav" });
        setAudioBlob(blob);
        console.log("Recorded audio blob: ", blob);
        stream.getTracks().forEach((track) => track.stop());
      };

      setMediaRecorder(newMediaRecorder);
      setAudioChunks(newAudioChunks);
      newMediaRecorder.start();
      setRecording(true);
    });
  };

  const handleAudioUpload = async (e) => {
    e.preventDefault();
    setTextIsLoading(true);
    if (audioBlob && sessionId) {
      console.log("Uploading audio blob: ", audioBlob);
      const uploadResponse = await uploadFile(audioBlob, sessionId);
      if (uploadResponse) {
        setUploaded(true);
        console.log("Uploaded audio blob, Now waiting for the text . . .");
        const text = await fetchText(sessionId);
        setTextIsLoading(false);
        setConvertedText(text);
        console.log("Received the uploaded text: ", text);
      } else {
        alert("Error uploading audio file.");
        setTextIsLoading(false);
      }
    }
  };

  const processText = async () => {
    setTableIsLoading(true);
    const data = await processAudio(
      sessionId,
      "Give me the name of three employees whose name starts with C."
    );
    console.log("I received this from the final api call: ", data);
    console.log("This is data.dataframe: ", data.dataframe);
    setTableIsLoading(false);
    setProcessedData(data.dataframe);
  };

  return (
    <div className="w-full">
      {sessionId ? (
        <div className="max-w-[75%] max-md:max-w-full m-auto text-center bg-emerald-950 rounded-xl pb-10">
          <h1 className="text-[2.5rem] pt-10 pb-8">
            Connection Established with the Database Server
          </h1>
          <h2>Talk to the Data : </h2>
          <div className="w-full text-center">
            <button onClick={handleRecording}>
              {recording ? (
                <div className="bg-rose-400 m-auto p-2 rounded-xl mb-4 text-center transition-all duration-1000 ease-in text-slate-900">
                  <Image
                    src="/Images/recording_stop.png"
                    width={50}
                    height={50}
                    alt="Start Recording"
                    className="w-[40%] m-auto h-auto"
                  />
                  Stop Recording
                </div>
              ) : (
                <div className="bg-emerald-500 m-auto p-2 rounded-xl mb-4 text-center transition-all duration-1000 ease-in text-slate-900 shadow-emerald-500 shadow-lg ">
                  <Image
                    src="/Images/recording_start.png"
                    width={50}
                    height={50}
                    alt="Start Recording"
                    className="w-[40%] m-auto h-auto"
                  />
                  Start Recording
                </div>
              )}
            </button>
          </div>

          <form onSubmit={handleAudioUpload}>
            {audioBlob ? (
              <button
                type="submit"
                className="p-4 bg-emerald-500/70 font-bold rounded-xl transition-all duration-1000 ease-in mt-6 "
              >
                Upload Audio
              </button>
            ) : (
              <button
                type="submit"
                disabled={true}
                className="p-4 bg-slate-300 text-slate-500 rounded-xl transition-all duration-1000 ease-in mt-9"
              >
                Upload Audio
              </button>
            )}
          </form>
          {textIsLoading && (
            <LoadingAnimation
              message="Analyzing the text . . "
              className="transition-all ease-in duration-400"
            />
          )}

          <button
            onClick={processText}
            className="bg-slate-300 p-4 rounded-lg mt-10 text-slate-800"
          >
            Process the Test
          </button>
          {tableIsLoading && (
            <LoadingAnimation
              message="Fetching the table. . . "
              className="transition-all duration-1000 ease-in"
            />
          )}

          {uploaded && (
            <div>
              <p>File uploaded successfully !!</p>
            </div>
          )}

          {convertedText && (
            <div>
              <p>Voice Command Text: {convertedText}</p>
            </div>
          )}

          {processedData && (
            <div>
              <p>Processed Data:</p>
              <DataTable data={processedData} />
            </div>
          )}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Connected;
