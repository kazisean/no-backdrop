"use client";

import { useState } from "react";
import { useDropzone } from "react-dropzone";
import Image from "next/image";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);

  const onDrop = (acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: 'image/*' // Accept only image files
  });

  return (
    <div className="relative min-h-screen flex items-center justify-center p-8 sm:p-2 font-[family-name:var(--font-geist-sans)]">
      <div className="absolute inset-0 -z-10 h-full w-full bg-white bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px]"></div>
      <div className="flex flex-col items-center text-center">
        <h1 className="text-4xl lg:text-7xl font-black text-black mb-2">NoBackdrop.</h1>
        <p className="text-lg lg:text-2xl text-gray-700 mb-6">
          Remove Image background in seconds ʕ •ᴥ•ʔ
        </p>

        {/* Dropzone Section */}
        <div
          {...getRootProps()}
          className={`w-[800px] h-[400px] border-2 ${
            isDragActive ? "border-blue-400" : "border-gray-300"
          } border-dashed rounded-lg flex items-center justify-center bg-transparent backdrop-blur-lg hover:bg-gray-100 cursor-pointer`}
        >
          <input {...getInputProps()} />
          {isDragActive ? (
            <p className="text-gray-600">Drop the image here...</p>
          ) : (
            <p className="text-gray-600">
              Drag & drop an image here, or click to select one
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
