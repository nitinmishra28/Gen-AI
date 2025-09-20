// import React from "react";
// import {
//   CheckCircle,
//   BarChart3,
//   Sparkles,
//   FileText,
//   Mail,
//   Download,
//   Zap,
//   Send,
// } from "lucide-react";
// import styles from "./DownloadsStep.module.css";

// const DownloadsStep = ({
//   analysisData,
//   consultant,
//   generatedContent,
//   handleDownload,
// }) => {
//   const handleDownloadAnalysis = () => {
//     if (!analysisData) return;

//     const analysisReport = `
// CV-to-Assignment Analysis Report
// ================================

// Consultant: ${consultant.name}
// Overall Match Score: ${analysisData.overall_score}%
// Requirements Score: ${analysisData.requirements_score}%
// Wishes Score: ${analysisData.wishes_score}%

// REQUIREMENTS ANALYSIS:
// ${
//   analysisData.requirements
//     ?.map(
//       (req) => `
// ${req.title}: ${req.percentage}% match
// ${req.match ? "✓" : "✗"} ${req.explanation}
// `
//     )
//     .join("\n") || ""
// }

// WISHES ANALYSIS:
// ${
//   analysisData.wishes
//     ?.map(
//       (wish) => `
// ${wish.title}: ${wish.percentage}% match
// ✓ ${wish.explanation}
// `
//     )
//     .join("\n") || ""
// }
//     `.trim();

//     handleDownload(analysisReport, `${consultant.name}_Analysis_Report.txt`);
//   };

//   const downloadItems = [
//     {
//       icon: BarChart3,
//       title: "Analysis Report",
//       description: "Detailed matching analysis with scores and explanations",
//       filename: `${consultant.name}_Analysis_Report.txt`,
//       action: handleDownloadAnalysis,
//       color: "blue",
//       gradient: "from-blue-500 to-indigo-500",
//     },
//     {
//       icon: Sparkles,
//       title: "Motivation Letter",
//       description: "Requirement-by-requirement motivations",
//       filename: `${consultant.name}_Motivations.txt`,
//       action: () => {
//         const motivationContent = generatedContent.motivations
//           ? Object.entries(generatedContent.motivations)
//               .map(([id, motivation]) => `${motivation}\n`)
//               .join("\n")
//           : "";
//         handleDownload(motivationContent, `${consultant.name}_Motivations.txt`);
//       },
//       color: "purple",
//       gradient: "from-purple-500 to-pink-500",
//     },
//     {
//       icon: FileText,
//       title: "Cover Letter",
//       description: "Professional cover letter for the assignment",
//       filename: `${consultant.name}_Cover_Letter.txt`,
//       action: () => {
//         const coverLetter = generatedContent.coverLetter || "";
//         handleDownload(coverLetter, `${consultant.name}_Cover_Letter.txt`);
//       },
//       color: "indigo",
//       gradient: "from-indigo-500 to-blue-500",
//     },
//     {
//       icon: Mail,
//       title: "Introduction Email",
//       description: "Ready-to-send email to the client",
//       filename: `${consultant.name}_Introduction_Email.txt`,
//       action: () => {
//         const email = generatedContent.email || "";
//         handleDownload(email, `${consultant.name}_Introduction_Email.txt`);
//       },
//       color: "green",
//       gradient: "from-green-500 to-emerald-500",
//     },
//   ];

//   return (
//     <div className={styles.container}>
//       <div className={styles.card}>
//         <div className={styles.header}>
//           <div className={styles.headerContent}>
//             <div className={styles.headerIcon}>
//               <CheckCircle className={styles.icon} />
//             </div>
//             <h2 className={styles.title}>Process Complete!</h2>
//             <p className={styles.subtitle}>
//               All documents have been generated successfully. Download your
//               professional consultant proposal package.
//             </p>
//             <div className={styles.grid}>
//               <div className={styles.statCard}>
//                 <div className={styles.statValue}>
//                   {analysisData?.overall_score || 0}%
//                 </div>
//                 <div className={styles.statLabel}>Overall Match</div>
//               </div>
//               <div className={styles.statCard}>
//                 <div className={styles.statValue}>4</div>
//                 <div className={styles.statLabel}>Documents Generated</div>
//               </div>
//               <div className={styles.statCard}>
//                 <div className={styles.statValue}>Ready</div>
//                 <div className={styles.statLabel}>For Submission</div>
//               </div>
//             </div>
//           </div>
//         </div>
//       </div>

