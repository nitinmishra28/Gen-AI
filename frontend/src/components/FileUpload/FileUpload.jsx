import React, { useState, useCallback } from "react";
import { Upload, File, X } from "lucide-react";

const FileUpload = ({
  label,
  accept = ".pdf,.doc,.docx,.txt",
  file,
  onFileChange,
  className = "",
}) => {
  const [isDragOver, setIsDragOver] = useState(false);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback(
    (e) => {
      e.preventDefault();
      setIsDragOver(false);
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        onFileChange(files[0]);
      }
    },
    [onFileChange]
  );

  const handleFileChange = useCallback(
    (e) => {
      const selectedFile = e.target.files?.[0];
      onFileChange(selectedFile);
    },
    [onFileChange]
  );

  const removeFile = useCallback(() => {
    onFileChange(undefined);
  }, [onFileChange]);

  return (
    <div className={className}>
      <label className="block text-sm font-semibold text-gray-800 mb-3">
        {label}
      </label>

      {!file ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`group border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 cursor-pointer ${
            isDragOver
              ? "border-blue-500 bg-blue-50 scale-[1.02]"
              : "border-gray-300 hover:border-blue-400 hover:bg-blue-50/50"
          }`}
        >
          <input
            type="file"
            accept={accept}
            onChange={handleFileChange}
            className="hidden"
            id={`file-upload-${label.replace(/\s+/g, "-").toLowerCase()}`}
          />
          <label
            htmlFor={`file-upload-${label.replace(/\s+/g, "-").toLowerCase()}`}
            className="cursor-pointer block"
          >
            <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
              <Upload className="h-8 w-8 text-blue-600" />
            </div>
            <p className="text-base font-medium text-gray-700 mb-2">
              Click to upload or drag and drop
            </p>
            <p className="text-sm text-gray-500">
              PDF, DOC, DOCX, TXT files up to 10MB
            </p>
          </label>
        </div>
      ) : (
        <div className="border border-gray-200 rounded-xl p-4 bg-gradient-to-r from-blue-50 to-indigo-50">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                <File className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <span className="text-sm font-semibold text-gray-900 block">
                  {file.name}
                </span>
                <span className="text-xs text-gray-500">
                  {(file.size / 1024).toFixed(1)} KB
                </span>
              </div>
            </div>
            <button
              onClick={removeFile}
              className="w-8 h-8 rounded-full bg-white shadow-sm border border-gray-200 flex items-center justify-center text-gray-400 hover:text-red-600 hover:bg-red-50 hover:border-red-200 transition-all duration-200"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
