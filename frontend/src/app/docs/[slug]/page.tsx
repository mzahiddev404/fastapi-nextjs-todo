import { Metadata } from 'next';
import Link from 'next/link';
import { Button } from '@/components/ui';

// ISR Configuration - Revalidate every hour
export const revalidate = 3600; // 1 hour in seconds

// Static metadata generation
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const doc = await getDoc(slug);
  
  return {
    title: `${doc.title} - TODO App Documentation`,
    description: doc.description,
  };
}

// Static params generation for ISR
export async function generateStaticParams() {
  const docs = await getAllDocs();
  
  return docs.map((doc) => ({
    slug: doc.slug,
  }));
}

// Server-side data fetching for ISR
async function getDoc(slug: string) {
  // Simulate API call with delay
  await new Promise(resolve => setTimeout(resolve, 100));
  
  const docs = {
    'getting-started': {
      title: 'Getting Started',
      description: 'How to create an account and start managing your tasks',
      content: `# Getting Started with Your TODO App

Welcome to your personal task management system! This guide will help you get up and running in just a few minutes.

## Creating Your Account

1. **Sign Up**: Click "Sign Up" on the login page
2. **Enter Details**: Provide your name, email, and password
3. **Verify**: Check your email for verification (if required)
4. **Login**: Access your personal dashboard

## Your First Task

1. **Click "Add Task"** on your dashboard
2. **Enter Title**: Give your task a clear, descriptive name
3. **Add Description**: Provide more details if needed
4. **Set Due Date**: Choose when you want to complete it
5. **Add Labels**: Categorize your task for better organization
6. **Save**: Your task is now ready!

## Dashboard Overview

- **Task List**: See all your tasks in one place
- **Quick Actions**: Filter by status or view your profile
- **Add Button**: Create new tasks instantly
- **Progress**: Track your productivity

## Pro Tips

- Use clear, actionable task titles
- Set realistic due dates
- Create labels for different projects
- Review your tasks daily
- Celebrate completed tasks!`,
      lastUpdated: new Date().toISOString(),
      category: 'User Guide'
    },
    'task-management': {
      title: 'Task Management',
      description: 'Create, edit, and organize your tasks effectively',
      content: `# Task Management Guide

Master the art of task management with our comprehensive guide to creating, organizing, and completing your tasks.

## Creating Tasks

### Basic Task Creation
1. Click the **"Add Task"** button on your dashboard
2. Enter a clear, actionable title
3. Add a detailed description (optional but recommended)
4. Set a due date to stay on track
5. Choose a priority level (Low, Medium, High)
6. Add relevant labels for organization
7. Click **"Save"** to create your task

### Task Title Best Practices
- Use action verbs: "Write report" instead of "Report"
- Be specific: "Call John about project" instead of "Call John"
- Keep it concise but descriptive
- Make it actionable and clear

## Editing Tasks

### Making Changes
- Click on any task to view details
- Use the **"Edit"** button to modify task information
- Update title, description, due date, or priority
- Add or remove labels as needed
- Changes are saved automatically

### Task Status Management
- **Mark Complete**: Click the checkbox next to any task
- **Mark Pending**: Uncheck completed tasks to reactivate them
- **Delete**: Remove tasks you no longer need
- **Bulk Actions**: Select multiple tasks for batch operations

## Organizing Your Tasks

### Using Labels
- Create custom labels for different projects or categories
- Color-code your labels for visual organization
- Apply multiple labels to a single task
- Filter tasks by specific labels

### Priority Levels
- **High**: Urgent tasks that need immediate attention
- **Medium**: Important tasks with flexible timing
- **Low**: Nice-to-have tasks when you have time

### Due Dates
- Set realistic deadlines for your tasks
- Use the calendar picker for easy date selection
- Overdue tasks are highlighted in red
- Upcoming tasks show in yellow`,
      lastUpdated: new Date().toISOString(),
      category: 'User Guide'
    },
    'labels-and-filtering': {
      title: 'Labels & Filtering',
      description: 'Use labels to organize tasks and filter your view',
      content: `# Labels & Filtering Guide

Learn how to use labels and filtering to organize your tasks and stay focused on what matters most.

## Creating and Managing Labels

### Creating Labels
1. Go to your dashboard
2. Click **"Manage Labels"** (if available)
3. Enter a label name (e.g., "Work", "Personal", "Urgent")
4. Choose a color for visual identification
5. Save your new label

### Label Best Practices
- Use consistent naming conventions
- Keep labels broad but meaningful
- Use colors to group related labels
- Don't create too many labels (5-10 is ideal)

## Applying Labels to Tasks

### When Creating Tasks
- Select relevant labels from the dropdown
- You can apply multiple labels to one task
- Labels help categorize tasks by project, priority, or type

### When Editing Tasks
- Add or remove labels as needed
- Update labels when task priorities change
- Use labels to track task evolution

## Filtering Your Tasks

### Status Filtering
- **Pending Tasks**: View only incomplete tasks
- **Completed Tasks**: See what you've accomplished
- **All Tasks**: View everything in one list

### Label Filtering
- Click on any label to filter tasks
- View tasks for specific projects or categories
- Combine multiple filters for precise views

### Quick Filter Buttons
- Use the **"View Pending"** button for focus
- Click **"View Completed"** to review progress
- Switch between views easily

## Advanced Organization Tips

### Project-Based Organization
- Create labels for each project
- Use consistent naming: "Project-Name" format
- Color-code by project type

### Priority-Based Organization
- Use labels like "Urgent", "Important", "Later"
- Combine with priority levels for double organization
- Create views for different urgency levels

### Time-Based Organization
- Labels like "Today", "This Week", "This Month"
- Help with time management
- Easy to see what needs immediate attention`,
      lastUpdated: new Date().toISOString(),
      category: 'User Guide'
    },
    'tips-and-tricks': {
      title: 'Tips & Tricks',
      description: 'Pro tips to maximize your productivity',
      content: `# Productivity Tips & Tricks

Boost your productivity with these proven strategies and advanced techniques for using your TODO app effectively.

## Daily Task Management

### The 2-Minute Rule
- If a task takes less than 2 minutes, do it immediately
- Don't add it to your task list
- This prevents small tasks from cluttering your view

### Morning Planning
- Review your tasks each morning
- Identify your top 3 priorities for the day
- Focus on high-priority tasks first
- Plan realistic daily goals

### Evening Review
- Check off completed tasks
- Move unfinished tasks to the next day
- Reflect on what went well
- Adjust priorities for tomorrow

## Task Organization Strategies

### The Eisenhower Matrix
Organize tasks by urgency and importance:
- **Urgent & Important**: Do first
- **Important, Not Urgent**: Schedule
- **Urgent, Not Important**: Delegate or minimize
- **Neither**: Consider deleting

### Time Blocking
- Assign specific time slots to tasks
- Use due dates to create time pressure
- Block similar tasks together
- Leave buffer time between tasks

### The Pomodoro Technique
- Work on tasks in 25-minute focused sessions
- Take 5-minute breaks between sessions
- After 4 sessions, take a longer break
- Use task completion as a reward

## Advanced Features

### Label Strategy
- **@Context**: @home, @office, @phone
- **#Project**: #website, #presentation, #meeting
- **!Priority**: !urgent, !important, !low
- **$Time**: $5min, $30min, $2hours

### Task Naming Conventions
- Start with action verbs: "Call", "Write", "Review"
- Be specific: "Call John about budget" vs "Call John"
- Include context: "Write report (marketing)"
- Use consistent formatting

### Regular Maintenance
- **Weekly**: Review and clean up old tasks
- **Monthly**: Evaluate your label system
- **Quarterly**: Assess your productivity patterns
- **Annually**: Reset and reorganize completely

## Productivity Hacks

### The "Eat the Frog" Method
- Do your most difficult task first thing in the morning
- Get it out of the way early
- Build momentum for the rest of the day

### Batch Similar Tasks
- Group similar activities together
- Handle all phone calls at once
- Process all emails in one session
- Reduce context switching

### Use the 80/20 Rule
- Focus on the 20% of tasks that give 80% of results
- Identify your most impactful activities
- Prioritize these tasks above all others

### Celebrate Small Wins
- Check off completed tasks immediately
- Acknowledge your progress
- Use completion as motivation
- Track your daily accomplishments`,
      lastUpdated: new Date().toISOString(),
      category: 'User Guide'
    }
  };
  
  return docs[slug as keyof typeof docs] || {
    title: 'Page Not Found',
    description: 'The requested documentation page was not found',
    content: '# Page Not Found\n\nThe requested documentation page was not found.',
    lastUpdated: new Date().toISOString(),
    category: 'Error'
  };
}

