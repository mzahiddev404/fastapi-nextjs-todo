import { Metadata } from 'next';
import Link from 'next/link';
import { Button } from '@/components/ui';

// ISR Configuration - Revalidate every 2 hours
export const revalidate = 7200; // 2 hours in seconds

// Static metadata
export const metadata: Metadata = {
  title: 'Documentation - TODO App',
  description: 'Complete documentation for the TODO application',
};

// Server-side data fetching for ISR
async function getDocs() {
  // Simulate API call with delay
  await new Promise(resolve => setTimeout(resolve, 100));
  
  return [
    {
      slug: 'getting-started',
      title: 'Getting Started',
      description: 'How to create an account and start managing your tasks',
      category: 'User Guide',
      lastUpdated: new Date().toISOString(),
      readTime: '3 min read'
    },
    {
      slug: 'task-management',
      title: 'Task Management',
      description: 'Create, edit, and organize your tasks effectively',
      category: 'User Guide',
      lastUpdated: new Date().toISOString(),
      readTime: '5 min read'
    },
    {
      slug: 'labels-and-filtering',
      title: 'Labels & Filtering',
      description: 'Use labels to organize tasks and filter your view',
      category: 'User Guide',
      lastUpdated: new Date().toISOString(),
      readTime: '4 min read'
    },
    {
      slug: 'tips-and-tricks',
      title: 'Tips & Tricks',
      description: 'Pro tips to maximize your productivity',
      category: 'User Guide',
      lastUpdated: new Date().toISOString(),
      readTime: '3 min read'
    }
  ];
}

// ISR Server Component - This page is statically generated and revalidated
export default async function DocsPage() {
  const docs = await getDocs();
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link href="/" className="flex items-center space-x-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                <span>Back to Dashboard</span>
              </Link>
              <h1 className="text-xl font-semibold text-gray-900">Documentation</h1>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-6xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Welcome Banner */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-8">
            <h3 className="text-lg font-semibold text-green-900 mb-2">
              📚 User Documentation
            </h3>
            <p className="text-green-800 mb-4">
              Everything you need to know to get the most out of your TODO app. 
              From basic setup to advanced productivity tips.
            </p>
            <div className="text-sm text-green-700">
              <p><strong>Quick Start:</strong></p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>Create your account and start adding tasks</li>
                <li>Use labels to organize your work</li>
                <li>Filter tasks by status to stay focused</li>
                <li>Set due dates to meet your deadlines</li>
              </ul>
            </div>
          </div>

          {/* Page header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              User Guide
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Learn how to use your TODO app effectively. From creating your first task 
              to advanced productivity techniques.
            </p>
          </div>

          {/* Documentation grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            {docs.map((doc) => (
              <Link
                key={doc.slug}
                href={`/docs/${doc.slug}`}
                className="group bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 p-6"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                      {doc.title}
                    </h3>
                    <p className="text-gray-600 text-sm mt-1">
                      {doc.description}
                    </p>
                  </div>
                  <svg 
                    className="w-5 h-5 text-gray-400 group-hover:text-blue-500 transition-colors" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded-full">
                    {doc.category}
                  </span>
                  <span>{doc.readTime}</span>
                </div>
                
                <div className="mt-3 text-xs text-gray-400">
                  Last updated: {new Date(doc.lastUpdated).toLocaleDateString()}
                </div>
              </Link>
            ))}
          </div>

          {/* App Features Overview */}
          <div className="bg-white rounded-lg shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              App Features Overview
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium mb-3">
                  Task Management
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Create & Edit Tasks</h3>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Add detailed task descriptions</li>
                  <li>• Set due dates and priorities</li>
                  <li>• Mark tasks as complete</li>
                  <li>• Edit or delete anytime</li>
                </ul>
              </div>
              
              <div className="text-center">
                <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium mb-3">
                  Organization
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Labels & Categories</h3>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Create custom labels</li>
                  <li>• Color-code your tasks</li>
                  <li>• Filter by categories</li>
                  <li>• Stay organized</li>
                </ul>
              </div>
              
              <div className="text-center">
                <div className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium mb-3">
                  Filtering
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Smart Views</h3>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• View pending tasks</li>
                  <li>• See completed work</li>
                  <li>• Filter by labels</li>
                  <li>• Focus on what matters</li>
                </ul>
              </div>
              
              <div className="text-center">
                <div className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium mb-3">
                  Productivity
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Stay Focused</h3>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Track your progress</li>
                  <li>• Set realistic goals</li>
                  <li>• Monitor completion rates</li>
                  <li>• Boost productivity</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Call to action */}
          <div className="text-center">
            <div className="bg-white rounded-lg shadow-md p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Ready to Boost Your Productivity?
              </h3>
              <p className="text-gray-600 mb-6">
                Start organizing your tasks and achieving your goals with our simple yet powerful TODO app.
              </p>
              <div className="flex items-center justify-center space-x-4">
                <Link href="/docs/getting-started">
                  <Button variant="primary" size="lg">
                    Start Here
                  </Button>
                </Link>
                <Link href="/">
                  <Button variant="secondary" size="lg">
                    Go to Dashboard
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
