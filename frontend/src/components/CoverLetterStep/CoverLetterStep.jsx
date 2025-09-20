import React from "react";
import { FileText, Wand2, CheckCircle, Award, Send } from "lucide-react";

const CoverLetterStep = ({
  isGeneratingCoverLetter,
  generatedContent,
  consultant,
  openCustomizationModal,
}) => {
  if (isGeneratingCoverLetter) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-indigo-100 to-blue-100 rounded-full mb-6">
              <FileText className="h-10 w-10 text-indigo-600 animate-pulse" />
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-3">
              Generating Cover Letter
            </h2>
            <p className="text-gray-600 mb-8 text-lg">
              AI is crafting a personalized cover letter based on the analysis...
            </p>

            <div className="max-w-md mx-auto">
              <div className="animate-pulse space-y-3">
                {[1, 2, 3, 4, 5, 6].map((i) => (
                  <div
                    key={i}
                    className="h-3 bg-gray-200 rounded-full"
                    style={{ width: `${50 + i * 8}%` }}
                  ></div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        <div className="bg-gradient-to-r from-indigo-600 to-blue-600 p-8 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-3xl font-bold mb-2 flex items-center">
                <FileText className="w-8 h-8 mr-3" />
                Professional Cover Letter
              </h2>
              <p className="text-indigo-100 text-lg">
                AI-generated personalized cover letter for {consultant.name}
              </p>
            </div>
            <button
              onClick={() =>
                openCustomizationModal(
                  "coverletter",
                  generatedContent.coverLetter || "",
                  "Customize Cover Letter"
                )
              }
              className="group inline-flex items-center px-6 py-3 bg-white/20 hover:bg-white/30 text-white border border-white/30 rounded-xl font-medium transition-all duration-200 backdrop-blur-sm"
            >
              <Wand2 className="w-5 h-5 mr-2 group-hover:rotate-12 transition-transform" />
              Customize with AI
            </button>
          </div>
        </div>

        <div className="p-8">
          <div className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-2xl p-8 mb-8 border-2 border-gray-100">
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed text-base">
                {generatedContent.coverLetter || "Cover letter content will appear here..."}
              </pre>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
              <h4 className="font-semibold text-blue-900 mb-4 flex items-center">
                <CheckCircle className="w-5 h-5 mr-2" />
                Cover Letter Features
              </h4>
              <ul className="text-sm text-blue-800 space-y-2">
                <li>• Professional opening addressing hiring manager</li>
                <li>• Skills aligned with job requirements</li>
                <li>• Quantified achievements and experience</li>
                <li>• Company-specific customization</li>
                <li>• Strong closing with call-to-action</li>
              </ul>
            </div>

            <div className="bg-green-50 border border-green-200 rounded-xl p-6">
              <h4 className="font-semibold text-green-900 mb-4 flex items-center">
                <Award className="w-5 h-5 mr-2" />
                Quality Highlights
              </h4>
              <ul className="text-sm text-green-800 space-y-2">
                <li>• Addresses potential concerns proactively</li>
                <li>• Emphasizes relevant technical expertise</li>
                <li>• Shows enthusiasm for the specific role</li>
                <li>• Maintains professional yet personal tone</li>
                <li>• Optimized length for readability</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CoverLetterStep;
