'use client'

import { useState } from 'react'
import Layout from '../components/layout'
import { FileUpload } from "@/components/file-upload"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { uploadResumes, uploadJobDescription, uploadJobDescriptionText, analyzeResume } from "@/lib/api-client"
import { Loader2, User, FileText } from 'lucide-react'

interface ParsedContent {
  original_text: string;
  markdown_content: string;
  structured_data: Record<string, any>;
}

interface AnalysisResults {
  skillsMatch: number;
  experienceMatch: number;
  educationMatch: number;
  overallFit: number;
  recommendations: string[];
}

interface AnalysisResult {
  resumeId: string;
  fileName: string;
  parsed_resume: ParsedContent;
  parsed_job_description: ParsedContent;
  analysis_results: AnalysisResults;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export default function ResumeAnalysis() {
  const [resumes, setResumes] = useState<File[]>([])
  const [jobDescription, setJobDescription] = useState<File[]>([])
  const [jobDescriptionText, setJobDescriptionText] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [results, setResults] = useState<AnalysisResult[]>([])

  const handleAnalyze = async () => {
    if (resumes.length === 0 || (!jobDescription.length && !jobDescriptionText)) {
      setError("Please provide both resumes and a job description");
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      // Step 1: Upload job description
      let jobDescId;
      if (jobDescription.length > 0) {
        const jobUploadResult = await uploadJobDescription(jobDescription[0]);
        jobDescId = jobUploadResult.file_id;
      } else if (jobDescriptionText) {
        const jobUploadResult = await uploadJobDescriptionText(jobDescriptionText);
        jobDescId = jobUploadResult.file_id;
      } else {
        throw new Error("No job description provided");
      }

      // Step 2: Upload resumes and get analysis results
      const results = [];
      for (const resume of resumes) {
        // Upload resume
        const resumeUploadResult = await uploadResumes([resume]);
        const resumeId = resumeUploadResult.file_id;
        
        // Get analysis for this resume
        const analysisResult = await analyzeResume(resumeId, jobDescId);
        results.push({
          ...analysisResult,
          fileName: resume.name
        });
      }

      setResults(results);
      
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsAnalyzing(false);
    }

    console.log('Uploading job description:', jobDescription);
    console.log('Job description text:', jobDescriptionText);
    console.log('Uploading resumes:', resumes);
  };

  return (
    <Layout>
      <header className="bg-white shadow-sm py-4 mb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-800">Resume Analysis</h1>
            <p className="text-gray-600">Compare resumes with job descriptions</p>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Resume Upload Section */}
          <Card className="bg-white shadow-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Resume
              </CardTitle>
            </CardHeader>
            <CardContent>
              <FileUpload
                multiple={true}
                onFilesSelected={setResumes}
                maxFiles={10}
                acceptedFileTypes=".pdf,.doc,.docx"
              />
              {resumes.length > 0 && (
                <div className="mt-4">
                  <h4 className="font-medium mb-2">Selected Resumes:</h4>
                  <ul className="space-y-1">
                    {resumes.map((file, index) => (
                      <li key={index} className="text-sm text-gray-600">
                        {file.name}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Job Description Section */}
          <Card className="bg-white shadow-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Job Description
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <FileUpload
                multiple={false}
                onFilesSelected={setJobDescription}
                maxFiles={1}
                acceptedFileTypes=".pdf,.doc,.docx,.txt"
              />
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-background px-2 text-muted-foreground">Or paste job description</span>
                </div>
              </div>
              <Textarea
                placeholder="Paste job description here..."
                value={jobDescriptionText}
                onChange={(e) => setJobDescriptionText(e.target.value)}
                className="min-h-[200px]"
              />
            </CardContent>
          </Card>
        </div>

        {error && (
          <div className="mt-6 text-red-500 text-center bg-red-50 p-4 rounded-md">
            {error}
          </div>
        )}

        <div className="mt-8 flex justify-center">
          <Button
            size="lg"
            onClick={handleAnalyze}
            disabled={isAnalyzing || (resumes.length === 0 || (!jobDescription.length && !jobDescriptionText))}
            className="px-8 bg-indigo-600 hover:bg-indigo-700"
          >
            {isAnalyzing && <Loader2 className="mr-2 h-5 w-5 animate-spin" />}
            Analyze Resume
          </Button>
        </div>

        {/* Parsed Text Display Section */}
        {results.length > 0 && (
          <div className="mt-8">
            <h2 className="text-xl font-bold mb-4">Parsed Content</h2>
            <div className="space-y-6">
              {results.map((result, index) => (
                <Card key={index} className="bg-white shadow-sm">
                  <CardHeader>
                    <CardTitle>{result.fileName}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    {/* Parsed Resume Content */}
                    <div className="mb-4">
                      <h3 className="font-semibold mb-2">Parsed Resume:</h3>
                      {result.parsed_resume.original_text ? (
                        <pre className="bg-gray-50 p-4 rounded-md overflow-auto text-sm">
                          {result.parsed_resume.original_text}
                        </pre>
                      ) : (
                        <p className="text-gray-500">No parsed content available.</p>
                      )}
                    </div>

                    {/* Parsed Job Description Content */}
                    <div className="mb-4">
                      <h3 className="font-semibold mb-2">Parsed Job Description:</h3>
                      {result.parsed_job_description.original_text ? (
                        <pre className="bg-gray-50 p-4 rounded-md overflow-auto text-sm">
                          {result.parsed_job_description.original_text}
                        </pre>
                      ) : (
                        <p className="text-gray-500">No parsed content available.</p>
                      )}
                    </div>

                    {/* Existing Analysis Results */}
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Overall Match:</span>
                        <span className="font-bold">{result.analysis_results.overallFit}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Skills Match:</span>
                        <span>{result.analysis_results.skillsMatch}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Experience Match:</span>
                        <span>{result.analysis_results.experienceMatch}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Education Match:</span>
                        <span>{result.analysis_results.educationMatch}%</span>
                      </div>
                      <div className="mt-4">
                        <h4 className="font-medium mb-2">Recommendations:</h4>
                        <ul className="list-disc list-inside space-y-1">
                          {result.analysis_results.recommendations.map((rec: string, idx: number) => (
                            <li key={idx} className="text-sm text-gray-600">{rec}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Existing Results Section */}
        {results.length > 0 && (
          <div className="mt-8">
            <h2 className="text-xl font-bold mb-4">Analysis Results</h2>
            <div className="space-y-4">
              {results.map((result, index) => (
                <Card key={index} className="bg-white shadow-sm">
                  <CardHeader>
                    <CardTitle>{result.fileName}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    {/* Parsed Content Section */}
                    <div className="mb-6">
                      <h3 className="font-semibold mb-2">Parsed Resume Content</h3>
                      <pre className="bg-gray-50 p-4 rounded-md overflow-auto max-h-60 text-sm">
                        {result.parsed_resume?.markdown_content || 'No content available'}
                      </pre>
                    </div>
                    
                    <div className="mb-6">
                      <h3 className="font-semibold mb-2">Parsed Job Description</h3>
                      <pre className="bg-gray-50 p-4 rounded-md overflow-auto max-h-60 text-sm">
                        {result.parsed_job_description?.markdown_content || 'No content available'}
                      </pre>
                    </div>

                    {/* Analysis Results */}
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Overall Match:</span>
                        <span className="font-bold">{result.analysis_results.overallFit}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Skills Match:</span>
                        <span>{result.analysis_results.skillsMatch}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Experience Match:</span>
                        <span>{result.analysis_results.experienceMatch}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Education Match:</span>
                        <span>{result.analysis_results.educationMatch}%</span>
                      </div>
                      <div className="mt-4">
                        <h4 className="font-medium mb-2">Recommendations:</h4>
                        <ul className="list-disc list-inside space-y-1">
                          {result.analysis_results.recommendations.map((rec: string, idx: number) => (
                            <li key={idx} className="text-sm text-gray-600">{rec}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>
    </Layout>
  )
}

