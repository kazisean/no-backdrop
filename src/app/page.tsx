"use client";

import { useState, useCallback } from "react";
import { FileRejection } from "react-dropzone";
import Header from "@/components/ui/Header";
import Dropzone from "@/components/ui/Dropzone";
import LoadingIndicator from "@/components/ui/LoadingIndicator";
import ErrorMessage from "@/components/ui/ErrorMessage";

export default function Home() {
  const [processingFiles, setProcessingFiles] = useState<Map<string, { fileName: string; status: string }>>(new Map());
  const [errorMessage, setErrorMessage] = useState<string>("");

  const pollJobStatus = useCallback(async (jobId: string, fileName: string) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/status/${jobId}`
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
        
        // Remove from processing files
        setProcessingFiles(prev => {
          const updated = new Map(prev);
          updated.delete(jobId);
          return updated;
        });
        return;
      }

      const data = await response.json();
      if (data.status === "processing" || data.status === "pending") {
        setProcessingFiles(prev => {
          const updated = new Map(prev);
          updated.set(jobId, { fileName, status: data.status });
          return updated;
        });
        setTimeout(() => pollJobStatus(jobId, fileName), 2000);
      } else {
        throw new Error(data.message || "An unknown error occurred.");
      }
    } catch (error) {
      console.error("Error polling job status:", error);
      setErrorMessage(`Processing failed for ${fileName}. Please try again.`);
      setProcessingFiles(prev => {
        const updated = new Map(prev);
        updated.delete(jobId);
        return updated;
      });
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
      // Process all accepted files
      acceptedFiles.forEach(file => uploadFile(file));
    }
  };

  const uploadFile = async (file: File) => {
    const tempJobId = `uploading_${Date.now()}_${Math.random()}`;
    setProcessingFiles(prev => {
      const updated = new Map(prev);
      updated.set(tempJobId, { fileName: file.name, status: "uploading" });
      return updated;
    });

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();
      
      // Remove temp upload status and start polling
      setProcessingFiles(prev => {
        const updated = new Map(prev);
        updated.delete(tempJobId);
        return updated;
      });
      
      pollJobStatus(data.job_id, file.name);

    } catch (error) {
      console.error("Error uploading file:", error);
      setErrorMessage(
        `Upload failed for ${file.name}. Please try again.`
      );
      setProcessingFiles(prev => {
        const updated = new Map(prev);
        updated.delete(tempJobId);
        return updated;
      });
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center p-4 sm:p-2 font-[family-name:var(--font-geist-sans)]">
      <div className="absolute inset-0 -z-10 h-full w-full bg-white bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px]"></div>
      <div className="flex flex-col items-center text-center">
        <Header />
        <Dropzone onDrop={onDrop} />
        {errorMessage && <ErrorMessage message={errorMessage} />}
        {processingFiles.size > 0 && (
          <div className="mt-4 space-y-2">
            {Array.from(processingFiles.values()).map((file, index) => (
              <LoadingIndicator key={index} fileName={file.fileName} status={file.status} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
