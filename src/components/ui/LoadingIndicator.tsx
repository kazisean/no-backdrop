import React from "react";

interface LoadingIndicatorProps {
  fileName: string;
}

const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({ fileName }) => {
  return (
    <p className="mt-4 text-gray-600">Processing your image... {fileName}</p>
  );
};

export default LoadingIndicator;
