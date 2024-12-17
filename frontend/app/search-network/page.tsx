'use client'

import { useState } from 'react'
import Layout from '../components/layout'
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Badge } from "@/components/ui/badge"
import { Search, MapPin, Clock, ChevronDown, ChevronUp, ExternalLink } from 'lucide-react'

// Mock data for demonstration
const mockResults = [
  { id: 1, name: "John Doe", role: "Senior Cloud Architect", skills: ["Python", "AWS", "Docker"], location: "New York, USA", availability: "Available", matchPercentage: 95 },
  { id: 2, name: "Jane Smith", role: "UI/UX Designer", skills: ["Figma", "Sketch", "Adobe XD"], location: "London, UK", availability: "Open to offers", matchPercentage: 88 },
  { id: 3, name: "Mike Johnson", role: "DevOps Engineer", skills: ["Kubernetes", "Jenkins", "Terraform"], location: "San Francisco, USA", availability: "Not available", matchPercentage: 82 },
  { id: 4, name: "Emily Brown", role: "Data Scientist", skills: ["Python", "R", "Machine Learning"], location: "Boston, USA", availability: "Available", matchPercentage: 91 },
  { id: 5, name: "Alex Chen", role: "Full Stack Developer", skills: ["React", "Node.js", "MongoDB"], location: "Toronto, Canada", availability: "Open to offers", matchPercentage: 87 },
  { id: 6, name: "Sarah Lee", role: "Product Manager", skills: ["Agile", "Scrum", "User Research"], location: "Seattle, USA", availability: "Not available", matchPercentage: 79 },
  { id: 7, name: "Tom Wilson", role: "Cybersecurity Analyst", skills: ["Network Security", "Penetration Testing", "SIEM"], location: "Austin, USA", availability: "Available", matchPercentage: 93 },
  { id: 8, name: "Maria Garcia", role: "Mobile App Developer", skills: ["Swift", "Kotlin", "React Native"], location: "Barcelona, Spain", availability: "Open to offers", matchPercentage: 85 },
  { id: 9, name: "David Kim", role: "AI Research Scientist", skills: ["Deep Learning", "NLP", "Computer Vision"], location: "Seoul, South Korea", availability: "Not available", matchPercentage: 89 },
  { id: 10, name: "Lisa Nguyen", role: "UX Researcher", skills: ["User Testing", "Wireframing", "Data Analysis"], location: "Sydney, Australia", availability: "Available", matchPercentage: 86 },
]

export default function SearchNetworkPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [isFilterExpanded, setIsFilterExpanded] = useState(false)
  const [results, setResults] = useState(mockResults)

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    // Implement actual search logic here
    console.log("Searching for:", searchQuery)
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold mb-6">Search Network</h1>

        {/* Search Input Area */}
        <form onSubmit={handleSearch} className="mb-8">
          <div className="flex gap-2">
            <Input
              type="text"
              placeholder="Search by skills, role, or description..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-grow"
            />
            <Button type="submit">
              <Search className="mr-2 h-4 w-4" /> Search
            </Button>
          </div>
        </form>

        {/* Filter Section */}
        <div className="mb-8">
          <Button
            variant="outline"
            onClick={() => setIsFilterExpanded(!isFilterExpanded)}
            className="w-full justify-between"
          >
            Filters
            {isFilterExpanded ? <ChevronUp className="ml-2 h-4 w-4" /> : <ChevronDown className="ml-2 h-4 w-4" />}
          </Button>
          {isFilterExpanded && (
            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Skills</label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select skills" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="python">Python</SelectItem>
                    <SelectItem value="react">React</SelectItem>
                    <SelectItem value="aws">AWS</SelectItem>
                    {/* Add more skills as needed */}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Experience Level</label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select experience" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="entry">Entry Level</SelectItem>
                    <SelectItem value="mid">Mid Level</SelectItem>
                    <SelectItem value="senior">Senior Level</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                <Input type="text" placeholder="Enter location" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Availability Status</label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="available">Available</SelectItem>
                    <SelectItem value="open">Open to offers</SelectItem>
                    <SelectItem value="unavailable">Not available</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          )}
        </div>

        {/* Results Display */}
        <div className="space-y-6">
          {results.map((result) => (
            <div key={result.id} className="border-b pb-4">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="text-xl font-semibold text-blue-600 hover:underline">
                    <a href={`/profile/${result.id}`}>{result.name}</a>
                  </h3>
                  <p className="text-sm text-gray-600">{result.role}</p>
                </div>
                <Badge variant={result.matchPercentage >= 90 ? "default" : "secondary"}>
                  {result.matchPercentage}% Match
                </Badge>
              </div>
              <div className="text-sm text-gray-700 mb-2">
                <span className="font-semibold">Skills:</span> {result.skills.join(", ")}
              </div>
              <div className="flex items-center text-sm text-gray-600 space-x-4">
                <div className="flex items-center">
                  <MapPin className="mr-1 h-4 w-4" />
                  {result.location}
                </div>
                <div className="flex items-center">
                  <Clock className="mr-1 h-4 w-4" />
                  {result.availability}
                </div>
              </div>
              <div className="mt-2">
                <a href={`/profile/${result.id}`} className="text-sm text-gray-500 hover:text-gray-700 flex items-center">
                  View full profile <ExternalLink className="ml-1 h-3 w-3" />
                </a>
              </div>
            </div>
          ))}
        </div>

        {/* Results Navigation */}
        <div className="mt-8 flex justify-between items-center">
          <div className="text-sm text-gray-600">
            Showing 1-10 of {results.length} results
          </div>
          <div className="flex items-center space-x-2">
            <Button variant="outline" size="sm" disabled>Previous</Button>
            <Button variant="outline" size="sm">Next</Button>
          </div>
        </div>
      </div>
    </Layout>
  )
}

