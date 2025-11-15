# import os
# import logging
# from io import BytesIO
# from typing import Union, BinaryIO, List, Dict
# import asyncio
# from functools import lru_cache

# import PyPDF2
# import pdfplumber
# import docx
# from fastapi import UploadFile, HTTPException

# logger = logging.getLogger(__name__)


# class FileHandler:
#     """Handles file validation and text extraction for FastAPI applications."""

#     VALID_EXTENSIONS = ('.pdf', '.docx', '.doc', '.txt')
    
#     def __init__(self, max_size_mb: int = 10):
#         """
#         Initialize FileHandler with configurable size limits.
        
#         Args:
#             max_size_mb: Maximum file size in megabytes
#         """
#         self.max_size_mb = max_size_mb

#     async def validate_file(self, file: UploadFile, max_size_mb: int = None) -> None:
#         """
#         Enhanced file validation with content checking for FastAPI UploadFile.
        
#         Args:
#             file: FastAPI UploadFile object
#             max_size_mb: Optional override for max file size
            
#         Raises:
#             HTTPException: If file validation fails
#         """
#         max_size = max_size_mb or self.max_size_mb
        
#         try:
#             # Check file size
#             file_size = await self._get_file_size(file)
            
#             if file_size > max_size * 1024 * 1024:
#                 raise HTTPException(
#                     status_code=413,
#                     detail=f"File too large. Maximum size is {max_size}MB."
#                 )
            
#             if file_size == 0:
#                 raise HTTPException(
#                     status_code=400,
#                     detail="File is empty."
#                 )
            
#             # Validate file extension
#             if not file.filename:
#                 raise HTTPException(
#                     status_code=400,
#                     detail="Filename is required."
#                 )
                
#             ext = os.path.splitext(file.filename)[1].lower()
#             if ext not in self.VALID_EXTENSIONS:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=f"Unsupported file extension: {ext}. Supported: {', '.join(self.VALID_EXTENSIONS)}"
#                 )
            
#             # Validate file content headers
#             await self._validate_file_content(file, ext, file_size)
            
#         except HTTPException:
#             raise
#         except Exception as e:
#             logger.error(f"Error validating file {file.filename}: {e}", exc_info=True)
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"File validation failed: {str(e)}"
#             )

#     async def _get_file_size(self, file: UploadFile) -> int:
#         """Get file size asynchronously."""
#         # Read the entire file to get size
#         content = await file.read()
#         size = len(content)
#         # Reset file pointer
#         await file.seek(0)
#         return size

#     async def _validate_file_content(self, file: UploadFile, ext: str, file_size: int) -> None:
#         """Validate file content headers asynchronously."""
#         # Read header for validation
#         header_size = min(512, file_size)
#         header = await file.read(header_size)
#         await file.seek(0)  # Reset file pointer
        
#         if ext == '.pdf' and not header.startswith(b'%PDF-'):
#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid PDF file format - missing PDF header."
#             )
#         elif ext == '.docx' and not header.startswith(b'PK\x03\x04'):
#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid DOCX file format."
#             )
#         elif ext == '.doc' and not header.startswith(b'\xd0\xcf\x11\xe0'):
#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid DOC file format."
#             )

#     async def process_multiple_resumes(
#         self, 
#         files: List[UploadFile]
#     ) -> List[Dict[str, str]]:
#         """Process multiple resume files concurrently."""
#         async def process_single_resume(file: UploadFile) -> Dict[str, str]:
#             try:
#                 await self.validate_file(file)
#                 content = await file.read()
#                 await file.seek(0)
#                 text = await self.extract_text_from_file(content, file.filename)
                
#                 return {
#                     "filename": file.filename,
#                     "text": text,
#                     "status": "success",
#                     "error": None
#                 }
#             except Exception as e:
#                 logger.error(f"Error processing {file.filename}: {e}")
#                 return {
#                     "filename": file.filename,
#                     "text": "",
#                     "status": "error",
#                     "error": str(e)
#                 }
        
#         tasks = [process_single_resume(file) for file in files]
#         results = await asyncio.gather(*tasks, return_exceptions=False)
#         return results

