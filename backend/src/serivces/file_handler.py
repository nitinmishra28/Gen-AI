import os
import PyPDF2
import pdfplumber
import docx
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    """Handles file validation and text extraction."""

    VALID_EXTENSIONS = ('.pdf', '.docx', '.doc', '.txt')

    def validate_file(self, file, max_size_mb=10):
        """Enhanced file validation with content checking."""
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
        
        if size > max_size_mb * 1024 * 1024:
            raise ValueError(f"File too large. Maximum size is {max_size_mb}MB.")
        if size == 0:
            raise ValueError("File is empty.")
        
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in self.VALID_EXTENSIONS:
            raise ValueError(f"Unsupported file extension: {ext}. Supported: {', '.join(self.VALID_EXTENSIONS)}")
        
        header = file.read(min(512, size))
        file.seek(0)
        
        if ext == '.pdf' and not header.startswith(b'%PDF-'):
            raise ValueError("Invalid PDF file format - missing PDF header.")
        elif ext == '.docx' and not header.startswith(b'PK\x03\x04'):
            raise ValueError("Invalid DOCX file format.")
        elif ext == '.doc' and not header.startswith(b'\xd0\xcf\x11\xe0'):
            raise ValueError("Invalid DOC file format.")

    def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
        """Extract text from various file formats."""
        ext = os.path.splitext(filename)[1].lower()
        try:
            if ext == '.pdf':
                return self._extract_from_pdf(file_content)
            elif ext in ['.doc', '.docx']:
                return self._extract_from_docx(file_content)
            elif ext == '.txt':
                return file_content.decode('utf-8', errors='ignore')
            else:
                raise ValueError(f"Unsupported file type: {ext}")
        except Exception as e:
            logger.error(f"Error extracting text from {filename}: {e}", exc_info=True)
            raise Exception(f"Could not read '{filename}'. {str(e)}") from e

    def _extract_from_pdf(self, file_content: bytes) -> str:
        # Using pdfplumber first
        try:
            with pdfplumber.open(BytesIO(file_content)) as pdf:
                # Encryption check
                if not pdf.pages:
                     raise ValueError("PDF has no readable pages.")
                pdf.pages[0].extract_text() # Fails if encrypted
                
                text = "".join(page.extract_text() + "\n" for page in pdf.pages if page.extract_text())
                if text.strip():
                    return text
        except Exception as e:
            if any(x in str(e).lower() for x in ['password', 'encrypted']):
                raise ValueError("The PDF is password-protected and cannot be read.")
            logger.debug(f"pdfplumber failed, falling back to PyPDF2: {e}")

        # Fallback to PyPDF2
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            if pdf_reader.is_encrypted:
                raise ValueError("The PDF is password-protected and cannot be read.")
            
            text = "".join(page.extract_text() + "\n" for page in pdf_reader.pages if page.extract_text())
            if text.strip():
                logger.info("PDF extracted using PyPDF2 fallback")
                return text
        except Exception as e:
            raise ValueError("Could not extract text from PDF. The file may be corrupted or image-based.") from e

        raise ValueError("Could not extract any text from the PDF.")

    def _extract_from_docx(self, file_content: bytes) -> str:
        try:
            doc = docx.Document(BytesIO(file_content))
            all_text = [p.text for p in doc.paragraphs if p.text.strip()]
            for table in doc.tables:
                for row in table.rows:
                    row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_text:
                        all_text.append(" | ".join(row_text))
            
            if not all_text:
                raise ValueError("DOCX file appears empty or contains no readable text.")
            return "\n".join(all_text)
        except Exception as e:
            raise ValueError("Failed to process DOCX file. It may be corrupted.") from e
