import React from "react";
import { useDropzone, FileRejection } from "react-dropzone";

interface DropzoneProps {
  onDrop: (acceptedFiles: File[], rejectedFiles: FileRejection[]) => void;
}

const Dropzone: React.FC<DropzoneProps> = ({ onDrop }) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".jpeg", ".jpg", ".png"],
    },
    multiple: true,
  });

  return (
    <div
      {...getRootProps()}
      className={`w-full sm:w-[400px] md:w-[600px] lg:w-[800px] h-[200px] sm:h-[300px] lg:h-[400px] border-2 ${
        isDragActive ? "border-blue-400" : "border-gray-300"
      } border-dashed rounded-lg flex items-center justify-center bg-transparent backdrop-blur-lg hover:bg-gray-100 cursor-pointer`}
    >
      <input {...getInputProps()} />
      {isDragActive ? (
        <p className="text-gray-600 text-sm sm:text-base">
          Drop the image here...
        </p>
      ) : (
        <p className="text-gray-600 text-sm sm:text-base">
          Drag & drop image(s) here, or click to select
        </p>
      )}
    </div>
  );
};

export default Dropzone;
