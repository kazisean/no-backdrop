"use client";

import { useState } from "react";
import { useDropzone } from "react-dropzone";
import Image from "next/image";

export default function Home() {
  const [file, setFile] = useState<File>();
  const [loading, setLoading] = useState(false);

  const onDrop = (acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      uploadFile(acceptedFiles[0]);
    }
  };

  const uploadFile = async (file: File) => {
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    // Upload file to API
    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
        mode: "cors",
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "_nobg.png";
      link.click();

      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to process the image. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".jpg", ".jpeg", ".png"],
    },
  });

  return (
    <div className="relative min-h-screen flex items-center justify-center p-4 sm:p-2 font-[family-name:var(--font-geist-sans)]">
      <div className="absolute inset-0 -z-10 h-full w-full bg-white bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px]"></div>
      <div className="flex flex-col items-center text-center">
        <h1 className="text-3xl sm:text-4xl lg:text-7xl font-black text-black mb-2">
          NoBackdrop.
        </h1>
        <p className="text-sm sm:text-lg lg:text-2xl text-gray-700 mb-6">
          Remove Image background in seconds ʕ •ᴥ•ʔ
        </p>

        {/* Dropzone Section */}
        <div
          {...getRootProps()}
          className={`w-full sm:w-[400px] md:w-[600px] lg:w-[800px] h-[200px] sm:h-[300px] lg:h-[400px] border-2 ${
            isDragActive ? "border-blue-400" : "border-gray-300"
          } border-dashed rounded-lg flex items-center justify-center bg-transparent backdrop-blur-lg hover:bg-gray-100 cursor-pointer`}
        >
          <input {...getInputProps()} />
          {isDragActive ? (
            <p className="text-gray-600 text-sm sm:text-base">Drop the image here...</p>
          ) : (
            <p className="text-gray-600 text-sm sm:text-base">
              Drag & drop an image here, or click to select one
            </p>
          )}
        </div>

        {/* Loading Indicator */}
        {loading && <p className="mt-4 text-gray-600">Processing your image...</p>}
      </div>
    </div>
  );
}
