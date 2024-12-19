"use client"

import * as React from "react"
import { UploadCloud, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

interface FileUploadProps {
  files?: File[];
  setFiles: (files: File[]) => void;
  onFilesSelected?: (files: File[]) => void;
  onRemove?: (index: number) => void;
  accept?: Record<string, string[]>;
  multiple?: boolean;
  maxFiles?: number;
}

export function FileUpload({
  files = [],
  setFiles,
  onFilesSelected,
  onRemove,
  accept,
  multiple = false,
  maxFiles = 10
}: FileUploadProps) {
  const [selectedFiles, setSelectedFiles] = React.useState<File[]>(files)
  const fileInputRef = React.useRef<HTMLInputElement>(null)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || [])
    if (multiple) {
      if (files.length + selectedFiles.length > maxFiles) {
        alert(`You can only upload up to ${maxFiles} files`)
        return
      }
      setSelectedFiles(prev => [...prev, ...files])
      setFiles([...selectedFiles, ...files])
    } else {
      setSelectedFiles(files)
      setFiles(files)
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
      setFiles([...selectedFiles, ...files])
    } else {
      setSelectedFiles(files)
      setFiles(files)
    }
  }

  const removeFile = (index: number) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index)
    setSelectedFiles(newFiles)
    setFiles(newFiles)
    onRemove?.(index)
  }

  const getFormattedFileTypes = () => {
    if (!accept) return "PDF, DOC, DOCX, TXT"
    return Object.values(accept)
      .flat()
      .map((type: string) => type.toUpperCase().replace('.', ''))
      .join(', ')
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
                accept={Object.keys(accept || {}).join(',')}
                onChange={handleFileChange}
              />
              <p className="text-sm text-gray-500">
                or drag and drop files here ({getFormattedFileTypes()})
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