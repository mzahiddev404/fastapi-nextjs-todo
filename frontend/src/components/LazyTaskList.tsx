"use client";

import React, { useState, useCallback, useMemo } from 'react';
import { Task } from '@/types';
import { TaskList } from './TaskList';
import { LoadingSpinner } from './ui/LoadingSpinner';

interface LazyTaskListProps {
  tasks: Task[];
  onEditTask: (task: Task) => void;
  onToggleTaskStatus: (task: Task) => void;
  onDeleteTask: (task: Task) => void;
  onCreateTask: () => void;
  itemsPerPage?: number;
}

export function LazyTaskList({
  tasks,
  onEditTask,
  onToggleTaskStatus,
  onDeleteTask,
  onCreateTask,
  itemsPerPage = 10
}: LazyTaskListProps) {
  const [currentPage, setCurrentPage] = useState(1);
  const [isLoading, setIsLoading] = useState(false);

  // Memoize paginated tasks to avoid unnecessary recalculations
  const paginatedTasks = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return tasks.slice(startIndex, endIndex);
  }, [tasks, currentPage, itemsPerPage]);

  // Memoize total pages calculation
  const totalPages = useMemo(() => {
    return Math.ceil(tasks.length / itemsPerPage);
  }, [tasks.length, itemsPerPage]);

  // Memoize pagination info
  const paginationInfo = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage + 1;
    const endIndex = Math.min(currentPage * itemsPerPage, tasks.length);
    return { startIndex, endIndex, total: tasks.length };
  }, [currentPage, itemsPerPage, tasks.length]);

  // Simulate loading delay for better UX
  const handlePageChange = useCallback(async (newPage: number) => {
    if (newPage < 1 || newPage > totalPages) return;
    
    setIsLoading(true);
    
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 300));
    
    setCurrentPage(newPage);
    setIsLoading(false);
  }, [totalPages]);

  // Memoize pagination handlers
  const goToNextPage = useCallback(() => {
    handlePageChange(currentPage + 1);
  }, [currentPage, handlePageChange]);

  const goToPreviousPage = useCallback(() => {
    handlePageChange(currentPage - 1);
  }, [currentPage, handlePageChange]);

  const goToPage = useCallback((page: number) => {
    handlePageChange(page);
  }, [handlePageChange]);

  // Generate page numbers for pagination
  const pageNumbers = useMemo(() => {
    const pages = [];
    const maxVisiblePages = 5;
    
    if (totalPages <= maxVisiblePages) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      const startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
      const endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
      
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }
    }
    
    return pages;
  }, [currentPage, totalPages]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <LoadingSpinner size="lg" text="Loading tasks..." />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <TaskList
        tasks={paginatedTasks}
        onEditTask={onEditTask}
        onToggleTaskStatus={onToggleTaskStatus}
        onDeleteTask={onDeleteTask}
        onCreateTask={onCreateTask}
      />
      
      {totalPages > 1 && (
        <div className="flex items-center justify-between px-4 py-3 bg-white border-t border-gray-200">
          <div className="flex-1 flex justify-between sm:hidden">
            <button
              onClick={goToPreviousPage}
              disabled={currentPage === 1}
              className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <button
              onClick={goToNextPage}
              disabled={currentPage === totalPages}
              className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
          
          <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-gray-700">
                Showing{' '}
                <span className="font-medium">{paginationInfo.startIndex}</span>
                {' '}to{' '}
                <span className="font-medium">{paginationInfo.endIndex}</span>
                {' '}of{' '}
                <span className="font-medium">{paginationInfo.total}</span>
                {' '}results
              </p>
            </div>
            
            <div>
              <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button
                  onClick={goToPreviousPage}
                  disabled={currentPage === 1}
                  className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span className="sr-only">Previous</span>
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
                
                {pageNumbers.map((page) => (
                  <button
                    key={page}
                    onClick={() => goToPage(page)}
                    className={`relative inline-flex items-center px-4 py-2 border text-sm font-medium ${
                      page === currentPage
                        ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                        : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                    }`}
                  >
                    {page}
                  </button>
                ))}
                
                <button
                  onClick={goToNextPage}
                  disabled={currentPage === totalPages}
                  className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span className="sr-only">Next</span>
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
