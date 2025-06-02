#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate comprehensive PDF guide for KOC App with TikTok Login
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

def create_koc_app_pdf():
    """Tạo PDF hướng dẫn app KOC hoàn chỉnh"""
    
    filename = "KOC_App_Guide_Complete.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#FF0050')  # TikTok pink
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=15,
        spaceBefore=20,
        textColor=colors.HexColor('#25F4EE')  # TikTok cyan
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.HexColor('#161823')  # TikTok dark
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY
    )
    
    story = []
    
    # Title Page
    story.append(Paragraph("🎯 KOC PRO APP", title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("📱 Ứng dụng quản lý KOC chuyên nghiệp", heading_style))
    story.append(Paragraph("🚀 Với TikTok Login & AI Assistant", heading_style))
    story.append(Spacer(1, 30))
    
    # App Overview
    story.append(Paragraph("📋 TỔNG QUAN ỨNG DỤNG", heading_style))
    story.append(Paragraph("""
    <b>KOC Pro App</b> là nền tảng quản lý toàn diện dành cho Key Opinion Consumer (KOC), 
    tích hợp đăng nhập TikTok và AI Assistant thông minh. Ứng dụng giúp KOC quản lý 
    chiến dịch, theo dõi hiệu suất, tương tác với khách hàng và tối ưu hóa thu nhập.
    """, normal_style))
    
    # Key Features
    story.append(Paragraph("✨ TÍNH NĂNG CHÍNH", heading_style))
    
    features_data = [
        ["🔐 TikTok Login", "Đăng nhập nhanh chóng qua TikTok account", "✅ Bảo mật cao"],
        ["📊 Dashboard KOC", "Theo dõi hiệu suất và thống kê chi tiết", "📈 Real-time"],
        ["💼 Quản lý chiến dịch", "Tạo, quản lý và theo dõi campaigns", "🎯 Hiệu quả"],
        ["🤖 AI Assistant", "Hỗ trợ tư vấn và tối ưu content", "🧠 Thông minh"],
        ["💰 Quản lý thu nhập", "Theo dõi doanh thu và hoa hồng", "💵 Minh bạch"],
        ["📱 Social Integration", "Kết nối đa nền tảng mạng xã hội", "🌐 Toàn diện"],
        ["📈 Analytics", "Phân tích chi tiết và báo cáo", "📊 Chuyên sâu"],
        ["🎨 Content Creator", "Công cụ tạo content chuyên nghiệp", "✨ Sáng tạo"]
    ]
    
    features_table = Table(features_data)
    features_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF0050')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(features_table)
    story.append(PageBreak())
    
    # TikTok Login Guide
    story.append(Paragraph("🔐 HƯỚNG DẪN ĐĂNG NHẬP TIKTOK", heading_style))
    
    story.append(Paragraph("Bước 1: Mở ứng dụng KOC Pro", subheading_style))
    story.append(Paragraph("""
    • Tải app từ App Store hoặc Google Play<br/>
    • Mở ứng dụng lần đầu tiên<br/>
    • Chọn "Đăng nhập với TikTok"
    """, normal_style))
    
    story.append(Paragraph("Bước 2: Kết nối TikTok Account", subheading_style))
    story.append(Paragraph("""
    • Nhấn nút "Login with TikTok" 🎵<br/>
    • Ứng dụng sẽ chuyển đến TikTok<br/>
    • Đăng nhập TikTok account của bạn<br/>
    • Cấp quyền truy cập cho KOC Pro App
    """, normal_style))
    
    story.append(Paragraph("Bước 3: Hoàn tất thiết lập", subheading_style))
    story.append(Paragraph("""
    • Xác thực thông tin cá nhân<br/>
    • Chọn lĩnh vực KOC (Beauty, Fashion, Tech, etc.)<br/>
    • Thiết lập mục tiêu thu nhập<br/>
    • Bắt đầu sử dụng app! 🚀
    """, normal_style))
    
    # Dashboard Guide
    story.append(Paragraph("📊 DASHBOARD KOC - BẢNG ĐIỀU KHIỂN", heading_style))
    
    story.append(Paragraph("📈 Thống kê tổng quan", subheading_style))
    story.append(Paragraph("""
    <b>Widget hiển thị:</b><br/>
    • Tổng số follower trên các platform<br/>
    • Doanh thu tháng này vs tháng trước<br/>
    • Số campaign đang hoạt động<br/>
    • Engagement rate trung bình<br/>
    • Top sản phẩm bán chạy
    """, normal_style))
    
    story.append(Paragraph("🎯 Quản lý chiến dịch", subheading_style))
    story.append(Paragraph("""
    <b>Tính năng chính:</b><br/>
    • Tạo campaign mới với wizard thông minh<br/>
    • Lịch đăng bài tự động<br/>
    • Theo dõi hiệu suất real-time<br/>
    • Tự động tính hoa hồng<br/>
    • Integration với TikTok Shop, Instagram Shopping
    """, normal_style))
    
    story.append(PageBreak())
    
    # AI Assistant Features
    story.append(Paragraph("🤖 AI ASSISTANT - TRỢ LÝ THÔNG MINH", heading_style))
    
    story.append(Paragraph("💬 Chat với AI", subheading_style))
    story.append(Paragraph("""
    <b>AI Assistant có thể:</b><br/>
    • Tư vấn content strategy phù hợp với niche<br/>
    • Đề xuất hashtag trending<br/>
    • Phân tích competitor<br/>
    • Tối ưu thời gian đăng bài<br/>
    • Tạo caption hấp dẫn<br/>
    • Dự đoán xu hướng sản phẩm
    """, normal_style))
    
    story.append(Paragraph("🎨 Content Creator AI", subheading_style))
    story.append(Paragraph("""
    <b>Công cụ tạo content:</b><br/>
    • AI Video Script Generator<br/>
    • Thumbnail Designer<br/>
    • Caption Writer với emoji<br/>
    • Hashtag Optimizer<br/>
    • Trend Analyzer<br/>
    • Voice-over Generator
    """, normal_style))
    
    # Revenue Management
    story.append(Paragraph("💰 QUẢN LÝ THU NHẬP", heading_style))
    
    story.append(Paragraph("📊 Theo dõi doanh thu", subheading_style))
    story.append(Paragraph("""
    <b>Dashboard doanh thu hiển thị:</b><br/>
    • Tổng doanh thu theo tháng/quý/năm<br/>
    • Breakdown theo từng platform<br/>
    • Hoa hồng từ affiliate marketing<br/>
    • Thu nhập từ livestream<br/>
    • Bonus từ việc hoàn thành KPI
    """, normal_style))
    
    story.append(Paragraph("💳 Thanh toán và rút tiền", subheading_style))
    story.append(Paragraph("""
    <b>Phương thức thanh toán:</b><br/>
    • Chuyển khoản ngân hàng<br/>
    • Ví điện tử (MoMo, ZaloPay)<br/>
    • PayPal cho thu nhập quốc tế<br/>
    • Crypto wallet (USDT, BTC)<br/>
    • Rút tiền nhanh 24/7
    """, normal_style))
    
    # Social Media Integration
    story.append(Paragraph("📱 TÍCH HỢP MẠNG XÃ HỘI", heading_style))
    
    platforms_data = [
        ["Platform", "Tính năng", "Lợi ích"],
        ["🎵 TikTok", "Auto post, Analytics, Shop integration", "Tăng reach và conversion"],
        ["📸 Instagram", "Story scheduler, Reels optimizer", "Build brand awareness"],
        ["📘 Facebook", "Page management, Ads tracking", "Mở rộng target audience"],
        ["📺 YouTube", "Video SEO, Monetization tracking", "Thu nhập dài hạn"],
        ["🐦 Twitter", "Thread creator, Trend monitoring", "Thought leadership"],
        ["📌 Pinterest", "Pin scheduler, Board optimization", "Drive traffic to products"]
    ]
    
    platforms_table = Table(platforms_data)
    platforms_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#25F4EE')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(platforms_table)
    
    story.append(PageBreak())
    
    # Advanced Features
    story.append(Paragraph("🚀 TÍNH NĂNG NÂNG CAO", heading_style))
    
    story.append(Paragraph("🎯 Smart Campaign Builder", subheading_style))
    story.append(Paragraph("""
    <b>Wizard tạo campaign thông minh:</b><br/>
    • Chọn mục tiêu: Awareness, Traffic, Conversion<br/>
    • AI suggest sản phẩm phù hợp với audience<br/>
    • Tự động tạo content calendar<br/>
    • Predict campaign performance<br/>
    • A/B testing tự động
    """, normal_style))
    
    story.append(Paragraph("📈 Advanced Analytics", subheading_style))
    story.append(Paragraph("""
    <b>Phân tích chuyên sâu:</b><br/>
    • Audience demographics & behavior<br/>
    • Content performance heatmap<br/>
    • Competitor benchmarking<br/>
    • ROI calculator cho từng campaign<br/>
    • Predictive analytics<br/>
    • Custom reports và export data
    """, normal_style))
    
    story.append(Paragraph("🤝 Collaboration Tools", subheading_style))
    story.append(Paragraph("""
    <b>Công cụ cộng tác:</b><br/>
    • Team workspace cho agency<br/>
    • Brand partnership marketplace<br/>
    • Contract management<br/>
    • Communication hub<br/>
    • Shared content library<br/>
    • Performance comparison với team
    """, normal_style))
    
    # Troubleshooting
    story.append(Paragraph("🔧 KHẮC PHỤC SỰ CỐ", heading_style))
    
    story.append(Paragraph("❌ Lỗi đăng nhập TikTok", subheading_style))
    story.append(Paragraph("""
    <b>Giải pháp:</b><br/>
    • Kiểm tra kết nối internet<br/>
    • Update app lên version mới nhất<br/>
    • Clear cache và restart app<br/>
    • Đăng xuất TikTok rồi đăng nhập lại<br/>
    • Liên hệ support: tiktok@kocpro.app
    """, normal_style))
    
    story.append(Paragraph("📊 Dữ liệu không đồng bộ", subheading_style))
    story.append(Paragraph("""
    <b>Giải pháp:</b><br/>
    • Pull to refresh trên dashboard<br/>
    • Kiểm tra quyền truy cập platform<br/>
    • Sync manual trong Settings<br/>
    • Đợi 5-10 phút cho auto sync<br/>
    • Contact support nếu vẫn lỗi
    """, normal_style))
    
    # Contact & Support
    story.append(Paragraph("📞 HỖ TRỢ & LIÊN HỆ", heading_style))
    
    support_data = [
        ["📧 Email", "support@kocpro.app", "24/7 Response"],
        ["💬 Live Chat", "In-app chat button", "8AM - 10PM"],
        ["📱 Hotline", "1900-KOC-PRO (1900-562-776)", "24/7 Support"],
        ["🎵 TikTok", "@kocpro_official", "Tips & Updates"],
        ["📘 Facebook", "fb.com/kocproapp", "Community"],
        ["📚 Help Center", "help.kocpro.app", "Guides & FAQs"]
    ]
    
    support_table = Table(support_data)
    support_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#161823')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(support_table)
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph("🎉 Chúc bạn thành công với KOC Pro App! 🚀", title_style))
    story.append(Paragraph(f"📅 Tài liệu được tạo: {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Created: {filename}")
    return filename

def create_koc_app_technical_spec():
    """Tạo PDF technical specification cho developers"""
    
    filename = "KOC_App_Technical_Specs.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TechTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2C3E50')
    )
    
    story = []
    
    # Technical Overview
    story.append(Paragraph("⚙️ KOC PRO APP - TECHNICAL SPECIFICATIONS", title_style))
    story.append(Spacer(1, 20))
    
    # Architecture
    story.append(Paragraph("🏗️ SYSTEM ARCHITECTURE", styles['Heading2']))
    story.append(Paragraph("""
    <b>Frontend:</b> React Native (iOS/Android) + React.js (Web)<br/>
    <b>Backend:</b> Node.js + Express.js<br/>
    <b>Database:</b> MongoDB (primary) + Redis (cache)<br/>
    <b>AI/ML:</b> Python FastAPI + Qwen2.5 (Ollama)<br/>
    <b>Auth:</b> OAuth 2.0 (TikTok, Google, Facebook)<br/>
    <b>Storage:</b> AWS S3 + CloudFront CDN<br/>
    <b>Hosting:</b> AWS ECS + Load Balancer
    """, styles['Normal']))
    
    # API Endpoints
    story.append(Paragraph("🔌 API ENDPOINTS", styles['Heading2']))
    
    api_data = [
        ["Method", "Endpoint", "Description"],
        ["POST", "/auth/tiktok", "TikTok OAuth login"],
        ["GET", "/dashboard/stats", "Get KOC statistics"],
        ["POST", "/campaigns", "Create new campaign"],
        ["GET", "/analytics/:id", "Get campaign analytics"],
        ["POST", "/ai/content", "Generate AI content"],
        ["GET", "/revenue/summary", "Revenue dashboard"],
        ["POST", "/social/post", "Cross-platform posting"],
        ["GET", "/trends/hashtags", "Trending hashtags"]
    ]
    
    api_table = Table(api_data)
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(api_table)
    
    # Database Schema
    story.append(Paragraph("💾 DATABASE SCHEMA", styles['Heading2']))
    story.append(Paragraph("""
    <b>Users Collection:</b><br/>
    • _id, tiktok_id, username, email<br/>
    • profile: {avatar, bio, niche, followers}<br/>
    • settings: {notifications, privacy}<br/>
    • created_at, updated_at<br/><br/>
    
    <b>Campaigns Collection:</b><br/>
    • _id, user_id, title, description<br/>
    • products: [{name, price, commission}]<br/>
    • schedule: {start_date, end_date}<br/>
    • performance: {views, clicks, sales}<br/><br/>
    
    <b>Analytics Collection:</b><br/>
    • _id, campaign_id, date, metrics<br/>
    • engagement: {likes, shares, comments}<br/>
    • conversion: {click_rate, purchase_rate}<br/>
    • revenue: {gross, commission, net}
    """, styles['Normal']))
    
    doc.build(story)
    print(f"✅ Created: {filename}")
    return filename

if __name__ == "__main__":
    print("🚀 Generating KOC App Documentation...")
    
    # Generate user guide
    user_guide = create_koc_app_pdf()
    
    # Generate technical specs
    tech_specs = create_koc_app_technical_spec()
    
    print("\n📚 Generated documents:")
    print(f"   📖 User Guide: {user_guide}")
    print(f"   ⚙️ Tech Specs: {tech_specs}")
    print("\n🎉 All documents created successfully!") 