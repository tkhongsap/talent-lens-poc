import { Card } from "./ui/card"

interface AnalysisResultsProps {
  results: {
    resumeInfo?: {
      skills: string[];
      experience: string[];
      education: string[];
    };
    jobInfo?: {
      requiredSkills: string[];
      requirements: string[];
      responsibilities: string[];
    };
    matchScore?: number;
  } | null;
  isLoading: boolean;
}

export function AnalysisResults({ results, isLoading }: AnalysisResultsProps) {
  if (isLoading) {
    return <div className="mt-4">Analyzing...</div>
  }

  if (!results) return null;

  return (
    <div className="mt-8 space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Resume Analysis */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Resume Analysis</h3>
          {results.resumeInfo && (
            <>
              <div className="mb-4">
                <h4 className="font-medium mb-2">Skills</h4>
                <div className="flex flex-wrap gap-2">
                  {results.resumeInfo.skills.map((skill, index) => (
                    <span key={index} className="bg-purple-100 text-purple-800 px-2 py-1 rounded-md text-sm">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
              <div className="mb-4">
                <h4 className="font-medium mb-2">Experience</h4>
                <ul className="list-disc list-inside">
                  {results.resumeInfo.experience.map((exp, index) => (
                    <li key={index} className="text-sm">{exp}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="font-medium mb-2">Education</h4>
                <ul className="list-disc list-inside">
                  {results.resumeInfo.education.map((edu, index) => (
                    <li key={index} className="text-sm">{edu}</li>
                  ))}
                </ul>
              </div>
            </>
          )}
        </Card>

        {/* Job Description Analysis */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Job Requirements Analysis</h3>
          {results.jobInfo && (
            <>
              <div className="mb-4">
                <h4 className="font-medium mb-2">Required Skills</h4>
                <div className="flex flex-wrap gap-2">
                  {results.jobInfo.requiredSkills.map((skill, index) => (
                    <span key={index} className="bg-blue-100 text-blue-800 px-2 py-1 rounded-md text-sm">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
              <div className="mb-4">
                <h4 className="font-medium mb-2">Requirements</h4>
                <ul className="list-disc list-inside">
                  {results.jobInfo.requirements.map((req, index) => (
                    <li key={index} className="text-sm">{req}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="font-medium mb-2">Responsibilities</h4>
                <ul className="list-disc list-inside">
                  {results.jobInfo.responsibilities.map((resp, index) => (
                    <li key={index} className="text-sm">{resp}</li>
                  ))}
                </ul>
              </div>
            </>
          )}
        </Card>
      </div>

      {/* Match Score */}
      {results.matchScore !== undefined && (
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-2">Match Score</h3>
          <div className="flex items-center gap-4">
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div
                className="bg-purple-600 h-4 rounded-full transition-all duration-500"
                style={{ width: `${results.matchScore}%` }}
              />
            </div>
            <span className="font-medium">{results.matchScore}%</span>
          </div>
        </Card>
      )}
    </div>
  )
}

