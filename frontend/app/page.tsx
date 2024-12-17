import Image from 'next/image'
import Link from 'next/link'
import { ArrowRight } from 'lucide-react'
import Layout from './components/layout'

export default function LandingPage() {
  return (
    <Layout>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-gray-100 to-gray-200 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="md:w-1/2 mb-10 md:mb-0">
              <h1 className="text-4xl md:text-5xl font-bold mb-4 text-gray-800">
                See Beyond the Resume with TalentLens
              </h1>
              <p className="text-xl mb-8 text-gray-600">
                Transform your recruiting process into a precision instrument for discovering exceptional talent.
              </p>
              <Link href="/dashboard" className="bg-indigo-600 text-white px-6 py-3 rounded-md text-lg font-semibold hover:bg-indigo-700 transition-colors inline-flex items-center">
                Get Started
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </div>
            <div className="md:w-1/2">
              <Image
                src="/placeholder.svg"
                alt="TalentLens Dashboard"
                width={600}
                height={400}
                className="rounded-lg shadow-xl"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">Discover Hidden Potential</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                title: "AI-Powered Insights",
                description: "Our advanced algorithms analyze resumes to uncover skills and potential that traditional methods might miss."
              },
              {
                title: "Customizable Criteria",
                description: "Tailor your talent search with customizable evaluation criteria that align with your organization's unique needs."
              },
              {
                title: "Comprehensive Talent Profiles",
                description: "Get a 360-degree view of candidates with detailed profiles that go beyond surface-level information."
              }
            ].map((feature, index) => (
              <div key={index} className="bg-gray-50 p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-4 text-gray-800">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Process Section */}
      <section className="py-20 bg-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">Precision Recruiting Process</h2>
          <div className="relative">
            <div className="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-indigo-200"></div>
            {[
              { title: "Upload Job Description", description: "Start by defining your ideal candidate profile." },
              { title: "Configure AI Settings", description: "Customize TalentLens to focus on your specific recruiting criteria." },
              { title: "Analyze Resumes", description: "Let our AI process and evaluate candidate resumes efficiently." },
              { title: "Review Insights", description: "Explore in-depth analysis and candidate comparisons." },
              { title: "Make Informed Decisions", description: "Use data-driven insights to select the best candidates for interviews." },
              { title: "Refine and Improve", description: "Continuously optimize your recruiting process based on outcomes and feedback." }
            ].map((step, index) => (
              <div key={index} className={`flex items-center mb-8 ${index % 2 === 0 ? 'justify-start' : 'justify-end'}`}>
                <div className={`w-1/2 ${index % 2 === 0 ? 'pr-8 text-right' : 'pl-8'}`}>
                  <div className="bg-white p-6 rounded-lg shadow-sm">
                    <h3 className="text-xl font-semibold mb-2 text-gray-800">{step.title}</h3>
                    <p className="text-gray-600">{step.description}</p>
                  </div>
                </div>
                <div className="absolute left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center text-white font-bold">
                  {index + 1}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-indigo-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Recruiting Process?</h2>
          <p className="text-xl mb-8">Start using TalentLens to discover exceptional talent today.</p>
          <Link href="/dashboard" className="bg-white text-indigo-600 px-8 py-4 rounded-md text-lg font-semibold hover:bg-gray-100 transition-colors inline-flex items-center">
            Get Started
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </section>
    </Layout>
  )
}

