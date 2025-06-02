#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test PDF knowledge base functionality
"""

from knowledge_base import KnowledgeBase
import os

def test_pdf_knowledge_base():
    """Test loading PDF và search"""
    print("🔍 Testing PDF Knowledge Base...")
    
    # Check if PDF exists
    pdf_file = "demo_huong_dan_app.pdf"
    if not os.path.exists(pdf_file):
        print(f"❌ PDF file not found: {pdf_file}")
        return False
    
    print(f"📄 Found PDF: {pdf_file}")
    
    try:
        # Initialize knowledge base
        kb = KnowledgeBase()
        print("✅ Knowledge base initialized")
        
        # Load PDF
        print("📚 Loading PDF into knowledge base...")
        kb.load_pdf(pdf_file)
        print("✅ PDF loaded successfully!")
        
        # Test searches
        test_queries = [
            "đăng ký",
            "thanh toán", 
            "app chậm",
            "hướng dẫn"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Searching for: '{query}'")
            results = kb.search(query, k=3)
            print(f"   Found {len(results)} results")
            
            if results:
                for i, result in enumerate(results[:2]):
                    content_preview = result['content'][:150].replace('\n', ' ')
                    print(f"   {i+1}. {content_preview}...")
            else:
                print("   No results found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_pdf_knowledge_base()
    if success:
        print("\n🎉 PDF Knowledge base test passed!")
    else:
        print("\n💥 PDF Knowledge base test failed!") 