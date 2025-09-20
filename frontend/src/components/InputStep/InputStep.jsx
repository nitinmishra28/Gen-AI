import React from "react";
import { Brain, FileText, User, Calendar, Building2, Sparkles,ArrowRight } from "lucide-react";
import FileUpload from "../FileUpload/FileUpload";

const InputStep = ({
  assignment,
  setAssignment,
  consultant,
  setConsultant,
  cvFile,
  setCvFile,
  assignmentFile,
  setAssignmentFile,
  handleInputSubmit,
}) => {
  return (
    <div className="max-w-7xl mx-auto">
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        <div className="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 p-8 text-white">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-white/20 rounded-full mb-4">
              <Brain className="w-8 h-8" />
            </div>
            <h2 className="text-3xl font-bold mb-2">AI-Powered CV Analysis</h2>
            <p className="text-blue-100 text-lg">
              Transform your recruitment process with intelligent matching
            </p>
          </div>
        </div>

        <div className="p-8">
          <form onSubmit={handleInputSubmit} className="space-y-8">
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
                <div className="flex items-center mb-6">
                  <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-lg flex items-center justify-center mr-3">
                    <FileText className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">
                      Assignment Details
                    </h3>
                    <p className="text-sm text-gray-600">
                      Configure the job requirements
                    </p>
                  </div>
                </div>

                <div className="space-y-6">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-semibold text-gray-800 mb-2">
                        Date <span className="text-red-500">*</span>
                      </label>
                      <div className="relative">
                        <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                        <input
                          type="date"
                          value={assignment.date}
                          onChange={(e) =>
                            setAssignment((prev) => ({
                              ...prev,
                              date: e.target.value,
                            }))
                          }
                          className="w-full pl-10 pr-3 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                          required
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-800 mb-2">
                        Client <span className="text-red-500">*</span>
                      </label>
                      <div className="relative">
                        <Building2 className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                        <input
                          type="text"
                          value={assignment.client}
                          onChange={(e) =>
                            setAssignment((prev) => ({
                              ...prev,
                              client: e.target.value,
                            }))
                          }
                          className="w-full pl-10 pr-3 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                          placeholder="e.g., Shell, DNB, Government Agency"
                          required
                        />
                      </div>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-800 mb-2">
                      Assignment Title <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      value={assignment.title}
                      onChange={(e) =>
                        setAssignment((prev) => ({
                          ...prev,
                          title: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                      placeholder="e.g., Senior Data Engineer, BI Developer"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-800 mb-2">
                      Job Description
                    </label>
                    <textarea
                      value={assignment.description}
                      onChange={(e) =>
                        setAssignment((prev) => ({
                          ...prev,
                          description: e.target.value,
                        }))
                      }
                      rows={6}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors resize-none"
                      placeholder="Paste the job description here or upload a file below..."
                    />
                  </div>

                  <FileUpload
                    label="Assignment Document (Optional)"
                    file={assignmentFile}
                    onFileChange={setAssignmentFile}
                    accept=".pdf,.doc,.docx,.txt"
                  />
                </div>
              </div>

              <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-6 border border-green-100">
                <div className="flex items-center mb-6">
                  <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg flex items-center justify-center mr-3">
                    <User className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">
                      Consultant Profile
                    </h3>
                    <p className="text-sm text-gray-600">
                      Enter candidate information
                    </p>
                  </div>
                </div>

                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-semibold text-gray-800 mb-2">
                      Consultant Name <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      value={consultant.name}
                      onChange={(e) =>
                        setConsultant((prev) => ({
                          ...prev,
                          name: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors"
                      placeholder="e.g., Steven McNeal"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-800 mb-2">
                      Contact Company
                    </label>
                    <input
                      type="text"
                      value={consultant.contactCompany}
                      onChange={(e) =>
                        setConsultant((prev) => ({
                          ...prev,
                          contactCompany: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors"
                      placeholder="e.g., CircleNine"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-800 mb-2">
                      Contact Person
                    </label>
                    <input
                      type="text"
                      value={consultant.contactPerson}
                      onChange={(e) =>
                        setConsultant((prev) => ({
                          ...prev,
                          contactPerson: e.target.value,
                        }))
                      }
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors"
                      placeholder="e.g., John Doe"
                    />
                  </div>

                  <FileUpload
                    label="CV Document *"
                    file={cvFile}
                    onFileChange={setCvFile}
                    accept=".pdf,.doc,.docx,.txt"
                  />

                  <div className="bg-white/70 backdrop-blur-sm border border-green-200 rounded-xl p-4">
                    <h4 className="font-semibold text-green-900 mb-3 flex items-center">
                      <Sparkles className="w-4 h-4 mr-2" />
                      AI Analysis Preview
                    </h4>
                    <ul className="text-sm text-green-800 space-y-1">
                      <li>• Deep CV analysis against requirements</li>
                      <li>• Intelligent matching with explanations</li>
                      <li>• Personalized motivations & cover letters</li>
                      <li>• Professional email generation</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex justify-end pt-8 border-t border-gray-200">
              <button
                type="submit"
                className="group inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-indigo-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                <Brain className="mr-3 h-5 w-5" />
                Start AI Analysis
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default InputStep;
