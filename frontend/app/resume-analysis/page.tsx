'use client'

import { useState } from 'react'
import Layout from '../components/layout'
import { FileUpload } from "@/components/file-upload"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { uploadResumes, uploadJobDescription, analyzeResume } from "@/lib/api-client"
import { Loader2, User, FileText, Copy, Check } from 'lucide-react'
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import { ChevronDown, ChevronUp } from 'lucide-react'

interface ParsedContent {
  original_text: string;
  markdown_content: string;
  structured_data?: Record<string, any>;
}

interface AnalysisResults {
  skillsMatch: number;
  experienceMatch: number;
  educationMatch: number;
  overallFit: number;
  recommendations: string[];
  detailed_analysis?: {
    executive_summary?: string;
    fit_analysis?: {
      overall_assessment?: string;
      fit_score?: number;
    };
    key_strengths?: {
      skills?: string[];
      experience?: string[];
      notable_achievements?: string[];
    };
    areas_for_development?: {
      skills_gaps?: string[];
      experience_gaps?: string[];
      recommendations?: string[];
    };
    score_breakdown?: {
      skills_match?: string | number;
      experience_match?: string | number;
    };
    interesting_fact?: string;
  };
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
  const [jobDescription, setJobDescription] = useState<File[]>([])
  const [resumes, setResumes] = useState<File[]>([])
  const [error, setError] = useState<string | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [results, setResults] = useState<AnalysisResult[]>([])
  const [copiedStates, setCopiedStates] = useState<{ [key: string]: boolean }>({})
  const [openStates, setOpenStates] = useState<{ [key: string]: boolean }>({})

  const handleAnalyze = async () => {
    if (resumes.length === 0 || !jobDescription.length) {
      setError("Please provide both resumes and a job description");
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      // Step 1: Upload job description
      let jobDescId;
      try {
        const jobUploadResult = await uploadJobDescription(jobDescription[0]);
        jobDescId = jobUploadResult.file_id;
        console.log("Job description uploaded successfully:", jobDescId);
      } catch (err: unknown) {
        if (err instanceof Error) {
          throw new Error(`Failed to upload job description: ${err.message}`);
        } else {
          throw new Error('Failed to upload job description: An unknown error occurred');
        }
      }

      // Step 2: Upload resumes and get analysis results
      const results = [];
      for (const resume of resumes) {
        try {
          // Upload resume
          console.log("Uploading resume:", resume.name);
          const resumeUploadResult = await uploadResumes([resume]);
          const resumeId = resumeUploadResult.file_id;
          console.log("Resume uploaded successfully:", resumeId);
          
          // Get analysis for this resume
          console.log("Requesting analysis for resume:", resumeId);
          const analysisResult = await analyzeResume(resumeId, jobDescId);
          results.push({
            ...analysisResult,
            fileName: resume.name
          });
        } catch (err: unknown) {
          console.error(`Failed to process resume ${resume.name}:`, err);
          if (err instanceof Error) {
            throw err;
          } else {
            throw new Error(`Failed to process resume ${resume.name}: An unknown error occurred`);
          }
        }
      }

      setResults(results);
      
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsAnalyzing(false);
    }

    console.log('Uploading job description:', jobDescription);
    console.log('Uploading resumes:', resumes);
  };

