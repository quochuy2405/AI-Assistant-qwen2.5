#!/usr/bin/env python3
"""
Script tạo PDF mẫu hướng dẫn sử dụng app để demo AI Assistant
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfutils
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from datetime import datetime

def create_demo_pdf():
    """Tạo file PDF demo hướng dẫn app"""
    
    # Tạo file PDF
    filename = "demo_huong_dan_app.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=1*inch)
    
    # Tạo styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor='darkblue'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor='darkgreen'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor='darkred'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leftIndent=0,
        rightIndent=0
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=4,
        leftIndent=20,
        bulletIndent=10
    )
    
    # Nội dung PDF
    story = []
    
    # Trang bìa
    story.append(Paragraph("HƯỚNG DẪN SỬ DỤNG", title_style))
    story.append(Paragraph("ESHOP MOBILE APP", title_style))
    story.append(Spacer(1, 50))
    story.append(Paragraph("Phiên bản 2.1.0", styles['Normal']))
    story.append(Paragraph(f"Cập nhật: {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
    story.append(PageBreak())
    
    # Mục lục
    story.append(Paragraph("MỤC LỤC", heading_style))
    toc_items = [
        "1. Giới thiệu về EShop App",
        "2. Hướng dẫn cài đặt",
        "3. Đăng ký và đăng nhập",
        "4. Giao diện chính",
        "5. Tìm kiếm và duyệt sản phẩm",
        "6. Thêm sản phẩm vào giỏ hàng",
        "7. Thanh toán",
        "8. Quản lý đơn hàng",
        "9. Cài đặt tài khoản",
        "10. Câu hỏi thường gặp (FAQ)",
        "11. Liên hệ hỗ trợ"
    ]
    for item in toc_items:
        story.append(Paragraph(item, bullet_style))
    
    story.append(PageBreak())
    
    # Chương 1: Giới thiệu
    story.append(Paragraph("1. GIỚI THIỆU VỀ ESHOP APP", heading_style))
    story.append(Paragraph("""
    EShop là ứng dụng mua sắm trực tuyến hàng đầu Việt Nam, cung cấp hàng triệu sản phẩm từ 
    các thương hiệu uy tín. Với giao diện thân thiện và tính năng thông minh, EShop giúp bạn 
    có trải nghiệm mua sắm tuyệt vời ngay trên điện thoại.
    """, normal_style))
    
    story.append(Paragraph("Tính năng nổi bật:", subheading_style))
    features = [
        "• Giao diện đẹp, dễ sử dụng",
        "• Tìm kiếm thông minh với AI",
        "• Thanh toán đa dạng: thẻ, ví điện tử, COD",
        "• Giao hàng nhanh toàn quốc",
        "• Chăm sóc khách hàng 24/7",
        "• Ưu đãi và khuyến mãi hấp dẫn"
    ]
    for feature in features:
        story.append(Paragraph(feature, bullet_style))
    
    story.append(PageBreak())
    
    # Chương 2: Cài đặt
    story.append(Paragraph("2. HƯỚNG DẪN CÀI ĐẶT", heading_style))
    
    story.append(Paragraph("Cho Android:", subheading_style))
    story.append(Paragraph("""
    1. Mở Google Play Store trên điện thoại
    2. Tìm kiếm "EShop - Mua sắm online"
    3. Nhấn "Cài đặt" và chờ ứng dụng tải về
    4. Mở ứng dụng và bắt đầu sử dụng
    """, normal_style))
    
    story.append(Paragraph("Cho iOS:", subheading_style))
    story.append(Paragraph("""
    1. Mở App Store trên iPhone/iPad
    2. Tìm kiếm "EShop Vietnam"
    3. Nhấn "Tải" và xác thực bằng Face ID/Touch ID
    4. Chờ ứng dụng cài đặt hoàn tất
    """, normal_style))
    
    story.append(Paragraph("Yêu cầu hệ thống:", subheading_style))
    story.append(Paragraph("• Android 7.0 trở lên", bullet_style))
    story.append(Paragraph("• iOS 12.0 trở lên", bullet_style))
    story.append(Paragraph("• Kết nối Internet ổn định", bullet_style))
    story.append(Paragraph("• Dung lượng trống tối thiểu 200MB", bullet_style))
    
    story.append(PageBreak())
    
    # Chương 3: Đăng ký và đăng nhập
    story.append(Paragraph("3. ĐĂNG KÝ VÀ ĐĂNG NHẬP", heading_style))
    
    story.append(Paragraph("Đăng ký tài khoản mới:", subheading_style))
    story.append(Paragraph("""
    1. Mở ứng dụng EShop
    2. Nhấn nút "Đăng ký" ở màn hình chính
    3. Nhập số điện thoại hoặc email
    4. Tạo mật khẩu mạnh (tối thiểu 8 ký tự)
    5. Nhập mã OTP được gửi về
    6. Hoàn tất thông tin cá nhân
    """, normal_style))
    
    story.append(Paragraph("Đăng nhập:", subheading_style))
    story.append(Paragraph("""
    • Sử dụng số điện thoại/email và mật khẩu
    • Đăng nhập bằng Facebook
    • Đăng nhập bằng Google
    • Sử dụng vân tay/Face ID (nếu đã thiết lập)
    """, normal_style))
    
    story.append(Paragraph("Quên mật khẩu:", subheading_style))
    story.append(Paragraph("""
    1. Nhấn "Quên mật khẩu" ở màn hình đăng nhập
    2. Nhập email/số điện thoại đăng ký
    3. Kiểm tra mã OTP trong tin nhắn/email
    4. Tạo mật khẩu mới
    """, normal_style))
    
    story.append(PageBreak())
    
    # Chương 4: Giao diện chính
    story.append(Paragraph("4. GIAO DIỆN CHÍNH", heading_style))
    
    story.append(Paragraph("Thanh điều hướng dưới:", subheading_style))
    nav_items = [
        "• Trang chủ: Xem sản phẩm nổi bật, khuyến mãi",
        "• Danh mục: Duyệt sản phẩm theo ngành hàng",
        "• Tìm kiếm: Tìm kiếm sản phẩm bằng từ khóa",
        "• Giỏ hàng: Xem và quản lý giỏ hàng",
        "• Tài khoản: Cài đặt và quản lý tài khoản"
    ]
    for item in nav_items:
        story.append(Paragraph(item, bullet_style))
    
    story.append(Paragraph("Trang chủ bao gồm:", subheading_style))
    homepage_items = [
        "• Banner khuyến mãi",
        "• Sản phẩm flash sale",
        "• Danh mục phổ biến",
        "• Sản phẩm đề xuất",
        "• Thương hiệu nổi tiếng",
        "• Tin tức và xu hướng"
    ]
    for item in homepage_items:
        story.append(Paragraph(item, bullet_style))
    
    story.append(PageBreak())
    
    # Chương 5: Tìm kiếm sản phẩm
    story.append(Paragraph("5. TÌM KIẾM VÀ DUYỆT SẢN PHẨM", heading_style))
    
    story.append(Paragraph("Cách tìm kiếm:", subheading_style))
    story.append(Paragraph("""
    1. Nhấn vào ô tìm kiếm ở đầu trang
    2. Nhập tên sản phẩm, thương hiệu hoặc từ khóa
    3. Chọn từ gợi ý hoặc nhấn nút tìm kiếm
    4. Sử dụng bộ lọc để thu hẹp kết quả
    """, normal_style))
    
    story.append(Paragraph("Bộ lọc tìm kiếm:", subheading_style))
    filter_items = [
        "• Khoảng giá: Từ thấp đến cao",
        "• Thương hiệu: Chọn nhãn hiệu yêu thích",
        "• Đánh giá: Từ 3-5 sao",
        "• Vị trí: Gần bạn nhất",
        "• Loại giao hàng: Nhanh, tiết kiệm",
        "• Khuyến mãi: Có ưu đãi đặc biệt"
    ]
    for item in filter_items:
        story.append(Paragraph(item, bullet_style))
    
    story.append(Paragraph("Duyệt theo danh mục:", subheading_style))
    story.append(Paragraph("""
    • Điện tử - Công nghệ
    • Thời trang Nam - Nữ
    • Mẹ & Bé
    • Nhà cửa - Đời sống
    • Sức khỏe - Làm đẹp
    • Thể thao - Du lịch
    """, normal_style))
    
    story.append(PageBreak())
    
    # Chương 6: Giỏ hàng
    story.append(Paragraph("6. THÊM SẢN PHẨM VÀO GIỎ HÀNG", heading_style))
    
    story.append(Paragraph("Cách thêm sản phẩm:", subheading_style))
    story.append(Paragraph("""
    1. Xem chi tiết sản phẩm
    2. Chọn màu sắc, kích thước (nếu có)
    3. Chọn số lượng muốn mua
    4. Nhấn "Thêm vào giỏ hàng"
    5. Tiếp tục mua sắm hoặc thanh toán
    """, normal_style))
    
    story.append(Paragraph("Quản lý giỏ hàng:", subheading_style))
    cart_features = [
        "• Xem tổng số sản phẩm và giá tiền",
        "• Thay đổi số lượng sản phẩm",
        "• Xóa sản phẩm không cần",
        "• Lưu sản phẩm yêu thích",
        "• Áp dụng mã giảm giá",
        "• Chọn phương thức giao hàng"
    ]
    for item in cart_features:
        story.append(Paragraph(item, bullet_style))
    
    story.append(PageBreak())
    
    # Chương 7: Thanh toán
    story.append(Paragraph("7. THANH TOÁN", heading_style))
    
    story.append(Paragraph("Các bước thanh toán:", subheading_style))
    story.append(Paragraph("""
    1. Kiểm tra giỏ hàng và nhấn "Thanh toán"
    2. Xác nhận địa chỉ giao hàng
    3. Chọn phương thức giao hàng
    4. Chọn phương thức thanh toán
    5. Áp dụng mã giảm giá (nếu có)
    6. Xác nhận và hoàn tất đơn hàng
    """, normal_style))
    
    story.append(Paragraph("Phương thức thanh toán:", subheading_style))
    payment_methods = [
        "• COD (Thanh toán khi nhận hàng)",
        "• Thẻ tín dụng/ghi nợ",
        "• Ví điện tử: ZaloPay, MoMo, VNPay",
        "• Chuyển khoản ngân hàng",
        "• Thanh toán qua QR Code"
    ]
    for method in payment_methods:
        story.append(Paragraph(method, bullet_style))
    
    story.append(Paragraph("Phí giao hàng:", subheading_style))
    story.append(Paragraph("""
    • Miễn phí giao hàng cho đơn từ 500.000đ
    • Giao hàng nhanh: 15.000đ - 25.000đ
    • Giao hàng tiết kiệm: 10.000đ - 15.000đ
    • Giao hàng hỏa tốc: 30.000đ - 50.000đ
    """, normal_style))
    
    story.append(PageBreak())
    
    # Chương 8: Quản lý đơn hàng
    story.append(Paragraph("8. QUẢN LÝ ĐƠN HÀNG", heading_style))
    
    story.append(Paragraph("Theo dõi đơn hàng:", subheading_style))
    story.append(Paragraph("""
    1. Vào mục "Tài khoản" > "Đơn hàng của tôi"
    2. Xem danh sách đơn hàng theo trạng thái
    3. Nhấn vào đơn hàng để xem chi tiết
    4. Theo dõi vị trí giao hàng real-time
    """, normal_style))
    
    story.append(Paragraph("Trạng thái đơn hàng:", subheading_style))
    order_status = [
        "• Chờ xác nhận: Đơn hàng đang được xử lý",
        "• Đã xác nhận: Shop đã nhận đơn",
        "• Đang chuẩn bị: Đóng gói sản phẩm",
        "• Đang giao hàng: Shipper đang vận chuyển",
        "• Đã giao: Đơn hàng hoàn thành",
        "• Đã hủy: Đơn hàng bị hủy bỏ"
    ]
    for status in order_status:
        story.append(Paragraph(status, bullet_style))
    
    story.append(Paragraph("Đổi trả hàng:", subheading_style))
    story.append(Paragraph("""
    • Thời hạn đổi trả: 7-15 ngày tùy sản phẩm
    • Điều kiện: Hàng còn nguyên tem, chưa sử dụng
    • Cách thức: Tạo yêu cầu trong app > Chờ xác nhận > Gửi hàng
    • Chi phí: Miễn phí nếu lỗi từ shop
    """, normal_style))
    
    story.append(PageBreak())
    
    # Chương 9: Cài đặt tài khoản
    story.append(Paragraph("9. CÀI ĐẶT TÀI KHOẢN", heading_style))
    
    story.append(Paragraph("Thông tin cá nhân:", subheading_style))
    profile_items = [
        "• Cập nhật ảnh đại diện",
        "• Thay đổi tên hiển thị",
        "• Thêm/sửa số điện thoại",
        "• Cập nhật email",
        "• Thông tin sinh nhật",
        "• Giới tính"
    ]
    for item in profile_items:
        story.append(Paragraph(item, bullet_style))
    
    story.append(Paragraph("Địa chỉ giao hàng:", subheading_style))
    story.append(Paragraph("""
    • Thêm nhiều địa chỉ giao hàng
    • Đặt địa chỉ mặc định
    • Sửa/xóa địa chỉ không dùng
    • Lưu địa chỉ văn phòng, nhà riêng
    """, normal_style))
    
    story.append(Paragraph("Bảo mật:", subheading_style))
    security_items = [
        "• Đổi mật khẩu định kỳ",
        "• Bật xác thực 2 lớp",
        "• Thiết lập vân tay/Face ID",
        "• Quản lý thiết bị đăng nhập",
        "• Xem lịch sử hoạt động"
    ]
    for item in security_items:
        story.append(Paragraph(item, bullet_style))
    
    story.append(PageBreak())
    
    # Chương 10: FAQ
    story.append(Paragraph("10. CÂU HỎI THƯỜNG GẶP (FAQ)", heading_style))
    
    faqs = [
        ("Làm sao để tracking đơn hàng?", 
         "Vào 'Tài khoản' > 'Đơn hàng của tôi' > Chọn đơn cần theo dõi. Bạn sẽ thấy trạng thái và vị trí hiện tại của đơn hàng."),
        
        ("Tại sao không nhận được mã OTP?", 
         "Kiểm tra spam/rác, đảm bảo số điện thoại chính xác, thử gửi lại sau 1 phút. Nếu vẫn không nhận được, liên hệ hotline."),
        
        ("Cách hủy đơn hàng?", 
         "Chỉ có thể hủy khi đơn hàng ở trạng thái 'Chờ xác nhận'. Vào chi tiết đơn hàng > Nhấn 'Hủy đơn' > Chọn lý do."),
        
        ("Sản phẩm bị lỗi thì làm sao?", 
         "Tạo yêu cầu đổi trả trong 'Đơn hàng của tôi' > Chọn 'Trả hàng/Hoàn tiền' > Upload hình ảnh và mô tả lỗi."),
        
        ("Làm sao để được miễn phí ship?", 
         "Đơn hàng từ 500.000đ được miễn phí giao hàng tiêu chuẩn. Một số sản phẩm có chương trình freeship riêng."),
        
        ("Có thể thay đổi địa chỉ giao hàng không?", 
         "Chỉ có thể thay đổi khi đơn hàng chưa được xác nhận. Sau khi shop xác nhận thì không thể thay đổi.")
    ]
    
    for question, answer in faqs:
        story.append(Paragraph(f"Q: {question}", subheading_style))
        story.append(Paragraph(f"A: {answer}", normal_style))
        story.append(Spacer(1, 10))
    
    story.append(PageBreak())
    
    # Chương 11: Liên hệ hỗ trợ
    story.append(Paragraph("11. LIÊN HỆ HỖ TRỢ", heading_style))
    
    story.append(Paragraph("Kênh hỗ trợ khách hàng:", subheading_style))
    contact_info = [
        "• Hotline: 1900 1234 (8h-22h hàng ngày)",
        "• Email: support@eshop.vn",
        "• Chat trực tuyến trong app (24/7)",
        "• Facebook: fb.com/eshopvietnam",
        "• Zalo OA: @eshopvn"
    ]
    for contact in contact_info:
        story.append(Paragraph(contact, bullet_style))
    
    story.append(Paragraph("Trung tâm trợ giúp:", subheading_style))
    story.append(Paragraph("""
    Truy cập mục "Trợ giúp" trong app để tìm câu trả lời nhanh cho các vấn đề thường gặp. 
    Hệ thống tự động phân loại và đưa ra giải pháp phù hợp.
    """, normal_style))
    
    story.append(Paragraph("Thời gian phản hồi:", subheading_style))
    response_times = [
        "• Chat trực tuyến: Ngay lập tức",
        "• Hotline: Trong 30 giây",
        "• Email: Trong 2-4 giờ",
        "• Facebook/Zalo: Trong 1 giờ"
    ]
    for time in response_times:
        story.append(Paragraph(time, bullet_style))
    
    story.append(Spacer(1, 30))
    story.append(Paragraph("Cảm ơn bạn đã sử dụng EShop!", title_style))
    story.append(Paragraph("Chúc bạn có trải nghiệm mua sắm tuyệt vời!", normal_style))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Đã tạo file PDF: {filename}")
    return filename

if __name__ == "__main__":
    try:
        filename = create_demo_pdf()
        print(f"🎉 File PDF demo đã được tạo: {filename}")
        print("📄 Bạn có thể sử dụng file này để test ứng dụng AI")
    except Exception as e:
        print(f"❌ Lỗi tạo PDF: {e}")
        print("💡 Cài đặt reportlab: pip install reportlab") 