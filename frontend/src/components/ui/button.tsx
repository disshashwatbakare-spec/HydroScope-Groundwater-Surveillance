import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "destructive" | "teal";
  size?: "xs" | "sm" | "md" | "lg";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", ...props }, ref) => {
    const base =
      "inline-flex items-center justify-center gap-1.5 font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-1 focus-visible:ring-offset-[#080E1A] disabled:pointer-events-none disabled:opacity-50 select-none cursor-pointer";

    const variants = {
      primary:
        "bg-blue-600 text-white hover:bg-blue-500 border border-blue-500/40 shadow-sm shadow-blue-600/20 active:scale-[0.98]",
      secondary:
        "bg-white/8 text-white hover:bg-white/12 border border-white/12 shadow-xs active:scale-[0.98]",
      outline:
        "bg-transparent text-slate-300 hover:text-white hover:bg-white/5 border border-white/15 active:scale-[0.98]",
      ghost:
        "bg-transparent text-slate-400 hover:text-white hover:bg-white/5",
      destructive:
        "bg-rose-600 text-white hover:bg-rose-500 border border-rose-500/40 shadow-xs shadow-rose-600/20 active:scale-[0.98]",
      teal:
        "bg-teal-600 text-white hover:bg-teal-500 border border-teal-500/40 shadow-xs shadow-teal-600/20 active:scale-[0.98]",
    };

    const sizes = {
      xs: "text-xs px-2.5 py-1 rounded-lg",
      sm: "text-xs px-3 py-1.5 rounded-lg",
      md: "text-sm px-4 py-2 rounded-xl",
      lg: "text-sm px-5 py-2.5 rounded-xl font-semibold",
    };

    return (
      <button
        ref={ref}
        className={cn(base, variants[variant], sizes[size], className)}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";