//       <div className={styles.downloadGrid}>
//         {downloadItems.map((item, index) => (
//           <div key={index} className={styles.downloadCard}>
//             <div className={styles.downloadHeader}>
//               <div className={styles.downloadIcon}>
//                 <item.icon className={styles.icon} />
//               </div>
//               <div>
//                 <h3 className={styles.downloadTitle}>{item.title}</h3>
//                 <p className={styles.downloadDescription}>{item.description}</p>
//               </div>
//             </div>
//             <div className={styles.filename}>
//               <File className={styles.fileIcon} />
//               <span className={styles.filenameText}>{item.filename}</span>
//             </div>
//             <button
//               onClick={item.action}
//               className={`${styles.downloadButton} ${styles[item.color]}`}
//             >
//               <Download className={styles.downloadIcon} />
//               Download File
//             </button>
//           </div>
//         ))}
//       </div>

//       <div className={styles.nextStepsCard}>
//         <h3 className={styles.nextStepsTitle}>
//           <Zap className={styles.zapIcon} />
//           Next Steps & Recommendations
//         </h3>
//         <div className={styles.nextStepsGrid}>
//           <div className={styles.nextStepsSection}>
//             <h4 className={styles.sectionTitle}>
//               <Send className={styles.icon} />
//               Client Communication
//             </h4>
//             <ul className={styles.sectionList}>
//               <li className={styles.listItem}>
//                 <CheckCircle className={styles.checkIcon} />
//                 Send the introduction email to{" "}
//                 {consultant.contactPerson || "the contact person"}
//               </li>
//               <li className={styles.listItem}>
//                 <CheckCircle className={styles.checkIcon} />
//                 Attach the cover letter and motivations
//               </li>
//               <li className={styles.listItem}>
//                 <CheckCircle className={styles.checkIcon} />
//                 Include the original CV document
//               </li>
//               <li className={styles.listItem}>
//                 <CheckCircle className={styles.checkIcon} />
//                 Follow up within 2-3 business days
//               </li>
//             </ul>
//           </div>
//           <div className={styles.nextStepsSection}>
//             <h4 className={styles.sectionTitle}>
//               <BarChart3 className={styles.icon} />
//               Internal Process
//             </h4>
//             <ul className={styles.sectionList}>
//               <li className={styles.listItem}>
//                 <CheckCircle className={styles.checkIcon} />
//                 Save analysis report for future reference
//               </li>
//               <li className={styles.listItem}>
//                 <CheckCircle className={styles.checkIcon} />
//                 Update consultant profile with new skills
//               </li>
//               <li className={styles.listItem}>
//                 <CheckCircle className={styles.checkIcon} />
//                 Track proposal status in CRM system
//               </li>
//               <li className={styles.listItem}>
//                 <CheckCircle className={styles.checkIcon} />
//                 Schedule follow-up reminders
//               </li>
//             </ul>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default DownloadsStep;











import React from "react";
import {
  CheckCircle,
  BarChart3,
  Sparkles,
  FileText,
  Mail,
  Download,
  Zap,
  Send,
  File,
} from "lucide-react";