#     async def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
#         """
#         Extract text from various file formats asynchronously.
        
#         Args:
#             file_content: Raw file content as bytes
#             filename: Name of the file (used for extension detection)
            
#         Returns:
#             Extracted text content
            
#         Raises:
#             HTTPException: If text extraction fails
#         """
#         ext = os.path.splitext(filename)[1].lower()
        
#         try:
#             # Run text extraction in thread pool to avoid blocking
#             loop = asyncio.get_event_loop()
            
#             if ext == '.pdf':
#                 text = await loop.run_in_executor(
#                     None, self._extract_from_pdf, file_content
#                 )
#             elif ext in ['.doc', '.docx']:
#                 text = await loop.run_in_executor(
#                     None, self._extract_from_docx, file_content
#                 )
#             elif ext == '.txt':
#                 text = await loop.run_in_executor(
#                     None, self._extract_from_txt, file_content
#                 )
#             else:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=f"Unsupported file type: {ext}"
#                 )
            
#             if not text.strip():
#                 raise HTTPException(
#                     status_code=400,
#                     detail=f"No readable text found in {filename}"
#                 )
                
#             return text
            
#         except HTTPException:
#             raise
#         except Exception as e:
#             logger.error(f"Error extracting text from {filename}: {e}", exc_info=True)
#             raise HTTPException(
#                 status_code=500,
#                 detail=f"Could not read '{filename}'. {str(e)}"
#             )

#     def _extract_from_txt(self, file_content: bytes) -> str:
#         """Extract text from TXT files with encoding detection."""
#         encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
#         for encoding in encodings:
#             try:
#                 return file_content.decode(encoding)
#             except UnicodeDecodeError:
#                 continue
                
#         # If all encodings fail, use utf-8 with error handling
#         return file_content.decode('utf-8', errors='ignore')

#     def _extract_from_pdf(self, file_content: bytes) -> str:
#         """Extract text from PDF files (runs in thread pool)."""
#         # Try pdfplumber first (better text extraction)
#         try:
#             with pdfplumber.open(BytesIO(file_content)) as pdf:
#                 # Check for encrypted/empty PDFs
#                 if not pdf.pages:
#                     raise ValueError("PDF has no readable pages.")
                
#                 # Test if we can read the first page (fails if encrypted)
#                 first_page_text = pdf.pages[0].extract_text()
#                 if first_page_text is None and len(pdf.pages) > 0:
#                     # Might be encrypted, let's check
#                     pdf.pages[0].extract_text()
                
#                 text_parts = []
#                 for page in pdf.pages:
#                     page_text = page.extract_text()
#                     if page_text:
#                         text_parts.append(page_text)
                
#                 if text_parts:
#                     return "\n".join(text_parts)
                    
#         except Exception as e:
#             if any(keyword in str(e).lower() for keyword in ['password', 'encrypted', 'decrypt']):
#                 raise ValueError("The PDF is password-protected and cannot be read.")
#             logger.debug(f"pdfplumber failed, falling back to PyPDF2: {e}")

#         # Fallback to PyPDF2
#         try:
#             pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            
#             if pdf_reader.is_encrypted:
#                 raise ValueError("The PDF is password-protected and cannot be read.")
            
#             text_parts = []
#             for page in pdf_reader.pages:
#                 page_text = page.extract_text()
#                 if page_text:
#                     text_parts.append(page_text)
            
#             if text_parts:
#                 logger.info("PDF extracted using PyPDF2 fallback")
#                 return "\n".join(text_parts)
                
#         except Exception as e:
#             if "password" in str(e).lower() or "encrypted" in str(e).lower():
#                 raise ValueError("The PDF is password-protected and cannot be read.")
#             raise ValueError("Could not extract text from PDF. The file may be corrupted or image-based.") from e

#         raise ValueError("Could not extract any text from the PDF. The file may be image-based or corrupted.")

#     def _extract_from_docx(self, file_content: bytes) -> str:
#         """Extract text from DOCX files (runs in thread pool)."""
#         try:
#             doc = docx.Document(BytesIO(file_content))
#             text_parts = []
            
