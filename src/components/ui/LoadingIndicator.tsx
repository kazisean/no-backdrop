import React from "react";

interface LoadingIndicatorProps {
  fileName: string;
  status: string;
}

const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({ fileName, status }) => {
  
  const getStatusMessage = () => {
    switch (status) {
      case "uploading":
        return `Uploading ${fileName}...`;
      case "pending":
        return "Your image is in the queue...";
      case "processing":
        return `Processing ${fileName}...`;
      default:
        return "Processing your image...";
    }
  };

  return (
    <div className="text-gray-600">
      <p>{getStatusMessage()}</p>
    </div>
  )
};

export default LoadingIndicator;