const DownloadsStep = ({
  analysisData,
  consultant,
  generatedContent,
  handleDownload,
}) => {
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
${
  analysisData.requirements
    ?.map(
      (req) => `
${req.title}: ${req.percentage}% match
${req.match ? "✓" : "✗"} ${req.explanation}
`
    )
    .join("\n") || ""
}

WISHES ANALYSIS:
${
  analysisData.wishes
    ?.map(
      (wish) => `
${wish.title}: ${wish.percentage}% match
✓ ${wish.explanation}
`
    )
    .join("\n") || ""
}
    `.trim();

    handleDownload(analysisReport, `${consultant.name}_Analysis_Report.txt`);
  };

  const downloadItems = [
    {
      icon: BarChart3,
      title: "Analysis Report",
      description: "Detailed matching analysis with scores and explanations",
      filename: `${consultant.name}_Analysis_Report.txt`,
      action: handleDownloadAnalysis,
      color: "blue",
      gradient: "from-blue-500 to-indigo-500",
    },
    {
      icon: Sparkles,
      title: "Motivation Letter",
      description: "Requirement-by-requirement motivations",
      filename: `${consultant.name}_Motivations.txt`,
      action: () => {
        const motivationContent = generatedContent.motivations
          ? Object.entries(generatedContent.motivations)
              .map(([id, motivation]) => `${motivation}\n`)
              .join("\n")
          : "";
        handleDownload(motivationContent, `${consultant.name}_Motivations.txt`);
      },
      color: "purple",
      gradient: "from-purple-500 to-pink-500",
    },
    {
      icon: FileText,
      title: "Cover Letter",
      description: "Professional cover letter for the assignment",
      filename: `${consultant.name}_Cover_Letter.txt`,
      action: () => {
        const coverLetter = generatedContent.coverLetter || "";
        handleDownload(coverLetter, `${consultant.name}_Cover_Letter.txt`);
      },
      color: "indigo",
      gradient: "from-indigo-500 to-blue-500",
    },
    {
      icon: Mail,
      title: "Introduction Email",
      description: "Ready-to-send email to the client",
      filename: `${consultant.name}_Introduction_Email.txt`,
      action: () => {
        const email = generatedContent.email || "";
        handleDownload(email, `${consultant.name}_Introduction_Email.txt`);
      },
      color: "green",
      gradient: "from-green-500 to-emerald-500",
    },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        <div className="bg-gradient-to-r from-green-500 via-emerald-500 to-teal-500 p-8 text-white">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-white/20 rounded-full mb-6">
              <CheckCircle className="h-10 w-10" />
            </div>
            <h2 className="text-4xl font-bold mb-3">Process Complete!</h2>
            <p className="text-green-100 text-xl mb-6">
              All documents have been generated successfully. Download your
              professional consultant proposal package.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <div className="text-3xl font-bold mb-1">
                  {analysisData?.overall_score || 0}%
                </div>
                <div className="text-green-100 text-sm uppercase tracking-wide">Overall Match</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <div className="text-3xl font-bold mb-1">4</div>
                <div className="text-green-100 text-sm uppercase tracking-wide">Documents Generated</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <div className="text-3xl font-bold mb-1">Ready</div>
                <div className="text-green-100 text-sm uppercase tracking-wide">For Submission</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        {downloadItems.map((item, index) => (
          <div key={index} className="bg-white rounded-xl p-6 border border-gray-100 hover:shadow-lg transition-all duration-200">
            <div className="flex items-center mb-4">
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center mr-3 ${
                item.color === 'blue' ? 'bg-blue-100' :
                item.color === 'purple' ? 'bg-purple-100' :
                item.color === 'indigo' ? 'bg-indigo-100' :
                'bg-green-100'
              }`}>
                <item.icon className={`h-6 w-6 ${
                  item.color === 'blue' ? 'text-blue-600' :
                  item.color === 'purple' ? 'text-purple-600' :
                  item.color === 'indigo' ? 'text-indigo-600' :
                  'text-green-600'
                }`} />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">{item.title}</h3>
                <p className="text-sm text-gray-600">{item.description}</p>
              </div>
            </div>
            <div className="flex items-center mb-4 bg-gray-50 rounded-lg p-3 border border-gray-100">
              <File className="w-5 h-5 text-gray-500 mr-2" />
              <span className="text-sm text-gray-700">{item.filename}</span>
            </div>
            <button
              onClick={item.action}
              className={`w-full flex items-center justify-center px-4 py-3 text-white rounded-xl font-medium transition-all duration-200 ${
                item.color === 'blue' ? 'bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600' :
                item.color === 'purple' ? 'bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600' :
                item.color === 'indigo' ? 'bg-gradient-to-r from-indigo-500 to-blue-500 hover:from-indigo-600 hover:to-blue-600' :
                'bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600'
              }`}
            >
              <Download className="w-5 h-5 mr-2" />
              Download File
            </button>
          </div>
        ))}
      </div>

      <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-8 border border-gray-100">
        <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <Zap className="w-6 h-6 mr-2 text-yellow-500" />
          Next Steps & Recommendations
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-gray-900 flex items-center">
              <Send className="w-5 h-5 mr-2" />
              Client Communication
            </h4>
            <ul className="space-y-2">
              <li className="flex items-start text-sm text-gray-700">
                <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-1 flex-shrink-0" />
                Send the introduction email to{" "}
                {consultant.contactPerson || "the contact person"}
              </li>
              <li className="flex items-start text-sm text-gray-700">
                <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-1 flex-shrink-0" />
                Attach the cover letter and motivations
              </li>
              <li className="flex items-start text-sm text-gray-700">
                <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-1 flex-shrink-0" />
                Include the original CV document
              </li>
              <li className="flex items-start text-sm text-gray-700">
                <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-1 flex-shrink-0" />
                Follow up within 2-3 business days
              </li>
            </ul>
          </div>
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-gray-900 flex items-center">
              <BarChart3 className="w-5 h-5 mr-2" />
              Internal Process
            </h4>
            <ul className="space-y-2">
              <li className="flex items-start text-sm text-gray-700">
                <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-1 flex-shrink-0" />
                Save analysis report for future reference
              </li>
              <li className="flex items-start text-sm text-gray-700">
                <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-1 flex-shrink-0" />
                Update consultant profile with new skills
              </li>
              <li className="flex items-start text-sm text-gray-700">
                <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-1 flex-shrink-0" />
                Track proposal status in CRM system
              </li>
              <li className="flex items-start text-sm text-gray-700">
                <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-1 flex-shrink-0" />
                Schedule follow-up reminders
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DownloadsStep;
