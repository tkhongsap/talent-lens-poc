"use client"

import * as React from "react"
import { UploadCloud, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

interface FileUploadProps {
  multiple?: boolean
  onFilesSelected: (files: File[]) => void
  acceptedFileTypes?: string
  maxFiles?: number
}

export function FileUpload({
  multiple = false,
  onFilesSelected,
  acceptedFileTypes = ".pdf,.doc,.docx",
  maxFiles = 10,
}: FileUploadProps) {
  const [selectedFiles, setSelectedFiles] = React.useState<File[]>([])
  const fileInputRef = React.useRef<HTMLInputElement>(null)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || [])
    if (multiple) {
      if (files.length + selectedFiles.length > maxFiles) {
        alert(`You can only upload up to ${maxFiles} files`)
        return
      }
      setSelectedFiles(prev => [...prev, ...files])
      onFilesSelected([...selectedFiles, ...files])
    } else {
      setSelectedFiles(files)
      onFilesSelected(files)
    }
  }

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    const files = Array.from(event.dataTransfer.files)
    if (multiple) {
      if (files.length + selectedFiles.length > maxFiles) {
        alert(`You can only upload up to ${maxFiles} files`)
        return
      }
      setSelectedFiles(prev => [...prev, ...files])
      onFilesSelected([...selectedFiles, ...files])
    } else {
      setSelectedFiles(files)
      onFilesSelected(files)
    }
  }

  const removeFile = (index: number) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index)
    setSelectedFiles(newFiles)
    onFilesSelected(newFiles)
  }

  return (
    <div className="w-full">
      <Card
        className="border-dashed"
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
      >
        <CardContent className="pt-6">
          <div className="flex flex-col items-center justify-center space-y-2">
            <UploadCloud className="h-8 w-8 text-gray-400" />
            <div className="text-center">
              <Button
                variant="ghost"
                onClick={() => fileInputRef.current?.click()}
              >
                Choose files
              </Button>
              <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                multiple={multiple}
                accept={acceptedFileTypes}
                onChange={handleFileChange}
              />
              <p className="text-sm text-gray-500">
                or drag and drop {multiple ? "files" : "a file"} here
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {selectedFiles.length > 0 && (
        <div className="mt-4 space-y-2">
          {selectedFiles.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between rounded-lg border p-2"
            >
              <span className="text-sm truncate">{file.name}</span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeFile(index)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
} 