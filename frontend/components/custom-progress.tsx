interface CustomProgressProps {
  value: number
  max: number
  label: string
  color: string
}

export function CustomProgress({ value, max, label, color }: CustomProgressProps) {
  const percentage = (value / max) * 100

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span className="font-medium text-gray-700">{label}</span>
        <span className="text-gray-500">{value}</span>
      </div>
      <div className="h-2 w-full bg-gray-100 rounded-full overflow-hidden">
        <div 
          className="h-full rounded-full transition-all duration-500 ease-out"
          style={{ 
            width: `${percentage}%`,
            backgroundColor: color
          }} 
        />
      </div>
    </div>
  )
}

