import Link from 'next/link'
import { FileText, Users, Clock } from 'lucide-react'

export default function Dashboard() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Quick Stats</h2>
        <div className="space-y-4">
          <div className="flex items-center">
            <FileText className="h-6 w-6 text-indigo-600 mr-2" />
            <span>152 Resumes Analyzed</span>
          </div>
          <div className="flex items-center">
            <Users className="h-6 w-6 text-indigo-600 mr-2" />
            <span>24 Pending Reviews</span>
          </div>
        </div>
      </div>
      <div className="bg-white p-6 rounded-lg shadow md:col-span-2">
        <h2 className="text-xl font-semibold mb-4">Active Analyses</h2>
        <div className="space-y-4">
          {[1, 2, 3].map((item) => (
            <div key={item} className="flex items-center justify-between border-b pb-2">
              <span className="font-medium">Senior Developer - Project {item}</span>
              <Link href={`/analysis/${item}`} className="text-indigo-600 hover:text-indigo-800">
                View Results
              </Link>
            </div>
          ))}
        </div>
      </div>
      <div className="bg-white p-6 rounded-lg shadow md:col-span-3">
        <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
        <div className="space-y-4">
          {[1, 2, 3, 4, 5].map((item) => (
            <div key={item} className="flex items-center text-sm">
              <Clock className="h-4 w-4 text-gray-400 mr-2" />
              <span>New resume uploaded for Project {item}</span>
              <span className="ml-auto text-gray-500">2 hours ago</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

