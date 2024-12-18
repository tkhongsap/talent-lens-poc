import { useState } from "react"
import ResumeUpload from "./resume-upload"
import JobDescriptionModule from "./job-description-module"
import { AnalysisResults } from "./analysis-results"
import { Button } from "./ui/button"

export function Dashboard() {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResults, setAnalysisResults] = useState(null)
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [jobDescription, setJobDescription] = useState("")

  const handleAnalyze = async () => {
    if (!resumeFile || !jobDescription) {
      alert("Please upload both resume and job description")
      return
    }

    setIsAnalyzing(true)
    try {
      const formData = new FormData()
      formData.append("resume", resumeFile)
      formData.append("job_description", jobDescription)

      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      })

      const data = await response.json()
      setAnalysisResults(data)
    } catch (error) {
      console.error("Analysis failed:", error)
      alert("Analysis failed. Please try again.")
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-8">Resume Analysis</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ResumeUpload onFileSelect={setResumeFile} />
        <JobDescriptionModule 
          value={jobDescription}
          onChange={setJobDescription}
        />
      </div>

      <div className="mt-6">
        <Button
          onClick={handleAnalyze}
          disabled={isAnalyzing || !resumeFile || !jobDescription}
          className="w-full md:w-auto"
        >
          {isAnalyzing ? "Analyzing..." : "Analyze Resume"}
        </Button>
      </div>

      <AnalysisResults 
        results={analysisResults}
        isLoading={isAnalyzing}
      />
    </div>
  )
}

