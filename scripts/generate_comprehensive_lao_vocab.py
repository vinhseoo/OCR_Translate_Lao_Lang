"""
Script tự động sinh và nạp bộ từ điển đại trà thông dụng tiếng Lào (Lao Common Lexicon Generator)
Mục tiêu: Đưa kho từ vựng từ ~1,530 từ lên 3,000+ từ vựng giao tiếp, đời sống, học tập, công việc.
Đảm bảo 100% tuân thủ Quy chuẩn Unicode NFC (The Lao Golden Rule #1).
"""
import sys
import os
import csv
from pathlib import Path

# Force UTF-8 on Windows Console
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing.normalize import normalize_lao

CSV_PATH = PROJECT_ROOT / "data" / "dictionaries" / "lao_vi_en.csv"

# ==============================================================================
# DANH SÁCH BỘ TỪ THÔNG DỤNG MỞ RỘNG (MASSIVE EVERYDAY LAO CORPUS)
# ==============================================================================

RAW_VOCAB = [
    # --- 1. MẪU CÂU & TỪ GIAO TIẾP XÃ GIAO HÀNG NGÀY ---
    ("ສະບາຍດີຕອນເຊົ້າ", "chào buổi sáng", "good morning", "sabai dee ton sao", "phrase", "giao_tiep", "ສະບາຍດີຕອນເຊົ້າອາຈານ", "Chào buổi sáng thầy giáo"),
    ("ສະບາຍດີຕອນສວາຍ", "chào buổi trưa", "good afternoon", "sabai dee ton suay", "phrase", "giao_tiep", "ສະບາຍດີຕອນສວາຍທຸກຄົນ", "Chào buổi trưa mọi người"),
    ("ສະບາຍດີຕອນແລງ", "chào buổi tối", "good evening", "sabai dee ton laeng", "phrase", "giao_tiep", "ສະບາຍດີຕອນແລງເພື່ອນ", "Chào buổi tối bạn bè"),
    ("ນອນຫຼັບຝັນດີ", "chúc ngủ ngon", "good night", "non lap fan dee", "phrase", "giao_tiep", "ນອນຫຼັບຝັນດີເດີ້", "Chúc ngủ ngon nhé"),
    ("ຝັນດີ", "chúc ngủ ngon / mộng đẹp", "sweet dreams", "fan dee", "phrase", "giao_tiep", "ຝັນດີເດີ້", "Ngủ ngon nhé"),
    ("ໂຊກດີ", "chúc may mắn", "good luck", "sok dee", "phrase", "giao_tiep", "ຂໍໃຫ້ເຈົ້າໂຊກດີ", "Chúc bạn may mắn"),
    ("ຍິນດີຕ້ອນຮັບ", "nhiệt liệt chào đón", "welcome", "yin dee ton hap", "phrase", "giao_tiep", "ຍິນດີຕ້ອນຮັບສູ່ປະເທດລາວ", "Chào mừng đến với nước Lào"),
    ("ຍິນດີທີ່ໄດ້ຮູ້ຈັກ", "rất vui được làm quen", "nice to meet you", "yin dee thee dai hoo jak", "phrase", "giao_tiep", "ຍິນດີທີ່ໄດ້ຮູ້ຈັກທ່ານ", "Rất vui được quen biết ngài"),
    ("ລາກ່ອນ", "tạm biệt", "goodbye", "la gon", "phrase", "giao_tiep", "ລາກ່ອນແລ້ວພົບກັນໃໝ່", "Tạm biệt rồi gặp lại sau"),
    ("ພົບກັນໃໝ່", "hẹn gặp lại", "see you again", "phop kan mai", "phrase", "giao_tiep", "ມື້ອື່ນພົບກັນໃໝ່", "Ngày mai gặp lại nhé"),
    ("ໄປກ່ອນເດີ້", "tôi đi trước nhé", "I'm leaving now", "pai gon der", "phrase", "giao_tiep", "ຂ້ອຍຂໍໄປກ່ອນເດີ້", "Tôi xin phép đi trước nhé"),
    ("ຂໍໂທດຫຼາຍໆ", "vô cùng xin lỗi", "so sorry / apologize", "kho thot lai lai", "phrase", "giao_tiep", "ຂ້ອຍຂໍໂທດຫຼາຍໆເດີ້", "Tôi vô cùng xin lỗi nhé"),
    ("ບໍ່ມີບັນຫາ", "không có vấn đề gì", "no problem", "bor mee ban ha", "phrase", "giao_tiep", "ເລື່ອງນ້ອຍ ບໍ່ມີບັນຫາ", "Chuyện nhỏ, không vấn đề gì"),
    ("ບໍ່ເປັນຫຍັງດອກ", "không sao đâu mà", "don't worry about it", "bor pen yang dok", "phrase", "giao_tiep", "ບໍ່ເປັນຫຍັງດອກ ຢ່າຄິດຫຼາຍ", "Không sao đâu, đừng suy nghĩ nhiều"),
    ("ຊ່ວຍຂ້ອຍແດ່", "hãy giúp tôi với", "please help me", "suay khoy dae", "phrase", "giao_tiep", "ກະລຸນາຊ່ວຍຂ້ອຍແດ່", "Làm ơn giúp tôi với"),
    ("ກະລຸນາ", "làm ơn / xin vui lòng", "please", "ka lu na", "adv", "giao_tiep", "ກະລຸນາລໍຖ້າຈັກໜ່ອຍ", "Làm ơn chờ một chút"),
    ("ຈັກໜ່ອຍ", "một chút / lát nữa", "a little / in a moment", "jak noy", "adv", "thoi_gian", "ຖ້າຂ້ອຍຈັກໜ່ອຍ", "Đợi tôi một chút"),
    ("ດຽວນີ້", "ngay bây giờ", "right now", "diao nee", "adv", "thoi_gian", "ມາຮອດດຽວນີ້", "Đến ngay bây giờ"),
    ("ໄວໆ", "nhanh lên", "hurry up / quickly", "vai vai", "adv", "giao_tiep", "ຍ່າງໄວໆແດ່", "Đi nhanh lên chút"),
    ("ຊ້າໆ", "từ từ / chậm rãi", "slowly", "sa sa", "adv", "giao_tiep", "ເວົ້າຊ້າໆແດ່", "Nói chậm chậm lại chút"),

    # --- 2. HỌ HÀNG & GIA ĐÌNH MỞ RỘNG ---
    ("ພໍ່ເຖົ້າ", "ông ngoại", "maternal grandfather", "phor thao", "noun", "gia_dinh", "ພໍ່ເຖົ້າຢູ່ບ້ານນອກ", "Ông ngoại ở quê"),
    ("ແມ່ເຖົ້າ", "bà ngoại", "maternal grandmother", "mae thao", "noun", "gia_dinh", "ແມ່ເຖົ້າເຮັດເຂົ້າຕົ້ມ", "Bà ngoại làm bánh tét"),
    ("ປູ່", "ông nội", "paternal grandfather", "pu", "noun", "gia_dinh", "ປູ່ມີສຸຂະພາບແຂງແຮງ", "Ông nội sức khỏe dồi dào"),
    ("ຍ່າ", "bà nội", "paternal grandmother", "ya", "noun", "gia_dinh", "ຍ່າອາຍຸແປດສິບປີ", "Bà nội tám mươi tuổi"),
    ("ລຸງ", "bác trai", "uncle (older)", "loong", "noun", "gia_dinh", "ລຸງຂ້ອຍເປັນນາຍບ້ານ", "Bác trai tôi làm trưởng thôn"),
    ("ປ້າ", "bác gái", "aunt (older)", "pa", "noun", "gia_dinh", "ປ້າເຮັດແກງແຊບ", "Bác gái nấu canh ngon"),
    ("ອາວ", "chú (em trai bố)", "uncle (younger brother of father)", "aao", "noun", "gia_dinh", "ອາວໄປເຮັດວຽກ", "Chú đi làm việc"),
    ("ອາ", "cô (em gái bố)", "aunt (younger sister of father)", "aa", "noun", "gia_dinh", "ອາສອນໜັງສື", "Cô dạy học"),
    ("ນ້າບ່າວ", "cậu (em trai mẹ)", "maternal uncle", "na bao", "noun", "gia_dinh", "ນ້າບ່າວຊື້ລົດໃໝ່", "Cậu mua xe mới"),
    ("ນ້າສາວ", "dì (em gái mẹ)", "maternal aunt", "na sao", "noun", "gia_dinh", "ນ້າສາວຂາຍເຄື່ອງ", "Dì bán hàng"),
    ("ຫຼານຊາຍ", "cháu trai", "nephew / grandson", "lan xai", "noun", "gia_dinh", "ຫຼານຊາຍຮຽນເກັ່ງ", "Cháu trai học giỏi"),
    ("ຫຼານສາວ", "cháu gái", "niece / granddaughter", "lan sao", "noun", "gia_dinh", "ຫຼານສາວໜ້າຮັກ", "Cháu gái dễ thương"),
    ("ລູກເຂີຍ", "con rể", "son-in-law", "look khoey", "noun", "gia_dinh", "ລູກເຂີຍດຸໝັ່ນ", "Con rể chăm chỉ"),
    ("ລູກໃພ້", "con dâu", "daughter-in-law", "look phai", "noun", "gia_dinh", "ລູກໃພ້ດີ", "Con dâu hiền"),
    ("ອ້າຍເຂີຍ", "anh rể", "brother-in-law (older)", "ai khoey", "noun", "gia_dinh", "ອ້າຍເຂີຍຂັບລົດ", "Anh rể lái xe"),
    ("ເອື້ອຍໃພ້", "chị dâu", "sister-in-law (older)", "euay phai", "noun", "gia_dinh", "ເອື້ອຍໃພ້ໄປຕະຫຼາດ", "Chị dâu đi chợ"),
    ("ພໍ່ແມ່", "cha mẹ / bố mẹ", "parents", "phor mae", "noun", "gia_dinh", "ຂ້ອຍຮັກພໍ່ແມ່", "Tôi thương cha mẹ"),
    ("ຍາດຕິພີ່ນ້ອງ", "bà con thân thích / họ hàng", "relatives", "yat ti phee nong", "noun", "gia_dinh", "ຍາດຕິພີ່ນ້ອງມາຢາມ", "Họ hàng đến thăm"),
    ("ຄອບຄົວໃຫຍ່", "đại gia đình", "extended family", "khop khua yai", "noun", "gia_dinh", "ພວກເຮົາມີຄອບຄົວໃຫຍ່", "Chúng tôi có một đại gia đình"),
    ("ຄູ່ສົມລົດ", "vợ chồng / cặp đôi kết hôn", "spouse / married couple", "khu som lod", "noun", "gia_dinh", "ຄູ່ສົມລົດໃໝ່", "Cặp vợ chồng mới cưới"),

    # --- 3. ĐỒNG TIỀN, MUA SẮM & KINH TẾ (SHOPPING & COMMERCE) ---
    ("ລາຄາ", "giá cả", "price", "la kha", "noun", "mua_sam", "ລາຄານີ້ຖືກແລ້ວ", "Giá này rẻ rồi"),
    ("ລາຄາຖືກ", "giá rẻ", "cheap price", "la kha theuk", "adj", "mua_sam", "ເຄື່ອງຢູ່ຕະຫຼາດລາຄາຖືກ", "Đồ ở chợ giá rẻ"),
    ("ລາຄາແພງ", "giá đắt", "expensive price", "la kha phaeng", "adj", "mua_sam", "ໂທລະສັບລາຄາແພງ", "Điện thoại giá đắt"),
    ("ຫຼຸດລາຄາ", "giảm giá", "discount", "loot la kha", "verb", "mua_sam", "ຫຼຸດລາຄາໃຫ້ແດ່ໄດ້ບໍ່", "Giảm giá cho tôi chút được không"),
    ("ໃບຮັບເງິນ", "biên lai / hóa đơn thu tiền", "receipt", "bai hap ngen", "noun", "mua_sam", "ຂໍໃບຮັບເງິນແດ່", "Cho xin biên lai với"),
    ("ໃບເກັບເງິນ", "hóa đơn thanh toán", "invoice / bill", "bai kep ngen", "noun", "mua_sam", "ກວດກາໃບເກັບເງິນ", "Kiểm tra hóa đơn"),
    ("ເງິນສົດ", "tiền mặt", "cash", "ngen sod", "noun", "mua_sam", "ຂ້ອຍຈ່າຍເປັນເງິນສົດ", "Tôi thanh toán bằng tiền mặt"),
    ("ເງິນໂອນ", "tiền chuyển khoản", "bank transfer money", "ngen on", "noun", "mua_sam", "ຈ່າຍດ້ວຍເງິນໂອນ", "Thanh toán bằng chuyển khoản"),
    ("ໂອນເງິນ", "chuyển khoản tiền", "transfer money", "on ngen", "verb", "mua_sam", "ຂ້ອຍຈະໂອນເງິນໃຫ້", "Tôi sẽ chuyển tiền cho"),
    ("ເງິນທອນ", "tiền thối lại / tiền thừa", "change (money)", "ngen thon", "noun", "mua_sam", "ນີ້ແມ່ນເງິນທອນຂອງເຈົ້າ", "Đây là tiền thừa của bạn"),
    ("ທອນເງິນ", "thối tiền lại", "give change", "thon ngen", "verb", "mua_sam", "ຢ່າລືມທອນເງິນ", "Đừng quên thối tiền"),
    ("ຕູ້ເອທີເອັມ", "cây ATM", "ATM machine", "too ATM", "noun", "mua_sam", "ໄປຖອນເງິນຢູ່ຕູ້ເອທີເອັມ", "Đi rút tiền ở cây ATM"),
    ("ຖອນເງິນ", "rút tiền", "withdraw money", "thon ngen", "verb", "tai_chinh", "ຂ້ອຍໄປຖອນເງິນ", "Tôi đi rút tiền"),
    ("ຝາກເງິນ", "gửi tiền tiết kiệm", "deposit money", "fak ngen", "verb", "tai_chinh", "ຝາກເງິນເຂົ້າທະນາຄານ", "Gửi tiền vào ngân hàng"),
    ("ບັນຊີທະນາຄານ", "tài khoản ngân hàng", "bank account", "ban see tha na khan", "noun", "tai_chinh", "ເລກບັນຊີທະນາຄານ", "Số tài khoản ngân hàng"),
    ("ບັດເຄຣດິດ", "thẻ tín dụng", "credit card", "bat credit", "noun", "tai_chinh", "ຮູດບັດເຄຣດິດ", "Quẹt thẻ tín dụng"),
    ("ດອກເບ້ຍ", "lãi suất", "interest rate", "dok bia", "noun", "tai_chinh", "ດອກເບ້ຍເງິນຝາກ", "Lãi suất tiền gửi"),
    ("ໜີ້ສິນ", "nợ nần", "debt", "nee sin", "noun", "tai_chinh", "ບໍ່ມີໜີ້ສິນ", "Không có nợ nần"),
    ("ກູ້ຢືມ", "vay mượn", "borrow / loan", "ku yeum", "verb", "tai_chinh", "ກູ້ຢືມເງິນຈາກທະນາຄານ", "Vay tiền từ ngân hàng"),
    ("ລົງທຶນ", "đầu tư", "invest", "long theun", "verb", "tai_chinh", "ລົງທຶນໃສ່ທຸລະກິດ", "Đầu tư vào kinh doanh"),
    ("ກຳໄລ", "lợi nhuận / tiền lời", "profit", "kam lai", "noun", "tai_chinh", "ໄດ້ກຳໄລຫຼາຍ", "Thu được nhiều lợi nhuận"),
    ("ຂາດທຶນ", "thua lỗ", "loss (financial)", "khat theun", "verb", "tai_chinh", "ປີນີ້ບໍ່ຂາດທຶນ", "Năm nay không bị lỗ"),
    ("ຮ້ານຄ້າ", "cửa hàng buôn bán", "retail store", "han kha", "noun", "mua_sam", "ຮ້ານຄ້າເປີດແຕ່ເຊົ້າ", "Cửa hàng mở từ sáng"),
    ("ສັບພະສິນຄ້າ", "trung tâm thương mại bách hóa", "department store / mall", "sap pha sin kha", "noun", "mua_sam", "ໄປສູນສັບພະສິນຄ້າ", "Đi trung tâm bách hóa"),
    ("ຕະຫຼາດກາງຄືນ", "chợ đêm", "night market", "ta lat kang kheun", "noun", "mua_sam", "ຕະຫຼາດກາງຄືນຫຼວງພະບາງ", "Chợ đêm Luang Prabang"),
    ("ຕະຫຼາດເຊົ້າ", "chợ sáng", "morning market", "ta lat sao", "noun", "mua_sam", "ຕະຫຼາດເຊົ້າວຽງຈັນ", "Chợ Sáng Viêng Chăn"),
    ("ລູກຄ້າ", "khách hàng", "customer / client", "look kha", "noun", "mua_sam", "ລູກຄ້າຄືພະເຈົ້າ", "Khách hàng là thượng đế"),
    ("ແມ່ຄ້າ", "bà chủ tiệm / người bán hàng nữ", "female seller", "mae kha", "noun", "mua_sam", "ແມ່ຄ້າຍິ້ມແຍ້ມ", "Bà bán hàng tươi cười"),
    ("ພໍ່ຄ້າ", "ông chủ tiệm / thương nhân nam", "merchant / vendor", "phor kha", "noun", "mua_sam", "ພໍ່ຄ້າມາຈາກຕ່າງແຂວງ", "Thương gia đến từ tỉnh khác"),

    # --- 4. CÁC TỪ LOẠI DANH TỪ GHÉP: ການ- (HÀNH ĐỘNG / DANH TỪ HÓA) ---
    ("ການຮຽນ", "việc học tập", "study / learning", "kan hian", "noun", "giao_duc", "ການຮຽນມີຄວາມສຳຄັນ", "Việc học tập có tầm quan trọng"),
    ("ການສອນ", "việc giảng dạy", "teaching", "kan son", "noun", "giao_duc", "ການສອນຂອງຄູດີຫຼາຍ", "Việc dạy của cô rất hay"),
    ("ການສຶກສາ", "ngành giáo dục", "education", "kan seuk sa", "noun", "giao_duc", "ກະຊວງສຶກສາທິການ", "Bộ Giáo dục"),
    ("ການເຮັດວຽກ", "việc làm / lao động", "working / labor", "kan hed viak", "noun", "cong_viec", "ການເຮັດວຽກເປັນທີມ", "Làm việc theo nhóm"),
    ("ການເດີນທາງ", "chuyến đi / sự du hành", "travel / journey", "kan dern thang", "noun", "du_lich", "ຂໍໃຫ້ການເດີນທາງປອດໄພ", "Chúc chuyến đi bình an"),
    ("ການທ່ອງທ່ຽວ", "ngành du lịch", "tourism", "kan thong thiao", "noun", "du_lich", "ການທ່ອງທ່ຽວລາວຂະຫຍາຍຕົວ", "Du lịch Lào đang phát triển"),
    ("ການສື່ສານ", "sự truyền thông / giao tiếp", "communication", "kan seu san", "noun", "cong_nghe", "ການສື່ສານທັນສະໄໝ", "Truyền thông hiện đại"),
    ("ການຄ້າ", "hoạt động thương mại", "trade / commerce", "kan kha", "noun", "kinh_te", "ການຄ້າລະຫວ່າງປະເທດ", "Thương mại quốc tế"),
    ("ການແພດ", "ngành y tế", "medicine / healthcare", "kan phaed", "noun", "y_te", "ຄວາມກ້າວໜ້າທາງການແພດ", "Tiến bộ trong y học"),
    ("การເມືອງ", "chính trị", "politics", "kan meuang", "noun", "xa_hoi", "ສະພາບການເມືອງສະຫງົບ", "Tình hình chính trị ổn định"),
    ("ການປົກຄອງ", "sự cai trị / quản lý hành chính", "governance / administration", "kan pok khong", "noun", "xa_hoi", "ລະບົບການປົກຄອງ", "Hệ thống quản lý hành chính"),
    ("ການຜະລິດ", "khâu sản xuất", "production / manufacturing", "kan pha lit", "noun", "kinh_te", "ການຜະລິດສິນຄ້າກະສິກຳ", "Sản xuất nông sản"),
    ("ການກໍ່ສ້າງ", "ngành xây dựng", "construction", "kan kor sang", "noun", "kinh_te", "ການກໍ່ສ້າງຂົວຂ້າມນ້ຳຂອງ", "Xây dựng cầu qua sông Mê Kông"),
    ("ການຂົນສົ່ງ", "ngành giao thông vận tải", "transportation / logistics", "kan khon song", "noun", "kinh_te", "ການຂົນສົ່ງສິນຄ້າ", "Vận tải hàng hóa"),
    ("ການບໍລິການ", "khâu phục vụ / dịch vụ", "service", "kan bor li kan", "noun", "kinh_te", "ການບໍລິການດີເດັ່ນ", "Dịch vụ xuất sắc"),
    ("ການຮ່ວມມື", "sự hợp tác hữu nghị", "cooperation / partnership", "kan huam meu", "noun", "quan_he", "ການຮ່ວມມືລາວ-ຫວຽດ", "Sự hợp tác Lào - Việt"),
    ("ການປ່ຽນແປງ", "sự biến đổi / thay đổi", "change / transformation", "kan pian paeng", "noun", "doi_song", "ການປ່ຽນແປງດິນຟ້າອາກາດ", "Biến đổi khí hậu"),
    ("ການພັດທະນາ", "sự phát triển", "development", "kan phat tha na", "noun", "kinh_te", "ການພັດທະນາປະເທດຊາດ", "Sự phát triển đất nước"),
    ("ການຊ່ວຍເຫຼືອ", "sự trợ giúp / cứu trợ", "assistance / aid", "kan suay leua", "noun", "xa_hoi", "ໄດ້ຮັບການຊ່ວຍເຫຼືອ", "Nhận được sự trợ giúp"),
    ("ການປົກປັກຮັກສາ", "sự giữ gìn và bảo vệ", "preservation / protection", "kan pok pak hak sa", "noun", "xa_hoi", "ການປົກປັກຮັກສາສິ່ງແວດລ້ອມ", "Bảo vệ môi trường"),
    ("ການແຂ່ງຂັນ", "cuộc thi đấu / cạnh tranh", "competition / match", "kan khaeng khan", "noun", "the_thao", "ການແຂ່ງຂັນບານເຕະ", "Cuộc thi đấu bóng đá"),
    ("ການສອບເສັງ", "kỳ thi cử", "examination / test", "kan sop seng", "noun", "giao_duc", "ຜົນການສອບເສັງອອກແລ້ວ", "Kết quả thi đã có rồi"),
    ("ການນຳໃຊ້", "việc áp dụng / sử dụng", "utilization / application", "kan nam sai", "noun", "cong_nghe", "ການນຳໃຊ້ເຕັກໂນໂລຊີ", "Ứng dụng công nghệ"),
    ("ການຄົ້ນຄວ້າ", "việc nghiên cứu khoa học", "research", "kan khon khua", "noun", "khoa_hoc", "ການຄົ້ນຄວ້າວິທະຍາສາດ", "Nghiên cứu khoa học"),

    # --- 5. CÁC TỪ LOẠI DANH TỪ GHÉP: ຄວາມ- (TÍNH CHẤT / TRẠNG THÁI TÂM LÝ) ---
    ("ຄວາມຮັກ", "tình yêu thương", "love", "khuam hak", "noun", "cam_xuc", "ຄວາມຮັກຂອງແມ່ຍິ່ງໃຫຍ່", "Tình thương của mẹ vĩ đại"),
    ("ຄວາມສຸກ", "niềm hạnh phúc", "happiness", "khuam sook", "noun", "cam_xuc", "ຂໍໃຫ້ມີຄວາມສຸກຕະຫຼອດໄປ", "Chúc luôn luôn hạnh phúc"),
    ("ຄວາມທຸກ", "nỗi thống khổ / đau khổ", "suffering / misery", "khuam thook", "noun", "cam_xuc", "ຜ່ານຜ່າຄວາມທຸກຍາກ", "Vượt qua gian khổ"),
    ("ຄວາມສະອາດ", "vệ sinh / sự sạch sẽ", "cleanliness", "khuam sa at", "noun", "doi_song", "ຮັກສາຄວາມສະອາດ", "Giữ gìn vệ sinh"),
    ("ຄວາມງາມ", "vẻ đẹp / mỹ thuật", "beauty", "khuam ngam", "noun", "nghe_thuat", "ຄວາມງາມທຳມະຊາດ", "Vẻ đẹp thiên nhiên"),
    ("ຄວາມຈິງ", "sự thật chân thực", "truth / fact", "khuam jing", "noun", "doi_song", "ເວົ້າຄວາມຈິງສະເໝີ", "Luôn nói sự thật"),
    ("ຄວາມຫວັງ", "niềm hy vọng", "hope", "khuam vang", "noun", "cam_xuc", "ຍັງມີຄວາມຫວັງຢູ່", "Vẫn còn niềm hy vọng"),
    ("ຄວາມຝັນ", "ước mơ / giấc chiêm bao", "dream", "khuam fan", "noun", "cam_xuc", "ເຮັດໃຫ້ຄວາມຝັນເປັນຈິງ", "Biến ước mơ thành hiện thực"),
    ("ຄວາມພະຍາຍາມ", "sự nỗ lực / kiên trì", "effort / perseverance", "khuam pha ya yam", "noun", "tinh_cach", "ຄວາມພະຍາຍາມຢູ່ໃສ ຄວາມສຳເລັດຢູ່ນັ້ນ", "Có công mài sắt có ngày nên kim"),
    ("ຄວາມສຳເລັດ", "sự thành công", "success", "khuam sam led", "noun", "cong_viec", "ສະແດງຄວາມຍິນດີກັບຄວາມສຳເລັດ", "Chúc mừng sự thành công"),
    ("ຄວາມຫຍຸ້ງຍາກ", "sự khó khăn / phiền toái", "difficulty / hardship", "khuam hyung yak", "noun", "doi_song", "ແກ້ໄຂຄວາມຫຍຸ້ງຍາກ", "Tháo gỡ những khó khăn"),
    ("ຄວາມປອດໄພ", "sự an toàn", "safety / security", "khuam pod phai", "noun", "doi_song", "ຄຳນຶງເຖິງຄວາມປອດໄພກ່ອນ", "Đặt an toàn lên trên hết"),
    ("ຄວາມສະດວກ", "sự tiện lợi", "convenience", "khuam sa duak", "noun", "doi_song", "ສ້າງຄວາມສະດວກສະບາຍ", "Tạo sự tiện nghi"),
    ("ຄວາມຮັບຜິດຊອບ", "tinh thần trách nhiệm", "responsibility", "khuam hap phid sop", "noun", "tinh_cach", "ມີຄວາມຮັບຜິດຊອບສູງ", "Có tinh thần trách nhiệm cao"),
    ("ຄວາມເຂົ້າໃຈ", "sự thấu hiểu", "understanding", "khuam khao jai", "noun", "cam_xuc", "ສ້າງຄວາມເຂົ້າໃຈເຊິ່ງກັນແລະກັນ", "Tạo sự hiểu biết lẫn nhau"),
    ("ຄວາມໄວ", "tốc độ", "speed / velocity", "khuam vai", "noun", "khoa_hoc", "ຈຳກັດຄວາມໄວ", "Giới hạn tốc độ"),
    ("ຄວາມແຮງ", "lực / sức mạnh cường độ", "strength / intensity", "khuam haeng", "noun", "khoa_hoc", "ຄວາມແຮງຂອງລົມ", "Cường độ của gió"),
    ("ຄວາມອົບອຸ່ນ", "sự ấm cúng / nồng ấm", "warmth", "khuam ob un", "noun", "cam_xuc", "ຄອບຄົວອົບອຸ່ນ", "Gia đình ấm cúng"),
    ("ຄວາມຊື່ສັດ", "đức tính thật thà / trung thực", "honesty / loyalty", "khuam seu sat", "noun", "tinh_cach", "ຄວາມຊື່ສັດເປັນສິ່ງສຳຄັນ", "Tính trung thực là điều quan trọng"),
    ("ຄວາມສະຫງົບ", "sự thanh bình / hòa bình", "peace / tranquility", "khuam sa ngop", "noun", "xa_hoi", "ຮັກສາຄວາມສະຫງົບ", "Gìn giữ hòa bình"),
    ("ຄວາມຮ້ອນ", "sức nóng / nhiệt độ", "heat", "khuam hon", "noun", "khoa_hoc", "ຄວາມຮ້ອນແສງຕາເວັນ", "Sức nóng của mặt trời"),
    ("ຄວາມເຢັນ", "hơi lạnh", "coldness / chill", "khuam yen", "noun", "khoa_hoc", "ຄວາມເຢັນຂອງລະດູໜາວ", "Cái lạnh của mùa đông"),
    ("ຄວາມມືດ", "bóng tối / bóng đêm", "darkness", "khuam meud", "noun", "tu_nhien", "ໃນຄວາມມືດ", "Trong bóng tối"),
    ("ຄວາມສະຫວ່າງ", "ánh sáng / sự sáng tỏ", "brightness / light", "khuam sa vang", "noun", "tu_nhien", "ຄວາມສະຫວ່າງຂອງດວງຈັນ", "Ánh sáng của mặt trăng"),

    # --- 6. CÁC TỪ LOẠI DANH TỪ GHÉP: ຜູ້- & ນັກ- (DANH XƯNG NGHỀ NGHIỆP / VAI TRÒ) ---
    ("ຜູ້ອຳນວຍການ", "giám đốc / hiệu trưởng", "director / principal", "phu am nuay kan", "noun", "chuc_vu", "ຜູ້ອຳນວຍການໂຮງຮຽນ", "Hiệu trưởng nhà trường"),
    ("ຜູ້ຈັດການ", "người quản lý / manager", "manager", "phu jad kan", "noun", "chuc_vu", "ຜູ້ຈັດການຮ້ານ", "Quản lý cửa hàng"),
    ("ຜູ້ຊ່ວຍ", "trợ lý / người giúp việc", "assistant / helper", "phu suay", "noun", "chuc_vu", "ຜູ້ຊ່ວຍອາຈານ", "Trợ giảng / trợ lý thầy"),
    ("ຜູ້ຊ່ຽວຊານ", "chuyên gia", "expert / specialist", "phu siao san", "noun", "chuc_vu", "ຜູ້ຊ່ຽວຊານດ້ານໄອທີ", "Chuyên gia công nghệ thông tin"),
    ("ຜູ້ໂດຍສານ", "hành khách", "passenger", "phu doy san", "noun", "giao_thong", "ຜູ້ໂດຍສານຂຶ້ນລົດໄຟ", "Hành khách lên tàu hỏa"),
    ("ຜູ້ຂັບຂີ່", "tài xế / người điều khiển xe", "driver / rider", "phu khap khee", "noun", "giao_thong", "ຜູ້ຂັບຂີ່ຕ້ອງໃສ່ໝວກກັນກະທົບ", "Người lái xe phải đội mũ bảo hiểm"),
    ("ຜູ້ປ່ວຍ", "bệnh nhân", "patient", "phu puay", "noun", "y_te", "ທ່ານໝໍກວດຜູ້ປ່ວຍ", "Bác sĩ khám cho bệnh nhân"),
    ("ຜູ້ແທນ", "đại biểu / người đại diện", "representative / delegate", "phu thaen", "noun", "xa_hoi", "ຜູ້ແທນປະຊາຊົນ", "Đại biểu nhân dân"),
    ("ຜູ້ຟັງ", "thính giả / người nghe", "listener / audience", "phu fang", "noun", "xa_hoi", "ຜູ້ຟັງລາຍການວິທະຍຸ", "Thính giả nghe đài phát thanh"),
    ("ຜູ້ອ່ານ", "độc giả / người đọc", "reader", "phu an", "noun", "xa_hoi", "ຈົດໝາຍຈາກຜູ້ອ່ານ", "Thư từ độc giả"),
    ("ຜູ້ຊົມ", "khán giả xem", "spectator / viewer", "phu xom", "noun", "xa_hoi", "ຜູ້ຊົມຕົບມືຊົມເຊີຍ", "Khán giả vỗ tay tán thưởng"),
    ("ຜູ້ສະໝັກ", "ứng viên / người nộp đơn", "candidate / applicant", "phu sa mak", "noun", "cong_viec", "ຜູ້ສະໝັກງານໃໝ່", "Ứng viên tìm việc mới"),
    ("ຜູ້ຜະລິດ", "nhà sản xuất", "producer / manufacturer", "phu pha lit", "noun", "kinh_te", "ຜູ້ຜະລິດກະສິກຳ", "Nhà sản xuất nông nghiệp"),
    ("ຜູ້ບໍລິໂພກ", "người tiêu dùng", "consumer", "phu bor li phok", "noun", "kinh_te", "ປົກປ້ອງສິດຂອງຜູ້ບໍລິໂພກ", "Bảo vệ quyền lợi người tiêu dùng"),
    ("ນັກທຸລະກິດ", "doanh nhân", "businessman / entrepreneur", "nak thu la kid", "noun", "nghe_nghiep", "ນັກທຸລະກິດໜຸ່ມ", "Doanh nhân trẻ"),
    ("ນັກກິລາ", "vận động viên thể thao", "athlete / sportsman", "nak ki la", "noun", "nghe_nghiep", "ນັກກິລາແລ່ນໄວ", "Vận động viên điền kinh"),
    ("ນັກຂ່າວ", "phóng viên / nhà báo", "journalist / reporter", "nak khao", "noun", "nghe_nghiep", "ນັກຂ່າວລົງພາກສະໜາມ", "Phóng viên xuống hiện trường"),
    ("ນັກຮ້ອງ", "ca sĩ", "singer", "nak hong", "noun", "nghe_nghiep", "ນັກຮ້ອງສຽງດີ", "Ca sĩ có giọng hát hay"),
    ("ນັກສະແດງ", "diễn viên", "actor / actress", "nak sa daeng", "noun", "nghe_nghiep", "ນັກສະແດງຮູບເງົາ", "Diễn viên điện ảnh"),
    ("ນັກວິທະຍາສາດ", "nhà khoa học", "scientist", "nak vit tha ya sad", "noun", "nghe_nghiep", "ນັກວິທະຍາສາດຄົ້ນຄວ້າ", "Nhà khoa học nghiên cứu"),
    ("ນັກບິນ", "phi công", "pilot", "nak bin", "noun", "nghe_nghiep", "ນັກບິນຂັບເຮືອບິນ", "Phi công lái máy bay"),
    ("ນັກຂຽນ", "nhà văn / tác giả", "writer / author", "nak khian", "noun", "nghe_nghiep", "ນັກຂຽນປຶ້ມ", "Tác giả cuốn sách"),
    ("ນັກແຕ້ມ", "họa sĩ", "painter / artist", "nak taem", "noun", "nghe_nghiep", "ນັກແຕ້ມຮູບງາມ", "Họa sĩ vẽ tranh đẹp"),
    ("ນັກກົດໝາຍ", "luật sư / chuyên gia luật", "lawyer / jurist", "nak kod mai", "noun", "nghe_nghiep", "ປຶກສານັກກົດໝາຍ", "Tham khảo ý kiến luật sư"),
    ("ນັກການທູດ", "nhà ngoại giao", "diplomat", "nak kan thoot", "noun", "nghe_nghiep", "ຄະນະນັກການທູດ", "Đoàn ngoại giao"),

    # --- 7. CÔNG NGHỆ, THIẾT BỊ ĐIỆN TỬ & INTERNET (DIGITAL & MODERN TECH) ---
    ("ໂທລະສັບມືຖື", "điện thoại di động", "mobile phone / smartphone", "tho la sap meu theu", "noun", "cong_nghe", "ໂທລະສັບມືຖືລຸ້ນໃໝ່", "Điện thoại di động đời mới"),
    ("ສາກແບັດ", "sạc pin", "charge battery", "sak bat", "verb", "cong_nghe", "ຂ້ອຍກຳລັງສາກແບັດ", "Tôi đang sạc pin"),
    ("ແບັດເຕີຣີ", "pin điện thoại / ắc quy", "battery", "bat ter ry", "noun", "cong_nghe", "ແບັດເຕີຣີໝົດແລ້ວ", "Hết pin rồi"),
    ("ສາຍສາກ", "dây cáp sạc", "charging cable", "sai sak", "noun", "cong_nghe", "ຢືມສາຍສາກແດ່", "Cho mượn dây sạc với"),
    ("ຫູຟັງ", "tai nghe", "headphones / earphones", "hoo fang", "noun", "cong_nghe", "ໃສ່ຫູຟັງຟັງເພງ", "Đeo tai nghe nghe nhạc"),
    ("ອິນເຕີເນັດ", "mạng internet", "internet", "in ter net", "noun", "cong_nghe", "ເຊື່ອມຕໍ່ອິນເຕີເນັດ", "Kết nối internet"),
    ("ສັນຍານໄວໄຟ", "sóng Wifi", "Wi-Fi signal", "san yan wifi", "noun", "cong_nghe", "ຂໍລະຫັດສັນຍານໄວໄຟແດ່", "Cho xin mật khẩu Wifi với"),
    ("ລະຫັດຜ່ານ", "mật khẩu / password", "password", "la hat phan", "noun", "cong_nghe", "ປ້ອນລະຫັດຜ່ານ", "Nhập mật khẩu"),
    ("ຊື່ຜູ້ໃຊ້", "tên đăng nhập / username", "username", "xeu phu sai", "noun", "cong_nghe", "ກະລຸນາໃສ່ຊື່ຜູ້ໃຊ້", "Vui lòng nhập tên người dùng"),
    ("ດາວໂຫຼດ", "tải xuống", "download", "down load", "verb", "cong_nghe", "ດາວໂຫຼດເອກະສານ", "Tải tài liệu về"),
    ("ອັບໂຫຼດ", "tải lên", "upload", "up load", "verb", "cong_nghe", "ອັບໂຫຼດຮູບພາບ", "Tải ảnh lên"),
    ("ອີເມວ", "thư điện tử / email", "email", "ee mew", "noun", "cong_nghe", "ສົ່ງອີເມວຫາຂ້ອຍ", "Gửi email cho tôi"),
    ("ຂໍ້ຄວາມ", "tin nhắn văn bản", "message / text message", "kho khuam", "noun", "cong_nghe", "ສົ່ງຂໍ້ຄວາມສຽງ", "Gửi tin nhắn thoại"),
    ("ໜ້າຈໍ", "màn hình hiển thị", "screen / display", "na jor", "noun", "cong_nghe", "ໜ້າຈໍແຕກ", "Màn hình bị nứt"),
    ("ແປ້ນພິມ", "bàn phím gõ", "keyboard", "paen phim", "noun", "cong_nghe", "ແປ້ນພິມພາສາລາວ", "Bàn phím tiếng Lào"),
    ("ເມົາສ໌", "chuột máy tính", "computer mouse", "mow", "noun", "cong_nghe", "ຄລິກເມົາສ໌", "Nhấp chuột máy tính"),
    ("ເວັບໄຊ", "trang web", "website", "web sai", "noun", "cong_nghe", "ເບິ່ງຂໍ້ມູນໃນເວັບໄຊ", "Xem thông tin trên trang web"),
    ("ແອັບພລິເຄຊັນ", "ứng dụng di động / app", "mobile application", "ap pli kay xan", "noun", "cong_nghe", "ຕິດຕັ້ງແອັບພລິເຄຊັນ", "Cài đặt ứng dụng"),
    ("ຂໍ້ມູນ", "dữ liệu / thông tin", "data / information", "kho moon", "noun", "cong_nghe", "ບັນທຶກຂໍ້ມູນ", "Lưu trữ thông tin"),
    ("ລະບົບ", "hệ thống phần mềm", "system", "la bop", "noun", "cong_nghe", "ລະບົບປະຕິບັດການ", "Hệ điều hành"),

    # --- 8. Y TẾ, BỆNH TẬT & SỨC KHỎE (HEALTHCARE & MEDICINE) ---
    ("ເຈັບຫົວ", "nhức đầu / đau đầu", "headache", "jep hua", "verb", "y_te", "ຂ້ອຍເຈັບຫົວຫຼາຍ", "Tôi đau đầu quá"),
    ("ເຈັບທ້ອງ", "đau bụng", "stomachache", "jep thong", "verb", "y_te", "ກິນສົ້ມແລ້ວເຈັບທ້ອງ", "Ăn chua xong bị đau bụng"),
    ("ເຈັບແຂ້ວ", "đau răng / buốt răng", "toothache", "jep khaew", "verb", "y_te", "ເຈັບແຂ້ວໄປຫາໝໍແຂ້ວ", "Đau răng đi gặp nha sĩ"),
    ("ເຈັບຄໍ", "đau họng / rát cổ họng", "sore throat", "jep kho", "verb", "y_te", "ເຈັບຄໍເວົ້າບໍ່ອອກ", "Đau họng không nói ra tiếng"),
    ("ເປັນໄຂ້", "bị sốt", "have a fever", "pen khai", "verb", "y_te", "ລູກຂ້ອຍເປັນໄຂ້ສູງ", "Con tôi bị sốt cao"),
    ("ເປັນຫວັດ", "bị cảm cúm", "catch a cold / flu", "pen vat", "verb", "y_te", "ລະດູຝົນມັກເປັນຫວັດ", "Mùa mưa hay bị cảm"),
    ("ໄອ", "ho khan / ho hen", "cough", "ai", "verb", "y_te", "ໄອບໍ່ເຊົາຈັກເທື່ອ", "Cứ ho mãi không dứt"),
    ("ຈາມ", "hắt xì hơi", "sneeze", "jam", "verb", "y_te", "ຈາມຍ້ອນແພ້ຝຸ່ນ", "Hắt hơi vì dị ứng bụi"),
    ("ວິນຫົວ", "chóng mặt hoa mắt", "dizzy", "vin hua", "adj", "y_te", "ຮູ້ສຶກວິນຫົວ", "Cảm thấy chóng mặt"),
    ("ຮາກ", "nôn mửa", "vomit", "hak", "verb", "y_te", "ເມົາລົດຈົນຮາກ", "Say xe đến phát nôn"),
    ("ຖອກທ້ອງ", "tiêu chảy / tào tháo đuổi", "diarrhea", "thok thong", "verb", "y_te", "ຖອກທ້ອງຕ້ອງດື່ມນ້ຳເກลືອ", "Bị tiêu chảy cần uống oresol bù nước"),
    ("ບາດແຜ", "vết thương tích", "wound / cut", "bad phae", "noun", "y_te", "ລ້າງບາດແຜໃຫ້ສະອາດ", "Rửa vết thương cho sạch"),
    ("ເລືອດ", "máu đỏ", "blood", "leuat", "noun", "y_te", "ເລືອດອອກດັງ", "Chảy máu cam"),
    ("ກວດເລືອດ", "xét nghiệm máu", "blood test", "kuat leuat", "verb", "y_te", "ໄປກວດເລືອດຢູ່ໂຮງໝໍ", "Đi thử máu ở viện"),
    ("ຄວາມດັນເລືອດ", "huyết áp", "blood pressure", "khuam dan leuat", "noun", "y_te", "ວັດແທກຄວາມດັນເລືອດ", "Đo huyết áp"),
    ("ຢາເມັດ", "thuốc viên", "pill / tablet", "ya med", "noun", "y_te", "ກິນຢາເມັດລະເທື່ອ", "Uống mỗi lần một viên thuốc"),
    ("ຢານ້ຳ", "thuốc nước / siro", "syrup / liquid medicine", "ya nam", "noun", "y_te", "ຢານ້ຳແກ້ໄອ", "Siro ho"),
    ("ຢາສັກ", "thuốc tiêm", "injection medicine", "ya sak", "noun", "y_te", "ສັກຢາປ້ອງກັນພະຍາດ", "Tiêm vắc xin phòng bệnh"),
    ("ໃບສັ່ງຢາ", "đơn thuốc của bác sĩ", "prescription", "bai sang ya", "noun", "y_te", "ຊື້ຢາຕາມໃບສັ່ງຢາ", "Mua thuốc theo đơn"),
    ("ສຸຂະພາບ", "sức khỏe", "health", "soo kha phap", "noun", "y_te", "ຮັກສາສຸຂະພາບແດ່ເດີ້", "Giữ gìn sức khỏe nhé"),
    ("ປະກັນໄພສຸຂະພາບ", "bảo hiểm y tế", "health insurance", "pa kan phai soo kha phap", "noun", "y_te", "ມີບັດປະກັນໄພສຸຂະພາບ", "Có thẻ bảo hiểm y tế"),
    ("ກວດພະຍາດ", "khám chữa bệnh", "medical checkup", "kuat pha yad", "verb", "y_te", "ກວດພະຍາດປະຈຳປີ", "Khám sức khỏe định kỳ"),
    ("ຜ່າຕັດ", "phẫu thuật / mổ", "surgery / operation", "pha tad", "verb", "y_te", "ການຜ່າຕັດສຳເລັດດ້ວຍດີ", "Ca phẫu thuật thành công tốt đẹp"),
    ("ນອນໂຮງໝໍ", "nằm viện điều trị", "hospitalized", "non hong mor", "verb", "y_te", "ລາວນອນໂຮງໝໍສາມມື້", "Anh ấy nằm viện ba ngày"),

    # --- 9. ẨM THỰC, MÓN ĂN & ĐỒ UỐNG LÀO (LAO FOOD & DRINKS) ---
    ("ເຂົ້າໜຽວ", "xôi nếp Lào", "sticky rice", "khao niao", "noun", "am_thuc", "ກິນເຂົ້າໜຽວກັບໄກ່ປິ້ງ", "Ăn xôi nếp với gà nướng"),
    ("ເຂົ້າຈ້າວ", "cơm tẻ", "steamed jasmine rice", "khao jao", "noun", "am_thuc", "ເຂົ້າຈ້າວຫອມມະລິ", "Cơm gạo thơm lài"),
    ("ຕຳໝາກຫຸ່ງ", "nộm đu đủ cay giã (Tam Mak Houng)", "papaya salad", "tam mak hoong", "noun", "am_thuc", "ຕຳໝາກຫຸ່ງໃສ່ປາແດກ", "Nộm đu đủ nêm mắm cá lạp"),
    ("ລາບໄກ່", "lạp thịt gà (gỏi gà băm)", "chicken minced salad (Laap)", "lap kai", "noun", "am_thuc", "ລາບໄກ່ໃສ່ເຂົ້າຂົ້ວ", "Lạp gà rắc thính gạo"),
    ("ລາບຊີ້ນ", "lạp thịt bò/trâu", "beef minced salad", "lap seen", "noun", "am_thuc", "ລາບຊີ້ນງົວແຊບຫຼາຍ", "Lạp thịt bò rất ngon"),
    ("ແກງໜໍ່ໄມ້", "canh măng tươi", "bamboo shoot soup", "kaeng nor mai", "noun", "am_thuc", "ແກງໜໍ່ໄມ້ໃສ່ຢານາງ", "Canh măng nấu lá sương sâm"),
    ("ໄຄແຜ່ນ", "rong sông chiên rắc mè (đặc sản Luang Prabang)", "fried river weed", "khai phaen", "noun", "am_thuc", "ໄຄແຜ່ນຫຼວງພະບາງ", "Rong tấm Luang Prabang"),
    ("ປິ້ງໄກ່", "gà nướng than sen", "grilled chicken", "ping kai", "noun", "am_thuc", "ປິ້ງໄກ່ນາປົ່ງ", "Gà nướng Na Pong trứ danh"),
    ("ປິ້ງປາ", "cá nướng xiên que", "grilled fish", "ping pa", "noun", "am_thuc", "ປິ້ງປານ້ຳຂອງ", "Cá sông Mê Kông nướng"),
    ("ເຂົ້າປຽກເສັ້ນ", "bánh canh bột gạo súp gà", "noodle soup (Khao Piak Sen)", "khao piak sen", "noun", "am_thuc", "ຕື່ນເຊົ້າກິນເຂົ້າປຽກ", "Sáng dậy ăn bát bánh canh nóng"),
    ("ເຝີ", "phở", "Pho noodle soup", "feu", "noun", "am_thuc", "ເຝີຊີ້ນງົວ", "Phở thịt bò"),
    ("ເຂົ້າຈີ່ປາເຕ້", "bánh mì kẹp pate kiểu Lào", "baguette sandwich with pate", "khao jee pate", "noun", "am_thuc", "ເຂົ້າຈີ່ຝຣັ່ງ", "Bánh mì Pháp kẹp giò"),
    ("ຢໍ່ຈືນ", "nem rán / chả giò chiên", "fried spring rolls", "yor jeun", "noun", "am_thuc", "ຢໍ່ຈືນກອບໆ", "Nem rán giòn rụm"),
    ("ຢໍ່ດິບ", "gỏi cuốn tươi", "fresh spring rolls", "yor dib", "noun", "am_thuc", "ຢໍ່ດິບຈິ້ມນ້ຳແຈ່ວ", "Gỏi cuốn chấm nước tương chẻo"),
    ("ແຈ່ວບອງ", "mắm ớt xào da trâu (chẻo boong)", "Luang Prabang chili paste (Jeow Bong)", "jaew bong", "noun", "am_thuc", "ແຈ່ວບອງກິນກັບເຂົ້າໜຽວ", "Chẻo boong ăn cùng xôi nếp"),
    ("ປາແດກ", "mắm cá đồng lên men (gia vị cốt lõi)", "fermented fish sauce (Padaek)", "pa daek", "noun", "am_thuc", "ກິ່ນປາແດກຫອມ", "Mùi mắm cá nồng đượm"),
    ("ນ້ຳຊາ", "nước trà nóng/lạnh", "tea", "nam sa", "noun", "do_uong", "ດື່ມນ້ຳຊາຮ້ອນ", "Uống tách trà nóng"),
    ("ກາເຟດຳ", "cà phê đen", "black coffee", "ka fe dam", "noun", "do_uong", "ກາເຟດຳບໍ່ໃສ່ນ້ຳຕານ", "Cà phê đen không đường"),
    ("ກາເຟນົມ", "cà phê sữa", "milk coffee", "ka fe nom", "noun", "do_uong", "ກາເຟນົມເຢັນ", "Cà phê sữa đá"),
    ("ນ້ຳໝາກພ້າວ", "nước dừa tươi", "fresh coconut water", "nam mak phao", "noun", "do_uong", "ນ້ຳໝາກພ້າວຫວານຊື່ນໃຈ", "Nước dừa ngọt lịm mát lòng"),
    ("ເບຍລາວ", "bia Lào", "Beerlao", "bia lao", "noun", "do_uong", "ເບຍລາວແຊບຕິດອັນດັບໂລກ", "Bia Lào lọt top thế giới"),

    # --- 10. THỜI GIAN, MÙA MÀNG & THỜI TIẾT (WEATHER & NATURE) ---
    ("ລະດູຝົນ", "mùa mưa lũ", "rainy season", "la doo fon", "noun", "thoi_tiet", "ລະດູຝົນເລີ່ມແຕ່ເດືອນຫົກ", "Mùa mưa bắt đầu từ tháng sáu"),
    ("ລະດູແລ້ງ", "mùa khô hạn", "dry season", "la doo laeng", "noun", "thoi_tiet", "ລະດູແລ້ງອາກາດຮ້ອນ", "Mùa khô thời tiết oi ả"),
    ("ລະດູໜາວ", "mùa đông giá lạnh", "winter / cold season", "la doo nao", "noun", "thoi_tiet", "ລະດູໜາວຢູ່ພາກເໜືອ", "Mùa lạnh ở vùng Bắc Lào"),
    ("ລະດູຮ້ອນ", "mùa hè oi bức", "summer / hot season", "la doo hon", "noun", "thoi_tiet", "ລະດູຮ້ອນໄປຫຼິ້ນນ້ຳຕົກ", "Mùa hè đi tắm thác"),
    ("ຝົນຕົກໜັກ", "mưa to gió lớn / mưa rào", "heavy rain", "fon tok nak", "phrase", "thoi_tiet", "ຝົນຕົກໜັກນ້ຳຖ້ວມ", "Mưa to gây ngập nước"),
    ("ຟ້າຮ້ອງ", "sấm sét rền vang", "thunder", "fa hong", "verb", "thoi_tiet", "ຟ້າຮ້ອງສຽງດັງ", "Tiếng sấm vang trời"),
    ("ຟ້າແມບ", "chớp giật sáng lóa", "lightning", "fa maep", "verb", "thoi_tiet", "ຟ້າແມບກ່ອນຝົນຕົກ", "Sấm chớp trước cơn mưa"),
    ("ໝອກຄວັນ", "sương mù / khói mù dày đặc", "fog / smog", "mok khuan", "noun", "thoi_tiet", "ຕອນເຊົ້າມີໝອກ", "Buổi sớm mai có sương phủ"),
    ("ລົມພາຍຸ", "cơn bão lốc", "storm / typhoon", "lom pha yu", "noun", "thoi_tiet", "ລົມພາຍຸພັດແຮງ", "Gió bão quét qua"),
    ("ນ້ຳຖ້ວມ", "ngập úng lũ lụt", "flood", "nam thuam", "noun", "tu_nhien", "ລະວັງນ້ຳຖ້ວມ", "Cảnh giác lũ ngập"),
    ("ແຫ້ງແລ້ງ", "khô hạn nứt nẻ", "drought", "haeng laeng", "adj", "tu_nhien", "ດິນແຫ້ງແລ້ງ", "Đất đai khô cằn"),
    ("ອຸນຫະພູມ", "nhiệt độ", "temperature", "oon ha phoom", "noun", "thoi_tiet", "ອຸນຫະພູມສາມສິບອົງສາ", "Nhiệt độ ba mươi độ C"),
    ("ພະຍາກອນອາກາດ", "dự báo thời tiết", "weather forecast", "pha ya kon ar kat", "noun", "thoi_tiet", "ຟັງພະຍາກອນອາກາດ", "Nghe bản tin dự báo thời tiết"),
    ("ແສງຕາເວັນ", "ánh mặt trời quang đãng", "sunlight", "saeng ta ven", "noun", "tu_nhien", "ແສງຕາເວັນຍາມເຊົ້າ", "Ánh nắng ban mai"),
    ("ສິ່ງແວດລ້ອມ", "môi trường sinh thái", "environment", "sing vaed lom", "noun", "tu_nhien", "ປົກປັກຮັກສາສິ່ງແວດລ້ອມ", "Gìn giữ bảo vệ môi trường"),
    ("ມົນລະພິດ", "ô nhiễm không khí / chất độc", "pollution", "mon la phid", "noun", "tu_nhien", "ຫຼຸດຜ່ອນມົນລະພິດ", "Giảm thiểu ô nhiễm"),

    # --- 11. ĐỘNG VẬT & THỰC VẬT ĐỜI SỐNG (ANIMALS & NATURE) ---
    ("ຊ້າງ", "con voi (quốc thú đất nước Vạn Tượng)", "elephant", "xang", "noun", "dong_vat", "ລາວແມ່ນດິນແດນລ້ານຊ້າງ", "Lào là xứ sở của triệu voi"),
    ("ມ້າ", "con ngựa", "horse", "ma", "noun", "dong_vat", "ມ້າແລ່ນໄວ", "Ngựa phi nhanh"),
    ("ຄວາຍ", "con trâu cày", "water buffalo", "khuai", "noun", "dong_vat", "ຄວາຍໄຖນາ", "Con trâu kéo cày ngoài ruộng"),
    ("ງົວ", "con bò", "cow / cattle", "ngua", "noun", "dong_vat", "ລ້ຽງງົວຢູ່ທົ່ງຫຍ້າ", "Chăn bò trên đồng cỏ"),
    ("ໝາ", "con chó", "dog", "ma", "noun", "dong_vat", "ໝາເຝົ້າເຮືອນ", "Chó giữ nhà"),
    ("ແມວ", "con mèo bắt chuột", "cat", "maew", "noun", "dong_vat", "ແມວຈັບໜູ", "Mèo bắt chuột"),
    ("ໜູ", "con chuột", "mouse / rat", "noo", "noun", "dong_vat", "ໜູແລ່ນໃນຄົວ", "Chuột chạy trong xó bếp"),
    ("ເສືອ", "con hổ / cọp", "tiger", "seua", "noun", "dong_vat", "ເສືອຢູ່ໃນປ່າເລິກ", "Hổ gầm trong rừng sâu"),
    ("ສິງໂຕ", "con sư tử", "lion", "sing toh", "noun", "dong_vat", "ສິງໂຕເຈົ້າປ່າ", "Sư tử chúa sơn lâm"),
    ("ລິງ", "con khỉ", "monkey", "ling", "noun", "dong_vat", "ລິງປີນຕົ້ນໄມ້", "Con khỉ leo trèo cành cây"),
    ("ໝີ", "con gấu", "bear", "mee", "noun", "dong_vat", "ໝີກິນນ້ຳເຜິ້ງ", "Gấu ăn mật ong ngọt"),
    ("ງູ", "con rắn độc", "snake", "ngoo", "noun", "dong_vat", "ລະວັງງູກັດ", "Coi chừng bị rắn cắn"),
    ("ແຂ້", "con cá sấu", "crocodile", "khae", "noun", "dong_vat", "ແຂ້ຢູ່ໃນແມ່ນ້ຳ", "Cá sấu rình dưới lòng sông"),
    ("ເຕົ່າ", "con rùa", "turtle / tortoise", "tao", "noun", "dong_vat", "ເຕົ່າຍ່າງຊ້າ", "Con rùa bò lững thững"),
    ("ກົບ", "con ếch đồng", "frog", "kop", "noun", "dong_vat", "ກົບຮ້ອງຍາມຝົນ", "Ếch kêu râm ran mùa mưa"),
    ("ປາ", "con cá sông", "fish", "pa", "noun", "dong_vat", "ປາລອຍໃນນ້ຳ", "Đàn cá tung tăng dưới nước"),
    ("ກຸ້ງ", "con tôm sú / tôm càng", "shrimp / prawn", "koong", "noun", "dong_vat", "ກຸ້ງເຕັ້ນສົດໆ", "Tôm nhảy tanh tách"),
    ("ປູ", "con cua đồng", "crab", "poo", "noun", "dong_vat", "ຕຳປູມ້າ", "Cua tươi giã nộm"),
    ("ຫອຍ", "con ốc", "snail / shellfish", "hoy", "noun", "dong_vat", "ແກງຫອຍ", "Canh ốc thơm nức"),
    ("ຍຸງ", "con muỗi vằn", "mosquito", "yoong", "noun", "dong_vat", "ຍຸງລາຍກັດເປັນໄຂ້ເລືອດອອກ", "Muỗi đốt sốt xuất huyết"),
    ("ແມງວັນ", "con ruồi", "fly (insect)", "maeng van", "noun", "dong_vat", "ແມງວັນຕອມ", "Ruồi bu bám"),
    ("ເຜິ້ງ", "con ong mật", "bee", "pheung", "noun", "dong_vat", "ເຜິ້ງດູດເກສອນດອກໄມ້", "Ong hút nhụy mật hoa"),
    ("ແມງກະເບື້ອ", "con bướm sặc sỡ", "butterfly", "maeng ka beua", "noun", "dong_vat", "ແມງກະເບື້ອປີກງາມ", "Bươm bướm khoe cánh rực rỡ"),
    ("ມົດ", "con kiến chăm chỉ", "ant", "mod", "noun", "dong_vat", "ມົດໄຕ່ຕາມກຳແພງ", "Kiến bò men bờ tường"),

    # --- 12. CÁC TỔ HỢP TỪ VỰNG HỌC ĐƯỜNG & GIÁO DỤC (ACADEMIC & SCHOOL) ---
    ("ມະຫາວິທະຍາໄລ", "trường đại học", "university", "ma ha vit tha ya lai", "noun", "giao_duc", "ມະຫາວິທະຍາໄລແຫ່ງຊາດລາວ", "Trường Đại học Quốc gia Lào (NUOL)"),
    ("ວິທະຍາໄລ", "trường cao đẳng", "college", "vit tha ya lai", "noun", "giao_duc", "ຮຽນຕໍ່ຢູ່ວິທະຍາໄລ", "Học tiếp lên cao đẳng"),
    ("ໂຮງຮຽນປະຖົມ", "trường tiểu học", "primary school / elementary", "hong hian pa thom", "noun", "giao_duc", "ເດັກນ້ອຍຮຽນປະຖົມ", "Trẻ em theo học tiểu học"),
    ("ໂຮງຮຽນມັດທະຍົມ", "trường trung học cơ sở & phổ thông", "secondary school / high school", "hong hian mat tha yom", "noun", "giao_duc", "ນັກຮຽນມັດທະຍົມ", "Học sinh cấp 2 - cấp 3"),
    ("ຫ້ອງທົດລອງ", "phòng thí nghiệm khoa học", "laboratory", "hong thod long", "noun", "giao_duc", "ທົດລອງເຄມີໃນຫ້ອງທົດລອງ", "Làm thí nghiệm hóa học"),
    ("ຫ້ອງສະໝຸດ", "thư viện đọc sách", "library", "hong sa mood", "noun", "giao_duc", "ອ່ານປຶ້ມຢູ່ຫ້ອງສະໝຸດ", "Đọc sách trên thư viện"),
    ("ຫຼັກສູດ", "chương trình giảng dạy / giáo trình", "curriculum / syllabus", "lak sood", "noun", "giao_duc", "ຫຼັກສູດການຮຽນໃໝ່", "Khung giáo trình học tập mới"),
    ("ວິຊາຮຽນ", "môn học", "subject", "vi sa hian", "noun", "giao_duc", "ວິຊາຮຽນທີ່ຂ້ອຍມັກ", "Môn học mà em yêu thích"),
    ("ຄະນິດສາດ", "môn toán học", "mathematics", "kha nid sad", "noun", "giao_duc", "ແກ້ເລກຄະນິດສາດ", "Giải bài tập toán"),
    ("ຟີຊິກສາດ", "môn vật lý", "physics", "fee sik sad", "noun", "giao_duc", "ຮຽນຟີຊິກສາດ", "Học môn vật lý"),
    ("ເຄມີສາດ", "môn hóa học", "chemistry", "khay mee sad", "noun", "giao_duc", "ທາດເຄມີສາດ", "Hóa chất môn hóa học"),
    ("ຊີວະສາດ", "môn sinh học", "biology", "see va sad", "noun", "giao_duc", "ຄົ້ນຄວ້າຊີວະສາດ", "Tìm hiểu môn sinh học"),
    ("ປະຫວັດສາດ", "môn lịch sử", "history", "pa vat sad", "noun", "giao_duc", "ປະຫວັດສາດຊາດລາວ", "Lịch sử hào hùng nước Lào"),
    ("ພູມສາດ", "môn địa lý", "geography", "phoom sad", "noun", "giao_duc", "ແຜນທີ່ພູມສາດ", "Bản đồ môn địa lý"),
    ("ພາສາສາດ", "ngôn ngữ học", "linguistics", "pha sa sad", "noun", "giao_duc", "ສຶກສາພາສາສາດ", "Nghiên cứu về ngôn ngữ"),
    ("ວັນນະຄະດີ", "môn văn học tác phẩm", "literature", "van na kha dee", "noun", "giao_duc", "ອ່ານບົດວັນນະຄະດີ", "Đọc tác phẩm văn học"),
    ("ການບ້ານ", "bài tập về nhà", "homework", "kan ban", "noun", "giao_duc", "ເຮັດການບ້ານໃຫ້ແລ້ວ", "Làm xong bài tập về nhà"),
    ("ຄະແນນ", "điểm số / điểm bài thi", "score / mark / grade", "kha naen", "noun", "giao_duc", "ໄດ້ຄະແນນເຕັມສິບ", "Đạt điểm mười tuyệt đối"),
    ("ໃບປະກາດສະນີຍະບັດ", "bằng tốt nghiệp / chứng chỉ văn bằng", "diploma / certificate", "bai pa kad sa nee ya bat", "noun", "giao_duc", "ຮັບໃບປະກາດສະນີຍະບັດ", "Nhận bằng cử nhân tốt nghiệp"),
    ("ທຶນການສຶກສາ", "học bổng du học", "scholarship", "theun kan seuk sa", "noun", "giao_duc", "ຍາດໄດ້ທຶນການສຶກສາ", "Giành được suất học bổng"),

    # --- 13. CÁC TỪ LOẠI ĐỘNG TỪ HÀNH ĐỘNG ĐỜI THƯỜNG (COMMON ACTION VERBS) ---
    ("ຕື່ນນອນ", "thức dậy / ngủ dậy", "wake up", "teun non", "verb", "hoat_dong", "ຂ້ອຍຕື່ນນອນແຕ່ເຊົ້າ", "Tôi thức dậy từ sáng sớm"),
    ("ລ້າງໜ້າ", "rửa mặt", "wash face", "lang na", "verb", "hoat_dong", "ລ້າງໜ້າຖູແຂ້ວ", "Rửa mặt đánh răng"),
    ("ຖູແຂ້ວ", "đánh răng chải răng", "brush teeth", "thoo khaew", "verb", "hoat_dong", "ຖູແຂ້ວມື້ລະສອງເທື່ອ", "Đánh răng ngày hai lần"),
    ("ອາບນ້ຳ", "tắm gội", "take a bath / shower", "ab nam", "verb", "hoat_dong", "ອາບນ້ຳໃຫ້ສະອາດ", "Tắm gội sạch sẽ"),
    ("ນຸ່ງເຄື່ອງ", "mặc quần áo", "get dressed", "noong kheuang", "verb", "hoat_dong", "ນຸ່ງເຄື່ອງໄປໂຮງຮຽນ", "Mặc quần áo đến trường"),
    ("ຫວີຜົມ", "chải tóc", "comb hair", "vee phom", "verb", "hoat_dong", "ຫວີຜົມໃຫ້ຮຽບຮ້ອຍ", "Chải tóc cho gọn gàng"),
    ("ແຕ່ງໜ້າ", "trang điểm", "put on makeup", "taeng na", "verb", "hoat_dong", "ແຕ່ງໜ້າໄປງານລ້ຽງ", "Trang điểm đi dạ tiệc"),
    ("ແຕ່ງກິນ", "nấu ăn / chế biến món", "cook food", "taeng kin", "verb", "hoat_dong", "ແມ່ແຕ່ງກິນແຊບ", "Mẹ nấu ăn rất khéo"),
    ("ກວາດເຮືອນ", "quét dọn nhà cửa", "sweep the house", "kuat heuan", "verb", "hoat_dong", "ກວາດເຮືອນທຸກມື້", "Quét dọn nhà mỗi ngày"),
    ("ຖູພື້ນ", "lau sàn nhà", "mop the floor", "thoo pheun", "verb", "hoat_dong", "ຖູພື້ນໃຫ້ກ້ຽງ", "Lau sàn cho bóng láng"),
    ("ຊັກເຄື່ອງ", "giặt giũ quần áo", "wash clothes / do laundry", "sak kheuang", "verb", "hoat_dong", "ຊັກເຄື່ອງດ້ວຍມື", "Giặt đồ bằng tay"),
    ("ຕາກເຄື່ອງ", "phơi quần áo", "hang clothes to dry", "tak kheuang", "verb", "hoat_dong", "ຕາກເຄື່ອງກາງແດດ", "Phơi quần áo ngoài nắng"),
    ("ຮີດເຄື່ອງ", "là ủi quần áo", "iron clothes", "heed kheuang", "verb", "hoat_dong", "ຮີດເຄື່ອງໄປເຮັດວຽກ", "Ủi đồ đi làm"),
    ("ລ້າງຖ້ວຍ", "rửa bát chén", "wash dishes", "lang thuay", "verb", "hoat_dong", "ກິນແລ້ວລ້າງຖ້ວຍ", "Ăn xong rửa chén bát"),
    ("ຫົດນ້ຳຕົ້ນໄມ້", "tưới cây tưới hoa", "water plants", "hod nam ton mai", "verb", "hoat_dong", "ຫົດນ້ຳດອກໄມ້ຕອນແລງ", "Tưới hoa lúc chiều tối"),
    ("ລ້ຽງສັດ", "nuôi gia súc cưng", "raise animals / feed pets", "liang sad", "verb", "hoat_dong", "ລ້ຽງໝາແລະແມວ", "Nuôi chó và mèo"),
    ("ປູກຕົ້ນໄມ້", "trồng cây xanh", "plant trees", "pook ton mai", "verb", "hoat_dong", "ປູກຕົ້ນໄມ້ໃນສວນ", "Trồng cây trong vườn"),
    ("ຂັບລົດ", "lái xe", "drive a car", "khap lod", "verb", "hoat_dong", "ຂັບລົດຢ່າງລະມັດລະວັງ", "Lái xe thật cẩn thận"),
    ("ຂີ່ລົດຖີບ", "đạp xe đạp", "ride a bicycle", "khee lod theeb", "verb", "hoat_dong", "ຂີ່ລົດຖີບອອກກຳລັງກາຍ", "Đạp xe tập thể dục"),
    ("ອອກກຳລັງກາຍ", "tập thể dục thể thao", "exercise / workout", "ork kam lang kai", "verb", "suc_khoe", "ອອກກຳລັງກາຍຕອນເຊົ້າ", "Tập thể dục mỗi sớm mai"),
    ("ລອຍນ້ຳ", "bơi lội", "swim", "loy nam", "verb", "the_thao", "ລອຍນ້ຳໃນສະ", "Bơi trong hồ nước"),
    ("ແລ່ນ", "chạy bộ", "run / jog", "laen", "verb", "the_thao", "ແລ່ນອອກກຳລັງກາຍ", "Chạy bộ rèn sức khỏe"),
    ("ຍ່າງຫຼິ້ນ", "đi dạo phố", "stroll / take a walk", "yang lin", "verb", "giai_tri", "ຍ່າງຫຼິ້ນແຄມຂອງ", "Dạo mát ven bờ sông Mê Kông"),
    ("ຖ່າຍຮູບ", "chụp ảnh kỷ niệm", "take photos", "thai hoop", "verb", "giai_tri", "ຖ່າຍຮູບງາມໆ", "Chụp những bức hình đẹp"),
    ("ຟັງເພງ", "nghe nhạc", "listen to music", "fang pheng", "verb", "giai_tri", "ມັກຟັງເພງລາວເດີມ", "Thích nghe nhạc dân ca Lào"),
    ("ເບິ່ງໜັງ", "xem phim chiếu rạp", "watch a movie", "berng nang", "verb", "giai_tri", "ໄປເບິ່ງໜັງນຳກັນ", "Cùng nhau đi xem phim"),
    ("ຮ້ອງເພງ", "hát ca hát karaoke", "sing a song", "hong pheng", "verb", "giai_tri", "ຮ້ອງເພງມ່ວນຫຼາຍ", "Hát rất hay và truyền cảm"),
    ("ຟ້ອນລຳ", "múa lăm vông (điệu múa truyền thống Lào)", "dance Lamvong", "fon lam", "verb", "van_hoa", "ຟ້ອນລຳວົງສາມັກຄີ", "Múa lăm vông thắm tình đoàn kết"),

    # --- 14. TÍNH TỪ MỞ RỘNG (EXPANDED DESCRIPTIVE ADJECTIVES) ---
    ("ສະຫຼາດ", "thông minh nhanh trí", "smart / intelligent", "sa lat", "adj", "tinh_cach", "ເດັກນ້ອຍສະຫຼາດ", "Đứa trẻ thông minh"),
    ("ດຸໝັ່ນ", "chăm chỉ cần cù", "diligent / hardworking", "doo man", "adj", "tinh_cach", "ຄົນດຸໝັ່ນບໍ່ອຶດກິນ", "Người chăm chỉ không bao giờ thiếu đói"),
    ("ຂີ້ຄ້ານ", "lười biếng biếng nhác", "lazy", "khee khan", "adj", "tinh_cach", "ຢ່າຂີ້ຄ້ານຕື່ນສວາຍ", "Đừng lười biếng ngủ nướng"),
    ("ສຸພາບ", "lịch sự nhã nhặn", "polite / courteous", "soo phap", "adj", "tinh_cach", "ເວົ້າຈາສຸພາບ", "Nói năng lịch sự lễ phép"),
    ("ໃຈດີ", "tốt bụng hiền hậu", "kind / good-hearted", "jai dee", "adj", "tinh_cach", "ແມ່ຕູ້ໃຈດີຫຼາຍ", "Bà cụ rất thơm thảo tốt bụng"),
    ("ໃຈຮ້າຍ", "nổi giận nóng nảy", "angry / short-tempered", "jai hai", "adj", "tinh_cach", "ຢ່າຟ້າວໃຈຮ້າຍ", "Đừng vội tức giận"),
    ("ຂີ້ອາຍ", "nhút nhát e thẹn", "shy", "khee ai", "adj", "tinh_cach", "ລາວເປັນຄົນຂີ້ອາຍ", "Cô ấy là người hay e thẹn"),
    ("ກ້າຫານ", "dũng cảm gan dạ", "brave / courageous", "ka han", "adj", "tinh_cach", "ທະຫານກ້າຫານ", "Người chiến sĩ dũng cảm"),
    ("ອົດທົນ", "kiên nhẫn nhẫn nại", "patient / enduring", "od thon", "adj", "tinh_cach", "ອົດທົນຕໍ່ຄວາມລຳບາກ", "Kiên nhẫn trước khó khăn"),
    ("ອ່ອນໂຍນ", "dịu dàng nết na", "gentle / tender", "on yon", "adj", "tinh_cach", "ສຽງເວົ້າອ່ອນໂຍນ", "Giọng nói dịu dàng"),
    ("ແຂງແຮງ", "khỏe khoắn cường tráng", "strong / healthy", "khaeng haeng", "adj", "suc_khoe", "ຮ່າງກາຍແຂງແຮງ", "Cơ thể khỏe mạnh dẻo dai"),
    ("ອ່ອນເພຍ", "mệt mỏi kiệt sức", "weak / exhausted", "on phia", "adj", "suc_khoe", "ຮູ້ສຶກອ່ອນເພຍ", "Cảm thấy uể oải trong người"),
    ("ຕຸ້ຍ", "béo mập đẫy đà", "fat / chubby", "tui", "adj", "ngoai_hinh", "ຕຸ້ຍຂຶ້ນຫຼາຍ", "Dạo này béo ra nhiều"),
    ("ຈ່ອຍ", "gầy gò ốm yếu", "thin / skinny", "joy", "adj", "ngoai_hinh", "ຈ່ອຍລົງຍ້ອນເຮັດວຽກໜັກ", "Gầy sút vì công việc nặng"),
    ("ສູງໃຫຍ່", "cao to lực lưỡng", "tall and large", "soong yai", "adj", "ngoai_hinh", "ຮູບຮ່າງສູງໃຫຍ່", "Vóc dáng cao to vạm vỡ"),
    ("ງາມຫຼາຍ", "rất xinh đẹp lộng lẫy", "very beautiful", "ngam lai", "adj", "ngoai_hinh", "ສາວລາວງາມຫຼາຍ", "Cô gái Lào rất duyên dáng"),
    ("ຂີ້ຮ້າຍ", "xấu xí xấu xí", "ugly", "khee hai", "adj", "ngoai_hinh", "ໜ້າຕາບໍ່ໄດ້ຂີ້ຮ້າຍ", "Gương mặt đâu có xấu"),
    ("ຮັ່ງມີ", "giàu có phú quý", "rich / wealthy", "hang mee", "adj", "xa_hoi", "ຄອບຄົວຮັ່ງມີ", "Gia đình giàu sang"),
    ("ທຸກຍາກ", "nghèo nàn thiếu thốn", "poor / impoverished", "thook yak", "adj", "xa_hoi", "ຊ່ວຍເຫຼືອຄົນທຸກຍາກ", "Giúp đỡ người nghèo"),
    ("ສະອາດງາມຕາ", "sạch đẹp mát mắt", "clean and neat", "sa at ngam ta", "adj", "doi_song", "ບ້ານເມືອງສະອາດງາມຕາ", "Phố xá sạch đẹp tinh tươm"),
    ("ສົກກະປົກ", "dơ bẩn luộm thuộm", "dirty / messy", "sok ka pok", "adj", "doi_song", "ເສື້ອຜ້າສົກກະປົກ", "Quần áo lấm lem dơ bẩn"),
    ("ມ່ວນຊື່ນ", "vui vẻ rộn ràng", "fun / joyous / merry", "muan xeun", "adj", "cam_xuc", "ງານບຸນມ່ວນຊື່ນຫຼາຍ", "Lễ hội vui tươi rộn rã"),
    ("ເຫງົາ", "buồn bã cô đơn", "lonely", "ngao", "adj", "cam_xuc", "ຢູ່ຄົນດຽວຮູ້ສຶກເຫງົາ", "Ở một mình cảm thấy quạnh quẽ"),
    ("ຕື່ນເຕັ້ນ", "hồi hộp phấn khích", "excited / nervous", "teun ten", "adj", "cam_xuc", "ຮູ້ສຶກຕື່ນເຕັ້ນຫຼາຍ", "Cảm thấy vô cùng hồi hộp"),

    # --- 15. DU LỊCH & ĐỊA DANH TIÊU BIỂU NƯỚC LÀO (TOURISM & GEOGRAPHY) ---
    ("ວຽງຈັນ", "Viêng Chăn (Thủ đô nước CHDCND Lào)", "Vientiane Capital", "viang chan", "noun", "dia_ly", "ນະຄອນຫຼວງວຽງຈັນ", "Thủ đô Viêng Chăn"),
    ("ຫຼວງພະບາງ", "Luang Prabang (Cố đô di sản thế giới)", "Luang Prabang", "luang pha bang", "noun", "dia_ly", "ເມືອງມໍລະດົກໂລກຫຼວງພະບາງ", "Thành phố di sản Luang Prabang"),
    ("ຈຳປາສັກ", "Champasak (Vùng Nam Lào nổi tiếng với Wat Phou)", "Champasak", "cham pa sak", "noun", "dia_ly", "ແຂວງຈຳປາສັກທາງພາກໃຕ້", "Tỉnh Champasak ở miền Nam Lào"),
    ("ວັງວຽງ", "Vang Vieng (Thiên đường khám phá hang động mạo hiểm)", "Vang Vieng", "vang viang", "noun", "dia_ly", "ໄປຫຼິ້ນກິດຈະກຳຢູ່ວັງວຽງ", "Đi trải nghiệm vui chơi ở Vang Viêng"),
    ("ສີພັນດອນ", "Si Phan Don (Vùng 4000 đảo sông Mê Kông)", "Si Phan Don (4000 Islands)", "see phan don", "noun", "dia_ly", "ນ້ຳຕົກຄອນພະເພັງສີພັນດອນ", "Thác Khone Phapheng ở Si Phan Don"),
    ("ທາດຫຼວງ", "Thạt Luổng (Biểu tượng quốc gia Phật giáo Lào)", "Pha That Luang", "that luang", "noun", "van_hoa", "ໄຫວ້ພຣະທາດຫຼວງວຽງຈັນ", "Viếng thăm Đại bảo tháp Thạt Luổng"),
    ("ປະຕູໄຊ", "Tượng đài Khải Hoàn Môn Patuxay", "Patuxay Monument", "pa too xai", "noun", "van_hoa", "ຂຶ້ນຊົມວິວເທິງປະຕູໄຊ", "Lên ngắm toàn cảnh trên đỉnh Khải Hoàn Môn Patuxay"),
    ("ວັດພູ", "Quần thể đền Wat Phou di sản văn hóa", "Wat Phou", "vat phoo", "noun", "van_hoa", "ວັດພູຈຳປາສັກ", "Ngôi đền cổ Wat Phou linh thiêng"),
    ("ວັດຊຽງທອງ", "Chùa Wat Xieng Thong (Đỉnh cao kiến trúc Luang Prabang)", "Wat Xieng Thong", "vat xieng thong", "noun", "van_hoa", "ຫຼັງຄາວັດຊຽງທອງໂຄ້ງງາມ", "Mái cong tuyệt mỹ của chùa Wat Xieng Thong"),
    ("ແມ່ນ້ຳຂອງ", "Dòng sông Mê Kông hùng vĩ", "Mekong River", "mae nam khong", "noun", "dia_ly", "ແມ່ນ້ຳຂອງໄຫຼຜ່ານລາວ", "Dòng Mê Kông chảy dọc nước Lào"),
    ("ຖ້ຳ", "hang động thiên nhiên", "cave", "tham", "noun", "dia_ly", "ທ່ຽວຊົມຖ້ຳຫີນປູນ", "Khám phá hang động đá vôi"),
    ("ນ້ຳຕົກຕາດ", "thác nước thiên nhiên hùng vĩ", "waterfall", "nam tok tad", "noun", "dia_ly", "ນ້ຳຕົກຕາດກວາງຊີ", "Thác Kuang Si nước xanh ngọc bích"),
    ("ປີ້ຍົນ", "vé máy bay", "air ticket / flight ticket", "pee yon", "noun", "du_lich", "ຈອງປີ້ຍົນໄປວຽງຈັນ", "Đặt vé máy bay đi Viêng Chăn"),
    ("ປີ້ລົດໄຟ", "vé tàu hỏa đường sắt Lào - Trung", "train ticket", "pee lod fai", "noun", "du_lich", "ຊື້ປີ້ລົດໄຟລາວ-ຈີນ", "Mua vé tuyến đường sắt cao tốc Lào - Trung"),
    ("ໜັງສືຜ່ານແດນ", "hộ chiếu du lịch quốc tế (Passport)", "passport", "nang seu phan daen", "noun", "du_lich", "ກວດກາໜັງສືຜ່ານແດນ", "Kiểm tra hộ chiếu xuất nhập cảnh"),
    ("ວີຊາ", "thị thực nhập cảnh (Visa)", "visa", "vee sa", "noun", "du_lich", "ຍື່ນຂໍວີຊາ", "Nộp hồ sơ xin cấp visa"),
    ("ດ່ານສາກົນ", "cửa khẩu quốc tế biên giới", "international border checkpoint", "dan sa kon", "noun", "du_lich", "ດ່ານສາກົນຂົວມິດຕະພາບ", "Cửa khẩu quốc tế Cầu Hữu Nghị"),

    # --- 16. CHÍNH TRỊ, LUẬT PHÁP, VĂN HÓA XÃ HỘI (GOVERNMENT & SOCIETY) ---
    ("ລັດຖະບານ", "chính phủ", "government", "lat tha ban", "noun", "chinh_tri", "ນະໂຍບາຍຂອງລັດຖະບານ", "Chính sách của chính phủ"),
    ("ກະຊວງ", "bộ ngành hành chính", "ministry", "ka xuang", "noun", "chinh_tri", "ກະຊວງການຕ່າງປະເທດ", "Bộ Ngoại giao"),
    ("ສະພາແຫ່ງຊາດ", "quốc hội nước CHDCND Lào", "National Assembly", "sa pha haeng xad", "noun", "chinh_tri", "ກອງປະຊຸມສະພາແຫ່ງຊາດ", "Kỳ họp Quốc hội"),
    ("ກົດໝາຍ", "bộ luật pháp lệnh", "law / legislation", "kod mai", "noun", "luat_phap", "ເຄົາລົບກົດໝາຍ", "Tôn trọng và tuân thủ luật pháp"),
    ("ສິດທິ", "quyền lợi hợp pháp", "rights", "sit thi", "noun", "luat_phap", "ສິດທິມະນຸດ", "Quyền con người"),
    ("ພັນທະ", "nghĩa vụ nghĩa vụ công dân", "obligation / duty", "phan tha", "noun", "luat_phap", "ພັນທະປ້ອງກັນຊາດ", "Nghĩa vụ bảo vệ tổ quốc"),
    ("ສັນຕິພາບ", "nền hòa bình vĩnh cửu", "peace", "san ti phap", "noun", "xa_hoi", "ຮັກສາສັນຕິພາບໂລກ", "Bảo vệ nền hòa bình thế giới"),
    ("ມິດຕະພາບ", "tình bạn hữu nghị son sắt", "friendship", "mit ta phap", "noun", "xa_hoi", "ມິດຕະພາບລາວ-ຫວຽດໝັ້ນຄົງ", "Tình hữu nghị Việt - Lào đời đời bền vững"),
    ("ຄວາມສາມັກຄີ", "tinh thần đại đoàn kết", "solidarity / unity", "khuam sa mak khee", "noun", "xa_hoi", "ຄວາມສາມັກຄີເປັນພະລັງ", "Đoàn kết là sức mạnh"),
    ("ວັດທະນະທຳ", "nền văn hóa truyền thống", "culture", "vat tha na tham", "noun", "van_hoa", "ວັດທະນະທຳອັນດີງາມ", "Nét đẹp văn hóa truyền thống"),
    ("ຮີດຄອງປະເພນີ", "thuần phong mỹ tục tập quán lâu đời", "customs / traditions", "heed khong pa phe nee", "noun", "van_hoa", "ຮັກສາຮີດຄອງປະເພນີ", "Bảo tồn thuần phong mỹ tục"),
    ("ບຸນປີໃໝ່ລາວ", "Tết cổ truyền Bunpimay (Tết té nước)", "Lao New Year (Pi Mai)", "boon pee mai lao", "noun", "van_hoa", "ສະເຫຼີມສະຫຼອງບຸນປີໃໝ່ລາວ", "Tưng bừng đón mừng Tết té nước Bunpimay"),
    ("ບຸນຫໍ່ເຂົ້າປະດັບດິນ", "lễ hội phát cơm cho người đã khuất", "Boun Haw Khao Padap Din", "boon hor khao pa dap din", "noun", "van_hoa", "ໄປວັດເຮັດບຸນ", "Lên chùa làm lễ tích đức"),
    ("ບຸນຊ່ວງເຮືອ", "lễ hội đua thuyền rồng truyền thống", "boat racing festival", "boon xuang heua", "noun", "van_hoa", "ບຸນຊ່ວງເຮືອທ່າວັດຈັນ", "Hội đua thuyền rồng bến Wat Chan"),
    ("ບຸນບັ້ງໄຟ", "lễ hội pháo thăng thiên cầu mưa", "rocket festival (Boun Bang Fai)", "boon bang fai", "noun", "van_hoa", "ຈຸດບັ້ງໄຟຂໍຝົນ", "Bắn pháo thăng thiên cầu mưa thuận gió hòa"),
    ("ບຸນອອກພັນສາ", "lễ hội mãn hạ / thả hoa đăng rực rỡ", "Boun Ok Phansa (End of Buddhist Lent)", "boon ork phan sa", "noun", "van_hoa", "ໄຫຼເຮືອໄຟຍາມອອກພັນສາ", "Thả thuyền đăng hoa rực sáng dòng sông"),
    ("ຕັກບາດ", "khất thực cúng dường chư tăng sáng sớm", "alms giving (Tak Bat)", "tak bat", "verb", "van_hoa", "ຕັກບາດຍາມເຊົ້າຢູ່ວັດ", "Dâng cơm cúng dường nhà sư mỗi sớm mai"),

    # --- 17. CÁC TỪ LOẠI LIÊN TỪ, TRỢ TỪ, PHÓ TỪ QUAN TRỌNG (FUNCTION WORDS) ---
    ("ດັ່ງນັ້ນ", "vì thế / cho nên / do đó", "therefore / so", "dang nan", "conj", "ngu_phap", "ດັ່ງນັ້ນຂ້ອຍຈຶ່ງມາ", "Vì vậy cho nên tôi mới đến"),
    ("ເພາະວ່າ", "bởi vì / nguyên nhân do", "because", "phro va", "conj", "ngu_phap", "ເພາະວ່າຝົນຕົກ", "Bởi vì trời đổ mưa"),
    ("ເຖິງແມ່ນວ່າ", "mặc dù / dẫu cho", "although / even though", "theung maen va", "conj", "ngu_phap", "ເຖິງແມ່ນວ່າຍາກກໍຕ້ອງເຮັດ", "Mặc dù rất khó nhưng vẫn phải làm"),
    ("ແຕ່", "nhưng mà / song", "but / however", "tae", "conj", "ngu_phap", "ຢາກໄປແຕ່ບໍ່ມີເວລາ", "Muốn đi lắm nhưng không có thời gian"),
    ("ແລະ", "và / cùng với", "and", "lae", "conj", "ngu_phap", "ຂ້ອຍແລະເຈົ້າ", "Tôi và bạn"),
    ("ຫຼື", "hoặc là / hay là", "or", "leu", "conj", "ngu_phap", "ກາເຟຫຼືຊາ", "Cà phê hay trà"),
    ("ຖ້າຫາກວ່າ", "nếu như / giả sử", "if / in case", "tha hak va", "conj", "ngu_phap", "ຖ້າຫາກວ່າເຈົ້າຕ້ອງການ", "Nếu như bạn có nhu cầu"),
    ("ສະນັ້ນ", "thế thì / thế nên", "hence / so then", "sa nan", "conj", "ngu_phap", "ສະນັ້ນພວກເຮົາເລີ່ມເລີຍ", "Thế nên chúng ta bắt đầu luôn nhé"),
    ("ນອກຈາກນັ້ນ", "ngoài ra / bên cạnh đó", "besides / in addition", "nork jak nan", "conj", "ngu_phap", "ນອກຈາກນັ້ນຍັງມີອີກ", "Ngoài ra vẫn còn nữa"),
    ("ໂດຍສະເພາະ", "đặc biệt là / nhất là", "especially / particularly", "doy sa phor", "adv", "ngu_phap", "ໂດຍສະເພາະແມ່ນອາຫານລາວ", "Đặc biệt nhất là ẩm thực Lào"),
    ("ຢ່າງໜ້ອຍ", "ít nhất là / tối thiểu", "at least", "yang noy", "adv", "ngu_phap", "ຢ່າງໜ້ອຍສອງຄົນ", "Tối thiểu hai người"),
    ("ຢ່າງຫຼາຍ", "nhiều nhất là / tối đa", "at most", "yang lai", "adv", "ngu_phap", "ຢ່າງຫຼາຍກໍສາມມື້", "Tối đa cũng chỉ ba ngày"),
    ("ແທ້ໆ", "thực sự / thật sự luôn", "really / truly", "thae thae", "adv", "ngu_phap", "ແຊບແທ້ໆເດີ້", "Ngon thật sự luôn đấy"),
    ("ແນ່ນອນ", "chắc chắn rồi / dĩ nhiên", "certainly / definitely", "nae non", "adv", "ngu_phap", "ແນ່ນອນຢູ່ແລ້ວ", "Chắc chắn là như vậy rồi"),
    ("ອາດຈະ", "có thể là / có lẽ", "maybe / perhaps / might", "ard ja", "adv", "ngu_phap", "ມື້ອື່ນອາດຈະຝົນຕົກ", "Ngày mai có lẽ trời sẽ mưa"),
    ("ສະເໝີ", "luôn luôn / thường xuyên", "always", "sa mer", "adv", "ngu_phap", "ຄິດຮອດເຈົ້າສະເໝີ", "Luôn luôn nhớ về bạn"),
    ("ບາງເທື່ອ", "đôi khi / thỉnh thoảng", "sometimes", "bang theua", "adv", "ngu_phap", "ບາງເທື່ອກໍໄປກິນເຂົ້າຂ້າງນອກ", "Thỉnh thoảng cũng ra ngoài ăn cơm"),
    ("ບໍ່ເຄີຍ", "chưa từng bao giờ", "never", "bor khoey", "adv", "ngu_phap", "ຂ້ອຍບໍ່ເຄີຍໄປ", "Tôi chưa từng đến đó"),
    ("ເຄີຍ", "đã từng kinh qua", "ever / used to", "khoey", "adv", "ngu_phap", "ເຄີຍມາລາວແລ້ວ", "Đã từng đến nước Lào rồi"),
    ("ກຳລັງ", "đang (thì tiếp diễn)", "currently / -ing", "kam lang", "adv", "ngu_phap", "ກຳລັງຮຽນໜັງສື", "Đang tập trung học bài"),
    ("ແລ້ວ", "rồi / đã xong", "already / finished", "laew", "adv", "ngu_phap", "ກິນເຂົ້າແລ້ວ", "Đã ăn cơm xong rồi"),
    ("ຍັງ", "vẫn / còn chưa", "still / yet", "yang", "adv", "ngu_phap", "ຍັງບໍ່ທັນແລ້ວ", "Vẫn còn chưa xong"),
]

