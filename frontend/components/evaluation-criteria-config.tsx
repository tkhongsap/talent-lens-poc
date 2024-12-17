'use client'

import { useState } from 'react'
import { Save, PlusCircle } from 'lucide-react'

const initialCriteria = [
  { name: 'Technical Skills', weight: 30 },
  { name: 'Experience', weight: 25 },
  { name: 'Education', weight: 20 },
  { name: 'Culture Fit', weight: 15 },
  { name: 'Soft Skills', weight: 10 },
]

export default function EvaluationCriteriaConfig() {
  const [criteria, setCriteria] = useState(initialCriteria)

  const handleWeightChange = (index: number, newWeight: number) => {
    const newCriteria = [...criteria]
    newCriteria[index].weight = newWeight
    setCriteria(newCriteria)
  }

  const totalWeight = criteria.reduce((sum, criterion) => sum + criterion.weight, 0)

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Evaluation Criteria</h2>
      <div className="space-y-4">
        {criteria.map((criterion, index) => (
          <div key={index} className="flex items-center space-x-4">
            <span className="w-1/3">{criterion.name}</span>
            <input
              type="range"
              min="0"
              max="100"
              value={criterion.weight}
              onChange={(e) => handleWeightChange(index, parseInt(e.target.value))}
              className="w-1/3"
            />
            <span className="w-1/6 text-right">{criterion.weight}%</span>
          </div>
        ))}
        <div className="flex justify-between items-center">
          <button className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
            <PlusCircle className="h-4 w-4 mr-2" />
            Add Custom Criterion
          </button>
          <span className={`font-bold ${totalWeight === 100 ? 'text-green-600' : 'text-red-600'}`}>
            Total: {totalWeight}%
          </span>
        </div>
        <button className="w-full flex items-center justify-center px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">
          <Save className="h-4 w-4 mr-2" />
          Save Configuration
        </button>
      </div>
    </div>
  )
}

