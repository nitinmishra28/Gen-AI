import React from "react";
import { CheckCircle } from "lucide-react";

const ProgressBar = ({ currentStep, steps, onStepClick }) => {
  return (
    <div className="w-full bg-white/80 backdrop-blur-sm border-b border-gray-200 px-6 py-6 sticky top-0 z-40">
      <div className="flex items-center justify-between max-w-6xl mx-auto">
        {steps.map((step, index) => (
          <div key={step.id} className="flex items-center">
            <div
              className={`flex flex-col items-center group ${
                onStepClick && step.completed ? "cursor-pointer" : ""
              }`}
              onClick={() =>
                onStepClick && step.completed && onStepClick(step.id)
              }
            >
              <div
                className={`flex items-center justify-center w-12 h-12 rounded-full border-2 transition-all duration-300 ${
                  step.completed
                    ? "bg-gradient-to-r from-green-500 to-emerald-500 border-green-500 text-white shadow-lg shadow-green-500/30"
                    : currentStep === step.id
                    ? "bg-gradient-to-r from-blue-500 to-indigo-500 border-blue-500 text-white shadow-lg shadow-blue-500/30"
                    : "bg-white border-gray-300 text-gray-400 shadow-sm"
                } ${
                  onStepClick && step.completed
                    ? "group-hover:scale-110 group-hover:shadow-xl"
                    : ""
                }`}
              >
                {step.completed ? (
                  <CheckCircle className="w-6 h-6" />
                ) : (
                  <div className="w-6 h-6 rounded-full bg-current opacity-50" />
                )}
              </div>
              <span
                className={`mt-3 text-sm font-medium transition-colors ${
                  currentStep === step.id
                    ? "text-blue-600"
                    : step.completed
                    ? "text-green-600"
                    : "text-gray-500"
                }`}
              >
                {step.label}
              </span>
            </div>
            {index < steps.length - 1 && (
              <div
                className={`w-20 h-1 mx-6 rounded-full transition-all duration-500 ${
                  steps[index + 1].completed
                    ? "bg-gradient-to-r from-green-500 to-emerald-500 shadow-sm"
                    : "bg-gray-200"
                }`}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProgressBar;
