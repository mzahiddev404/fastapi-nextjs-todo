"use client";

import { useRouter } from "next/navigation";
import { Card, CardHeader, CardContent, Button } from "@/components/ui";
import { Task } from "@/types";

interface TaskListProps {
  tasks: Task[];
  onEditTask: (task: Task) => void;
  onToggleTaskStatus: (task: Task) => void;
  onDeleteTask: (task: Task) => void;
  onCreateTask: () => void;
}

export function TaskList({ 
  tasks, 
  onEditTask, 
  onToggleTaskStatus, 
  onDeleteTask, 
  onCreateTask 
}: TaskListProps) {
  const router = useRouter();

  // Handle task title click to navigate to detail page
  const handleTaskClick = (task: Task) => {
    router.push(`/tasks/${task.id}`);
  };
  return (
    <Card className="shadow-sm">
      <CardHeader className="border-b border-gray-100">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              Tasks
            </h3>
            <p className="text-sm text-gray-500 mt-1">
              {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'} total
            </p>
          </div>
          <Button 
            size="sm" 
            onClick={onCreateTask}
            className="bg-blue-600 hover:bg-blue-700 text-white"
            aria-label="Create a new task"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            New Task
          </Button>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        {tasks.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h4 className="text-lg font-medium text-gray-900 mb-2">No tasks yet</h4>
            <p className="text-gray-500 mb-6">Get started by creating your first task</p>
            <Button 
              onClick={onCreateTask}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Create First Task
            </Button>
          </div>
        ) : (
          <div className="divide-y divide-gray-100" role="list" aria-label="Task list">
            {tasks.map((task) => (
              <div
                key={task.id}
                className={`p-4 hover:bg-gray-50 transition-colors ${
                  task.status === 'completed' 
                    ? 'bg-gray-50/50' 
                    : 'bg-white'
                }`}
                role="listitem"
                aria-label={`Task: ${task.title}, Status: ${task.status}, Priority: ${task.priority}`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0 mt-1">
                        <button
                          onClick={() => onToggleTaskStatus(task)}
                          className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
                            task.status === 'completed'
                              ? 'bg-green-500 border-green-500 text-white'
                              : 'border-gray-300 hover:border-green-400'
                          }`}
                          aria-label={`${task.status === "completed" ? "Mark as pending" : "Mark as complete"} task: ${task.title}`}
                        >
                          {task.status === 'completed' && (
                            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          )}
                        </button>
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <h4 
                          className={`font-medium cursor-pointer hover:text-blue-600 transition-colors ${
                            task.status === 'completed' 
                              ? 'line-through text-gray-500' 
                              : 'text-gray-900'
                          }`}
                          onClick={() => handleTaskClick(task)}
                          role="button"
                          tabIndex={0}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter' || e.key === ' ') {
                              e.preventDefault();
                              handleTaskClick(task);
                            }
                          }}
                          aria-label={`View details for task: ${task.title}`}
                        >
                          {task.title}
                        </h4>
                        
                        {task.description && (
                          <p className="text-sm text-gray-600 mt-1 line-clamp-2">{task.description}</p>
                        )}
                        
                        <div className="flex items-center space-x-3 mt-3">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            task.priority === 'high' 
                              ? 'bg-red-100 text-red-800'
                              : task.priority === 'medium'
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-green-100 text-green-800'
                          }`}>
                            {task.priority}
                          </span>
                          
                          {task.due_date && (
                            <span className="inline-flex items-center text-xs text-gray-500">
                              <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                              </svg>
                              {new Date(task.due_date).toLocaleDateString()}
                            </span>
                          )}
                          
                          {task.labels && task.labels.length > 0 && (
                            <div className="flex items-center space-x-1">
                              {task.labels.slice(0, 3).map((label, index) => (
                                <span
                                  key={index}
                                  className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                                  style={{ backgroundColor: label.color + '20', color: label.color }}
                                >
                                  {label.name}
                                </span>
                              ))}
                              {task.labels.length > 3 && (
                                <span className="text-xs text-gray-500">
                                  +{task.labels.length - 3} more
                                </span>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-1 ml-4" role="group" aria-label={`Actions for task: ${task.title}`}>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => onEditTask(task)}
                      className="text-gray-400 hover:text-gray-600 p-2"
                      aria-label={`Edit task: ${task.title}`}
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => onDeleteTask(task)}
                      className="text-gray-400 hover:text-red-600 p-2"
                      aria-label={`Delete task: ${task.title}`}
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