#             # Extract paragraph text
#             for paragraph in doc.paragraphs:
#                 if paragraph.text.strip():
#                     text_parts.append(paragraph.text.strip())
            
#             # Extract table text
#             for table in doc.tables:
#                 for row in table.rows:
#                     row_cells = []
#                     for cell in row.cells:
#                         if cell.text.strip():
#                             row_cells.append(cell.text.strip())
#                     if row_cells:
#                         text_parts.append(" | ".join(row_cells))
            
#             if not text_parts:
#                 raise ValueError("DOCX file appears empty or contains no readable text.")
                
#             return "\n".join(text_parts)
            
#         except Exception as e:
#             if "corrupted" in str(e).lower() or "invalid" in str(e).lower():
#                 raise ValueError("Failed to process DOCX file. It may be corrupted.") from e
#             raise ValueError(f"Failed to extract text from DOCX: {str(e)}") from e

#     async def process_multiple_files(self, files: List[UploadFile]) -> Dict[str, str]:
#         """
#         Process multiple files concurrently.
        
#         Args:
#             files: List of UploadFile objects
            
#         Returns:
#             Dictionary mapping filenames to extracted text
#         """
#         async def process_single_file(file: UploadFile) -> tuple:
#             """Process a single file and return (filename, text) tuple."""
#             try:
#                 # Validate file
#                 await self.validate_file(file)
                
#                 # Read content
#                 content = await file.read()
#                 await file.seek(0)  # Reset for potential reuse
                
#                 # Extract text
#                 text = await self.extract_text_from_file(content, file.filename)
#                 return file.filename, text
                
#             except Exception as e:
#                 logger.error(f"Error processing file {file.filename}: {e}")
#                 return file.filename, f"Error: {str(e)}"

#         # Process all files concurrently
#         tasks = [process_single_file(file) for file in files]
#         results = await asyncio.gather(*tasks, return_exceptions=True)
        
#         # Convert results to dictionary
#         processed_files = {}
#         for result in results:
#             if isinstance(result, Exception):
#                 logger.error(f"File processing error: {result}")
#                 continue
#             filename, text = result
#             processed_files[filename] = text
            
#         return processed_files

#     async def get_file_info(self, file: UploadFile) -> Dict:
#         """
#         Get detailed information about a file.
        
#         Args:
#             file: UploadFile object
            
#         Returns:
#             Dictionary with file information
#         """
#         size = await self._get_file_size(file)
#         await file.seek(0)  # Reset file pointer
        
#         return {
#             "filename": file.filename,
#             "content_type": file.content_type,
#             "size_bytes": size,
#             "size_mb": round(size / (1024 * 1024), 2),
#             "extension": os.path.splitext(file.filename)[1].lower() if file.filename else None,
#             "is_valid_type": os.path.splitext(file.filename)[1].lower() in self.VALID_EXTENSIONS if file.filename else False
#         }


# # Dependency function for FastAPI
# @lru_cache()
# def get_file_handler() -> FileHandler:
#     """
#     Dependency function to get a FileHandler instance.
#     Uses LRU cache for singleton pattern.
#     """
#     return FileHandler()




import os
import logging
from io import BytesIO
from typing import Union, BinaryIO, List, Dict
import asyncio
from functools import lru_cache

import PyPDF2
import pdfplumber
import docx
from fastapi import UploadFile, HTTPException

logger = logging.getLogger(__name__)


