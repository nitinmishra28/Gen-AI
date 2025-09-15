import React, { useState, useCallback, useEffect } from 'react';
import { 
  Building2, 
  Calendar, 
  User, 
  FileText, 
  Upload, 
  File, 
  X, 
  ArrowRight, 
  CheckCircle, 
  Circle, 
  Brain, 
  Clock, 
  TrendingUp, 
  XCircle, 
  Edit3, 
  Sparkles, 
  Mail, 
  Copy, 
  Check, 
  Download, 
  BarChart3 
} from 'lucide-react';

const API_BASE_URL = 'http://localhost:5000/api';

// File Upload Component
const FileUpload = ({ label, accept = '.pdf,.doc,.docx,.txt', file, onFileChange, className = '' }) => {
  const handleDragOver = useCallback((e) => {
    e.preventDefault();
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      onFileChange(files[0]);
    }
  }, [onFileChange]);

  const handleFileChange = useCallback((e) => {
    const selectedFile = e.target.files?.[0];
    onFileChange(selectedFile);
  }, [onFileChange]);

  const removeFile = useCallback(() => {
    onFileChange(undefined);
  }, [onFileChange]);

  return (
    <div className={className}>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>
      
      {!file ? (
        <div
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-500 hover:bg-blue-50 transition-colors cursor-pointer"
        >
          <input
            type="file"
            accept={accept}
            onChange={handleFileChange}
            className="hidden"
            id={`file-upload-${label.replace(/\s+/g, '-').toLowerCase()}`}
          />
          <label
            htmlFor={`file-upload-${label.replace(/\s+/g, '-').toLowerCase()}`}
            className="cursor-pointer"
          >
            <Upload className="mx-auto h-8 w-8 text-gray-400 mb-2" />
            <p className="text-sm text-gray-600">
              Click to upload or drag and drop
            </p>
            <p className="text-xs text-gray-400 mt-1">
              PDF, DOC, DOCX, TXT files
            </p>
          </label>
        </div>
      ) : (
        <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <File className="h-5 w-5 text-blue-600 mr-2" />
              <span className="text-sm font-medium text-gray-900">
                {file.name}
              </span>
            </div>
            <button
              onClick={removeFile}
              className="text-gray-400 hover:text-red-600 transition-colors"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">
            {(file.size / 1024).toFixed(1)} KB
          </p>
        </div>
      )}
    </div>
  );
};