  const handleCopy = async (text: string, id: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedStates(prev => ({ ...prev, [id]: true }))
      setTimeout(() => {
        setCopiedStates(prev => ({ ...prev, [id]: false }))
      }, 2000)
    } catch (err) {
      console.error('Failed to copy text:', err)
    }
  }

  const toggleCollapse = (id: string) => {
    setOpenStates(prev => ({ ...prev, [id]: !prev[id] }))
  }

  return (
    <Layout>
      <div className="container mx-auto py-8">
        <h1 className="text-2xl font-bold mb-8">Resume Analysis</h1>
        <p className="text-gray-600 mb-8">Compare resumes with job descriptions</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Resume Upload Section */}
          <div>
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <User className="w-5 h-5" /> Resume
            </h2>
            <FileUpload
              files={resumes}
              setFiles={setResumes}
              onRemove={(index: number) => {
                const newFiles = [...resumes];
                newFiles.splice(index, 1);
                setResumes(newFiles);
              }}
              accept={{
                'application/pdf': ['.pdf'],
                'application/msword': ['.doc'],
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
                'text/plain': ['.txt']
              }}
            />
          </div>

          {/* Job Description Upload Section */}
          <div>
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <FileText className="w-5 h-5" /> Job Description
            </h2>
            <FileUpload
              files={jobDescription}
              setFiles={setJobDescription}
              onRemove={(index: number) => {
                const newFiles = [...jobDescription];
                newFiles.splice(index, 1);
                setJobDescription(newFiles);
              }}
              accept={{
                'application/pdf': ['.pdf'],
                'application/msword': ['.doc'],
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
                'text/plain': ['.txt']
              }}
            />
          </div>
        </div>

        {error && (
          <div className="bg-red-50 text-red-500 p-4 rounded-md mb-4">
            {error}
          </div>
        )}

        <div className="mt-8 flex justify-center">
          <Button
            onClick={handleAnalyze}
            disabled={isAnalyzing || resumes.length === 0 || jobDescription.length === 0}
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              'Analyze Resume'
            )}
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
                    <div className="flex justify-between items-center">
                      <CardTitle>{result.fileName}</CardTitle>
                      <div className="flex gap-2">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-8 px-2"
                          onClick={() => handleCopy(result.parsed_resume.original_text, `resume-${index}`)}
                        >
                          {copiedStates[`resume-${index}`] ? (
                            <>
                              <Check className="h-4 w-4 mr-2" />
                              Copied
                            </>
                          ) : (
                            <>
                              <Copy className="h-4 w-4 mr-2" />
                              Copy
                            </>
                          )}
                        </Button>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <Collapsible
                      open={openStates[`content-${index}`] !== false}
                      onOpenChange={() => toggleCollapse(`content-${index}`)}
                    >
                      <div className="flex justify-between items-center mb-2">
                        <div className="flex items-center gap-2">
                          <CollapsibleTrigger asChild>
                            <Button variant="ghost" size="sm">
                              {openStates[`content-${index}`] === false ? (
                                <ChevronDown className="h-4 w-4" />
                              ) : (
                                <ChevronUp className="h-4 w-4" />
                              )}
                            </Button>
                          </CollapsibleTrigger>
                          <h3 className="text-lg font-semibold">Resume Summary</h3>
                        </div>
                      </div>
                      <CollapsibleContent>
                        <pre className="bg-gray-50 p-4 rounded-md overflow-auto text-sm whitespace-pre-wrap">
                          {result.parsed_resume.original_text}
                        </pre>
                      </CollapsibleContent>
                    </Collapsible>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Analysis Results Section */}
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
                    {/* Analysis Results */}
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Overall Match:</span>
                        <span className="font-bold">{result.analysis_results?.overallFit ?? 0}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Skills Match:</span>
                        <span>{result.analysis_results?.skillsMatch ?? 0}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Experience Match:</span>
                        <span>{result.analysis_results?.experienceMatch ?? 0}%</span>
                      </div>
                      {/* Recommendations Section */}
                      {result.analysis_results?.recommendations && 
                       result.analysis_results.recommendations.length > 0 && (
                        <div className="mt-4">
                          <h4 className="font-medium mb-2">Recommendations:</h4>
                          <ul className="list-disc list-inside space-y-1">
                            {result.analysis_results.recommendations.map((rec: string, idx: number) => (
                              <li key={idx} className="text-sm text-gray-600">{rec}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {/* Detailed Analysis Section */}
                      {result.analysis_results?.detailed_analysis && (
                        <div className="mt-4">
                          <h4 className="font-medium mb-2">Detailed Analysis:</h4>
                          <pre className="bg-gray-50 p-4 rounded-md overflow-auto text-sm">
                            {JSON.stringify(result.analysis_results.detailed_analysis, null, 2)}
                          </pre>
                        </div>
                      )}
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

