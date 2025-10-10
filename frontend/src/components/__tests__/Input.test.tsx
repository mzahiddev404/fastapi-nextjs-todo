// Input component tests
import { render, screen, fireEvent } from '@testing-library/react';
import { Input } from '../ui/Input';

describe('Input Component', () => {
  it('renders input with label', () => {
    render(<Input label="Test Label" />);
    expect(screen.getByLabelText(/test label/i)).toBeInTheDocument();
  });

  it('shows error message when error prop is provided', () => {
    render(<Input label="Test" error="This is an error" />);
    expect(screen.getByText('This is an error')).toBeInTheDocument();
    expect(screen.getByRole('alert')).toBeInTheDocument();
  });

  it('shows helper text when provided', () => {
    render(<Input label="Test" helperText="This is helper text" />);
    expect(screen.getByText('This is helper text')).toBeInTheDocument();
  });

  it('shows required indicator when required', () => {
    render(<Input label="Test" required />);
    expect(screen.getByText('*')).toBeInTheDocument();
  });

  it('handles value changes', () => {
    const handleChange = jest.fn();
    render(<Input label="Test" onChange={handleChange} />);
    
    const input = screen.getByLabelText(/test/i);
    fireEvent.change(input, { target: { value: 'new value' } });
    expect(handleChange).toHaveBeenCalled();
  });

  it('has proper accessibility attributes', () => {
    render(<Input label="Test" error="Error message" />);
    const input = screen.getByLabelText(/test/i);
    expect(input).toHaveAttribute('aria-invalid', 'true');
    expect(input).toHaveAttribute('aria-describedby');
  });
});
