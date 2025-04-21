import type React from "react";
import type { InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  icon?: React.ReactNode;
}

export const Input: React.FC<InputProps> = ({ className, icon, ...props }) => {
  return (
    <div className="relative">
      {icon && (
        <div className="pointer-events-none absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2">
          {icon}
        </div>
      )}
      <input
        className={`w-full rounded-xl border border-gray-300 px-4 py-2 text-sm text-gray-700 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 sm:py-3 sm:text-base ${icon ? "pl-11" : ""} ${className}`}
        {...props}
      />
    </div>
  );
};
