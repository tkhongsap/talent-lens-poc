'use client'

import { useState } from 'react'
import Layout from '../components/layout'
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { Button } from "@/components/ui/button"
import { ArrowLeft, ArrowRight, Download, Search } from 'lucide-react'
import { Input } from "@/components/ui/input"

// Enhanced mock data for demonstration
const candidates = [
  { id: 1, name: "John Doe", role: "Data Engineer", score: 85, skills: ["Python", "SQL", "Apache Spark", "AWS"], experience: 5 },
  { id: 2, name: "Jane Smith", role: "Data Scientist", score: 92, skills: ["Python", "R", "Machine Learning", "Statistical Analysis"], experience: 7 },
  { id: 3, name: "Mike Johnson", role: "AI Researcher", score: 88, skills: ["Deep Learning", "TensorFlow", "Computer Vision", "NLP"], experience: 6 },
  { id: 4, name: "Emily Brown", role: "Business Analyst", score: 78, skills: ["Data Visualization", "Excel", "SQL", "Tableau"], experience: 4 },
  { id: 5, name: "Alex Chen", role: "Machine Learning Engineer", score: 90, skills: ["Python", "Scikit-learn", "Keras", "Docker"], experience: 5 },
]

export default function AnalysisPage() {
  const [selectedCandidate, setSelectedCandidate] = useState(candidates[0])
  const [searchTerm, setSearchTerm] = useState("")

  const filteredCandidates = candidates.filter(candidate =>
    candidate.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    candidate.role.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-4xl font-bold mb-8 text-gray-800">Analysis Results</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h2 className="text-2xl font-semibold mb-4 text-gray-800">Candidates</h2>
              <div className="relative mb-4">
                <Input
                  type="text"
                  placeholder="Search candidates..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
              </div>
              <ul className="space-y-4 max-h-[calc(100vh-300px)] overflow-y-auto">
                {filteredCandidates.map((candidate) => (
                  <li 
                    key={candidate.id}
                    className={`p-4 rounded-md cursor-pointer transition-all ${
                      selectedCandidate.id === candidate.id 
                        ? 'bg-indigo-100 shadow-md' 
                        : 'hover:bg-gray-100'
                    }`}
                    onClick={() => setSelectedCandidate(candidate)}
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <span className="font-medium text-gray-800">{candidate.name}</span>
                        <p className="text-sm text-gray-600">{candidate.role}</p>
                      </div>
                      <span className="text-sm font-semibold text-indigo-600">Score: {candidate.score}</span>
                    </div>
                    <Progress value={candidate.score} className="mt-2" />
                  </li>
                ))}
              </ul>
            </div>
          </div>
          
          <div className="lg:col-span-2">
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h2 className="text-3xl font-semibold mb-6 text-gray-800">{selectedCandidate.name}</h2>
              <p className="text-lg text-gray-600 mb-4">{selectedCandidate.role}</p>
              <Tabs defaultValue="overview" className="mt-6">
                <TabsList className="mb-4">
                  <TabsTrigger value="overview">Overview</TabsTrigger>
                  <TabsTrigger value="skills">Skills</TabsTrigger>
                  <TabsTrigger value="experience">Experience</TabsTrigger>
                </TabsList>
                <TabsContent value="overview">
                  <div className="space-y-6">
                    <div>
                      <h3 className="text-xl font-medium mb-2 text-gray-800">Overall Score</h3>
                      <div className="flex items-center">
                        <Progress value={selectedCandidate.score} className="flex-grow h-4" />
                        <span className="ml-4 text-2xl font-bold text-indigo-600">{selectedCandidate.score}%</span>
                      </div>
                    </div>
                    <div>
                      <h3 className="text-xl font-medium mb-2 text-gray-800">Key Highlights</h3>
                      <ul className="list-disc list-inside space-y-2 text-gray-700">
                        <li>Strong technical skills in {selectedCandidate.skills.slice(0, 3).join(", ")}</li>
                        <li>{selectedCandidate.experience} years of relevant experience in {selectedCandidate.role}</li>
                        <li>Excellent problem-solving abilities and analytical skills</li>
                      </ul>
                    </div>
                  </div>
                </TabsContent>
                <TabsContent value="skills">
                  <h3 className="text-xl font-medium mb-4 text-gray-800">Technical Skills</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {selectedCandidate.skills.map((skill, index) => (
                      <div key={index} className="bg-gray-100 p-4 rounded-md">
                        <span className="font-medium text-gray-800">{skill}</span>
                        <Progress value={Math.random() * 40 + 60} className="mt-2" />
                      </div>
                    ))}
                  </div>
                </TabsContent>
                <TabsContent value="experience">
                  <h3 className="text-xl font-medium mb-4 text-gray-800">Work Experience</h3>
                  <div className="space-y-6">
                    <div>
                      <h4 className="font-medium text-gray-800">Senior {selectedCandidate.role} at Tech Co.</h4>
                      <p className="text-sm text-gray-600">2018 - Present</p>
                      <ul className="list-disc list-inside mt-2 text-gray-700">
                        <li>Led development of key features for flagship product</li>
                        <li>Implemented advanced {selectedCandidate.role.toLowerCase()} techniques to improve efficiency</li>
                        <li>Mentored junior team members and improved team productivity</li>
                      </ul>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-800">{selectedCandidate.role} at StartUp Inc.</h4>
                      <p className="text-sm text-gray-600">2015 - 2018</p>
                      <ul className="list-disc list-inside mt-2 text-gray-700">
                        <li>Developed and maintained multiple data pipelines and models</li>
                        <li>Collaborated with cross-functional teams to deliver projects on time</li>
                        <li>Implemented best practices for {selectedCandidate.role.toLowerCase()} workflows</li>
                      </ul>
                    </div>
                  </div>
                </TabsContent>
              </Tabs>
            </div>
          </div>
        </div>
        
        <div className="mt-8 flex justify-between">
          <Button variant="outline" className="flex items-center">
            <ArrowLeft className="mr-2 h-4 w-4" /> Previous Candidate
          </Button>
          <Button variant="outline" className="flex items-center">
            <Download className="mr-2 h-4 w-4" /> Export Report
          </Button>
          <Button variant="outline" className="flex items-center">
            Next Candidate <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </div>
      </div>
    </Layout>
  )
}