class FileHandler:
    """Handles file validation and text extraction for FastAPI applications."""

    VALID_EXTENSIONS = ('.pdf', '.docx', '.doc', '.txt')
    
    def __init__(self, max_size_mb: int = 10):
        """
        Initialize FileHandler with configurable size limits.
        
        Args:
            max_size_mb: Maximum file size in megabytes
        """
        self.max_size_mb = max_size_mb

    async def validate_file(self, file: UploadFile, max_size_mb: int = None) -> None:
        """
        Enhanced file validation with content checking for FastAPI UploadFile.
        
        Args:
            file: FastAPI UploadFile object
            max_size_mb: Optional override for max file size
            
        Raises:
            HTTPException: If file validation fails
        """
        max_size = max_size_mb or self.max_size_mb
        
        try:
            # Check file size
            file_size = await self._get_file_size(file)
            
            if file_size > max_size * 1024 * 1024:
                raise HTTPException(
                    status_code=413,
                    detail=f"File too large. Maximum size is {max_size}MB."
                )
            
            if file_size == 0:
                raise HTTPException(
                    status_code=400,
                    detail="File is empty."
                )
            
            # Validate file extension
            if not file.filename:
                raise HTTPException(
                    status_code=400,
                    detail="Filename is required."
                )
                
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in self.VALID_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file extension: {ext}. Supported: {', '.join(self.VALID_EXTENSIONS)}"
                )
            
            # Validate file content headers
            await self._validate_file_content(file, ext, file_size)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error validating file {file.filename}: {e}", exc_info=True)
            raise HTTPException(
                status_code=400,
                detail=f"File validation failed: {str(e)}"
            )

    async def _get_file_size(self, file: UploadFile) -> int:
        """Get file size asynchronously."""
        # Read the entire file to get size
        content = await file.read()
        size = len(content)
        # Reset file pointer
        await file.seek(0)
        return size

    async def _validate_file_content(self, file: UploadFile, ext: str, file_size: int) -> None:
        """Validate file content headers asynchronously."""
        # Read header for validation
        header_size = min(512, file_size)
        header = await file.read(header_size)
        await file.seek(0)  # Reset file pointer
        
        if ext == '.pdf' and not header.startswith(b'%PDF-'):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file format - missing PDF header."
            )
        elif ext == '.docx' and not header.startswith(b'PK\x03\x04'):
            raise HTTPException(
                status_code=400,
                detail="Invalid DOCX file format."
            )
        elif ext == '.doc' and not header.startswith(b'\xd0\xcf\x11\xe0'):
            raise HTTPException(
                status_code=400,
                detail="Invalid DOC file format."
            )

    async def process_multiple_resumes(
        self, 
        files: List[UploadFile]
    ) -> List[Dict[str, str]]:
        """Process multiple resume files concurrently."""
        async def process_single_resume(file: UploadFile) -> Dict[str, str]:
            try:
                await self.validate_file(file)
                content = await file.read()
                await file.seek(0)
                text = await self.extract_text_from_file(content, file.filename)
                
                return {
                    "filename": file.filename,
                    "text": text,
                    "status": "success",
                    "error": None
                }
            except Exception as e:
                logger.error(f"Error processing {file.filename}: {e}")
                return {
                    "filename": file.filename,
                    "text": "",
                    "status": "error",
                    "error": str(e)
                }
        
        tasks = [process_single_resume(file) for file in files]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return results

    async def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
        """
        Extract text from various file formats asynchronously.
        
        Args:
            file_content: Raw file content as bytes
            filename: Name of the file (used for extension detection)
            
        Returns:
            Extracted text content
            
        Raises:
            HTTPException: If text extraction fails
        """
        ext = os.path.splitext(filename)[1].lower()
        
        try:
            # Run text extraction in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            
            if ext == '.pdf':
                text = await loop.run_in_executor(
                    None, self._extract_from_pdf, file_content
                )
            elif ext in ['.doc', '.docx']:
                text = await loop.run_in_executor(
                    None, self._extract_from_docx, file_content
                )
            elif ext == '.txt':
                text = await loop.run_in_executor(
                    None, self._extract_from_txt, file_content
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {ext}"
                )
            
            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail=f"No readable text found in {filename}"
                )
                
            return text
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error extracting text from {filename}: {e}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Could not read '{filename}'. {str(e)}"
            )

    def _extract_from_txt(self, file_content: bytes) -> str:
        """Extract text from TXT files with encoding detection."""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                return file_content.decode(encoding)
            except UnicodeDecodeError:
                continue
                
        # If all encodings fail, use utf-8 with error handling
        return file_content.decode('utf-8', errors='ignore')

    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF files (runs in thread pool)."""
        # Try pdfplumber first (better text extraction)
        try:
            with pdfplumber.open(BytesIO(file_content)) as pdf:
                # Check for encrypted/empty PDFs
                if not pdf.pages:
                    raise ValueError("PDF has no readable pages.")
                
                # Test if we can read the first page (fails if encrypted)
                first_page_text = pdf.pages[0].extract_text()
                if first_page_text is None and len(pdf.pages) > 0:
                    # Might be encrypted, let's check
                    pdf.pages[0].extract_text()
                
                text_parts = []
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                
                if text_parts:
                    return "\n".join(text_parts)
                    
        except Exception as e:
            if any(keyword in str(e).lower() for keyword in ['password', 'encrypted', 'decrypt']):
                raise ValueError("The PDF is password-protected and cannot be read.")
            logger.debug(f"pdfplumber failed, falling back to PyPDF2: {e}")

        # Fallback to PyPDF2
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            
            if pdf_reader.is_encrypted:
                raise ValueError("The PDF is password-protected and cannot be read.")
            
            text_parts = []
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            
            if text_parts:
                logger.info("PDF extracted using PyPDF2 fallback")
                return "\n".join(text_parts)
                
        except Exception as e:
            if "password" in str(e).lower() or "encrypted" in str(e).lower():
                raise ValueError("The PDF is password-protected and cannot be read.")
            raise ValueError("Could not extract text from PDF. The file may be corrupted or image-based.") from e

        raise ValueError("Could not extract any text from the PDF. The file may be image-based or corrupted.")

    def _extract_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX files (runs in thread pool)."""
        try:
            doc = docx.Document(BytesIO(file_content))
            text_parts = []
            
            # Extract paragraph text
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text.strip())
            
            # Extract table text
            for table in doc.tables:
                for row in table.rows:
                    row_cells = []
                    for cell in row.cells:
                        if cell.text.strip():
                            row_cells.append(cell.text.strip())
                    if row_cells:
                        text_parts.append(" | ".join(row_cells))
            
            if not text_parts:
                raise ValueError("DOCX file appears empty or contains no readable text.")
                
            return "\n".join(text_parts)
            
        except Exception as e:
            if "corrupted" in str(e).lower() or "invalid" in str(e).lower():
                raise ValueError("Failed to process DOCX file. It may be corrupted.") from e
            raise ValueError(f"Failed to extract text from DOCX: {str(e)}") from e

    async def process_multiple_files(self, files: List[UploadFile]) -> Dict[str, str]:
        """
        Process multiple files concurrently.
        
        Args:
            files: List of UploadFile objects
            
        Returns:
            Dictionary mapping filenames to extracted text
        """
        async def process_single_file(file: UploadFile) -> tuple:
            """Process a single file and return (filename, text) tuple."""
            try:
                # Validate file
                await self.validate_file(file)
                
                # Read content
                content = await file.read()
                await file.seek(0)  # Reset for potential reuse
                
                # Extract text
                text = await self.extract_text_from_file(content, file.filename)
                return file.filename, text
                
            except Exception as e:
                logger.error(f"Error processing file {file.filename}: {e}")
                return file.filename, f"Error: {str(e)}"

        # Process all files concurrently
        tasks = [process_single_file(file) for file in files]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert results to dictionary
        processed_files = {}
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"File processing error: {result}")
                continue
            filename, text = result
            processed_files[filename] = text
            
        return processed_files

    async def get_file_info(self, file: UploadFile) -> Dict:
        """
        Get detailed information about a file.
        
        Args:
            file: UploadFile object
            
        Returns:
            Dictionary with file information
        """
        size = await self._get_file_size(file)
        await file.seek(0)  # Reset file pointer
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": size,
            "size_mb": round(size / (1024 * 1024), 2),
            "extension": os.path.splitext(file.filename)[1].lower() if file.filename else None,
            "is_valid_type": os.path.splitext(file.filename)[1].lower() in self.VALID_EXTENSIONS if file.filename else False
        }


# Dependency function for FastAPI
@lru_cache()
def get_file_handler() -> FileHandler:
    """
    Dependency function to get a FileHandler instance.
    Uses LRU cache for singleton pattern.
    """
    return FileHandler()
