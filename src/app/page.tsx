"use client";

import { useState } from "react";
import { FileRejection } from "react-dropzone";
import Header from "@/components/ui/Header";
import Dropzone from "@/components/ui/Dropzone";
import LoadingIndicator from "@/components/ui/LoadingIndicator";
import ErrorMessage from "@/components/ui/ErrorMessage";

export default function Home() {
  const [originalFileName, setOriginalFileName] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string>("");

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

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      const newFileName = file.name.replace(/\.[^/.]+$/, "");

      link.href = url;
      link.download = newFileName + "_nobg.png";
      link.click();

      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error uploading file:", error);
      setErrorMessage(
        "NoBackdrop is at capacity right now. Please try again later."
      );
    } finally {
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
        {loading && <LoadingIndicator fileName={originalFileName} />}
      </div>
    </div>
  );
}
