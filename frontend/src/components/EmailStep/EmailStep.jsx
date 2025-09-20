import React from "react";
import { Mail, Wand2, Send, CheckCircle, ArrowRight } from "lucide-react";

const EmailStep = ({
  isGeneratingEmail,
  generatedContent,
  consultant,
  openCustomizationModal,
  setCurrentStep,
}) => {
  if (isGeneratingEmail) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-green-100 to-emerald-100 rounded-full mb-6">
              <Mail className="h-10 w-10 text-green-600 animate-pulse" />
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-3">Generating Email</h2>
            <p className="text-gray-600 mb-8 text-lg">
              AI is composing a professional introduction email...
            </p>

            <div className="max-w-md mx-auto">
              <div className="animate-pulse space-y-3">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className="h-3 bg-gray-200 rounded-full"
                    style={{ width: `${40 + i * 15}%` }}
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
        <div className="bg-gradient-to-r from-green-600 to-emerald-600 p-8 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-3xl font-bold mb-2 flex items-center">
                <Mail className="w-8 h-8 mr-3" />
                Professional Email
              </h2>
              <p className="text-green-100 text-lg">Ready-to-send introduction email</p>
            </div>
            <button
              onClick={() =>
                openCustomizationModal(
                  "email",
                  generatedContent.email || "",
                  "Customize Introduction Email"
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
          <div className="bg-gradient-to-br from-gray-50 to-green-50 rounded-2xl p-8 mb-8 border-2 border-gray-100">
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed text-base">
                {generatedContent.email || "Email content will appear here..."}
              </pre>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
              <h4 className="font-semibold text-blue-900 mb-4 flex items-center">
                <Send className="w-5 h-5 mr-2" />
                Email Features
              </h4>
              <ul className="text-sm text-blue-800 space-y-2">
                <li>• Professional subject line with candidate name</li>
                <li>• Clear recommendation statement</li>
                <li>• Key skills and experience summary</li>
                <li>• Terms of offer section</li>
                <li>• Attachment references</li>
              </ul>
            </div>

            <div className="bg-green-50 border border-green-200 rounded-xl p-6">
              <h4 className="font-semibold text-green-900 mb-4 flex items-center">
                <CheckCircle className="w-5 h-5 mr-2" />
                Ready to Send
              </h4>
              <ul className="text-sm text-green-800 space-y-2">
                <li>• Addressed to contact person</li>
                <li>• Professional tone and structure</li>
                <li>• Call-to-action for follow-up</li>
                <li>• Proper business email format</li>
                <li>• Signed with your name</li>
              </ul>
            </div>
          </div>

          <div className="flex justify-end pt-6 border-t border-gray-200">
            <button
              onClick={() => setCurrentStep("downloads")}
              className="group inline-flex items-center px-8 py-4 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-xl hover:from-green-700 hover:to-emerald-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              View Downloads
              <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmailStep;