async function getAllDocs() {
  return [
    { slug: 'getting-started' },
    { slug: 'features' },
    { slug: 'api' }
  ];
}

// ISR Server Component - This page is statically generated and revalidated
export default async function DocPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const doc = await getDoc(slug);
  
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
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-500">
                Last updated: {new Date(doc.lastUpdated).toLocaleDateString()}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-8">
              {/* Help Banner */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
                <h3 className="text-lg font-semibold text-blue-900 mb-2">
                  💡 Need Help?
                </h3>
                <p className="text-blue-800 mb-2">
                  Can't find what you're looking for? Check out our other guides or contact support.
                </p>
                <div className="text-sm text-blue-700">
                  <p><strong>Quick Links:</strong></p>
                  <ul className="list-disc list-inside space-y-1 mt-1">
                    <li>Getting Started - Basic setup and first steps</li>
                    <li>Task Management - Creating and organizing tasks</li>
                    <li>Labels & Filtering - Advanced organization</li>
                    <li>Tips & Tricks - Productivity strategies</li>
                  </ul>
                </div>
              </div>

              {/* Document content */}
              <div className="prose prose-lg max-w-none">
                <h1 className="text-3xl font-bold text-gray-900 mb-4">
                  {doc.title}
                </h1>
                
                <div className="flex items-center space-x-4 mb-6 text-sm text-gray-500">
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                    {doc.category}
                  </span>
                  <span>Last updated: {new Date(doc.lastUpdated).toLocaleString()}</span>
                </div>
                
                <div className="whitespace-pre-wrap text-gray-700">
                  {doc.content}
                </div>
              </div>

              {/* Navigation */}
              <div className="mt-8 pt-6 border-t border-gray-200">
                <div className="flex items-center justify-between">
                  <Link href="/docs">
                    <Button variant="secondary">
                      All Documentation
                    </Button>
                  </Link>
                  
                  <div className="flex items-center space-x-4">
                    <Link href="/features">
                      <Button variant="secondary">
                        Features
                      </Button>
                    </Link>
                    <Link href="/">
                      <Button variant="primary">
                        Back to Dashboard
                      </Button>
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
