/**
 * @jest-environment jsdom
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { TaskList } from '../TaskList';
import { Task } from '@/types';

// Mock the useRouter hook
const mockPush = jest.fn();
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

// Mock tasks data
const mockTasks: Task[] = [
  {
    id: '1',
    title: 'Test Task 1',
    description: 'Test description 1',
    status: 'pending',
    priority: 'high',
    due_date: '2024-01-15',
    labels: [
      { id: '1', name: 'Work', color: '#ff0000' }
    ],
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
    user_id: 'user1'
  },
  {
    id: '2',
    title: 'Test Task 2',
    description: 'Test description 2',
    status: 'completed',
    priority: 'medium',
    due_date: '2024-01-20',
    labels: [
      { id: '2', name: 'Personal', color: '#00ff00' }
    ],
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
    user_id: 'user1'
  }
];

const mockProps = {
  tasks: mockTasks,
  onEditTask: jest.fn(),
  onToggleTaskStatus: jest.fn(),
  onDeleteTask: jest.fn(),
  onCreateTask: jest.fn(),
};

describe('TaskList Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders task list with tasks', () => {
    render(<TaskList {...mockProps} />);
    
    expect(screen.getByText('Tasks')).toBeInTheDocument();
    expect(screen.getByText('2 tasks total')).toBeInTheDocument();
    expect(screen.getByText('Test Task 1')).toBeInTheDocument();
    expect(screen.getByText('Test Task 2')).toBeInTheDocument();
  });

  it('renders empty state when no tasks', () => {
    render(<TaskList {...mockProps} tasks={[]} />);
    
    expect(screen.getByText('No tasks yet')).toBeInTheDocument();
    expect(screen.getByText('Get started by creating your first task')).toBeInTheDocument();
    expect(screen.getByText('Create First Task')).toBeInTheDocument();
  });

  it('calls onCreateTask when create button is clicked', () => {
    render(<TaskList {...mockProps} />);
    
    const createButton = screen.getByText('New Task');
    fireEvent.click(createButton);
    
    expect(mockProps.onCreateTask).toHaveBeenCalledTimes(1);
  });

  it('calls onToggleTaskStatus when checkbox is clicked', () => {
    render(<TaskList {...mockProps} />);
    
    const checkboxes = screen.getAllByRole('button', { name: /mark as/i });
    fireEvent.click(checkboxes[0]);
    
    expect(mockProps.onToggleTaskStatus).toHaveBeenCalledWith(mockTasks[0]);
  });

  it('calls onEditTask when edit button is clicked', () => {
    render(<TaskList {...mockProps} />);
    
    const editButtons = screen.getAllByRole('button', { name: /edit task/i });
    fireEvent.click(editButtons[0]);
    
    expect(mockProps.onEditTask).toHaveBeenCalledWith(mockTasks[0]);
  });

  it('calls onDeleteTask when delete button is clicked', () => {
    render(<TaskList {...mockProps} />);
    
    const deleteButtons = screen.getAllByRole('button', { name: /delete task/i });
    fireEvent.click(deleteButtons[0]);
    
    expect(mockProps.onDeleteTask).toHaveBeenCalledWith(mockTasks[0]);
  });

  it('navigates to task detail when task title is clicked', () => {
    render(<TaskList {...mockProps} />);
    
    const taskTitle = screen.getByText('Test Task 1');
    fireEvent.click(taskTitle);
    
    expect(mockPush).toHaveBeenCalledWith('/tasks/1');
  });

  it('displays task priority correctly', () => {
    render(<TaskList {...mockProps} />);
    
    expect(screen.getByText('high')).toBeInTheDocument();
    expect(screen.getByText('medium')).toBeInTheDocument();
  });

  it('displays task labels correctly', () => {
    render(<TaskList {...mockProps} />);
    
    expect(screen.getByText('Work')).toBeInTheDocument();
    expect(screen.getByText('Personal')).toBeInTheDocument();
  });

  it('displays due date correctly', () => {
    render(<TaskList {...mockProps} />);
    
    expect(screen.getByText('1/15/2024')).toBeInTheDocument();
    expect(screen.getByText('1/20/2024')).toBeInTheDocument();
  });

  it('shows completed task with strikethrough', () => {
    render(<TaskList {...mockProps} />);
    
    const completedTask = screen.getByText('Test Task 2');
    expect(completedTask).toHaveClass('line-through');
  });

  it('handles keyboard navigation for task titles', () => {
    render(<TaskList {...mockProps} />);
    
    const taskTitle = screen.getByText('Test Task 1');
    
    // Test Enter key
    fireEvent.keyDown(taskTitle, { key: 'Enter' });
    expect(mockPush).toHaveBeenCalledWith('/tasks/1');
    
    // Test Space key
    fireEvent.keyDown(taskTitle, { key: ' ' });
    expect(mockPush).toHaveBeenCalledWith('/tasks/1');
  });

  it('shows correct task count', () => {
    render(<TaskList {...mockProps} tasks={mockTasks} />);
    expect(screen.getByText('2 tasks total')).toBeInTheDocument();
    
    render(<TaskList {...mockProps} tasks={[mockTasks[0]]} />);
    expect(screen.getByText('1 task total')).toBeInTheDocument();
  });
});
