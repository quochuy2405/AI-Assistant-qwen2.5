#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load Zizi Project TXT vào knowledge base để train AI Assistant
"""

from knowledge_base import KnowledgeBase
import os

def load_zizi_txt():
    """Load file txt Zizi vào knowledge base"""
    print("📚 Loading Zizi Project TXT into knowledge base...")
    
    # Initialize knowledge base
    kb = KnowledgeBase()
    
    # Clear existing data first
    print("🧹 Clearing existing knowledge base...")
    kb.clear_all()
    
    # Load the Zizi txt file
    txt_file = "huong-dan-su-dung-zizi-project-day-du.txt"
    
    if os.path.exists(txt_file):
        try:
            print(f"📄 Loading: {txt_file}")
            success = kb.load_txt(txt_file)
            
            if success:
                print(f"✅ Successfully loaded: {txt_file}")
                
                # Show statistics
                stats = kb.get_statistics()
                print(f"\n📊 Knowledge Base Statistics:")
                print(f"   📚 Total documents: {stats['total_documents']}")
                print(f"   📄 Total chunks: {stats['total_chunks']}")
                print(f"   💾 Database size: {stats['database_size']} MB")
                
                # Test search
                print(f"\n🔍 Testing search functionality...")
                test_queries = [
                    "zizi project",
                    "hướng dẫn sử dụng",
                    "cài đặt",
                    "tính năng",
                    "login",
                    "dashboard"
                ]
                
                for query in test_queries:
                    results = kb.search(query, k=2)
                    print(f"📋 Query '{query}': Found {len(results)} results")
                    if results:
                        preview = results[0]['content'][:100].replace('\n', ' ')
                        print(f"   📝 Preview: {preview}...")
                
                return True
            else:
                print(f"❌ Failed to load: {txt_file}")
                return False
                
        except Exception as e:
            print(f"❌ Error loading {txt_file}: {e}")
            return False
    else:
        print(f"⚠️ File not found: {txt_file}")
        return False

def test_ai_with_zizi_knowledge():
    """Test AI Assistant với Zizi knowledge"""
    print(f"\n🤖 Testing AI Assistant with Zizi knowledge...")
    
    try:
        from api.responses import get_smart_response
        
        test_questions = [
            "Zizi project là gì?",
            "Làm sao cài đặt Zizi?",
            "Có những tính năng gì trong Zizi?",
            "Hướng dẫn sử dụng Zizi như thế nào?",
            "Cách login vào Zizi?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n📋 Question {i}: {question}")
            print("-" * 40)
            
            try:
                response = get_smart_response(question)
                print(f"🤖 AI Response:")
                print(response[:300] + "..." if len(response) > 300 else response)
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print("-" * 40)
            
    except ImportError as e:
        print(f"⚠️ Cannot test AI responses: {e}")
        print("Make sure API is properly set up")

if __name__ == "__main__":
    print("🚀 ZIZI PROJECT TRAINING SETUP")
    print("=" * 50)
    
    # Load Zizi txt
    success = load_zizi_txt()
    
    if success:
        print(f"\n✅ Zizi knowledge loaded successfully!")
        
        # Test AI with new knowledge
        test_ai_with_zizi_knowledge()
        
        print(f"\n🎉 TRAINING COMPLETED!")
        print("🤖 AI Assistant now knows about Zizi Project!")
        print("🔌 Start API server to use: python start_api_server.py")
    else:
        print(f"\n💥 Training failed!")
    
    print("=" * 50) 