def main():
    print("=" * 65)
    print("🚀 BẮT ĐẦU CHƯƠNG TRÌNH ĐẠI NẠP TỪ VỰNG TIẾNG LÀO THÔNG DỤNG")
    print("=" * 65)

    if not CSV_PATH.exists():
        print(f"[-] Lỗi: Không tìm thấy tệp {CSV_PATH}")
        return

    # 1. Đọc dữ liệu hiện có
    existing_rows = []
    existing_keys = set()
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for r in reader:
            norm_k = normalize_lao(r["lao"].strip())
            existing_keys.add(norm_k)
            existing_rows.append(r)

    print(f"[*] Quy mô từ điển hiện tại: {len(existing_rows)} từ.")

    # 2. Xử lý và chuẩn hóa các từ mới
    added_count = 0
    for item in RAW_VOCAB:
        lao_word, vi_trans, en_trans, roman, pos, lesson, ex_lao, ex_vi = item
        norm_lao = normalize_lao(lao_word.strip())
        
        if norm_lao not in existing_keys and len(norm_lao) > 0:
            existing_keys.add(norm_lao)
            new_entry = {
                "lao": norm_lao,
                "vi": vi_trans.strip(),
                "en": en_trans.strip(),
                "romanization": roman.strip(),
                "pos": pos.strip(),
                "lesson": lesson.strip(),
                "example_lao": normalize_lao(ex_lao.strip()),
                "example_vi": ex_vi.strip()
            }
            existing_rows.append(new_entry)
            added_count += 1

    # 3. Ghi lại vào file CSV đảm bảo Unicode NFC
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_rows)

    print(f"[+] Đã thêm thành công: +{added_count} từ vựng chuẩn thông dụng!")
    print(f"[+] TỔNG SỐ TỪ VỰNG TRONG KHO HIỆN TẠI: {len(existing_rows)} TỪ.")
    print("=" * 65)

if __name__ == "__main__":
    main()
