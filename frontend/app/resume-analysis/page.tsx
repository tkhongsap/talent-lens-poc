'use client'

import { useState } from 'react'
import { FileUpload } from "@/components/file-upload"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { uploadResumes, uploadJobDescription } from "@/lib/api-client"
import { Loader2 } from "lucide-react"

export default function ResumeAnalysis() {
  const [resumes, setResumes] = useState<File[]>([])
  const [jobDescription, setJobDescription] = useState<File[]>([])
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAnalyze = async () => {
    if (resumes.length === 0 || jobDescription.length === 0) {
      setError("Please upload both resumes and a job description")
      return
    }

    setIsUploading(true)
    setError(null)

    try {
      // Upload job description first
      const jobUploadResult = await uploadJobDescription(jobDescription[0])
      
      // Then upload resumes
      const resumeUploadResult = await uploadResumes(resumes)

      // TODO: Handle the analysis results
      console.log({ jobUploadResult, resumeUploadResult })
      
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="container mx-auto py-10 space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Upload Resumes</CardTitle>
          </CardHeader>
          <CardContent>
            <FileUpload
              multiple={true}
              onFilesSelected={setResumes}
              maxFiles={10}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Upload Job Description</CardTitle>
          </CardHeader>
          <CardContent>
            <FileUpload
              multiple={false}
              onFilesSelected={setJobDescription}
              maxFiles={1}
            />
          </CardContent>
        </Card>
      </div>

      {error && (
        <div className="text-red-500 text-center">{error}</div>
      )}

      <div className="flex justify-center">
        <Button
          size="lg"
          onClick={handleAnalyze}
          disabled={isUploading || resumes.length === 0 || jobDescription.length === 0}
        >
          {isUploading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          Analyze Resumes
        </Button>
      </div>
    </div>
  )
}

