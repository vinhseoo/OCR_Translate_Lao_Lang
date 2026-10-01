"""
Script Bổ Sung Mega Batch (Đưa từ điển lên > 1,500 mục từ toàn diện).
Bao gồm:
- Văn hóa, Lễ hội & Phong tục cổ truyền Lào (Boun Pi Mai, Baci, Boun Bang Fai, ...)
- Kinh doanh, Ngân hàng, Tài chính & Tín dụng
- Công nghệ thông tin, AI, Khoa học dữ liệu
- Tính từ tính cách, tâm lý sâu sắc
- Động từ giao tiếp, công sở, đàm phán
- Khẩu ngữ lớp học & giao tiếp người học online
Chuẩn hóa NFC nghiêm ngặt.
"""
import os
import sys
import csv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing.normalize import normalize_lao

sys.stdout.reconfigure(encoding='utf-8')


def run_mega_batch():
    dict_file = os.path.join(PROJECT_ROOT, "data", "dictionaries", "lao_vi_en.csv")
    
    entries = {}
    if os.path.exists(dict_file):
        with open(dict_file, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for r in reader:
                k = normalize_lao(r.get("lao", "").strip())
                if k:
                    entries[k] = {
                        "lao": k,
                        "vi": r.get("vi", "").strip(),
                        "en": r.get("en", "").strip(),
                        "romanization": r.get("romanization", "").strip(),
                        "pos": r.get("pos", "").strip(),
                        "lesson": r.get("lesson", "").strip(),
                        "example_lao": normalize_lao(r.get("example_lao", "").strip()),
                        "example_vi": r.get("example_vi", "").strip(),
                    }
    
    mega_items = [
        # --- VĂN HÓA, LỄ HỘI & PHONG TỤC LÀO ---
        ("ບຸນປີໃໝ່ລາວ", "Tết cổ truyền Lào (Pi Mai Lao / Lễ hội Té nước)", "Lao New Year (Pi Mai)", "bun-pee-mai-laao", "noun", "Văn hóa Lào", "ສະຫຼອງບຸນປີໃໝ່ລາວ", "Ăn Tết cổ truyền Lào"),
        ("ບຸນບັ້ງໄຟ", "Lễ hội Pháo Thăng Thiên cầu mưa", "Rocket Festival (Boun Bang Fai)", "bun-bang-fai", "noun", "Văn hóa Lào", "ຈູດບັ້ງໄຟຂໍຝົນ", "Bắn pháo thăng thiên cầu mưa thuận gió hòa"),
        ("ບຸນຊ່ວງເຮືອ", "Lễ hội Đua thuyền truyền thống", "Boat Racing Festival", "bun-xuang-heua", "noun", "Văn hóa Lào", "ແຂ່ງຂັນບຸນຊ່ວງເຮືອ", "Thi đấu đua thuyền"),
        ("ບຸນຫໍ່ເຂົ້າປະດັບດິນ", "Lễ hội Cúng đất trời (Rằm tháng 9)", "Boun Haw Khao Padap Din", "bun-haw-khao-pa-dap-din", "noun", "Văn hóa Lào", "ເຮັດບຸນຫໍ່ເຂົ້າປະດັບດິນ", "Lễ hội cúng dâng đất trời"),
        ("ບຸນເຂົ້າພັນສາ", "Lễ hội An cư Kiết hạ (Bắt đầu mùa chay Phật giáo)", "Boun Khao Phansa", "bun-khao-phan-saa", "noun", "Văn hóa Lào", "ເຂົ້າພັນສາສາມເດືອນ", "Ba tháng an cư kiết hạ"),
        ("ບຸນອອກພັນສາ", "Lễ hội Mãn hạ (Kết thúc mùa chay / Thả hoa đăng)", "Boun Awk Phansa", "bun-awk-phan-saa", "noun", "Văn hóa Lào", "ໄຫຼເຮືອໄຟບຸນອອກພັນສາ", "Thả thuyền hoa đăng rực rỡ"),
        ("ບຸນທາດຫຼວງ", "Đại lễ hội Thạt Luổng (Rằm tháng 12 Phật lịch)", "That Luang Festival", "bun-thaat-luang", "noun", "Văn hóa Lào", "ໄປທ່ຽວບຸນທາດຫຼວງ", "Đi trẩy hội Thạt Luổng"),
        ("ພິທີບາສີ", "Lễ buộc chỉ cổ tay Baci cầu an may mắn", "Baci ceremony / Soukhwan", "phi-thee-baa-see", "noun", "Văn hóa Lào", "ເຮັດພິທີບາສີສູ່ຂວັນ", "Làm lễ buộc chỉ cầu bình an"),
        ("ສາຍສິນ", "Sợi chỉ trắng may mắn", "Sacred white thread", "saai-sin", "noun", "Văn hóa Lào", "ຜູກແຂນດ້ວຍສາຍສິນ", "Buộc cổ tay bằng sợi chỉ trắng"),
        ("ພາຂວັນ", "Mâm lễ Baci cắm hoa Champa", "Phakhuan (Baci tray)", "phaa-khvan", "noun", "Văn hóa Lào", "ຈັດພາຂວັນສວຍງາມ", "Bày biện mâm lễ Baci tuyệt đẹp"),
        ("ບຸນກິນຈຽງ", "Tết người H'Mông Lào", "Hmong New Year", "bun-kin-chiang", "noun", "Văn hóa Lào", "ສະຫຼອງບຸນກິນຈຽງ", "Ăn Tết H'Mông"),
        ("ລຳວົງ", "Điệu múa Lăm Vông truyền thống", "Lamvong (traditional dance)", "lam-vong", "noun", "Nghệ thuật", "ຟ້ອນລຳວົງລາວ", "Múa điệu Lăm Vông uyển chuyển"),
        ("ສິ້ນໄໝ", "Váy tơ tằm dệt tay truyền thống", "Handwoven silk Sinh", "sin-mai", "noun", "Trang phục", "ນຸ່ງສິ້ນໄໝລາວ", "Mặc váy tơ tằm Lào"),

        # --- KINH DOANH, NGÂN HÀNG & TÀI CHÍNH ---
        ("ບັນຊີທະນາຄານ", "Tài khoản ngân hàng", "Bank account", "ban-xee-tha-naa-khaan", "noun", "Tài chính", "ເລກບັນຊີທະນາຄານ", "Số tài khoản ngân hàng"),
        ("ໂອນເງິນດ່ວນ", "Chuyển tiền nhanh 24/7", "Instant money transfer", "oon-ngoen-duan", "verb", "Tài chính", "ໂອນເງິນດ່ວນຜ່ານແອັບ", "Chuyển tiền nhanh qua app"),
        ("ສະກຸນເງິນ", "Đơn vị tiền tệ", "Currency", "sa-kun-ngoen", "noun", "Tài chính", "ສະກຸນເງິນກີບ", "Đơn vị tiền tệ Kíp"),
        ("ອັດຕາແລກປ່ຽນ", "Tỷ giá hối đoái", "Exchange rate", "at-taa-laek-pian", "noun", "Tài chính", "ອັດຕາແລກປ່ຽນເງິນຕາ", "Tỷ giá ngoại tệ"),
        ("ໃບຮຽກເກັບເງິນ", "Hóa đơn thanh toán", "Invoice / Bill", "bai-hiak-kep-ngoen", "noun", "Tài chính", "ສົ່ງໃບຮຽກເກັບເງິນ", "Gửi hóa đơn thu tiền"),
        ("ສິນເຊື່ອ", "Tín dụng", "Credit", "sin-xuea", "noun", "Tài chính", "ສິນເຊື່ອທະນາຄານ", "Tín dụng ngân hàng"),
        ("ເງິນກູ້", "Tiền vay / Khoản vay", "Loan", "ngoen-kuu", "noun", "Tài chính", "ກູ້ຢືມເງິນ", "Vay mượn vốn"),
        ("ເງິນຝາກປະຈຳ", "Tiền gửi tiết kiệm có kỳ hạn", "Fixed deposit", "ngoen-faak-pa-cham", "noun", "Tài chính", "ຝາກເງິນປະຈຳ", "Gửi tiết kiệm có kỳ hạn"),
        ("ຕູ້ເອທີເອັມ", "Cây rút tiền tự động ATM", "ATM machine", "tuu-ee-thee-em", "noun", "Tài chính", "ຖອນເງິນຢູ່ຕູ້ເອທີເອັມ", "Rút tiền ở cây ATM"),
        ("ທຸລະກຳ", "Giao dịch", "Transaction", "thu-la-kam", "noun", "Tài chính", "ທຸລະກຳທາງການເງິນ", "Giao dịch tài chính"),
        ("ຕະຫຼາດຫຼັກຊັບ", "Thị trường chứng khoán", "Stock exchange", "ta-laat-lak-sap", "noun", "Tài chính", "ຕະຫຼາດຫຼັກຊັບລາວ (LSX)", "Sở Giao dịch Chứng khoán Lào"),
        ("ຮຸ້ນ", "Cổ phiếu", "Stock / Shares", "hun", "noun", "Tài chính", "ຊື້ຮຸ້ນ", "Mua cổ phiếu"),
        ("ພາສີ", "Thuế quan / Hải quan", "Tax / Customs", "phaa-see", "noun", "Tài chính", "ເສຍພາສີ", "Đóng thuế"),
        ("ຄ່າທຳນຽມ", "Phí / Lệ phí", "Fee / Charge", "khaa-tham-niam", "noun", "Tài chính", "ຈ່າຍຄ່າທຳນຽມ", "Nộp lệ phí"),

        # --- ĐỘNG TỪ GIAO TIẾP, CÔNG SỞ & ĐÀM PHÁN ---
        ("ປຶກສາ", "Tham khảo / Hỏi ý kiến", "To consult", "peuk-saa", "verb", "Giao tiếp", "ປຶກສາກັບອາຈານ", "Xin ý kiến thầy giáo"),
        ("ປຶກສາຫາລື", "Thảo luận / Bàn bạc", "To discuss / To deliberate", "peuk-saa-haa-lue", "verb", "Giao tiếp", "ປຶກສາຫາລືຮ່ວມກັນ", "Cùng nhau bàn thảo"),
        ("ປະຊຸມ", "Họp / Hội họp", "To meet / Conference", "pa-xum", "verb", "Công sở", "ປະຊຸມວຽກ", "Họp bàn công việc"),
        ("ພົບປະ", "Gặp gỡ / Tiếp xúc", "To meet with", "phop-pa", "verb", "Giao tiếp", "ພົບປະສອງຝ່າຍ", "Gặp gỡ song phương"),
        ("ສຳພາດ", "Phỏng vấn", "To interview", "sam-phaat", "verb", "Công việc", "ສຳພາດງານ", "Phỏng vấn xin việc"),
        ("ແຈ້ງການ", "Thông báo", "To announce / Notification", "chaeng-kaan", "noun", "Công sở", "ອອກແຈ້ງການ", "Ra thông báo"),
        ("ລາຍງານ", "Báo cáo", "To report", "laai-ngaan", "verb", "Công sở", "ລາຍງານຜົນການຮຽນ", "Báo cáo kết quả học tập"),
        ("ສະເໜີ", "Đề xuất / Giới thiệu", "To propose / To suggest", "sa-noe", "verb", "Công sở", "ສະເໜີແຜນການ", "Đề xuất kế hoạch"),
        ("ອະນຸມັດ", "Phê duyệt / Cho phép", "To approve", "a-nu-mat", "verb", "Công sở", "ອະນຸມັດໂຄງການ", "Phê duyệt dự án"),
        ("ປະຕິເສດ", "Từ chối / Bác bỏ", "To refuse / To reject", "pa-ti-seet", "verb", "Giao tiếp", "ປະຕິເສດຄຳຂໍ", "Từ chối yêu cầu"),
        ("ຍອມຮັບ", "Chấp nhận / Thừa nhận", "To accept / To admit", "nyawm-hap", "verb", "Giao tiếp", "ຍອມຮັບຄວາມຈິງ", "Chấp nhận sự thật"),
        ("ຮຽກຮ້ອງ", "Kêu gọi / Đòi hỏi", "To call for / To demand", "hiak-hawng", "verb", "Xã hội", "ຮຽກຮ້ອງສັນຕິພາບ", "Kêu gọi hòa bình"),
        ("ສະໜັບສະໜູນ", "Ủng hộ / Tài trợ", "To support / To sponsor", "sa-nap-sa-nuun", "verb", "Xã hội", "ສະໜັບສະໜູນການສຶກສາ", "Ủng hộ giáo dục"),
        ("ຄັດຄ້ານ", "Phản đối", "To oppose / To object", "khat-khaan", "verb", "Giao tiếp", "ຄັດຄ້ານຂໍ້ສະເໜີ", "Phản đối đề xuất"),
        ("ຕໍ່ສູ້", "Chiến đấu / Phấn đấu", "To fight / To struggle", "taw-suu", "verb", "Hành động", "ຕໍ່ສູ້ເພື່ອຄວາມຍຸຕິທຳ", "Chiến đấu vì công lý"),
        ("ເຈລະຈາ", "Đàm phán / Thương lượng", "To negotiate", "chee-la-chaa", "verb", "Ngoại giao", "ເຈລະຈາສັນຕິພາບ", "Đàm phán hòa bình"),
        ("ລົງນາມ", "Ký kết (văn bản ngoại giao)", "To sign", "long-naam", "verb", "Ngoại giao", "ລົງນາມໃນສັນຍາ", "Ký kết vào hiệp định"),
        ("ເຊັນສັນຍາ", "Ký hợp đồng", "To sign contract", "xen-san-nyaa", "verb", "Kinh tế", "ເຊັນສັນຍາຮ່ວມມື", "Ký hợp đồng hợp tác"),

        # --- TÍNH TỪ TÍNH CÁCH & THẨM MỸ ---
        ("ສຸພາບ", "Lịch sự / Nhã nhặn", "Polite / Courteous", "su-phaap", "adjective", "Tính cách", "ຄົນສຸພາບຮຽບຮ້ອຍ", "Người lịch sự nhã nhặn"),
        ("ອ່ອນຫວານ", "Dịu dàng / Ngọt ngào", "Gentle / Sweet", "awn-vaan", "adjective", "Tính cách", "ສຽງເວົ້າອ່ອນຫວານ", "Giọng nói dịu dàng ngọt ngào"),
        ("ກ້າຫານ", "Dũng cảm / Can đảm", "Brave / Valiant", "kaa-haan", "adjective", "Tính cách", "ນ້ຳໃຈກ້າຫານ", "Tinh thần dũng cảm"),
        ("ຂີ້ອາຍ", "Nhút nhát / Hay xấu hổ", "Shy / Timid", "khee-aai", "adjective", "Tính cách", "ເດັກນ້ອຍຂີ້ອາຍ", "Đứa trẻ nhút nhát"),
        ("ຂີ້ຄ້ານ", "Lười biếng", "Lazy", "khee-khaan", "adjective", "Tính cách", "ຢ່າຂີ້ຄ້ານ", "Đừng lười biếng"),
        ("ດຸໝັ່ນ", "Chăm chỉ / Cần cù", "Diligent / Hardworking", "du-man", "adjective", "Tính cách", "ນັກຮຽນດຸໝັ່ນ", "Học sinh chăm chỉ cần cù"),
        ("ສັດຊື່", "Thật thà / Ngay thẳng", "Honest / Upright", "sat-xue", "adjective", "Tính cách", "ຄົນສັດຊື່ບໍລິສຸດ", "Người thật thà trong sáng"),
        ("ຊື່ສັດ", "Trung thành / Trung thực", "Loyal / Faithful", "xue-sat", "adjective", "Tính cách", "ຊື່ສັດຕໍ່ເພື່ອນມິດ", "Trung thực với bạn bè"),
        ("ກະຕັນຍູ", "Hiếu thảo / Biết ơn", "Grateful / Filial", "ka-tan-nyuu", "adjective", "Đạo đức", "ລູກກະຕັນຍູຕໍ່ພໍ່ແມ່", "Con cái hiếu thảo với cha mẹ"),
        ("ເມດຕາ", "Từ bi / Lòng nhân ái", "Merciful / Compassionate", "meet-taa", "adjective", "Đạo đức", "ມີຈິດໃຈເມດຕາ", "Có tấm lòng từ bi"),
        ("ຈິງໃຈ", "Chân thành / Thật lòng", "Sincere", "ching-chai", "adjective", "Tính cách", "ມິດຕະພາບຈິງໃຈ", "Tình bạn chân thành"),
        ("ສະຫຼາດ", "Thông minh / Lanh lợi", "Smart / Clever", "sa-laat", "adjective", "Trí tuệ", "ເດັກນ້ອຍສະຫຼາດຫຼາຍ", "Đứa bé rất thông minh"),
        ("ລະມັດລະວັງ", "Cẩn thận / Cảnh giác", "Careful / Cautious", "la-mat-la-vang", "adjective", "Tính cách", "ເຮັດວຽກລະມັດລະວັງ", "Làm việc cẩn thận"),
        ("ປະໝາດ", "Bất cẩn / Coi thường", "Careless / Reckless", "pa-maat", "adjective", "Tính cách", "ຢ່າປະໝາດ", "Chớ nên bất cẩn"),
        ("ສັບສົນ", "Rối rắm / Phức tạp", "Confused / Complicated", "sap-son", "adjective", "Trạng thái", "ເລື່ອງສັບສົນ", "Câu chuyện rối rắm"),
        ("ກັງວົນ", "Lo lắng / Băn khoăn", "Worried / Anxious", "kang-von", "adjective", "Tâm lý", "ຢ່າກັງວົນຫຼາຍ", "Đừng lo lắng quá"),
        ("ຕື່ນເຕັ້ນ", "Hồi hộp / Hào hứng", "Excited / Thrilled", "tuen-ten", "adjective", "Tâm lý", "ຮູ້ສຶກຕື່ນເຕັ້ນ", "Cảm thấy hồi hộp"),
        ("ສະຫງົບ", "Yên bình / Thanh bình", "Peaceful / Tranquil", "sa-ngop", "adjective", "Trạng thái", "ບ້ານເມືອງສະຫງົບ", "Đất nước yên bình"),
        ("ວຸ້ນວາຍ", "Hỗn loạn / Ồn ào", "Chaotic / Noisy", "vun-vaai", "adjective", "Trạng thái", "ສັງຄົມບໍ່ວຸ້ນວາຍ", "Xã hội trật tự không hỗn loạn"),
        ("ແອອັດ", "Chật chội / Chen chúc", "Crowded / Congested", "ae-at", "adjective", "Trạng thái", "ຈະລາຈອນແອອັດ", "Giao thông chen chúc tắc đường"),
        ("ກວ້າງຂວາງ", "Rộng rãi / Mênh mông", "Spacious / Vast", "kuaang-khuaang", "adjective", "Trạng thái", "ຫ້ອງກວ້າງຂວາງ", "Căn phòng rất rộng rãi"),
        ("ອຸດົມສົມບູນ", "Trù phú / Màu mỡ", "Fertile / Abundant", "u-dom-som-buun", "adjective", "Trạng thái", "ທຳມະຊາດອຸດົມສົມບູນ", "Thiên nhiên trù phú giàu đẹp"),

        # --- CÔNG NGHỆ THÔNG TIN & AI ---
        ("ການຮຽນຮູ້ຂອງເຄື່ອງ", "Học máy (Machine Learning)", "Machine Learning", "kaan-hian-huu-khawng-khueang", "noun", "AI & CNTT", "ລະບົບການຮຽນຮູ້ຂອງເຄື່ອງ", "Hệ thống học máy"),
        ("ເຄືອຂ່າຍປະສາດທຽມ", "Mạng nơ-ron nhân tạo (Artificial Neural Network)", "Artificial Neural Network", "khuea-khaai-pa-saat-thiam", "noun", "AI & CNTT", "ເຄືອຂ່າຍປະສາດທຽມເລິກ", "Mạng nơ-ron sâu (Deep Neural Network)"),
        ("ວິທະຍາສາດຂໍ້ມູນ", "Khoa học dữ liệu (Data Science)", "Data Science", "vit-tha-yaa-saat-khaw-muun", "noun", "AI & CNTT", "ຮຽນວິທະຍາສາດຂໍ້ມູນ", "Học ngành khoa học dữ liệu"),
        ("ການຂຽນໂຄ້ດ", "Viết mã lập trình (Coding)", "Coding / Programming", "kaan-khian-khoot", "noun", "AI & CNTT", "ຝຶກການຂຽນໂຄ້ດ Python", "Luyện viết code Python"),
        ("ລະບົບປະຕິບັດການ", "Hệ điều hành (OS)", "Operating System (OS)", "la-bop-pa-ti-bat-kaan", "noun", "AI & CNTT", "ລະບົບປະຕິບັດການ Windows", "Hệ điều hành Windows"),
        ("ຮາດແວ", "Phần cứng (Hardware)", "Hardware", "haat-vae", "noun", "AI & CNTT", "ອຸປະກອນຮາດແວ", "Thiết bị phần cứng"),
        ("ຊອບແວ", "Phần mềm (Software)", "Software", "sawp-vae", "noun", "AI & CNTT", "ພັດທະນາຊອບແວ", "Phát triển phần mềm"),
        ("ເຊີບເວີ", "Máy chủ (Server)", "Server", "soe-voe", "noun", "AI & CNTT", "ເຊີບເວີຄລາວ", "Máy chủ đám mây"),
        ("ຄລາວ", "Điện toán đám mây (Cloud computing)", "Cloud computing", "khlaao", "noun", "AI & CNTT", "ເກັບຂໍ້ມູນເທິງຄລາວ", "Lưu trữ dữ liệu trên đám mây"),
        ("ຈໍສະແດງຜົນ", "Màn hình hiển thị", "Display screen / Monitor", "chaw-sa-daeng-phon", "noun", "AI & CNTT", "ຈໍສະແດງຜົນຄົມຊັດ", "Màn hình hiển thị sắc nét"),
        ("ແປ້ນພິມ", "Bàn phím máy tính", "Keyboard", "paen-phim", "noun", "AI & CNTT", "ແປ້ນພິມພາສາລາວ", "Bàn phím gõ tiếng Lào"),
        ("ເມົ້າ", "Chuột máy tính", "Computer mouse", "mao", "noun", "AI & CNTT", "ຄລິກເມົ້າ", "Nhấp chuột máy tính"),

        # --- KHẨU NGỮ LỚP HỌC & GIAO TIẾP HỌC TẬP ---
        ("ອ່ານພ້ອມກັນ", "Cùng đọc to nào (khẩu ngữ lớp học)", "Read together", "aan-phawm-kan", "phrase", "Khẩu ngữ lớp học", "ນັກຮຽນອ່ານພ້ອມກັນເດີ", "Cả lớp cùng đọc to theo cô nào"),
        ("ເປີດໜ້າທີ", "Mở trang số... (khẩu ngữ lớp học)", "Open page...", "poet-naa-thee", "phrase", "Khẩu ngữ lớp học", "ເປີດໜ້າທີສິບ", "Mở trang số mười"),
        ("ຍົກມືຂຶ້ນ", "Giơ tay lên phát biểu", "Raise your hand", "nyok-mue-khuen", "phrase", "Khẩu ngữ lớp học", "ໃຜຮູ້ຍົກມືຂຶ້ນ", "Ai biết thì giơ tay lên"),
        ("ຟັງອາຈານ", "Lắng nghe giáo viên giảng", "Listen to teacher", "fang-aa-chaan", "phrase", "Khẩu ngữ lớp học", "ຟັງອາຈານອະທິບາຍ", "Lắng nghe thầy giải thích"),
        ("ເຮັດວຽກບ້ານ", "Làm bài tập về nhà", "Do homework", "het-viak-baan", "phrase", "Học tập", "ຢ່າລືມເຮັດວຽກບ້ານ", "Đừng quên làm bài tập về nhà"),
        ("ສົ່ງວຽກບ້ານ", "Nộp bài tập về nhà", "Submit homework", "song-viak-baan", "phrase", "Học tập", "ສົ່ງວຽກບ້ານຕົງເວລາ", "Nộp bài tập đúng hạn"),
        ("ເລີກຮຽນ", "Tan học", "School is dismissed", "loek-hian", "phrase", "Học tập", "ຮອດເວລາເລີກຮຽນແລ້ວ", "Đã đến giờ tan trường"),
    ]

    added = 0
    for item in mega_items:
        lao_txt, vi, en, rom, pos, lesson, ex_lao, ex_vi = item
        norm_lao = normalize_lao(lao_txt.strip())
        if not norm_lao:
            continue
            
        if norm_lao not in entries:
            entries[norm_lao] = {
                "lao": norm_lao,
                "vi": vi.strip(),
                "en": en.strip(),
                "romanization": rom.strip(),
                "pos": pos.strip(),
                "lesson": lesson.strip(),
                "example_lao": normalize_lao(ex_lao.strip()),
                "example_vi": ex_vi.strip(),
            }
            added += 1

    sorted_words = sorted(entries.keys())
    
    with open(dict_file, mode="w", encoding="utf-8", newline="") as f:
        fieldnames = ["lao", "vi", "en", "romanization", "pos", "lesson", "example_lao", "example_vi"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for w in sorted_words:
            writer.writerow(entries[w])
            
    print(f"[+] KẾT QUẢ ĐỢT MEGA BATCH:")
    print(f"    - Đã nạp thêm: {added} từ mới.")
    print(f"    - TỔNG DUNG LƯỢNG KHO TỪ ĐIỂN HIỆN TẠI: {len(sorted_words)} MỤC TỪ.")


if __name__ == "__main__":
    run_mega_batch()
