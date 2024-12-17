'use client'

import { useState } from 'react'
import { Upload, File, X } from 'lucide-react'

export default function ResumeUpload() {
  const [files, setFiles] = useState<File[]>([])

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    const droppedFiles = Array.from(e.dataTransfer.files)
    setFiles((prevFiles) => [...prevFiles, ...droppedFiles])
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files)
      setFiles((prevFiles) => [...prevFiles, ...selectedFiles])
    }
  }

  const removeFile = (index: number) => {
    setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index))
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Resume Upload</h2>
      <div
        className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center"
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
      >
        <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600 mb-2">Drag and drop your resumes here, or</p>
        <label className="cursor-pointer bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">
          Browse Files
          <input type="file" className="hidden" multiple onChange={handleFileInput} />
        </label>
      </div>
      {files.length > 0 && (
        <div className="mt-4">
          <h3 className="font-semibold mb-2">Uploaded Files:</h3>
          <ul className="space-y-2">
            {files.map((file, index) => (
              <li key={index} className="flex items-center justify-between bg-gray-100 p-2 rounded">
                <div className="flex items-center">
                  <File className="h-4 w-4 mr-2" />
                  <span>{file.name}</span>
                </div>
                <button onClick={() => removeFile(index)} className="text-red-600 hover:text-red-800">
                  <X className="h-4 w-4" />
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
      <button className="w-full mt-4 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700">
        Start Analysis
      </button>
    </div>
  )
}

