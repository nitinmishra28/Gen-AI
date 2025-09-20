import { API_BASE_URL } from "../constants/api";

const ApiService = {
  async analyzeCV(request) {
    try {
      const formData = new FormData();
      formData.append("cv_file", request.cvFile);
      if (request.assignmentFile) {
        formData.append("assignment_file", request.assignmentFile);
      }
      formData.append(
        "assignment_data",
        JSON.stringify(request.assignmentData)
      );
      formData.append(
        "consultant_data",
        JSON.stringify(request.consultantData)
      );

      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      return data;
    } catch (error) {
      return {
        success: false,
        error:
          error instanceof Error ? error.message : "Unknown error occurred",
      };
    }
  },

  async generateMotivations(data) {
    try {
      const response = await fetch(`${API_BASE_URL}/generate-motivations`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      return result;
    } catch (error) {
      return {
        success: false,
        error:
          error instanceof Error ? error.message : "Unknown error occurred",
      };
    }
  },

  async generateCoverLetter(data) {
    try {
      const response = await fetch(`${API_BASE_URL}/generate-cover-letter`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      return result;
    } catch (error) {
      return {
        success: false,
        error:
          error instanceof Error ? error.message : "Unknown error occurred",
      };
    }
  },

  async generateEmail(data) {
    try {
      const response = await fetch(`${API_BASE_URL}/generate-email`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      return result;
    } catch (error) {
      return {
        success: false,
        error:
          error instanceof Error ? error.message : "Unknown error occurred",
      };
    }
  },

  async customizeContent(data) {
    try {
      const response = await fetch(`${API_BASE_URL}/customize-content`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      return result;
    } catch (error) {
      return {
        success: false,
        error:
          error instanceof Error ? error.message : "Unknown error occurred",
      };
    }
  },
};

export default ApiService;