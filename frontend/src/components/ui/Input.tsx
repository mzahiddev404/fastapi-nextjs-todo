// Reusable Input component with consistent styling and accessibility
import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  required?: boolean;
}

export function Input({
  label,
  error,
  helperText,
  className = "",
  id,
  required,
  ...props
}: InputProps) {
  const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
  
  const baseClasses = "block w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-0 sm:text-sm transition-colors";
  
  const stateClasses = error
    ? "border-red-300 focus:ring-red-500 focus:border-red-500"
    : "border-gray-300 focus:ring-indigo-500 focus:border-indigo-500";

  return (
    <div className="space-y-1">
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-gray-700"
        >
          {label}
          {required && <span className="text-red-500 ml-1" aria-label="required">*</span>}
        </label>
      )}
      <input
        id={inputId}
        className={`${baseClasses} ${stateClasses} ${className}`}
        aria-invalid={error ? "true" : "false"}
        aria-describedby={error ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined}
        required={required}
        {...props}
      />
      {error && (
        <p id={`${inputId}-error`} className="text-sm text-red-600" role="alert" aria-live="polite">
          {error}
        </p>
      )}
      {helperText && !error && (
        <p id={`${inputId}-helper`} className="text-sm text-gray-500">
          {helperText}
        </p>
      )}
    </div>
  );
}
