import fitz  # PyMuPDF
import PyPDF2
import re
from typing import List, Dict

class PDFProcessor:
    """Xử lý file PDF và trích xuất text"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_and_chunk_pdf(self, pdf_path: str) -> List[Dict[str, str]]:
        """
        Trích xuất text từ PDF và chia thành các chunk nhỏ
        
        Args:
            pdf_path: Đường dẫn đến file PDF
            
        Returns:
            List các dict chứa text chunks
        """
        # Thử dùng PyMuPDF trước (tốt hơn cho layout phức tạp)
        try:
            text = self._extract_with_pymupdf(pdf_path)
        except:
            # Fallback sang PyPDF2
            try:
                text = self._extract_with_pypdf2(pdf_path)
            except Exception as e:
                raise Exception(f"Không thể đọc PDF: {str(e)}")
        
        # Làm sạch text
        cleaned_text = self._clean_text(text)
        
        # Chia thành chunks
        chunks = self._create_chunks(cleaned_text)
        
        return chunks
    
    def _extract_with_pymupdf(self, pdf_path: str) -> str:
        """Trích xuất text bằng PyMuPDF"""
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
            text += "\n\n"  # Thêm ngắt trang
        
        doc.close()
        return text
    
    def _extract_with_pypdf2(self, pdf_path: str) -> str:
        """Trích xuất text bằng PyPDF2"""
        text = ""
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
                text += "\n\n"  # Thêm ngắt trang
        
        return text
    
    def _clean_text(self, text: str) -> str:
        """Làm sạch text được trích xuất"""
        # Xóa ký tự đặc biệt không cần thiết
        text = re.sub(r'\x00', '', text)  # Xóa null characters
        
        # Chuẩn hóa khoảng trắng
        text = re.sub(r'\s+', ' ', text)  # Nhiều spaces thành 1 space
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Chuẩn hóa line breaks
        
        # Xóa khoảng trắng đầu cuối
        text = text.strip()
        
        return text
    
    def _create_chunks(self, text: str) -> List[Dict[str, str]]:
        """Chia text thành các chunks nhỏ"""
        chunks = []
        
        # Chia theo đoạn văn trước
        paragraphs = text.split('\n\n')
        
        current_chunk = ""
        chunk_id = 0
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # Kiểm tra nếu thêm đoạn này vào chunk hiện tại
            test_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph
            
            if len(test_chunk) <= self.chunk_size:
                current_chunk = test_chunk
            else:
                # Lưu chunk hiện tại (nếu có)
                if current_chunk:
                    chunks.append({
                        'id': f"chunk_{chunk_id}",
                        'content': current_chunk,
                        'length': len(current_chunk)
                    })
                    chunk_id += 1
                
                # Bắt đầu chunk mới
                if len(paragraph) <= self.chunk_size:
                    current_chunk = paragraph
                else:
                    # Đoạn quá dài, chia nhỏ hơn
                    sub_chunks = self._split_long_paragraph(paragraph)
                    for sub_chunk in sub_chunks:
                        chunks.append({
                            'id': f"chunk_{chunk_id}",
                            'content': sub_chunk,
                            'length': len(sub_chunk)
                        })
                        chunk_id += 1
                    current_chunk = ""
        
        # Thêm chunk cuối cùng
        if current_chunk:
            chunks.append({
                'id': f"chunk_{chunk_id}",
                'content': current_chunk,
                'length': len(current_chunk)
            })
        
        return chunks
    
    def _split_long_paragraph(self, paragraph: str) -> List[str]:
        """Chia đoạn văn dài thành các phần nhỏ hơn"""
        chunks = []
        sentences = re.split(r'[.!?]+', paragraph)
        
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            test_chunk = current_chunk + ". " + sentence if current_chunk else sentence
            
            if len(test_chunk) <= self.chunk_size:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk + ".")
                
                # Nếu câu vẫn quá dài, chia theo từ
                if len(sentence) > self.chunk_size:
                    word_chunks = self._split_by_words(sentence)
                    chunks.extend(word_chunks)
                    current_chunk = ""
                else:
                    current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk + ".")
        
        return chunks
    
    def _split_by_words(self, text: str) -> List[str]:
        """Chia text theo từ khi quá dài"""
        words = text.split()
        chunks = []
        current_chunk = ""
        
        for word in words:
            test_chunk = current_chunk + " " + word if current_chunk else word
            
            if len(test_chunk) <= self.chunk_size:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = word
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def get_pdf_metadata(self, pdf_path: str) -> Dict[str, any]:
        """Lấy metadata của PDF"""
        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            
            return {
                'title': metadata.get('title', ''),
                'author': metadata.get('author', ''),
                'subject': metadata.get('subject', ''),
                'creator': metadata.get('creator', ''),
                'producer': metadata.get('producer', ''),
                'creation_date': metadata.get('creationDate', ''),
                'modification_date': metadata.get('modDate', ''),
                'page_count': len(doc)
            }
        except Exception as e:
            return {'error': str(e)}
        finally:
            if 'doc' in locals():
                doc.close() 