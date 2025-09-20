// import React from "react";
// import { Sparkles, CheckCircle, MessageSquare, Wand2 } from "lucide-react";
// import styles from "./MotivationStep.module.css";

// const MotivationStep = ({
//   isGeneratingMotivations,
//   analysisData,
//   generatedContent,
//   openCustomizationModal,
// }) => {
//   if (isGeneratingMotivations) {
//     return (
//       <div className={styles.container}>
//         <div className={styles.card}>
//           <div className={styles.content}>
//             <div className={styles.iconContainer}>
//               <Sparkles className={styles.icon} />
//             </div>
//             <h2 className={styles.title}>Generating Motivations</h2>
//             <p className={styles.subtitle}>
//               AI is creating personalized motivations for each requirement...
//             </p>
//             <div className={styles.progress}>
//               <div className={styles.progressBars}>
//                 {[1, 2, 3, 4].map((i) => (
//                   <div
//                     key={i}
//                     className={styles.progressBar}
//                     style={{ width: `${60 + i * 10}%` }}
//                   ></div>
//                 ))}
//               </div>
//             </div>
//           </div>
//         </div>
//       </div>
//     );
//   }

//   const allRequirements = [
//     ...(analysisData?.requirements || []),
//     ...(analysisData?.wishes || []),
//   ];

//   return (
//     <div className={styles.container}>
//       <div className={styles.card}>
//         <div className={styles.header}>
//           <div className={styles.headerContent}>
//             <h2 className={styles.title}>
//               <Sparkles className={styles.icon} />
//               Requirement Motivations
//             </h2>
//             <p className={styles.subtitle}>
//               AI-generated personalized motivations
//             </p>
//           </div>
//           <div className={styles.count}>
//             <div className={styles.countValue}>
//               {Object.keys(generatedContent.motivations || {}).length}
//             </div>
//             <div className={styles.countLabel}>Motivations Generated</div>
//           </div>
//         </div>

//         <div className={styles.content}>
//           <div className={styles.items}>
//             {allRequirements.map((req) => (
//               <div key={req.id} className={styles.item}>
//                 <div className={styles.itemHeader}>
//                   <div className={styles.itemInfo}>
//                     <div className={styles.itemTags}>
//                       <span
//                         className={`${styles.tag} ${
//                           req.type === "require" ? styles.required : styles.preferred
//                         }`}
//                       >
//                         {req.type === "require" ? "Required" : "Preferred"}
//                       </span>
//                       {req.match && <CheckCircle className={styles.checkIcon} />}
//                       <span className={styles.match}>
//                         {req.percentage}% Match
//                       </span>
//                     </div>
//                     <h3 className={styles.itemTitle}>{req.title}</h3>
//                   </div>
//                   <button
//                     onClick={() =>
//                       openCustomizationModal(
//                         "motivation",
//                         generatedContent.motivations?.[req.id] || req.explanation,
//                         `Customize motivation for: ${req.title}`,
//                         req.id
//                       )
//                     }
//                     className={styles.customizeButton}
//                   >
//                     <Wand2 className={styles.wandIcon} />
//                     Customize with AI
//                   </button>
//                 </div>
//                 <div className={styles.motivation}>
//                   <h4 className={styles.motivationTitle}>
//                     <MessageSquare className={styles.icon} />
//                     Personalized Motivation
//                   </h4>
//                   <p className={styles.motivationText}>
//                     {generatedContent.motivations?.[req.id] || req.explanation}
//                   </p>
//                 </div>
//               </div>
//             ))}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default MotivationStep;




import React from "react";
import { Sparkles, CheckCircle, MessageSquare, Wand2 } from "lucide-react";

const MotivationStep = ({
  isGeneratingMotivations,
  analysisData,
  generatedContent,
  openCustomizationModal,
}) => {
  if (isGeneratingMotivations) {
    return (
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
          <div className="p-8">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full mb-6">
              <Sparkles className="h-10 w-10 text-purple-600 animate-pulse" />
            </div>
            <h2 className="text-3xl font-bold mb-2">Generating Motivations</h2>
            <p className="text-lg text-gray-600 mb-8">
              AI is creating personalized motivations for each requirement...
            </p>
            <div className="max-w-md mx-auto">
              <div className="animate-pulse space-y-4">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className="h-4 bg-gray-200 rounded-full"
                    style={{ width: `${60 + i * 10}%` }}
                  ></div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const allRequirements = [
    ...(analysisData?.requirements || []),
    ...(analysisData?.wishes || []),
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-8 text-white flex items-center justify-between">
          <div className="flex-1">
            <h2 className="text-3xl font-bold mb-2 flex items-center">
              <Sparkles className="w-6 h-6 mr-3" />
              Requirement Motivations
            </h2>
            <p className="text-purple-100 text-lg">
              AI-generated personalized motivations
            </p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold">
              {Object.keys(generatedContent.motivations || {}).length}
            </div>
            <div className="text-purple-100 text-sm">Motivations Generated</div>
          </div>
        </div>

        <div className="p-8">
          <div className="space-y-6">
            {allRequirements.map((req) => (
              <div key={req.id} className="group border border-gray-200 rounded-xl p-6 hover:shadow-md transition-all duration-200">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center mb-3">
                      <span
                        className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold mr-3 ${
                          req.type === "require" ? "bg-blue-100 text-blue-800" : "bg-green-100 text-green-800"
                        }`}
                      >
                        {req.type === "require" ? "Required" : "Preferred"}
                      </span>
                      {req.match && <CheckCircle className="h-4 w-4 text-green-600 mr-2" />}
                      <span className="text-lg font-semibold text-gray-900">
                        {req.percentage}% Match
                      </span>
                    </div>
                    <h3 className="font-bold text-gray-900 text-xl mb-2">{req.title}</h3>
                  </div>
                  <button
                    onClick={() =>
                      openCustomizationModal(
                        "motivation",
                        generatedContent.motivations?.[req.id] || req.explanation,
                        `Customize motivation for: ${req.title}`,
                        req.id
                      )
                    }
                    className="group/btn inline-flex items-center px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-sm font-medium rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all duration-200 opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0"
                  >
                    <Wand2 className="w-4 h-4 mr-2 group-hover/btn:rotate-12 transition-transform" />
                    Customize with AI
                  </button>
                </div>
                <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-6 border border-purple-100">
                  <h4 className="font-medium text-purple-900 flex items-center mb-3">
                    <MessageSquare className="w-5 h-5 mr-2" />
                    Personalized Motivation
                  </h4>
                  <p className="text-gray-700 leading-relaxed">
                    {generatedContent.motivations?.[req.id] || req.explanation}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MotivationStep;
