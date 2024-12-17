'use client'

import { useState } from 'react'
import { Upload, Save, FileText } from 'lucide-react'

export default function JobDescriptionModule() {
  const [jobDescription, setJobDescription] = useState('')

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Job Description</h2>
      <div className="space-y-4">
        <textarea
          className="w-full h-48 p-2 border rounded-md"
          placeholder="Enter job description here..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
        />
        <div className="flex space-x-2">
          <button className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
            <Upload className="h-4 w-4 mr-2" />
            Upload JD
          </button>
          <button className="flex items-center px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">
            <FileText className="h-4 w-4 mr-2" />
            Load Template
          </button>
          <button className="flex items-center px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">
            <Save className="h-4 w-4 mr-2" />
            Save
          </button>
        </div>
      </div>
    </div>
  )
}

