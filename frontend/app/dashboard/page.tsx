'use client'

import { useState } from 'react'
import Layout from '../components/layout'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Users, Search, Globe, Zap, Briefcase, PlusCircle } from 'lucide-react'
import Link from 'next/link'

// Mock data
const networkData = {
  totalSize: 5280,
  activeTalentPool: 1250,
  extendedNetwork: 4030,
  currentOpportunities: 45
}

const networkComposition = [
  { name: 'IT & Software', value: 2500, color: '#0088ff' },
  { name: 'Finance', value: 1200, color: '#00d5b0' },
  { name: 'Marketing', value: 800, color: '#ffc107' },
  { name: 'Operations', value: 500, color: '#ff784d' },
  { name: 'Others', value: 280, color: '#9d7fff' }
]

const geographicalDistribution = [
  { name: 'North America', value: 2500, color: '#0088ff' },
  { name: 'Europe', value: 1500, color: '#00d5b0' },
  { name: 'Asia', value: 800, color: '#ffc107' },
  { name: 'South America', value: 300, color: '#ff784d' },
  { name: 'Africa', value: 100, color: '#9d7fff' },
  { name: 'Australia', value: 80, color: '#4a90e2' }
]

const skillsDistribution = [
  { name: 'Cloud Architecture', value: 850 },
  { name: 'Data Science', value: 720 },
  { name: 'DevOps', value: 680 },
  { name: 'UI/UX Design', value: 580 },
  { name: 'Product Management', value: 450 }
]

const distribution = [
  { name: 'Current Employees', value: 320 },
  { name: 'Active Candidates', value: 280 },
  { name: 'Recent Interviews', value: 250 }
]

const SKILL_COLORS = ['#2563eb', '#9333ea', '#16a34a', '#ea580c', '#dc2626']

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState('skills')
  const [timePeriod, setTimePeriod] = useState('30d')
  const maxSkillValue = Math.max(...skillsDistribution.map(skill => skill.value))
  const maxDistributionValue = Math.max(...distribution.map(item => item.value))

  return (
    <Layout>
      {/* Header Section */}
      <header className="bg-white shadow-sm py-4 mb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-800">Professional Network Dashboard</h1>
            <div className="flex items-center space-x-4">
              <div className="relative">
                <Input
                  type="text"
                  placeholder="Search network..."
                  className="pl-10 pr-4 py-2 rounded-md"
                />
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
              </div>
              <Select value={timePeriod} onValueChange={setTimePeriod}>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Select time period" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7d">Last 7 days</SelectItem>
                  <SelectItem value="30d">Last 30 days</SelectItem>
                  <SelectItem value="90d">Last 90 days</SelectItem>
                  <SelectItem value="1y">Last year</SelectItem>
                </SelectContent>
              </Select>
              <Link href="/add-professional" passHref>
                <Button className="flex items-center gap-2">
                  <PlusCircle size={16} />
                  Add Professional
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Network</CardTitle>
              <Users className="h-4 w-4 text-gray-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{networkData.totalSize.toLocaleString()}</div>
              <p className="text-xs text-gray-500">Professionals</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Talent Pool</CardTitle>
              <Zap className="h-4 w-4 text-gray-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{networkData.activeTalentPool.toLocaleString()}</div>
              <p className="text-xs text-gray-500">Ready for opportunities</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Extended Network</CardTitle>
              <Globe className="h-4 w-4 text-gray-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{networkData.extendedNetwork.toLocaleString()}</div>
              <p className="text-xs text-gray-500">Potential connections</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Current Opportunities</CardTitle>
              <Briefcase className="h-4 w-4 text-gray-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{networkData.currentOpportunities}</div>
              <p className="text-xs text-gray-500">Open positions</p>
            </CardContent>
          </Card>
        </div>

        {/* Network Visualization Area */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
          <TabsList>
            <TabsTrigger value="skills">Top Skills</TabsTrigger>
            <TabsTrigger value="composition">Composition</TabsTrigger>
            <TabsTrigger value="geography">Geography</TabsTrigger>
            <TabsTrigger value="distribution">Distribution</TabsTrigger>
          </TabsList>
          <TabsContent value="skills">
            <Card>
              <CardHeader>
                <CardTitle>Top Skills in Network</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {skillsDistribution.map((skill, index) => (
                  <div key={skill.name} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="font-medium text-gray-700">{skill.name}</span>
                      <span className="text-gray-500">{skill.value}</span>
                    </div>
                    <div className="h-2 w-full bg-gray-100 rounded-full overflow-hidden">
                      <div 
                        className="h-full rounded-full transition-all duration-500 ease-out"
                        style={{ 
                          width: `${(skill.value / maxSkillValue) * 100}%`,
                          backgroundColor: SKILL_COLORS[index]
                        }} 
                      />
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="composition">
            <Card>
              <CardHeader>
                <CardTitle>Network Composition</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {networkComposition.map((item) => (
                    <div key={item.name} className="flex items-center">
                      <div className="w-4 h-4 rounded-full mr-2" style={{ backgroundColor: item.color }}></div>
                      <span className="flex-1">{item.name}</span>
                      <span className="font-semibold">{((item.value / networkData.totalSize) * 100).toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="geography">
            <Card>
              <CardHeader>
                <CardTitle>Geographical Distribution</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {geographicalDistribution.map((item) => (
                    <div key={item.name} className="flex items-center">
                      <div className="w-4 h-4 rounded-full mr-2" style={{ backgroundColor: item.color }}></div>
                      <span className="flex-1">{item.name}</span>
                      <span className="font-semibold">{((item.value / networkData.totalSize) * 100).toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="distribution">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Distribution
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {distribution.map((item) => (
                  <div key={item.name} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="font-medium text-gray-700">{item.name}</span>
                      <span className="text-gray-500">{item.value}</span>
                    </div>
                    <div className="h-2 w-full bg-gray-100 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-blue-500 rounded-full transition-all duration-500 ease-out"
                        style={{ 
                          width: `${(item.value / maxDistributionValue) * 100}%`
                        }} 
                      />
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </Layout>
  )
}

