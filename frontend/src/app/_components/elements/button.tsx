import type React from "react";
import type { ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  className,
  ...props
}) => {
  return (
    <button
      className={`transform rounded-xl bg-blue-600 px-4 py-2 text-sm font-semibold text-white transition duration-300 ease-in-out hover:scale-105 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 sm:py-3 sm:text-base ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};
