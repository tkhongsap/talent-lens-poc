import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const mockData = [
  { name: 'Candidate A', score: 85 },
  { name: 'Candidate B', score: 72 },
  { name: 'Candidate C', score: 90 },
  { name: 'Candidate D', score: 68 },
  { name: 'Candidate E', score: 76 },
]

const criteriaData = [
  { name: 'Technical Skills', score: 90 },
  { name: 'Experience', score: 80 },
  { name: 'Education', score: 75 },
  { name: 'Culture Fit', score: 85 },
  { name: 'Soft Skills', score: 70 },
]

export default function AnalysisResults() {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Analysis Results</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-semibold mb-2">Overall Match Scores</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={mockData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="score" fill="#4F46E5" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div>
          <h3 className="text-lg font-semibold mb-2">Criteria Breakdown</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={criteriaData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="name" type="category" />
              <Tooltip />
              <Bar dataKey="score" fill="#4F46E5" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="mt-6">
        <h3 className="text-lg font-semibold mb-2">Key Highlights</h3>
        <ul className="list-disc list-inside space-y-2">
          <li>Candidate C has the highest overall match score of 90%</li>
          <li>Technical Skills and Culture Fit are the strongest areas across candidates</li>
          <li>Education scores are relatively lower, suggesting potential areas for improvement</li>
        </ul>
      </div>
      <div className="mt-6 flex justify-end">
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">
          View Detailed Analysis
        </button>
      </div>
    </div>
  )
}

