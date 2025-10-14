"use client";

import { useRouter } from "next/navigation";
import { Card, CardHeader, CardContent, Button } from "@/components/ui";
import { Task } from "@/types";
import { useLabels } from "@/hooks/useLabels";

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
  const { labels } = useLabels();

  // Helper function to get label name by ID
  const getLabelName = (labelId: string) => {
    const label = labels.find(l => l.id === labelId);
    return label ? label.name : labelId;
  };

  // Helper function to get label color by ID  
  const getLabelColor = (labelId: string) => {
    const label = labels.find(l => l.id === labelId);
    return label ? label.color : "#3B82F6";
  };

  // Handle task title click to navigate to detail page
  const handleTaskClick = (task: Task) => {
    router.push(`/tasks/${task.id}`);
  };
  return (
    <div className="transform hover:scale-[1.01] transition-transform duration-300">
    <Card className="shadow-[0_25px_80px_-15px_rgba(59,130,246,0.5)] border-2 border-blue-200/50 bg-white/95 backdrop-blur-xl rounded-2xl overflow-hidden relative group hover:border-blue-300 hover:shadow-[0_30px_90px_-15px_rgba(59,130,246,0.6)] transition-all duration-500">
      {/* Animated gradient overlay for depth */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-100/60 via-cyan-100/40 to-indigo-100/60 opacity-60 pointer-events-none"></div>
      {/* Shine effect */}
      <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 pointer-events-none"></div>
      
      <CardHeader className="border-b-2 border-blue-200/50 bg-gradient-to-r from-blue-100/80 via-cyan-100/60 to-indigo-100/80 p-4 sm:p-6 relative z-10">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 sm:gap-0">
          <div className="flex-1 min-w-0">
            <h3 className="text-xl sm:text-2xl font-bold text-gray-900 mb-1 truncate">
              Your Tasks
            </h3>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="inline-flex items-center px-2 sm:px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
              </span>
              <span className="text-gray-400 hidden xs:inline">•</span>
              <span className="text-xs sm:text-sm text-gray-600 hidden xs:inline">{tasks.filter(t => t.status === 'complete').length} completed</span>
            </div>
          </div>
          <Button 
            size="sm" 
            onClick={onCreateTask}
            className="w-full sm:w-auto bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all duration-200 border-0 text-sm"
            aria-label="Create a new task"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            New Task
          </Button>
        </div>
      </CardHeader>
      <CardContent className="p-0 relative z-10">
        {tasks.length === 0 ? (
          <div className="text-center py-16 px-4 relative">
            <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full flex items-center justify-center shadow-xl shadow-indigo-200/50">
              <svg className="w-10 h-10 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h4 className="text-2xl font-bold text-gray-900 mb-3">No tasks yet</h4>
            <p className="text-gray-600 mb-8 max-w-sm mx-auto">Ready to be productive? Create your first task and start organizing your day!</p>
            <Button 
              onClick={onCreateTask}
              className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all duration-200 border-0"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Create Your First Task
            </Button>
          </div>
        ) : (
          <div className="divide-y divide-gray-50" role="list" aria-label="Task list">
            {tasks.map((task) => (
              <div
                key={task.id}
                className={`p-3 sm:p-4 md:p-5 transition-all duration-500 border-l-[6px] relative group/task ${
                  task.status === 'complete' 
                    ? 'bg-gradient-to-r from-gray-100/60 to-slate-100/40 opacity-70 border-l-gray-400' 
                    : 'bg-gradient-to-r from-white/80 to-blue-50/30 hover:from-indigo-50/60 hover:to-purple-50/60 border-l-transparent hover:border-l-indigo-500 hover:scale-[1.02] hover:shadow-[0_10px_40px_-10px_rgba(79,70,229,0.3)] hover:pl-6'
                }`}
                role="listitem"
                aria-label={`Task: ${task.title}, Status: ${task.status}, Priority: ${task.priority}`}
              >
                {/* Task item shine effect */}
                {task.status !== 'complete' && (
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover/task:translate-x-full transition-transform duration-700 pointer-events-none"></div>
                )}
                <div className="flex items-start justify-between gap-2 sm:gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start space-x-2 sm:space-x-3">
                      <div className="flex-shrink-0 mt-0.5 sm:mt-1">
                        <button
                          onClick={(e) => {
                            e.stopPropagation(); // Prevent task detail navigation
                            onToggleTaskStatus(task);
                          }}
                          className={`w-5 h-5 sm:w-6 sm:h-6 rounded-md sm:rounded-lg border-2 flex items-center justify-center transition-all duration-200 shadow-sm ${
                            task.status === 'complete'
                              ? 'bg-gradient-to-br from-emerald-500 to-teal-500 border-emerald-500 text-white shadow-emerald-200'
                              : 'border-gray-300 hover:border-indigo-400 hover:bg-indigo-50 hover:shadow-md'
                          }`}
                          aria-label={`${task.status === "complete" ? "Mark as pending" : "Mark as complete"} task: ${task.title}`}
                          type="button"
                        >
                          {task.status === 'complete' && (
                            <svg className="w-3 h-3 sm:w-4 sm:h-4" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          )}
                        </button>
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <h4 
                          className={`text-base sm:text-lg font-semibold cursor-pointer hover:text-indigo-600 transition-colors break-words ${
                            task.status === 'complete' 
                              ? 'line-through text-gray-400' 
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
                          <p className="text-xs sm:text-sm text-gray-600 mt-1.5 sm:mt-2 line-clamp-2 leading-relaxed break-words">{task.description}</p>
                        )}
                        
                        <div className="flex items-center gap-2 mt-3 flex-wrap">
                          <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold shadow-sm ${
                            task.priority === 'high' 
                              ? 'bg-gradient-to-r from-red-500 to-pink-500 text-white'
                              : task.priority === 'medium'
                              ? 'bg-gradient-to-r from-amber-400 to-orange-400 text-white'
                              : 'bg-gradient-to-r from-emerald-400 to-teal-400 text-white'
                          }`}>
                            <span className="w-1.5 h-1.5 rounded-full bg-white mr-1.5"></span>
                            {task.priority.toUpperCase()}
                          </span>
                          
                          {task.deadline && (
                            <span className="inline-flex items-center px-2.5 py-1 bg-gray-100 rounded-lg text-xs font-medium text-gray-700">
                              <svg className="w-3.5 h-3.5 mr-1.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                              </svg>
                              {new Date(task.deadline).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                            </span>
                          )}
                          
                          {task.labels && task.labels.length > 0 && (
                            <div className="flex items-center gap-1.5">
                              {task.labels.slice(0, 3).map((labelId, index) => {
                                const labelName = getLabelName(labelId);
                                const labelColor = getLabelColor(labelId);
                                return (
                                  <span
                                    key={labelId || index}
                                    className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold shadow-sm max-w-full"
                                    style={{
                                      backgroundColor: `${labelColor}15`,
                                      color: labelColor,
                                      borderWidth: '1.5px',
                                      borderColor: labelColor
                                    }}
                                  >
                                    <span className="w-1.5 h-1.5 rounded-full mr-1.5 flex-shrink-0" style={{ backgroundColor: labelColor }}></span>
                                    <span className="truncate">{labelName}</span>
                                  </span>
                                );
                              })}
                              {task.labels.length > 3 && (
                                <span className="text-xs font-medium text-gray-500 px-2">
                                  +{task.labels.length - 3} more
                                </span>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2 ml-4" role="group" aria-label={`Actions for task: ${task.title}`}>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => onEditTask(task)}
                      className="text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 p-2.5 rounded-lg transition-all duration-200"
                      aria-label={`Edit task: ${task.title}`}
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => onDeleteTask(task)}
                      className="text-gray-400 hover:text-red-600 hover:bg-red-50 p-2.5 rounded-lg transition-all duration-200"
                      aria-label={`Delete task: ${task.title}`}
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
    </div>
  );
}
