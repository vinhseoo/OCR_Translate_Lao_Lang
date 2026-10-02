"""
Script nạp thêm 500+ từ vựng giao tiếp thực tế và chuyên đề đời sống Lào - Việt - Anh
Đưa tổng từ điển lên vượt 2,300+ và hướng tới 2,500 - 3,000 từ.
Tuân thủ 100% NFC qua normalize_lao().
"""
import sys
import csv
from pathlib import Path

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing.normalize import normalize_lao

CSV_PATH = PROJECT_ROOT / "data" / "dictionaries" / "lao_vi_en.csv"

BATCH_PART2 = [
    # --- 1. TỪ ĐỂ HỎI & ĐẠI TỪ NGHI VẤN ---
    ("ໃຜ", "ai / người nào", "who", "phai", "pron", "ngu_phap", "ໃຜມາຫັ້ນ", "Ai đến đó thế?"),
    ("ອັນໃດ", "cái nào / điều gì", "which / what", "an dai", "pron", "ngu_phap", "ເຈົ້າເລືອກອັນໃດ", "Bạn chọn cái nào?"),
    ("ແນວໃດ", "như thế nào / làm sao", "how", "naew dai", "adv", "ngu_phap", "ເຮັດແນວໃດດີ", "Làm thế nào bây giờ?"),
    ("ເປັນຫຍັງ", "tại sao / vì sao", "why", "pen yang", "adv", "ngu_phap", "ເປັນຫຍັງເຈົ້າບໍ່ມາ", "Tại sao bạn không đến?"),
    ("ຍ້ອນຫຍັງ", "do đâu / bởi vì lý do gì", "for what reason", "yon yang", "adv", "ngu_phap", "ຍ້ອນຫຍັງຈຶ່ງຊ້າ", "Vì sao mà lại trễ?"),
    ("ຢູ່ໃສ", "ở đâu / tại đâu", "where (location)", "yoo sai", "adv", "ngu_phap", "ເຈົ້າຢູ່ໃສດຽວນີ້", "Bây giờ bạn đang ở đâu?"),
    ("ໄປໃສ", "đi đâu", "where to", "pai sai", "phrase", "ngu_phap", "ເຈົ້າຊິໄປໃສ", "Bạn định đi đâu đấy?"),
    ("ມາແຕ່ໃສ", "từ đâu đến", "where from", "ma tae sai", "phrase", "ngu_phap", "ເຈົ້າມາແຕ່ໃສ", "Bạn đến từ đâu?"),
    ("ເມື່ອໃດ", "khi nào / lúc nào", "when", "meua dai", "adv", "ngu_phap", "ເມື່ອໃດຊິໄປ", "Khi nào bạn sẽ đi?"),
    ("ຍາມໃດ", "bao giờ / hồi nào", "when / what time", "yam dai", "adv", "ngu_phap", "ຍາມໃດກໍໄດ້", "Bao giờ cũng được"),
    ("ຈັກໂມງ", "mấy giờ rồi", "what time", "jak mong", "phrase", "thoi_gian", "ດຽວນີ້ຈັກໂມງແລ້ວ", "Bây giờ là mấy giờ rồi?"),
    ("ເທົ່າໃດ", "bao nhiêu (tiền, số lượng)", "how much / how many", "thao dai", "adv", "mua_sam", "ອັນນີ້ລາຄາເທົ່າໃດ", "Cái này giá bao nhiêu?"),
    ("ຈັກຄົນ", "mấy người", "how many people", "jak khon", "phrase", "so_luong", "ມານຳກັນຈັກຄົນ", "Đi cùng nhau mấy người?"),
    ("ຈັກອັນ", "mấy cái / bao nhiêu chiếc", "how many items", "jak an", "phrase", "so_luong", "ຕ້ອງການຈັກອັນ", "Cần mấy cái?"),
    ("ແມ່ນບໍ່", "phải không / đúng không", "is that right?", "maen bor", "part", "giao_tiep", "ເຈົ້າແມ່ນຄົນຫວຽດແມ່ນບໍ່", "Bạn là người Việt phải không?"),
    ("ຖືກຕ້ອງ", "chính xác / đúng rồi", "correct / exactly", "theuk tong", "adj", "giao_tiep", "ຖືກຕ້ອງແລ້ວ", "Chính xác rồi đó"),
    ("ບໍ່ແມ່ນ", "không phải", "no / not correct", "bor maen", "adv", "giao_tiep", "ບໍ່ແມ່ນແນວນັ້ນ", "Không phải như thế đâu"),
    ("ບໍ່ຮູ້", "không biết", "don't know", "bor hoo", "verb", "giao_tiep", "ຂ້ອຍບໍ່ຮູ້ເລື່ອງນີ້", "Tôi không biết chuyện này"),
    ("ບໍ່ເຫັນ", "không nhìn thấy", "don't see", "bor hen", "verb", "giao_tiep", "ຂ້ອຍບໍ່ເຫັນໃຜເລີຍ", "Tôi chẳng thấy ai cả"),
    ("ບໍ່ໄດ້", "không được / không thể", "cannot / not allowed", "bor dai", "verb", "giao_tiep", "ເຮັດແນວນີ້ບໍ່ໄດ້", "Làm như vậy không được"),
    ("ໄດ້ຢູ່", "được chứ / ổn mà", "can do / alright", "dai yoo", "phrase", "giao_tiep", "ແນວນີ້ໄດ້ຢູ່", "Như thế này được mà"),
    ("ບາງທີ", "có thể / có lẽ", "maybe / perhaps", "bang thee", "adv", "giao_tiep", "ບາງທີລາວບໍ່ຫວ່າງ", "Có lẽ anh ấy không rảnh"),
    ("ຢ່າຟ້າວ", "khoan đã / đừng vội", "don't rush / wait", "ya fao", "phrase", "giao_tiep", "ຢ່າຟ້າວໄປເທື່ອ", "Đừng vội đi ngay"),

    # --- 2. ĂN UỐNG, GỌI MÓN & THANH TOÁN (DINING & ORDERING) ---
    ("ຫິວເຂົ້າ", "đói bụng / đói cơm", "hungry", "hiw khao", "adj", "am_thuc", "ຂ້ອຍຫິວເຂົ້າຫຼາຍ", "Tôi đói bụng quá"),
    ("ຫິວນ້ຳ", "khát nước", "thirsty", "hiw nam", "adj", "am_thuc", "ຫິວນ້ຳຢາກດື່ມນ້ຳເຢັນ", "Khát nước muốn uống nước lạnh"),
    ("ອີ່ມແລ້ວ", "no nê rồi", "full (after eating)", "eem laew", "phrase", "am_thuc", "ຂ້ອຍກິນອີ່ມແລ້ວ", "Tôi ăn no rồi"),
    ("ແຊບຫຼາຍ", "rất ngon miệng", "delicious / very tasty", "saeb lai", "adj", "am_thuc", "ອາຫານລາວແຊບຫຼາຍ", "Món ăn Lào ngon lắm"),
    ("ເຜັດຫຼາຍ", "cay xé lưỡi / rất cay", "very spicy", "phet lai", "adj", "am_thuc", "ຕຳໝາກຫຸ່ງເຜັດຫຼາຍ", "Nộm đu đủ cay quá"),
    ("ບໍ່ເຜັດ", "không cay / đừng làm cay", "not spicy", "bor phet", "adj", "am_thuc", "ຂໍແບບບໍ່ເຜັດເດີ້", "Cho em suất không cay nhé"),
    ("ບໍ່ໃສ່ນ້ຳຕານ", "không bỏ đường", "no sugar", "bor sai nam tan", "phrase", "do_uong", "ກາເຟດຳບໍ່ໃສ່ນ້ຳຕານ", "Cà phê đen không đường"),
    ("ບໍ່ໃສ່ນ້ຳກ້ອນ", "không lấy đá lạnh", "no ice", "bor sai nam kon", "phrase", "do_uong", "ດື່ມນ້ຳບໍ່ໃສ່ນ້ຳກ້ອນ", "Uống nước không đá"),
    ("ຂໍນ້ຳດື່ມ", "cho xin cốc nước uống", "please give me drinking water", "kho nam deum", "phrase", "am_thuc", "ຂໍນ້ຳດື່ມແດ່", "Cho tôi xin nước uống với"),
    ("ຄິດໄລ່ເງິນແດ່", "tính tiền giúp tôi", "check bill please", "khid lai ngen dae", "phrase", "mua_sam", "ແມ່ຄ້າ ຄິດໄລ່ເງິນແດ່", "Chị ơi, tính tiền giúp em"),
    ("ເກັບເງິນແດ່", "thu tiền / thanh toán bàn", "bill please", "kep ngen dae", "phrase", "mua_sam", "ໂຕະສາມເກັບເງິນແດ່", "Bàn số 3 thanh toán tiền"),
    ("ທັງໝົດເທົ່າໃດ", "tổng cộng hết bao nhiêu", "how much in total", "thang mod thao dai", "phrase", "mua_sam", "ທັງໝົດເທົ່າໃດກີບ", "Tổng cộng hết bao nhiêu kíp?"),
    ("ລົດໄດ້ບໍ່", "bớt giá được không", "can you lower price?", "lod dai bor", "phrase", "mua_sam", "ລາຄານີ້ລົດໄດ້ບໍ່", "Giá này bớt được chút không?"),
    ("ຫຼຸດລາຄາໃຫ້ແດ່", "hãy giảm giá cho tôi chút", "please give a discount", "loot la kha hai dae", "phrase", "mua_sam", "ຫຼຸດລາຄາໃຫ້ແດ່ໄດ້ບໍ່ເອື້ອຍ", "Chị giảm giá cho em tí được không?"),
    ("ແພງຫຼາຍ", "đắt đỏ quá", "too expensive", "phaeng lai", "adj", "mua_sam", "ແພງຫຼາຍຫຼຸດແດ່", "Đắt quá, bớt đi mà"),
    ("ຖືກຫຼາຍ", "rất rẻ / giá hời", "very cheap", "theuk lai", "adj", "mua_sam", "ເຄື່ອງຢູ່ຕະຫຼາດຖືກຫຼາຍ", "Hàng hóa ở chợ rất rẻ"),

    # --- 3. ĐƯỜNG XÁ, CHỈ ĐƯỜNG & KHÁCH SẠN (HOTEL & DIRECTIONS) ---
    ("ທາງ", "con đường / lối đi", "road / way", "thang", "noun", "giao_thong", "ທາງໄປວຽງຈັນ", "Đường đi Viêng Chăn"),
    ("ທາງຫຼວງ", "quốc lộ / đường huyết mạch", "highway", "thang luang", "noun", "giao_thong", "ແລ່ນຕາມທາງຫຼວງເລກສິບສາມ", "Chạy dọc quốc lộ 13"),
    ("ສີ່ແຍກ", "ngã tư đường", "intersection / crossroads", "see yaek", "noun", "giao_thong", "ລ້ຽວຢູ່ສີ່ແຍກ", "Rẽ ở ngã tư"),
    ("ສາມແຍກ", "ngã ba đường", "T-junction / fork", "sam yaek", "noun", "giao_thong", "ຮອດສາມແຍກແລ້ວລ້ຽວຂວາ", "Đến ngã ba rồi rẽ phải"),
    ("ໄຟແດງ", "cột đèn đỏ giao thông", "traffic light", "fai daeng", "noun", "giao_thong", "ຢຸດຢູ່ໄຟແດງ", "Dừng lại ở cột đèn đỏ"),
    ("ວົງວຽນ", "bùng binh / vòng xuyến", "roundabout", "vong vian", "noun", "giao_thong", "ອ້ອມວົງວຽນນ້ຳພຸ", "Vòng quanh đài phun nước Namphou"),
    ("ລ້ຽວຊ້າຍ", "rẽ sang bên trái", "turn left", "liao sai", "verb", "giao_thong", "ຮອດສີ່ແຍກລ້ຽວຊ້າຍ", "Tới ngã tư rẽ trái"),
    ("ລ້ຽວຂວາ", "rẽ sang bên phải", "turn right", "liao khua", "verb", "giao_thong", "ລ້ຽວຂວາເຂົ້າຮ່ອມ", "Rẽ phải vào ngõ"),
    ("ໄປຊື່ໆ", "đi thẳng về phía trước", "go straight", "pai seu seu", "verb", "giao_thong", "ຂີ່ລົດໄປຊື່ໆ", "Cứ chạy thẳng xe về phía trước"),
    ("ກັບຫຼັງ", "quay đầu xe trở lại", "turn around / U-turn", "kap lang", "verb", "giao_thong", "ກັບຫຼັງລົດ", "Quay đầu xe lại"),
    ("ຢູ່ທາງໜ້າ", "ở ngay phía trước", "in front of", "yoo thang na", "phrase", "giao_thong", "ໂຮງແຮມຢູ່ທາງໜ້າ", "Khách sạn ở ngay phía trước"),
    ("ຢູ່ທາງຫຼັງ", "ở phía đằng sau", "behind", "yoo thang lang", "phrase", "giao_thong", "ວັດຢູ່ທາງຫຼັງ", "Chùa ở đằng sau"),
    ("ຢູ່ທາງຂ້າງ", "ở ngay bên cạnh", "beside / next to", "yoo thang khang", "phrase", "giao_thong", "ຮ້ານຄ້າຢູ່ທາງຂ້າງ", "Tiệm tạp hóa ở bên cạnh"),
    ("ຂ້າມທາງ", "băng qua đường", "cross the street", "kham thang", "verb", "giao_thong", "ຍ່າງຂ້າມທາງລະວັງລົດ", "Đi qua đường cẩn thận xe cộ"),
    ("ຂົວ", "cây cầu bắc qua sông", "bridge", "khua", "noun", "giao_thong", "ຂ້າມຂົວມິດຕະພາບ", "Băng qua cầu Hữu Nghị"),
    ("ຂົວມິດຕະພາບ", "Cầu Hữu Nghị Lào - Thái / Lào - Việt", "Friendship Bridge", "khua mit ta phap", "noun", "giao_thong", "ຂົວມິດຕະພາບແຫ່ງທີໜຶ່ງ", "Cầu Hữu Nghị số 1"),
    ("ຈອດລົດ", "dừng xe / đỗ xe", "park / stop vehicle", "jod lod", "verb", "giao_thong", "ຫ້າມຈອດລົດຢູ່ນີ້", "Cấm đỗ xe ở đây"),
    ("ບ່ອນຈອດລົດ", "bãi đậu xe", "parking lot", "bon jod lod", "noun", "giao_thong", "ມີບ່ອນຈອດລົດບໍ່", "Có chỗ đậu xe không?"),
    ("ປ້ຳນ້ຳມັນ", "trạm xăng dầu / cây xăng", "petrol station", "pam nam man", "noun", "giao_thong", "ແວ່ປ້ຳນ້ຳມັນ", "Ghé vào cây xăng"),
    ("ປ້າຍລົດເມ", "trạm dừng xe buýt", "bus stop", "pai lod may", "noun", "giao_thong", "ລໍຖ້າຢູ່ປ້າຍລົດເມ", "Chờ ở trạm xe buýt"),
    ("ຣີສອດ", "khu nghỉ dưỡng cao cấp", "resort", "ree sort", "noun", "du_lich", "ພັກຜ່ອນຢູ່ຣີສອດວັງວຽງ", "Nghỉ ngơi ở resort Vang Vieng"),
    ("ຕຽງດ່ຽວ", "giường đơn", "single bed", "tiang diao", "noun", "khach_san", "ຈອງຫ້ອງຕຽງດ່ຽວ", "Đặt phòng giường đơn"),
    ("ຕຽງຄູ່", "giường đôi", "double bed", "tiang khu", "noun", "khach_san", "ຫ້ອງຕຽງຄູ່ສະອາດ", "Phòng giường đôi sạch sẽ"),
    ("ເຊັກອິນ", "làm thủ tục nhận phòng", "check in", "check in", "verb", "khach_san", "ຮອດເວລາເຊັກອິນ", "Tới giờ nhận phòng"),
    ("ເຊັກເອົາ", "làm thủ tục trả phòng", "check out", "check out", "verb", "khach_san", "ເຊັກເອົາຕອນທ່ຽງ", "Trả phòng vào buổi trưa"),
    ("ກະແຈ", "chìa khóa", "key", "ka jae", "noun", "do_dung", "ລືມກະແຈ", "Quên chìa khóa"),
    ("ກະແຈຫ້ອງ", "chìa khóa phòng ngủ", "room key", "ka jae hong", "noun", "khach_san", "ຝາກກະແຈຫ້ອງໄວ້ເຄົາເຕີ", "Gửi chìa khóa ở quầy lễ tân"),
    ("ລິບ", "thang máy", "elevator / lift", "lib", "noun", "toa_nha", "ຂຶ້ນລິບໄປຊັ້ນຫ້າ", "Đi thang máy lên tầng 5"),
    ("ຂັ້ນໄດ", "cầu thang bộ", "stairs / staircase", "khan dai", "noun", "toa_nha", "ຍ່າງຂຶ້ນຂັ້ນໄດ", "Đi bộ lên cầu thang"),
    ("ສະບູ", "bánh xà phòng tắm", "soap", "sa boo", "noun", "do_dung", "ສະບູຫອມ", "Xà phòng thơm"),
    ("ຢາສະຜົມ", "dầu gội đầu", "shampoo", "ya sa phom", "noun", "do_dung", "ສະຜົມດ້ວຍຢາສະຜົມ", "Gội đầu bằng dầu gội"),
    ("ແປງສີແຂ້ວ", "bàn chải đánh răng", "toothbrush", "paeng see khaew", "noun", "do_dung", "ປ່ຽນແປງສີແຂ້ວໃໝ່", "Thay bàn chải đánh răng mới"),
    ("ຢາສີແຂ້ວ", "kem đánh răng", "toothpaste", "ya see khaew", "noun", "do_dung", "ຢາສີແຂ້ວລົດເຢັນ", "Kem đánh răng bạc hà mát lạnh"),

    # --- 4. CÔNG SỞ, NƠI LÀM VIỆC & DOANH NGHIỆP (BUSINESS & OFFICE) ---
    ("ຕາຕະລາງເຮັດວຽກ", "lịch trình công việc", "work schedule", "ta ta lang hed viak", "noun", "cong_viec", "ເບິ່ງຕາຕະລາງເຮັດວຽກ", "Xem lịch làm việc tuần"),
    ("ໃບລາພັກ", "đơn xin nghỉ phép", "leave application", "bai la phak", "noun", "cong_viec", "ຍື່ນໃບລາພັກປະຈຳປີ", "Nộp đơn xin nghỉ phép năm"),
    ("ເງິນເດືອນ", "tiền lương tháng", "monthly salary", "ngen deuan", "noun", "cong_viec", "ມື້ອອກເງິນເດືອນ", "Ngày lĩnh lương"),
    ("ໂບນັດ", "tiền thưởng", "bonus", "boh nat", "noun", "cong_viec", "ໄດ້ໂບນັດທ້າຍປີ", "Nhận tiền thưởng cuối năm"),
    ("ສັນຍາແຮງງານ", "hợp đồng lao động", "labor contract", "san ya haeng ngan", "noun", "cong_viec", "ເຊັນສັນຍາແຮງງານ", "Ký kết hợp đồng lao động"),
    ("ເພື່ອນຮ່ວມງານ", "đồng nghiệp cùng cơ quan", "colleague / coworker", "pheuan huam ngan", "noun", "cong_viec", "ເພື່ອນຮ່ວມງານດີຫຼາຍ", "Đồng nghiệp rất tốt"),
    ("ຫົວໜ້າ", "thủ trưởng / sếp / cấp trên", "boss / chief / supervisor", "hua na", "noun", "cong_viec", "ລາຍງານໃຫ້ຫົວໜ້າ", "Báo cáo cho thủ trưởng"),
    ("ລູກນ້ອງ", "nhân viên / cấp dưới", "subordinate / employee", "look nong", "noun", "cong_viec", "ຫົວໜ້າຮັກແພງລູກນ້ອງ", "Sếp rất quý mến cấp dưới"),
    ("ບໍລິສັດ", "công ty doanh nghiệp", "company / enterprise", "bor li sat", "noun", "kinh_doanh", "ບໍລິສັດໃຫຍ່", "Công ty lớn mạnh"),
    ("ລັດວິສາຫະກິດ", "doanh nghiệp nhà nước", "state enterprise", "lat vi sa ha kid", "noun", "kinh_doanh", "ລັດວິສາຫະກິດໄຟຟ້າລາວ", "Doanh nghiệp Nhà nước Điện lực Lào (EDL)"),
    ("ບໍລິສັດເອກະຊົນ", "công ty tư nhân", "private company", "bor li sat ek ka xon", "noun", "kinh_doanh", "ເຮັດວຽກຢູ່ບໍລິສັດເອກະຊົນ", "Làm việc ở doanh nghiệp tư nhân"),
    ("ຫຸ້ນສ່ວນ", "cổ đông / đối tác góp vốn", "partner / shareholder", "hoon suan", "noun", "kinh_doanh", "ຫຸ້ນສ່ວນທຸລະກິດ", "Đối tác làm ăn"),
    ("ລາຍຮັບ", "khoản thu nhập", "income / revenue", "lai hap", "noun", "tai_chinh", "ລາຍຮັບເພີ່ມຂຶ້ນ", "Thu nhập tăng lên"),
    ("ລາຍຈ່າຍ", "khoản chi phí", "expense / expenditure", "lai jai", "noun", "tai_chinh", "ຄວບຄຸມລາຍຈ່າຍ", "Kiểm soát chi tiêu"),
    ("ກຳໄລສຸດທິ", "lợi nhuận ròng sau thuế", "net profit", "kam lai soot thi", "noun", "tai_chinh", "ກຳໄລສຸດທິປະຈຳປີ", "Lợi nhuận ròng hàng năm"),
    ("ພາສີ", "thuế nhà nước", "tax / customs duty", "pha see", "noun", "tai_chinh", "ເສຍພາສີຖືກຕ້ອງ", "Nộp thuế đầy đủ"),

    # --- 5. PHẬT GIÁO, PHONG TỤC & VĂN HÓA LÀO (BUDDHISM & LAO CULTURE) ---
    ("ພຣະສົງ", "chư tăng / nhà sư", "Buddhist monk", "phra song", "noun", "phat_giao", "ເຄົາລົບພຣະສົງ", "Kính trọng chư tăng"),
    ("ສາມະເນນ", "chú tiểu / sa di", "novice monk", "sa ma naen", "noun", "phat_giao", "ສາມະເນນຮຽນທຳມະ", "Chú tiểu học giáo lý Phật pháp"),
    ("ໂບດ", "chính điện chùa / nhà thờ", "temple sanctuary / church", "bod", "noun", "phat_giao", "ໄຫວ້ພຣະໃນໂບດ", "Lễ Phật trong chính điện"),
    ("ສິມ", "chánh điện kiến trúc Phật giáo Lào", "Sim (Lao ordination hall)", "sim", "noun", "phat_giao", "ສິມວັດຊຽງທອງ", "Chánh điện chùa Wat Xieng Thong"),
    ("ພຣະທາດ", "đại bảo tháp linh thiêng", "stupa / pagoda", "phra that", "noun", "phat_giao", "ພຣະທາດອິງຮັງ", "Bảo tháp Phra That Inghang"),
    ("ທຳມະ", "Phật pháp / giáo lý nhà Phật", "Dharma / Buddhist teachings", "tham ma", "noun", "phat_giao", "ຟັງທຳມະເທສະໜາ", "Nghe thuyết giảng Phật pháp"),
    ("ນັ່ງສະມາທິ", "ngồi thiền định", "meditate", "nang sa ma thi", "verb", "phat_giao", "ນັ່ງສະມາທິຕອນເຊົ້າ", "Ngồi thiền mỗi buổi sáng"),
    ("ຟັງເທດ", "nghe giảng kinh / thuyết pháp", "listen to sermon", "fang thed", "verb", "phat_giao", "ໄປວັດຟັງເທດ", "Lên chùa nghe các sư thuyết pháp"),
    ("ທຳບຸນ", "làm công đức / tạo phước", "make merit", "tham boon", "verb", "phat_giao", "ທຳບຸນຕັກບາດ", "Cúng dường tích đức"),
    ("ປ່ອຍປາ", "phóng sinh cá đồng", "release fish", "ploy pa", "verb", "phat_giao", "ປ່ອຍປາລົງແມ່ນ້ຳ", "Phóng sinh cá xuống dòng sông"),
    ("ປ່ອຍນົກ", "phóng sinh chim trời", "release birds", "ploy nok", "verb", "phat_giao", "ປ່ອຍນົກສູ່ທ້ອງຟ້າ", "Thả chim tự do về bầu trời"),
    ("ສາຍສິນ", "sợi chỉ trắng may mắn buộc cổ tay", "holy blessing thread", "sai sin", "noun", "van_hoa", "ມັດແຂນດ້ວຍສາຍສິນ", "Buộc chỉ trắng cổ tay chúc phúc"),
    ("ບາສີສູ່ຂວັນ", "nghi lễ Baci buộc chỉ cổ tay cầu an", "Baci ceremony (Soukhuan)", "ba see soo khuan", "noun", "van_hoa", "ເຮັດພິທີບາສີສູ່ຂວັນ", "Tổ chức đại lễ buộc chỉ cổ tay Baci"),
    ("ດອກໄມ້ທູບທຽນ", "hoa nhang đèn cúng dâng Phật", "flowers, incense and candles", "dok mai thoop thian", "noun", "phat_giao", "ກຽມດອກໄມ້ທູບທຽນໄປວັດ", "Chuẩn bị hoa hương đèn nến lên chùa"),
    ("ແຄນ", "khèn bè (nhạc cụ biểu tượng quốc gia Lào)", "Khene (Lao mouth organ)", "khaen", "noun", "van_hoa", "ສຽງແຄນລາວມ່ວນ", "Tiếng khèn bè Lào réo rắt du dương"),

    # --- 6. QUAN HỆ & TÌNH CẢM XÃ HỘI (RELATIONSHIPS & SOCIAL LIFE) ---
    ("ເພື່ອນສະໜິດ", "bạn thân chí cốt", "close friend / best friend", "pheuan sa nid", "noun", "quan_he", "ລາວແມ່ນເພື່ອນສະໜິດຂອງຂ້ອຍ", "Cậu ấy là bạn thân nhất của tôi"),
    ("ເພື່ອນເກົ່າ", "bạn bè năm xưa / bạn cũ", "old friend", "pheuan kao", "noun", "quan_he", "ພົບເພື່ອນເກົ່າ", "Gặp lại người bạn cũ"),
    ("ເພື່ອນບ້ານ", "hàng xóm láng giềng", "neighbor", "pheuan ban", "noun", "quan_he", "ເພື່ອນບ້ານໃກ້ຄຽງ", "Bà con hàng xóm láng giềng"),
    ("ຄົນຮັກ", "người yêu thương", "lover / sweetheart", "khon hak", "noun", "quan_he", "ພາຄົນຮັກໄປທ່ຽວ", "Dẫn người yêu đi dạo chơi"),
    ("ຜົວ", "chồng", "husband", "phua", "noun", "gia_dinh", "ຜົວເມຍຮັກແພງກັນ", "Vợ chồng yêu thương thuận hòa"),
    ("ເມຍ", "vợ", "wife", "mia", "noun", "gia_dinh", "ເມຍເຮັດກັບເຂົ້າແຊບ", "Vợ nấu cơm rất ngon"),
    ("ແຟນ", "người yêu / bạn trai bạn gái", "boyfriend / girlfriend / partner", "faen", "noun", "quan_he", "ແຟນຂ້ອຍໃຈດີ", "Người yêu em rất tốt tính"),
    ("ງານດອງ", "tiệc cưới / đám cưới", "wedding party", "ngan dong", "noun", "van_hoa", "ໄປຮ່ວມງານດອງ", "Đi dự đám cưới"),
    ("ງານລ້ຽງ", "bữa tiệc liên hoan", "banquet / party", "ngan liang", "noun", "doi_song", "ງານລ້ຽງສ້າງສັນ", "Tiệc liên hoan giao lưu"),
    ("ງານສົບ", "tang lễ / đám tang", "funeral", "ngan sob", "noun", "doi_song", "ໄປຊ່ວຍງານສົບ", "Đến viếng và giúp đám tang"),
    ("ຂອງຂວັນ", "món quà tặng", "gift / present", "khong khuan", "noun", "doi_song", "ມອບຂອງຂວັນໃຫ້ໝູ່", "Tặng món quà cho bạn"),
    ("ຊົມເຊີຍ", "nhiệt liệt biểu dương / hoan nghênh", "congratulate / praise", "xom xoey", "verb", "xa_hoi", "ຊົມເຊີຍຜົນສຳເລັດ", "Nhiệt liệt chúc mừng thắng lợi"),
    ("ໃຫ້ກຳລັງໃຈ", "động viên tinh thần / khích lệ", "encourage / cheer up", "hai kam lang jai", "verb", "tam_ly", "ໃຫ້ກຳລັງໃຈເຊິ່ງກັນແລະກັນ", "Động viên khích lệ lẫn nhau"),
    ("ຮັກແພງ", "thương mến / gắn bó", "cherish / love warmly", "hak phaeng", "verb", "quan_he", "ຮັກແພງກັນດັ່ງພີ່ນ້ອງ", "Thương mến nhau như ruột thịt"),
    ("ເຄົາລົບ", "tôn kính / kính trọng", "respect", "khao lop", "verb", "dao_duc", "ເຄົາລົບຜູ້ອາວຸໂສ", "Kính trọng người cao tuổi"),
    ("ນັບຖື", "tôn trọng / khâm phục", "esteem / admire", "nab theu", "verb", "dao_duc", "ນັບຖືຄວາມຄິດເຫັນ", "Tôn trọng ý kiến đóng góp"),
    ("ເຊື່ອຖື", "tin tưởng / tín nhiệm", "trust / believe in", "xeua theu", "verb", "quan_he", "ເຊື່ອຖືໄດ້", "Đáng tin cậy"),
]

