#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load KOC App PDFs into knowledge base for AI Assistant
"""

from knowledge_base import KnowledgeBase
import os

def load_koc_pdfs_to_knowledge_base():
    """Load KOC app PDFs vào knowledge base"""
    print("📚 Loading KOC App PDFs into knowledge base...")
    
    # Initialize knowledge base
    kb = KnowledgeBase()
    
    # List of PDF files to load
    pdf_files = [
        "KOC_App_Guide_Complete.pdf",
        "KOC_App_Technical_Specs.pdf",
        "demo_huong_dan_app.pdf"  # Existing demo PDF
    ]
    
    loaded_count = 0
    
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            try:
                print(f"📄 Loading: {pdf_file}")
                kb.load_pdf(pdf_file)
                loaded_count += 1
                print(f"✅ Successfully loaded: {pdf_file}")
            except Exception as e:
                print(f"❌ Error loading {pdf_file}: {e}")
        else:
            print(f"⚠️ File not found: {pdf_file}")
    
    print(f"\n🎉 Loaded {loaded_count} PDF files into knowledge base!")
    
    # Test search functionality
    print("\n🔍 Testing search functionality...")
    test_queries = [
        "KOC app",
        "TikTok login", 
        "đăng nhập",
        "dashboard",
        "AI assistant",
        "quản lý chiến dịch",
        "technical specs"
    ]
    
    for query in test_queries:
        results = kb.search(query, k=2)
        print(f"📋 Query '{query}': Found {len(results)} results")
        if results:
            # Show first result preview
            preview = results[0]['content'][:150].replace('\n', ' ')
            print(f"   📝 Preview: {preview}...")
    
    return loaded_count

if __name__ == "__main__":
    success_count = load_koc_pdfs_to_knowledge_base()
    print(f"\n✅ Knowledge base updated with {success_count} documents!")
    print("🤖 AI Assistant can now answer questions about KOC App!") 