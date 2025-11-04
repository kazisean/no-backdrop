"use client";

import { useState, useCallback } from "react";
import { FileRejection } from "react-dropzone";
import Header from "@/components/ui/Header";
import Dropzone from "@/components/ui/Dropzone";
import LoadingIndicator from "@/components/ui/LoadingIndicator";
import ErrorMessage from "@/components/ui/ErrorMessage";

export default function Home() {
  const [originalFileName, setOriginalFileName] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [pollingStatus, setPollingStatus] = useState<string>("");

  const pollJobStatus = useCallback(async (jobId: string, fileName: string) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/status${jobId}`
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Polling failed");
      }

      // if the response is an image, the job is done
      if (response.headers.get("Content-Type")?.includes("image")) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        const newFileName = fileName.replace(/\.[^/.]+$/, "");
        link.href = url;
        link.download = `${newFileName}_nobg.png`;
        link.click();
        window.URL.revokeObjectURL(url);
        
        setLoading(false);
        setPollingStatus("");
        return;
      }

      const data = await response.json();
      if (data.status === "processing" || data.status === "pending") {
        setPollingStatus(data.status);
        setTimeout(() => pollJobStatus(jobId, fileName), 2000);
      } else {
        throw new Error(data.message || "An unknown error occurred.");
      }
    } catch (error) {
      console.error("Error polling job status:", error);
      setErrorMessage("Image processing failed. Please try again.");
      setLoading(false);
      setPollingStatus("");
    }
  }, []);

  const onDrop = (acceptedFiles: File[], rejectedFiles: FileRejection[]) => {
    setErrorMessage("");

    if (rejectedFiles.length > 0) {
      setErrorMessage(
        "Invalid file type. Please upload a .jpg, .jpeg, or .png image."
      );
      return;
    }

    if (acceptedFiles.length > 0) {
      const newFile = acceptedFiles[0];
      setOriginalFileName(newFile.name);
      uploadFile(newFile);
    }
  };

  const uploadFile = async (file: File) => {
    setLoading(true);
    setPollingStatus("uploading")

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/upload`,
        {
          method: "POST",
          body: formData,
          mode: "cors",
        }
      );

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();
      pollJobStatus(data.job_id, file.name);

    } catch (error) {
      console.error("Error uploading file:", error);
      setErrorMessage(
        "NoBackdrop is at capacity right now. Please try again later."
      );
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center p-4 sm:p-2 font-[family-name:var(--font-geist-sans)]">
      <div className="absolute inset-0 -z-10 h-full w-full bg-white bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px]"></div>
      <div className="flex flex-col items-center text-center">
        <Header />
        <Dropzone onDrop={onDrop} />
        {errorMessage && <ErrorMessage message={errorMessage} />}
        {loading && <LoadingIndicator fileName={originalFileName} status={pollingStatus}/>}
      </div>
    </div>
  );
}