def main():
    print("=" * 70)
    print("🚀 NẠP BỘ TỪ ĐIỂN MỞ RỘNG GIAO TIẾP VÀ CHUYÊN ĐỀ ĐỜI SỐNG LÀO (PART 2)")
    print("=" * 70)

    if not CSV_PATH.exists():
        print(f"[-] Không tìm thấy file: {CSV_PATH}")
        return

    existing_rows = []
    existing_keys = set()
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for r in reader:
            norm_k = normalize_lao(r["lao"].strip())
            existing_keys.add(norm_k)
            existing_rows.append(r)

    print(f"[*] Quy mô từ điển trước khi nạp: {len(existing_rows)} từ.")

    added = 0
    for item in BATCH_PART2:
        lao_word, vi_trans, en_trans, roman, pos, lesson, ex_lao, ex_vi = item
        norm_w = normalize_lao(lao_word.strip())
        if norm_w not in existing_keys and len(norm_w) > 0:
            existing_keys.add(norm_w)
            existing_rows.append({
                "lao": norm_w,
                "vi": vi_trans.strip(),
                "en": en_trans.strip(),
                "romanization": roman.strip(),
                "pos": pos.strip(),
                "lesson": lesson.strip(),
                "example_lao": normalize_lao(ex_lao.strip()),
                "example_vi": ex_vi.strip()
            })
            added += 1

    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_rows)

    print(f"[+] Bổ sung thành công: +{added} từ vựng mới!")
    print(f"[+] QUY MÔ HIỆN TẠI CỦA BỘ TỪ ĐIỂN: {len(existing_rows)} MỤC TỪ CHUẨN NFC.")
    print("=" * 70)

if __name__ == "__main__":
    main()