// Progress Bar Component
const ProgressBar = ({ currentStep, steps, onStepClick }) => {
  return (
    <div className="w-full bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between max-w-4xl mx-auto">
        {steps.map((step, index) => (
          <div key={step.id} className="flex items-center">
            <div 
              className={`flex flex-col items-center ${onStepClick && step.completed ? 'cursor-pointer' : ''}`}
              onClick={() => onStepClick && step.completed && onStepClick(step.id)}
            >
              <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 transition-colors ${
                step.completed 
                  ? 'bg-green-600 border-green-600 text-white'
                  : currentStep === step.id
                    ? 'bg-blue-600 border-blue-600 text-white'
                    : 'bg-white border-gray-300 text-gray-400'
              } ${onStepClick && step.completed ? 'hover:bg-green-700' : ''}`}>
                {step.completed ? (
                  <CheckCircle className="w-6 h-6" />
                ) : (
                  <Circle className="w-6 h-6" />
                )}
              </div>
              <span className={`mt-2 text-xs font-medium ${
                currentStep === step.id ? 'text-blue-600' : step.completed ? 'text-green-600' : 'text-gray-500'
              }`}>
                {step.label}
              </span>
            </div>
            {index < steps.length - 1 && (
              <div className={`w-16 h-0.5 mx-4 ${
                steps[index + 1].completed ? 'bg-green-600' : 'bg-gray-200'
              }`} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

// API Service
const ApiService = {
  async analyzeCV(request) {
    try {
      const formData = new FormData();
      formData.append('cv_file', request.cvFile);
      if (request.assignmentFile) {
        formData.append('assignment_file', request.assignmentFile);
      }
      formData.append('assignment_data', JSON.stringify(request.assignmentData));
      formData.append('consultant_data', JSON.stringify(request.consultantData));

      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      return data;
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  },

  async generateMotivations(data) {
    try {
      const response = await fetch(`${API_BASE_URL}/generate-motivations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      return result;
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  },

  async generateCoverLetter(data) {
    try {
      const response = await fetch(`${API_BASE_URL}/generate-cover-letter`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      return result;
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  },

  async generateEmail(data) {
    try {
      const response = await fetch(`${API_BASE_URL}/generate-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      return result;
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  }
};

// Main App Component
function App() {
  const [currentStep, setCurrentStep] = useState('input');
  const [completedSteps, setCompletedSteps] = useState(new Set());
  const [analysisData, setAnalysisData] = useState(null);
  const [generatedContent, setGeneratedContent] = useState({});
  const [cvText, setCvText] = useState('');
  const [inputData, setInputData] = useState(null);

  // Form states
  const [assignment, setAssignment] = useState({
    date: '',
    client: '',
    title: '',
    description: ''
  });

  const [consultant, setConsultant] = useState({
    name: '',
    contactCompany: '',
    contactPerson: ''
  });

  const [cvFile, setCvFile] = useState();
  const [assignmentFile, setAssignmentFile] = useState();

  // Loading states
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isGeneratingMotivations, setIsGeneratingMotivations] = useState(false);
  const [isGeneratingCoverLetter, setIsGeneratingCoverLetter] = useState(false);
  const [isGeneratingEmail, setIsGeneratingEmail] = useState(false);

  // Progress states
  const [progress, setProgress] = useState(0);
  const [currentTask, setCurrentTask] = useState('');

  const steps = [
    { id: 'input', label: 'Input', completed: completedSteps.has('input') },
    { id: 'analysis', label: 'Analysis', completed: completedSteps.has('analysis') },
    { id: 'motivation', label: 'Motivation', completed: completedSteps.has('motivation') },
    { id: 'coverletter', label: 'Cover Letter', completed: completedSteps.has('coverletter') },
    { id: 'email', label: 'Email', completed: completedSteps.has('email') },
    { id: 'downloads', label: 'Downloads', completed: completedSteps.has('downloads') }
  ];

  const handleStepComplete = (step, data) => {
    setCompletedSteps(prev => new Set([...prev, step]));
    
    if (step === 'analysis' && data) {
      setAnalysisData(data);
    }
    
    if ((step === 'motivation' || step === 'coverletter' || step === 'email') && data) {
      setGeneratedContent(prev => ({ ...prev, ...data }));
    }

    // Move to next step
    const stepOrder = ['input', 'analysis', 'motivation', 'coverletter', 'email', 'downloads'];
    const currentIndex = stepOrder.indexOf(step);
    if (currentIndex < stepOrder.length - 1) {
      setCurrentStep(stepOrder[currentIndex + 1]);
    }
  };

  const handleStepNavigation = (step) => {
    setCurrentStep(step);
  };

  // Input Step Handler
  const handleInputSubmit = async (e) => {
    e.preventDefault();
    if (!cvFile || !assignment.date || !assignment.client || !assignment.title || !consultant.name) {
      alert('Please fill in all required fields and upload a CV file.');
      return;
    }

    const data = { assignment, consultant, cvFile, assignmentFile };
    setInputData(data);
    handleStepComplete('input', data);
    
    // Start analysis automatically
    await performAnalysis(data);
  };

  // Analysis Function
  const performAnalysis = async (data) => {
    setIsAnalyzing(true);
    setCurrentStep('analysis');
    
    const tasks = [
      'Parsing CV document...',
      'Extracting skills and experience...',
      'Analyzing assignment requirements...',
      'Matching consultant profile...',
      'Calculating compatibility scores...',
      'Generating detailed explanations...'
    ];

    let taskIndex = 0;
    const interval = setInterval(() => {
      if (taskIndex < tasks.length) {
        setCurrentTask(tasks[taskIndex]);
        setProgress((taskIndex + 1) * (100 / tasks.length));
        taskIndex++;
      } else {
        clearInterval(interval);
      }
    }, 1000);

    try {
      const result = await ApiService.analyzeCV({
        cvFile: data.cvFile,
        assignmentFile: data.assignmentFile,
        assignmentData: data.assignment,
        consultantData: data.consultant
      });

      clearInterval(interval);
      setIsAnalyzing(false);

      if (result.success) {
        handleStepComplete('analysis', result.analysis);
        // Extract CV text for later use
        setCvText(result.cv_text || '');
      } else {
        alert('Analysis failed: ' + result.error);
      }
    } catch (error) {
      clearInterval(interval);
      setIsAnalyzing(false);
      alert('Analysis failed: ' + error.message);
    }
  };

  // Generate Motivations
  const generateMotivations = async () => {
    if (!analysisData) return;
    
    setIsGeneratingMotivations(true);
    setCurrentStep('motivation');

    try {
      const allRequirements = [...(analysisData.requirements || []), ...(analysisData.wishes || [])];
      const result = await ApiService.generateMotivations({
        cv_text: cvText,
        requirements: allRequirements,
        consultant_name: consultant.name
      });

      setIsGeneratingMotivations(false);

      if (result.success) {
        handleStepComplete('motivation', { motivations: result.motivations });
      } else {
        alert('Motivation generation failed: ' + result.error);
      }
    } catch (error) {
      setIsGeneratingMotivations(false);
      alert('Motivation generation failed: ' + error.message);
    }
  };

  // Generate Cover Letter
  const generateCoverLetter = async () => {
    if (!analysisData) return;
    
    setIsGeneratingCoverLetter(true);
    setCurrentStep('coverletter');

    try {
      const result = await ApiService.generateCoverLetter({
        cv_text: cvText,
        assignment_info: assignment,
        consultant_name: consultant.name,
        analysis_result: analysisData
      });

      setIsGeneratingCoverLetter(false);

      if (result.success) {
        handleStepComplete('coverletter', { coverLetter: result.cover_letter });
      } else {
        alert('Cover letter generation failed: ' + result.error);
      }
    } catch (error) {
      setIsGeneratingCoverLetter(false);
      alert('Cover letter generation failed: ' + error.message);
    }
  };

  // Generate Email
  const generateEmail = async () => {
    if (!analysisData) return;
    
    setIsGeneratingEmail(true);
    setCurrentStep('email');

    try {
      const result = await ApiService.generateEmail({
        consultant_info: consultant,
        assignment_info: assignment,
        analysis_result: analysisData
      });

      setIsGeneratingEmail(false);

      if (result.success) {
        handleStepComplete('email', { email: result.email });
      } else {
        alert('Email generation failed: ' + result.error);
      }
    } catch (error) {
      setIsGeneratingEmail(false);
      alert('Email generation failed: ' + error.message);
    }
  };

  // Auto-trigger next steps
  useEffect(() => {
    if (currentStep === 'motivation' && !isGeneratingMotivations && analysisData && !completedSteps.has('motivation')) {
      generateMotivations();
    }
  }, [currentStep, analysisData]);

  useEffect(() => {
    if (currentStep === 'coverletter' && !isGeneratingCoverLetter && completedSteps.has('motivation') && !completedSteps.has('coverletter')) {
      generateCoverLetter();
    }
  }, [currentStep, completedSteps]);

  useEffect(() => {
    if (currentStep === 'email' && !isGeneratingEmail && completedSteps.has('coverletter') && !completedSteps.has('email')) {
      generateEmail();
    }
  }, [currentStep, completedSteps]);

  // Download function
  const handleDownload = (content, filename) => {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Render current step content
  const renderCurrentStep = () => {
    switch (currentStep) {
      case 'input':
        return (
          <div className="max-w-6xl mx-auto">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
              <div className="mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Assignment & Consultant Information</h2>
                <p className="text-gray-600">Enter the assignment details and consultant information to begin the matching process.</p>
              </div>

              <form onSubmit={handleInputSubmit} className="space-y-8">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <div className="space-y-6">
                    <div className="flex items-center mb-4">
                      <FileText className="h-5 w-5 text-blue-600 mr-2" />
                      <h3 className="text-lg font-semibold text-gray-900">Assignment Details</h3>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Date <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                          <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                          <input
                            type="date"
                            value={assignment.date}
                            onChange={(e) => setAssignment(prev => ({ ...prev, date: e.target.value }))}
                            className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            required
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Client <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                          <Building2 className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                          <input
                            type="text"
                            value={assignment.client}
                            onChange={(e) => setAssignment(prev => ({ ...prev, client: e.target.value }))}
                            className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            placeholder="e.g., Shell, DNB, Government Agency"
                            required
                          />
                        </div>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Assignment Title <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        value={assignment.title}
                        onChange={(e) => setAssignment(prev => ({ ...prev, title: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="e.g., Senior Data Engineer, BI Developer"
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Job Description
                      </label>
                      <textarea
                        value={assignment.description}
                        onChange={(e) => setAssignment(prev => ({ ...prev, description: e.target.value }))}
                        rows={6}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
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

                  <div className="space-y-6">
                    <div className="flex items-center mb-4">
                      <User className="h-5 w-5 text-blue-600 mr-2" />
                      <h3 className="text-lg font-semibold text-gray-900">Consultant Information</h3>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Consultant Name <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        value={consultant.name}
                        onChange={(e) => setConsultant(prev => ({ ...prev, name: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="e.g., Steven McNeal"
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Contact Company
                      </label>
                      <input
                        type="text"
                        value={consultant.contactCompany}
                        onChange={(e) => setConsultant(prev => ({ ...prev, contactCompany: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="e.g., CircleNine"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Contact Person
                      </label>
                      <input
                        type="text"
                        value={consultant.contactPerson}
                        onChange={(e) => setConsultant(prev => ({ ...prev, contactPerson: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="e.g., John Doe"
                      />
                    </div>

                    <FileUpload
                      label="CV Document *"
                      file={cvFile}
                      onFileChange={setCvFile}
                      accept=".pdf,.doc,.docx,.txt"
                    />

                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <h4 className="font-medium text-blue-900 mb-2">What happens next?</h4>
                      <ul className="text-sm text-blue-800 space-y-1">
                        <li>• AI will analyze the CV against assignment requirements</li>
                        <li>• Generate detailed matching scores and explanations</li>
                        <li>• Create personalized motivation letters</li>
                        <li>• Compose professional cover letters and emails</li>
                      </ul>
                    </div>
                  </div>
                </div>

                <div className="flex justify-end pt-6 border-t border-gray-200">
                  <button
                    type="submit"
                    className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
                  >
                    Start Analysis
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </button>
                </div>
              </form>
            </div>
          </div>
        );

      case 'analysis':
        if (isAnalyzing) {
          return (
            <div className="max-w-4xl mx-auto">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-6">
                    <Brain className="h-8 w-8 text-blue-600 animate-pulse" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">AI Analysis in Progress</h2>
                  <p className="text-gray-600 mb-8">Our AI is analyzing the CV against assignment requirements...</p>
                  
                  <div className="max-w-md mx-auto">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700">Progress</span>
                      <span className="text-sm font-medium text-blue-600">{Math.round(progress)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all duration-500 ease-out"
                        style={{ width: `${progress}%` }}
                      ></div>
                    </div>
                    <p className="text-sm text-gray-500 mt-4 flex items-center justify-center">
                      <Clock className="h-4 w-4 mr-2" />
                      {currentTask}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          );
        }

        return (
          <div className="max-w-6xl mx-auto space-y-6">
            {/* Overall Score Card */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">Analysis Complete</h2>
                  <p className="text-gray-600">Detailed matching results for {consultant.name}</p>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-green-600">{analysisData?.overall_score || 0}%</div>
                  <div className="text-sm text-gray-500">Overall Match</div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-blue-50 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-blue-900">Requirements</p>
                      <p className="text-2xl font-bold text-blue-600">{analysisData?.requirements_score || 0}%</p>
                    </div>
                    <TrendingUp className="h-8 w-8 text-blue-600" />
                  </div>
                  <p className="text-xs text-blue-700 mt-2">
                    {analysisData?.requirements?.filter(r => r.match).length || 0} of {analysisData?.requirements?.length || 0} requirements met
                  </p>
                </div>

                <div className="bg-green-50 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-green-900">Wishes</p>
                      <p className="text-2xl font-bold text-green-600">{analysisData?.wishes_score || 0}%</p>
                    </div>
                    <CheckCircle className="h-8 w-8 text-green-600" />
                  </div>
                  <p className="text-xs text-green-700 mt-2">
                    {analysisData?.wishes?.filter(w => w.match).length || 0} of {analysisData?.wishes?.length || 0} wishes fulfilled
                  </p>
                </div>

                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-900">Total Score</p>
                      <p className="text-2xl font-bold text-gray-600">{analysisData?.overall_score || 0}%</p>
                    </div>
                    <Brain className="h-8 w-8 text-gray-600" />
                  </div>
                  <p className="text-xs text-gray-700 mt-2">Strong candidate match</p>
                </div>
              </div>
            </div>

            {/* Requirements Analysis */}
            {analysisData?.requirements && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Requirements Analysis</h3>
                <div className="space-y-4">
                  {analysisData.requirements.map((req) => (
                    <div key={req.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <div className="flex items-center mb-2">
                            {req.match ? (
                              <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
                            ) : (
                              <XCircle className="h-5 w-5 text-red-600 mr-2" />
                            )}
                            <h4 className="font-medium text-gray-900">{req.title}</h4>
                          </div>
                          <p className="text-sm text-gray-600 mb-2">{req.description}</p>
                        </div>
                        <div className="text-right ml-4">
                          <div className={`text-lg font-bold ${req.match ? 'text-green-600' : 'text-red-600'}`}>
                            {req.percentage}%
                          </div>
                          <div className="text-xs text-gray-500">Match</div>
                        </div>
                      </div>
                      <div className="bg-gray-50 rounded p-3">
                        <p className="text-sm text-gray-700">{req.explanation}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Wishes Analysis */}
            {analysisData?.wishes && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Wishes Analysis</h3>
                <div className="space-y-4">
                  {analysisData.wishes.map((wish) => (
                    <div key={wish.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <div className="flex items-center mb-2">
                            <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
                            <h4 className="font-medium text-gray-900">{wish.title}</h4>
                          </div>
                          <p className="text-sm text-gray-600 mb-2">{wish.description}</p>
                        </div>
                        <div className="text-right ml-4">
                          <div className="text-lg font-bold text-green-600">{wish.percentage}%</div>
                          <div className="text-xs text-gray-500">Match</div>
                        </div>
                      </div>
                      <div className="bg-gray-50 rounded p-3">
                        <p className="text-sm text-gray-700">{wish.explanation}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );

      case 'motivation':
        if (isGeneratingMotivations) {
          return (
            <div className="max-w-4xl mx-auto">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-100 rounded-full mb-6">
                    <Sparkles className="h-8 w-8 text-purple-600 animate-pulse" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Generating Motivations</h2>
                  <p className="text-gray-600 mb-8">AI is creating personalized motivations for each requirement...</p>
                  
                  <div className="max-w-md mx-auto">
                    <div className="animate-pulse space-y-4">
                      <div className="h-4 bg-gray-200 rounded w-3/4 mx-auto"></div>
                      <div className="h-4 bg-gray-200 rounded w-1/2 mx-auto"></div>
                      <div className="h-4 bg-gray-200 rounded w-5/6 mx-auto"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        }

        const allRequirements = [...(analysisData?.requirements || []), ...(analysisData?.wishes || [])];

        return (
          <div className="max-w-6xl mx-auto space-y-6">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">Requirement Motivations</h2>
                  <p className="text-gray-600">AI-generated motivations for each requirement.</p>
                </div>
                <div className="text-sm text-gray-500">
                  {Object.keys(generatedContent.motivations || {}).length} motivations generated
                </div>
              </div>

              <div className="space-y-6">
                {allRequirements.map((req) => (
                  <div key={req.id} className="border border-gray-200 rounded-lg p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center mb-2">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium mr-3 ${
                            req.type === 'require' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                          }`}>
                            {req.type === 'require' ? 'Requirement' : 'Wish'}
                          </span>
                          {req.match && <CheckCircle className="h-4 w-4 text-green-600 mr-2" />}
                          <span className="text-lg font-medium text-gray-900">{req.percentage}% Match</span>
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">{req.title}</h3>
                      </div>
                    </div>

                    <div className="bg-gray-50 rounded-lg p-4">
                      <p className="text-gray-700 leading-relaxed">
                        {generatedContent.motivations?.[req.id] || req.explanation}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case 'coverletter':
        if (isGeneratingCoverLetter) {
          return (
            <div className="max-w-4xl mx-auto">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-100 rounded-full mb-6">
                    <Sparkles className="h-8 w-8 text-indigo-600 animate-pulse" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Generating Cover Letter</h2>
                  <p className="text-gray-600 mb-8">AI is crafting a personalized cover letter based on the analysis...</p>
                  
                  <div className="max-w-md mx-auto">
                    <div className="animate-pulse space-y-4">
                      <div className="h-4 bg-gray-200 rounded w-full"></div>
                      <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                      <div className="h-4 bg-gray-200 rounded w-4/5"></div>
                      <div className="h-4 bg-gray-200 rounded w-full"></div>
                      <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        }

        return (
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                    <FileText className="h-6 w-6 text-blue-600 mr-2" />
                    Cover Letter
                  </h2>
                  <p className="text-gray-600">AI-generated personalized cover letter for {consultant.name}</p>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-6 mb-6">
                <div className="prose max-w-none">
                  <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed">
                    {generatedContent.coverLetter || 'Cover letter content will appear here...'}
                  </pre>
                </div>
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <h4 className="font-medium text-blue-900 mb-2">Cover Letter Highlights</h4>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>• Addresses the education gap proactively and positively</li>
                  <li>• Emphasizes practical experience with Azure, SQL, and data platforms</li>
                  <li>• Shows leadership experience as Scrum Master and PO</li>
                  <li>• Demonstrates business-technical translation skills</li>
                  <li>• Maintains professional yet personal tone</li>
                </ul>
              </div>
            </div>
          </div>
        );

      case 'email':
        if (isGeneratingEmail) {
          return (
            <div className="max-w-4xl mx-auto">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-6">
                    <Sparkles className="h-8 w-8 text-green-600 animate-pulse" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Generating Email</h2>
                  <p className="text-gray-600 mb-8">AI is composing a professional introduction email...</p>
                  
                  <div className="max-w-md mx-auto">
                    <div className="animate-pulse space-y-4">
                      <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                      <div className="h-4 bg-gray-200 rounded w-full"></div>
                      <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                      <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        }

        return (
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                    <Mail className="h-6 w-6 text-green-600 mr-2" />
                    Introduction Email
                  </h2>
                  <p className="text-gray-600">Professional email ready to send to the client</p>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-6 mb-6">
                <div className="prose max-w-none">
                  <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed">
                    {generatedContent.email || 'Email content will appear here...'}
                  </pre>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-medium text-blue-900 mb-2">Email Features</h4>
                  <ul className="text-sm text-blue-800 space-y-1">
                    <li>• Professional subject line with candidate name</li>
                    <li>• Clear recommendation statement</li>
                    <li>• Key skills and experience summary</li>
                    <li>• Terms of offer section</li>
                    <li>• Attachment references</li>
                  </ul>
                </div>
                
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h4 className="font-medium text-green-900 mb-2">Ready to Send</h4>
                  <ul className="text-sm text-green-800 space-y-1">
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
                  onClick={() => setCurrentStep('downloads')}
                  className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
                >
                  View Downloads
                  <ArrowRight className="ml-2 h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        );

      case 'downloads':
        const handleDownloadAnalysis = () => {
          if (!analysisData) return;
          
          const analysisReport = `
CV-to-Assignment Analysis Report
================================

Consultant: ${consultant.name}
Overall Match Score: ${analysisData.overall_score}%
Requirements Score: ${analysisData.requirements_score}%
Wishes Score: ${analysisData.wishes_score}%

REQUIREMENTS ANALYSIS:
${analysisData.requirements?.map(req => `
${req.title}: ${req.percentage}% match
${req.match ? '✓' : '✗'} ${req.explanation}
`).join('\n') || ''}

WISHES ANALYSIS:
${analysisData.wishes?.map(wish => `
${wish.title}: ${wish.percentage}% match
✓ ${wish.explanation}
`).join('\n') || ''}
          `.trim();

          handleDownload(analysisReport, `${consultant.name}_Analysis_Report.txt`);
        };

        const downloadItems = [
          {
            icon: BarChart3,
            title: 'Analysis Report',
            description: 'Detailed matching analysis with scores and explanations',
            filename: `${consultant.name}_Analysis_Report.txt`,
            action: handleDownloadAnalysis,
            color: 'blue'
          },
          {
            icon: FileText,
            title: 'Motivation Letter',
            description: 'Requirement-by-requirement motivations',
            filename: `${consultant.name}_Motivations.txt`,
            action: () => {
              const motivationContent = generatedContent.motivations ? 
                Object.entries(generatedContent.motivations)
                  .map(([id, motivation]) => `${motivation}\n`)
                  .join('\n') : '';
              handleDownload(motivationContent, `${consultant.name}_Motivations.txt`);
            },
            color: 'purple'
          },
          {
            icon: FileText,
            title: 'Cover Letter',
            description: 'Professional cover letter for the assignment',
            filename: `${consultant.name}_Cover_Letter.txt`,
            action: () => {
              const coverLetter = generatedContent.coverLetter || '';
              handleDownload(coverLetter, `${consultant.name}_Cover_Letter.txt`);
            },
            color: 'indigo'
          },
          {
            icon: Mail,
            title: 'Introduction Email',
            description: 'Ready-to-send email to the client',
            filename: `${consultant.name}_Introduction_Email.txt`,
            action: () => {
              const email = generatedContent.email || '';
              handleDownload(email, `${consultant.name}_Introduction_Email.txt`);
            },
            color: 'green'
          }
        ];

        return (
          <div className="max-w-6xl mx-auto space-y-6">
            {/* Success Header */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-6">
                  <CheckCircle className="h-8 w-8 text-green-600" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Process Complete!</h2>
                <p className="text-gray-600 mb-6">
                  All documents have been generated successfully. Download the files below to complete your consultant proposal.
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-2xl mx-auto">
                  <div className="bg-blue-50 rounded-lg p-4">
                    <div className="text-2xl font-bold text-blue-600">{analysisData?.overall_score || 0}%</div>
                    <div className="text-sm text-blue-800">Overall Match</div>
                  </div>
                  <div className="bg-green-50 rounded-lg p-4">
                    <div className="text-2xl font-bold text-green-600">4</div>
                    <div className="text-sm text-green-800">Documents Generated</div>
                  </div>
                  <div className="bg-purple-50 rounded-lg p-4">
                    <div className="text-2xl font-bold text-purple-600">Ready</div>
                    <div className="text-sm text-purple-800">For Submission</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Download Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {downloadItems.map((item, index) => (
                <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center">
                      <div className={`inline-flex items-center justify-center w-10 h-10 bg-${item.color}-100 rounded-lg mr-3`}>
                        <item.icon className={`h-5 w-5 text-${item.color}-600`} />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">{item.title}</h3>
                        <p className="text-sm text-gray-600">{item.description}</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500 font-mono">{item.filename}</span>
                    <button
                      onClick={item.action}
                      className={`inline-flex items-center px-4 py-2 bg-${item.color}-600 text-white text-sm font-medium rounded-md hover:bg-${item.color}-700 transition-colors`}
                    >
                      <Download className="h-4 w-4 mr-2" />
                      Download
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Summary */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Next Steps</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">For the Client</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Send the introduction email to {consultant.contactPerson || 'the contact person'}</li>
                    <li>• Attach the cover letter and motivations</li>
                    <li>• Include the original CV document</li>
                    <li>• Follow up within 2-3 business days</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Internal Process</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Save analysis report for future reference</li>
                    <li>• Update consultant profile with new skills</li>
                    <li>• Track proposal status in CRM system</li>
                    <li>• Schedule follow-up reminders</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Building2 className="h-8 w-8 text-blue-600 mr-3" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">ABC.org</h1>
                <p className="text-sm text-gray-500">AI CV-to-Assignment Matching Tool</p>
              </div>
            </div>
            <div className="text-sm text-gray-500">
              Data Professional Staffing Solutions
            </div>
          </div>
        </div>
      </header>

      {/* Progress Bar */}
      <ProgressBar 
        currentStep={currentStep} 
        steps={steps}
        onStepClick={handleStepNavigation}
      />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderCurrentStep()}
      </main>
    </div>
  );
}

export default App;