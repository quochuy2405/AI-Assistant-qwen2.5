import chromadb
import json
import os
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
import numpy as np
from datetime import datetime

class KnowledgeBase:
    """Quản lý knowledge base cho AI Assistant"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Khởi tạo embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Tạo hoặc lấy collection
        collection_name = "app_guide_knowledge"
        try:
            # Thử lấy collection có sẵn
            self.collection = self.client.get_collection(collection_name)
        except Exception as e:
            try:
                # Nếu không tồn tại, tạo mới
                self.collection = self.client.create_collection(
                    name=collection_name,
                    metadata={"description": "Knowledge base for app guidance"}
                )
            except Exception as create_error:
                # Nếu tạo mới thất bại, thử get_or_create
                try:
                    self.collection = self.client.get_or_create_collection(
                        name=collection_name,
                        metadata={"description": "Knowledge base for app guidance"}
                    )
                except Exception as final_error:
                    print(f"Lỗi khởi tạo collection: {final_error}")
                    raise final_error
        
        # File để lưu metadata
        self.metadata_file = os.path.join(persist_directory, "metadata.json")
        self.load_metadata()
    
    def load_metadata(self):
        """Tải metadata từ file"""
        try:
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
            else:
                self.metadata = {
                    'documents': [],
                    'total_chunks': 0,
                    'last_updated': None
                }
        except Exception:
            self.metadata = {
                'documents': [],
                'total_chunks': 0,
                'last_updated': None
            }
    
    def save_metadata(self):
        """Lưu metadata vào file"""
        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi lưu metadata: {e}")
    
    def add_documents(self, text_chunks: List[Dict[str, str]], document_name: str):
        """
        Thêm tài liệu vào knowledge base
        
        Args:
            text_chunks: List các text chunks
            document_name: Tên tài liệu
        """
        if not text_chunks:
            return
        
        # Tạo embeddings cho tất cả chunks
        texts = [chunk['content'] for chunk in text_chunks]
        embeddings = self.embedding_model.encode(texts)
        
        # Chuẩn bị dữ liệu cho ChromaDB
        ids = []
        metadatas = []
        documents = []
        
        for i, chunk in enumerate(text_chunks):
            chunk_id = f"{document_name}_{chunk['id']}"
            ids.append(chunk_id)
            documents.append(chunk['content'])
            metadatas.append({
                'document_name': document_name,
                'chunk_id': chunk['id'],
                'length': chunk['length'],
                'timestamp': datetime.now().isoformat()
            })
        
        # Thêm vào collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings.tolist(),
            documents=documents,
            metadatas=metadatas
        )
        
        # Cập nhật metadata
        if document_name not in self.metadata['documents']:
            self.metadata['documents'].append(document_name)
        
        self.metadata['total_chunks'] += len(text_chunks)
        self.metadata['last_updated'] = datetime.now().isoformat()
        
        self.save_metadata()
        
        print(f"Đã thêm {len(text_chunks)} chunks từ {document_name}")
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, any]]:
        """
        Tìm kiếm thông tin liên quan đến câu hỏi
        
        Args:
            query: Câu hỏi tìm kiếm
            k: Số lượng kết quả trả về
            
        Returns:
            List các document liên quan
        """
        if self.collection.count() == 0:
            return []
        
        try:
            # Tạo embedding cho query
            query_embedding = self.embedding_model.encode([query])
            
            # Tìm kiếm
            results = self.collection.query(
                query_embeddings=query_embedding.tolist(),
                n_results=min(k, self.collection.count())
            )
            
            # Xử lý kết quả
            search_results = []
            
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    result = {
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else 0,
                        'id': results['ids'][0][i]
                    }
                    search_results.append(result)
            
            return search_results
            
        except Exception as e:
            print(f"Lỗi tìm kiếm: {e}")
            return []
    
    def search_by_document(self, document_name: str, query: str = None, k: int = 10) -> List[Dict[str, any]]:
        """
        Tìm kiếm trong một tài liệu cụ thể
        
        Args:
            document_name: Tên tài liệu
            query: Câu hỏi (optional)
            k: Số lượng kết quả
            
        Returns:
            List các chunk từ tài liệu đó
        """
        try:
            if query:
                # Tìm kiếm theo query trong document
                query_embedding = self.embedding_model.encode([query])
                
                results = self.collection.query(
                    query_embeddings=query_embedding.tolist(),
                    n_results=k,
                    where={"document_name": document_name}
                )
            else:
                # Lấy tất cả chunk từ document
                results = self.collection.get(
                    where={"document_name": document_name},
                    limit=k
                )
            
            # Xử lý kết quả
            search_results = []
            
            if results['documents']:
                documents = results['documents'][0] if isinstance(results['documents'][0], list) else results['documents']
                metadatas = results['metadatas'][0] if isinstance(results['metadatas'][0], list) else results['metadatas']
                ids = results['ids'][0] if isinstance(results['ids'][0], list) else results['ids']
                
                for i in range(len(documents)):
                    result = {
                        'content': documents[i],
                        'metadata': metadatas[i],
                        'id': ids[i]
                    }
                    if 'distances' in results:
                        result['distance'] = results['distances'][0][i]
                    search_results.append(result)
            
            return search_results
            
        except Exception as e:
            print(f"Lỗi tìm kiếm theo tài liệu: {e}")
            return []
    
    def delete_document(self, document_name: str) -> bool:
        """
        Xóa tài liệu khỏi knowledge base
        
        Args:
            document_name: Tên tài liệu cần xóa
            
        Returns:
            True nếu xóa thành công
        """
        try:
            # Lấy tất cả IDs của document
            results = self.collection.get(
                where={"document_name": document_name}
            )
            
            if results['ids']:
                # Xóa tất cả chunks của document
                self.collection.delete(ids=results['ids'])
                
                # Cập nhật metadata
                if document_name in self.metadata['documents']:
                    self.metadata['documents'].remove(document_name)
                
                self.metadata['total_chunks'] -= len(results['ids'])
                self.metadata['last_updated'] = datetime.now().isoformat()
                
                self.save_metadata()
                
                print(f"Đã xóa tài liệu {document_name}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Lỗi xóa tài liệu: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, any]:
        """Lấy thống kê về knowledge base"""
        try:
            collection_count = self.collection.count()
            
            return {
                'total_documents': len(self.metadata['documents']),
                'total_chunks': collection_count,
                'documents': self.metadata['documents'],
                'last_updated': self.metadata['last_updated'],
                'database_size': self._get_db_size()
            }
        except Exception:
            return {
                'total_documents': 0,
                'total_chunks': 0,
                'documents': [],
                'last_updated': None,
                'database_size': 0
            }
    
    def _get_db_size(self) -> float:
        """Tính kích thước database (MB)"""
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(self.persist_directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
            return round(total_size / (1024 * 1024), 2)  # Convert to MB
        except Exception:
            return 0
    
    def clear_all(self) -> bool:
        """Xóa toàn bộ knowledge base"""
        try:
            # Xóa collection
            self.client.delete_collection("app_guide_knowledge")
            
            # Tạo lại collection mới
            self.collection = self.client.create_collection(
                name="app_guide_knowledge",
                metadata={"description": "Knowledge base for app guidance"}
            )
            
            # Reset metadata
            self.metadata = {
                'documents': [],
                'total_chunks': 0,
                'last_updated': None
            }
            self.save_metadata()
            
            print("Đã xóa toàn bộ knowledge base")
            return True
            
        except Exception as e:
            print(f"Lỗi xóa knowledge base: {e}")
            return False
    
    def get_document_list(self) -> List[str]:
        """Lấy danh sách tài liệu"""
        return self.metadata['documents'].copy()
    
    def is_empty(self) -> bool:
        """Kiểm tra knowledge base có trống không"""
        return self.collection.count() == 0 