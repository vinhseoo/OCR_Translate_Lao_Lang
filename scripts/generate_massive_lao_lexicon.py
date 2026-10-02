"""
Script tạo kho từ vựng tiếng Lào siêu mở rộng (Ultra-Scale Lao Lexicon Builder)
Bổ sung toàn diện các lĩnh vực:
- Cơ thể người, Giải phẫu
- Nội thất gia đình, Nhà cửa, Đồ dùng
- Thời trang, Quần áo, Phụ kiện
- Ẩm thực, Gia vị, Rau củ quả
- Màu sắc, Thiên nhiên, Cây cỏ
- Tiền tệ, Giao dịch, Số đếm và Định lượng
- Hành động hàng ngày, Tâm lý cảm xúc (các từ ghép với ໃຈ, ຂີ້, ຕາ)
- Phương tiện, Địa điểm, Chức danh, Hành chính
Đảm bảo chuẩn hóa Unicode NFC 100%.
"""
import sys
import csv
from pathlib import Path

# Force UTF-8 on Windows Console
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing.normalize import normalize_lao

CSV_PATH = PROJECT_ROOT / "data" / "dictionaries" / "lao_vi_en.csv"

# ==============================================================================
# DANH MỤC TỪ VỰNG SIÊU MỞ RỘNG
# ==============================================================================

VOCAB_DATA = [
    # --- CƠ THỂ & GIẢI PHẪU (ANATOMY) ---
    ("ຫົວ", "đầu", "head", "hua", "noun", "co_the", "ສັ່ນຫົວ", "Lắc đầu"),
    ("ໜ້າ", "khuôn mặt", "face", "na", "noun", "co_the", "ລ້າງໜ້າ", "Rửa mặt"),
    ("ໜ້າຜາກ", "trán", "forehead", "na phak", "noun", "co_the", "ໜ້າຜາກກວ້າງ", "Trán rộng"),
    ("ຕາ", "mắt", "eye", "ta", "noun", "co_the", "ຕາແຈ້ງ", "Mắt sáng"),
    ("ດັງ", "mũi", "nose", "dang", "noun", "co_the", "ດັງໂດ່ງ", "Mũi cao"),
    ("ປາກ", "miệng", "mouth", "pak", "noun", "co_the", "ອ້າປາກ", "Há miệng"),
    ("ສົບ", "môi", "lip", "sob", "noun", "co_the", "ຮິມສົບແດງ", "Làn môi đỏ"),
    ("ແຂ້ວ", "răng", "tooth / teeth", "khaew", "noun", "co_the", "ແຂ້ວຂາວ", "Răng trắng"),
    ("ລີ້ນ", "lưỡi", "tongue", "leen", "noun", "co_the", "ແລບລີ້ນ", "Thè lưỡi"),
    ("ຫູ", "tai", "ear", "hoo", "noun", "co_the", "ຫູໜວກ", "Điếc tai"),
    ("ຄໍ", "cổ / họng", "neck / throat", "kho", "noun", "co_the", "ຄໍຍາວ", "Cổ dài"),
    ("ບ່າ", "vai", "shoulder", "ba", "noun", "co_the", "ບ່າກວ້າງ", "Bờ vai rộng"),
    ("ແຂນ", "cánh tay", "arm", "khaen", "noun", "co_the", "ຍົກແຂນ", "Giơ tay lên"),
    ("ສອກ", "khuỷu tay / cùi chỏ", "elbow", "sok", "noun", "co_the", "ສອກຕຳ", "Cùi chỏ va chạm"),
    ("ມື", "bàn tay", "hand", "meu", "noun", "co_the", "ຈັບມື", "Bắt tay nhau"),
    ("ນິ້ວມື", "ngón tay", "finger", "nio meu", "noun", "co_the", "ນິ້ວມືທັງສິບ", "Mười ngón tay"),
    ("ເລັບມື", "móng tay", "fingernail", "leb meu", "noun", "co_the", "ຕັດເລັບມື", "Cắt móng tay"),
    ("ເອິກ", "ngực", "chest / breast", "oek", "noun", "co_the", "ໜ້າເອິກ", "Lồng ngực"),
    ("ທ້ອງ", "bụng", "belly / stomach", "thong", "noun", "co_the", "ອີ່ມທ້ອງ", "No bụng"),
    ("ສາຍບື", "rốn", "navel", "sai beu", "noun", "co_the", "ສາຍບືເດັກນ້ອຍ", "Dây rốn sơ sinh"),
    ("ຫຼັງ", "lưng", "back", "lang", "noun", "co_the", "ເຈັບຫຼັງ", "Đau lưng"),
    ("ແອວ", "eo / thắt lưng", "waist", "aeo", "noun", "co_the", "ແອວກິ່ວ", "Eo thon"),
    ("ຂາ", "chân / bắp đùi", "leg / thigh", "kha", "noun", "co_the", "ຂາຍາວ", "Chân dài"),
    ("ຫົວເຂົ່າ", "đầu gối", "knee", "hua khao", "noun", "co_the", "ເຈັບຫົວເຂົ່າ", "Đau khớp gối"),
    ("ຕີນ", "bàn chân", "foot / feet", "teen", "noun", "co_the", "ລ້າງຕີນ", "Rửa chân sạch sẽ"),
    ("ນິ້ວຕີນ", "ngón chân", "toe", "nio teen", "noun", "co_the", "ນິ້ວຕີນທັງຫ້າ", "Năm ngón chân"),
    ("ເລັບຕີນ", "móng chân", "toenail", "leb teen", "noun", "co_the", "ຕັດເລັບຕີນ", "Cắt móng chân"),
    ("ຜົມ", "tóc", "hair", "phom", "noun", "co_the", "ຜົມດຳຍາວ", "Tóc đen nhánh dài"),
    ("ໜວດ", "ria mép", "mustache", "nuad", "noun", "co_the", "ແກ້ມໜວດ", "Ria mép quanh cằm"),
    ("ເຄົາ", "râu quai nón", "beard", "khao", "noun", "co_the", "ໂກນເຄົາ", "Cạo râu sạch sẽ"),
    ("ຜິວໜັງ", "làn da", "skin", "phiu nang", "noun", "co_the", "ຜິວໜັງຂາວ", "Làn da trắng trẻo"),
    ("ກະດູກ", "xương cốt", "bone", "ka dook", "noun", "co_the", "ກະດູກຫັກ", "Bị gãy xương"),
    ("ຫົວໃຈ", "trái tim", "heart", "hua jai", "noun", "co_the", "ຫົວໃຈເຕັ້ນໄວ", "Nhịp tim đập nhanh"),
    ("ປອດ", "lá phổi", "lungs", "pod", "noun", "co_the", "ຫາຍໃຈເອົາປອດ", "Hít căng buồng phổi"),
    ("ຕັບ", "lá gan", "liver", "tap", "noun", "co_the", "ຕັບແຂງ", "Bệnh xơ gan"),
    ("ໝາກໄຂ່ຫຼັງ", "thận / quả cật", "kidney", "mak khai lang", "noun", "co_the", "ລ້າງໝາກໄຂ່ຫຼັງ", "Chạy thận nhân tạo"),

    # --- ĐỒ GIA DỤNG & NỘI THẤT (HOME & FURNITURE) ---
    ("ໂຕະ", "cái bàn", "table / desk", "toh", "noun", "do_dung", "ໂຕະເຮັດວຽກ", "Bàn làm việc"),
    ("ຕັ່ງ", "cái ghế ngồi", "chair", "tang", "noun", "do_dung", "ນັ່ງເທິງຕັ່ງ", "Ngồi trên ghế"),
    ("ຕຽງ", "cái giường ngủ", "bed", "tiang", "noun", "do_dung", "ຕຽງນອນໃຫຍ່", "Giường ngủ lớn"),
    ("ຕູ້", "cái tủ", "cabinet / closet", "too", "noun", "do_dung", "ຕູ້ໄມ້ສັກ", "Tủ gỗ tếch"),
    ("ຕູ້ເສື້ອຜ້າ", "tủ quần áo", "wardrobe", "too seua pha", "noun", "do_dung", "ແขວນເສື້ອໃນຕູ້", "Treo đồ trong tủ"),
    ("ຕູ້ເຢັນ", "tủ lạnh", "refrigerator", "too yen", "noun", "do_dung", "ເອົານ້ຳໃສ່ຕູ້ເຢັນ", "Để nước vào tủ lạnh"),
    ("ຕູ້ໜັງສື", "tủ sách", "bookshelf", "too nang seu", "noun", "do_dung", "ຈັດປຶ້ມໃສ່ຕູ້", "Xếp sách vào tủ"),
    ("ໂທລະພາບ", "vô tuyến / tivi", "television", "tho la phap", "noun", "do_dung", "ເບິ່ງໂທລະພາບ", "Xem tivi tin tức"),
    ("ພັດລົມ", "quạt máy", "fan (electric)", "phad lom", "noun", "do_dung", "ເປີດພັດລົມເຢັນໆ", "Bật quạt cho mát"),
    ("ໝໍ້", "cái nồi nấu", "pot", "mor", "noun", "do_dung", "ໝໍ້ຕົ້ມແກງ", "Nồi nấu canh"),
    ("ໝໍ້ຫຸງເຂົ້າ", "nồi cơm điện", "rice cooker", "mor hoong khao", "noun", "do_dung", "ໝໍ້ຫຸງເຂົ້າໄຟຟ້າ", "Nồi cơm điện"),
    ("ໝໍ້ຂາງ", "cái chảo chiên rán", "pan / skillet", "mor khang", "noun", "do_dung", "ຂົ້ວຜັກໃສ່ໝໍ້ຂາງ", "Xào rau trong chảo"),
    ("ຈານ", "cái đĩa thức ăn", "plate / dish", "jan", "noun", "do_dung", "ໃສ່ເຂົ້າໃນຈານ", "Bới cơm ra đĩa"),
    ("ຖ້ວຍ", "cái bát / tô", "bowl", "thuay", "noun", "do_dung", "ຖ້ວຍແກງຮ້ອນ", "Bát canh nóng"),
    ("ບ່ວງ", "cái thìa / muỗng", "spoon", "buang", "noun", "do_dung", "ຕັກກິນດ້ວຍບ່ວງ", "Múc ăn bằng thìa"),
    ("ສ້ອມ", "cái nĩa / xiên", "fork", "som", "noun", "do_dung", "ບ່ວງແລະສ້ອມ", "Thìa và nĩa"),
    ("ຈອກ", "cái ly / cốc", "glass / cup", "jok", "noun", "do_dung", "ຈອກແກ້ວ", "Cốc thủy tinh"),
    ("ຈອກນ້ຳ", "cốc nước", "water cup", "jok nam", "noun", "do_dung", "ຂໍຈອກນ້ຳແດ່", "Cho xin cốc nước"),
    ("ມີດ", "con dao thái", "knife", "meed", "noun", "do_dung", "ມີດຄົມຫຼາຍ", "Con dao rất sắc"),
    ("ຂຽງ", "cái thớt", "chopping board", "khiang", "noun", "do_dung", "ຊອຍຊີ້ນເທິງຂຽງ", "Thái thịt trên thớt"),
    ("ກະຕິກນ້ຳຮ້ອນ", "phích nước nóng", "thermos / kettle", "ka tik nam hon", "noun", "do_dung", "ຕົ້ມນ້ຳຮ້ອນ", "Đun phích nước nóng"),
    ("ຜ້າຫົ່ມ", "cái chăn đắp", "blanket", "pha hom", "noun", "do_dung", "ຫົ່ມຜ້າໜາວ", "Đắp chăn ấm mùa lạnh"),
    ("ໝອນ", "cái gối đầu", "pillow", "mon", "noun", "do_dung", "ໝອນນຸ່ມ", "Gối đầu êm ái"),
    ("ມຸ້ງ", "cái màn / mùng chống muỗi", "mosquito net", "moong", "noun", "do_dung", "ກາງມຸ້ງນອນ", "Mắc màn đi ngủ"),
    ("ຜ້າເຊັດໂຕ", "khăn tắm", "bath towel", "pha sed toh", "noun", "do_dung", "ຜ້າເຊັດໂຕສະອາດ", "Khăn tắm sạch sẽ"),
    ("ຜ້າພົມ", "tấm thảm trải sàn", "carpet / rug", "pha phom", "noun", "do_dung", "ປູຜ້າພົມ", "Trải thảm phòng khách"),
    ("ຜ້າມ່ານ", "rèm cửa sổ / rèm che", "curtain", "pha man", "noun", "do_dung", "ດຶງຜ້າມ່ານ", "Kéo rèm cửa"),
    ("ດອກໄຟ", "bóng đèn thắp sáng", "light bulb", "dok fai", "noun", "do_dung", "ປ່ຽນດອກໄຟໃໝ່", "Thay bóng đèn mới"),
    ("ປະຕູ", "cánh cửa ra vào", "door", "pa too", "noun", "do_dung", "ປິດປະຕູແດ່", "Hãy đóng cửa lại"),
    ("ປ່ອງຢ້ຽມ", "cửa sổ", "window", "pong yiam", "noun", "do_dung", "ເປີດປ່ອງຢ້ຽມຮັບລົມ", "Mở cửa sổ đón gió"),
    ("ຫຼັງຄາ", "mái nhà", "roof", "lang kha", "noun", "do_dung", "ຫຼັງຄາເຮືອນມຸງດິນຂໍ", "Mái nhà lợp ngói đỏ"),
    ("ກຳແພງ", "bức tường bao quanh", "wall", "kam phaeng", "noun", "do_dung", "ທາສີກຳແພງ", "Sơn tường nhà"),
    ("ຮົ້ວ", "hàng rào bảo vệ", "fence", "hua", "noun", "do_dung", "ຮົ້ວໄມ້ໄຜ່", "Hàng rào tre"),

    # --- THỜI TRANG & PHỤ KIỆN (CLOTHING & ACCESSORIES) ---
    ("ເສື້ອ", "cái áo", "shirt / upper garment", "seua", "noun", "thoi_trang", "ເສື້ອສີຂາວ", "Áo sơ mi trắng"),
    ("ເສື້ອເຊີດ", "áo sơ mi công sở", "collared shirt", "seua xerd", "noun", "thoi_trang", "ນຸ່ງເສື້ອເຊີດໄປເຮັດວຽກ", "Mặc sơ mi đi làm"),
    ("ເສື້ອຍືດ", "áo phông / thun", "T-shirt", "seua yeud", "noun", "thoi_trang", "ເສື້ອຍືດໃສ່ສະບາຍ", "Áo thun mặc thoải mái"),
    ("ເສື້ອກັນໜາວ", "áo ấm / áo khoác mùa đông", "winter jacket / sweater", "seua kan nao", "noun", "thoi_trang", "ໃສ່ເສື້ອກັນໜາວ", "Mặc áo khoác ấm"),
    ("ເສື້ອຝົນ", "áo mưa", "raincoat", "seua fon", "noun", "thoi_trang", "ໃສ່ເສື້ອຝົນກັນປຽກ", "Mặc áo mưa chống ướt"),
    ("ສິ້ນ", "váy Sinh truyền thống Lào", "Sinh (Lao traditional skirt)", "sin", "noun", "thoi_trang", "ນຸ່ງສິ້ນໄໝ", "Mặc váy lụa Lào duyên dáng"),
    ("ໂສ້ງ", "quần", "pants / trousers", "song", "noun", "thoi_trang", "ໂສ້ງຢີນ", "Quần jean bò"),
    ("ໂສ້ງຂາຍາວ", "quần dài", "long trousers", "song kha yao", "noun", "thoi_trang", "ນຸ່ງໂສ້ງຂາຍາວ", "Mặc quần dài lịch sự"),
    ("ໂສ້ງຂາສັ້ນ", "quần đùi / soóc", "shorts", "song kha san", "noun", "thoi_trang", "ໂສ້ງຂາສັ້ນຢູ່ບ້ານ", "Quần soóc mặc ở nhà"),
    ("ເກີບ", "đôi giày / dép", "shoes / footwear", "keup", "noun", "thoi_trang", "ໃສ່ເກີບ", "Mang giày vào chân"),
    ("ເກີບຜ້າ", "giày vải / bata", "sneakers / canvas shoes", "keup pha", "noun", "thoi_trang", "ເກີບຜ້າແລ່ນອອກກຳລັງ", "Giày thể thao chạy bộ"),
    ("ເກີບສົ້ນສູງ", "giày cao gót", "high heels", "keup son soong", "noun", "thoi_trang", "ເກີບສົ້ນສູງຜູ້ຍິງ", "Giày cao gót nữ"),
    ("ຖົງຕີນ", "tất vớ", "socks", "thong teen", "noun", "thoi_trang", "ຖົງຕີນສີດຳ", "Đôi tất màu đen"),
    ("ໝວກ", "mũ / nón", "hat / cap", "muak", "noun", "thoi_trang", "ໃສ່ໝວກກັນແດດ", "Đội mũ che nắng"),
    ("ໝວກກັນກະທົບ", "mũ bảo hiểm xe máy", "helmet", "muak kan ka thob", "noun", "thoi_trang", "ໃສ່ໝວກກັນກະທົບກ່ອນຂີ່ລົດ", "Đội mũ bảo hiểm trước khi lái"),
    ("ສາຍແອວ", "thắt lưng / dây nịt", "belt", "sai aeo", "noun", "thoi_trang", "ສາຍແອວໜັງແທ້", "Thắt lưng da thật"),
    ("ໂມງ", "đồng hồ đeo tay", "wrist watch / clock", "mong", "noun", "thoi_trang", "ໂມງຂ້ອມູນ", "Đồng hồ đeo cổ tay"),
    ("ແວ່ນຕາ", "kính đeo mắt cận/viễn", "eyeglasses / glasses", "vaen ta", "noun", "thoi_trang", "ໃສ່ແວ່ນຕາອ່ານໜັງສື", "Đeo kính đọc sách"),
    ("ແວ່ນກັນແດດ", "kính râm mát", "sunglasses", "vaen kan daed", "noun", "thoi_trang", "ແວ່ນກັນແດດຕອນທ່ຽງ", "Đeo kính râm buổi trưa"),
    ("ກະເປົາ", "túi xách / cặp xách", "bag / handbag", "ka pao", "noun", "thoi_trang", "ກະເປົາສະພາຍ", "Túi đeo chéo"),
    ("ກະເປົາເງິນ", "ví bóp đựng tiền", "wallet / purse", "ka pao ngen", "noun", "thoi_trang", "ລືມກະເປົາເງິນຢູ່ບ້ານ", "Quên ví tiền ở nhà"),
    ("ສາຍຄໍ", "dây chuyền đeo cổ", "necklace", "sai kho", "noun", "thoi_trang", "ສາຍຄໍຄຳ", "Dây chuyền vàng 24K"),
    ("ແຫວນ", "nhẫn ngón tay", "ring", "vaen", "noun", "thoi_trang", "ແຫວນໝັ້ນ", "Chiếc nhẫn đính hôn"),
    ("ຕຸ້ມຫູ", "bông tai / hoa tai", "earrings", "toom hoo", "noun", "thoi_trang", "ຕຸ້ມຫູເພັດ", "Bông tai đính kim cương"),
    ("ສາຍແຂນ", "vòng lắc tay", "bracelet", "sai khaen", "noun", "thoi_trang", "ສາຍແຂນເງິນ", "Lắc bạc đeo tay"),

    # --- CÁC TỪ GHÉP VỚI ໃຈ- (TÂM TRẠNG, TÍNH CÁCH CON NGƯỜI) ---
    ("ໃຈດຳ", "nhẫn tâm / độc ác", "cruel / black-hearted", "jai dam", "adj", "tinh_cach", "ຄົນໃຈດຳ", "Kẻ nhẫn tâm"),
    ("ໃຈກວ້າງ", "rộng lượng / hào hiệp", "generous / open-minded", "jai kuang", "adj", "tinh_cach", "ເພິ່ນເປັນຄົນໃຈກວ້າງ", "Bác ấy là người đại lượng"),
    ("ໃຈແຄບ", "hẹp hòi / nhỏ nhen", "narrow-minded", "jai khaep", "adj", "tinh_cach", "ຢ່າເປັນຄົນໃຈແຄບ", "Đừng làm người hẹp hòi"),
    ("ໃຈເຢັນ", "bình tĩnh / điềm đạm", "calm / patient", "jai yen", "adj", "tinh_cach", "ໃຈເຢັນໆເດີ້", "Bình tĩnh nào, chớ vội"),
    ("ໃຈຮ້ອນ", "nóng vội / hấp tấp nóng nảy", "impatient / hot-tempered", "jai hon", "adj", "tinh_cach", "ຄົນໃຈຮ້ອນເຮັດວຽກບໍ່ດີ", "Người nóng vội làm việc hỏng việc"),
    ("ໃຈແຂງ", "cứng rắn / sắt đá", "hard-hearted / determined", "jai khaeng", "adj", "tinh_cach", "ລາວໃຈແຂງຫຼາຍ", "Anh ta rất sắt đá"),
    ("ໃຈອ່ອນ", "mềm lòng / dễ mủi lòng", "soft-hearted", "jai on", "adj", "tinh_cach", "ເຫັນແລ້ວໃຈອ່ອນ", "Thấy cảnh đó liền mềm lòng"),
    ("ໃຈງ່າຍ", "dễ dãi / cả tin", "easy-going / gullible", "jai ngai", "adj", "tinh_cach", "ຢ່າໃຈງ່າຍເຊື່ອຄົນອື່ນ", "Đừng vội tin người cả tin"),
    ("ໃຈເດັດ", "dứt khoát quyết đoán", "resolute / daring", "jai ded", "adj", "tinh_cach", "ການຕັດສິນໃຈເດັດດ່ຽວ", "Quyết định rất dứt khoát"),
    ("ໃຈນ້ອຍ", "dễ tự ái dỗi hờn", "touchy / easily offended", "jai noy", "adj", "tinh_cach", "ມັກໃຈນ້ອຍ", "Tính hay dỗi tự ái"),
    ("ດີໃຈ", "vui mừng hoan hỉ", "glad / happy", "dee jai", "adj", "cam_xuc", "ດີໃຈທີ່ໄດ້ພົບເຈົ້າ", "Rất vui mừng được gặp bạn"),
    ("ເສຍໃຈ", "buồn bã / tiếc nuối", "sad / sorrowful", "sia jai", "adj", "cam_xuc", "ຂ້ອຍເສຍໃຈນຳເດີ້", "Tôi xin chia buồn cùng bạn"),
    ("ສົນໃຈ", "hứng thú quan tâm", "interested", "son jai", "verb", "cam_xuc", "ສົນໃຈຮຽນພາສາລາວ", "Hứng thú học tiếng Lào"),
    ("ຕັ້ງໃຈ", "chuyên tâm quyết chí", "attentive / determined", "tang jai", "verb", "cam_xuc", "ຕັ້ງໃຈຮຽນໜັງສື", "Chăm chú học bài"),
    ("ໝັ້ນໃຈ", "tự tin chắc chắn", "confident", "man jai", "adj", "cam_xuc", "ຂ້ອຍໝັ້ນໃຈໃນຕົວເອງ", "Tôi tự tin vào bản thân"),
    ("ໜັກໃຈ", "nặng lòng trĩu âu lo", "worried / troubled", "nak jai", "adj", "cam_xuc", "ຮູ້ສຶກໜັກໃຈກັບວຽກນີ້", "Thấy nặng lòng với công việc"),
    ("ສະບາຍໃຈ", "thư thái thanh thản", "relieved / at ease", "sa bai jai", "adj", "cam_xuc", "ເຮັດແລ້ວສະບາຍໃຈ", "Làm xong cảm thấy thanh thản"),
    ("ນ້ຳໃຈ", "tấm lòng nghĩa cử", "spirit / hospitality / goodwill", "nam jai", "noun", "xa_hoi", "ນ້ຳໃຈອັນປະເສີດ", "Tấm lòng cao đẹp"),

    # --- CÁC TỪ GHÉP VỚI ขี้- / ຂີ້- (TẬP TÍNH, THÓI QUEN) ---
    ("ຂີ້ຕົວະ", "nói dối / kẻ lừa dối", "liar / deceitful", "khee tua", "verb", "tinh_cach", "ຢ່າຂີ້ຕົວະຂ້ອຍ", "Đừng có nói dối tôi"),
    ("ຂີ້ໂມ້", "khoe khoang khoác lác", "boastful / bragging", "khee moh", "adj", "tinh_cach", "ເວົ້າຂີ້ໂມ້ຫຼາຍ", "Nói năng khoác lác quá"),
    ("ຂີ້ລືມ", "đãng trí hay quên", "forgetful", "khee leum", "adj", "tinh_cach", "ຄົນເຖົ້າມັກຂີ້ລືມ", "Người già hay bị đãng trí"),
    ("ຂີ້ໜຽວ", "keo kiệt bủn xỉn", "stingy / miserly", "khee niao", "adj", "tinh_cach", "ຂີ້ໜຽວບໍ່ຍອມຈ່າຍ", "Bủn xỉn không chịu chi"),
    ("ຂີ້ຢ້ານ", "nhát gan sợ sệt", "coward / timid", "khee yan", "adj", "tinh_cach", "ຂີ້ຢ້ານຄວາມມືດ", "Nhát gan sợ bóng tối"),
    ("ຂີ້ໂລບ", "tham lam vô đáy", "greedy", "khee lob", "adj", "tinh_cach", "ຄົນຂີ້ໂລບ", "Kẻ tham lam"),
    ("ຂີ້ໂກງ", "gian lận lừa đảo", "cheater / dishonest", "khee kong", "adj", "tinh_cach", "ຫຼິ້ນເກມຂີ້ໂກງ", "Chơi game gian lận"),
    ("ຂີ້ຄຽດ", "hay giận dỗi hờn mát", "sulky / grumpy", "khee khiad", "adj", "tinh_cach", "ຂີ້ຄຽດງ່າຍ", "Tính rất hay giận dỗi"),
    ("ຂີ້ເຫຼົ້າ", "sâu rượu nát rượu", "alcoholic / drunkard", "khee lao", "noun", "doi_song", "ກາຍເປັນຄົນຂີ້ເຫຼົ້າ", "Trở thành kẻ sâu rượu"),

    # --- RAU CỦ & GIA VỊ (VEGETABLES & SPICES) ---
    ("ຜັກກາດ", "rau cải bắp / cải xanh", "mustard greens / cabbage", "phak kad", "noun", "thuc_pham", "ຜັກກາດສົດ", "Rau cải xanh tươi"),
    ("ຜັກບົ່ວ", "củ hành lá", "scallion / green onion", "phak bua", "noun", "thuc_pham", "ຊອຍຜັກບົ່ວໃສ່ເຝີ", "Thái hành hoa vào phở"),
    ("ຜັກທຽມ", "củ tỏi", "garlic", "phak thiam", "noun", "thuc_pham", "ຫົວຜັກທຽມ", "Củ tỏi thơm"),
    ("ຜັກຫອມ", "rau thơm gia vị", "herbs", "phak hom", "noun", "thuc_pham", "ກິນຜັກຫອມກັບລາບ", "Ăn rau thơm với món lạp"),
    ("ຜັກບົ້ງ", "rau muống", "water spinach / morning glory", "phak bong", "noun", "thuc_pham", "ຜັກບົ້ງໄຟແດງ", "Rau muống xào tỏi"),
    ("ຜັກສະລັດ", "rau xà lách giòn", "lettuce", "phak sa lad", "noun", "thuc_pham", "ສະລັດຜັກສົດ", "Đĩa xà lách tươi giòn"),
    ("ຜັກຊີ", "rau mùi / ngò rí", "coriander / cilantro", "phak see", "noun", "thuc_pham", "ໂຮຍຜັກຊີໜ້າແກງ", "Rắc rau mùi lên mặt bát canh"),
    ("ຜັກແພວ", "rau răm thơm cay", "Vietnamese coriander", "phak phaew", "noun", "thuc_pham", "ກິນໄຂ່ຮ້າງກັບຜັກແພວ", "Ăn trứng vịt lộn kèm rau răm"),
    ("ຜັກອີຕູ່", "rau húng quế thơm Lào", "lemon basil", "phak ee too", "noun", "thuc_pham", "ແກງໜໍ່ໄມ້ໃສ່ຜັກອີຕູ່", "Canh măng nêm lá húng Lào"),
    ("ຂີງ", "củ gừng tươi", "ginger", "khing", "noun", "thuc_pham", "ນ້ຳຂີງຮ້ອນ", "Nước trà gừng nóng"),
    ("ຂ່າ", "củ riềng thơm", "galangal", "kha", "noun", "thuc_pham", "ຕົ້ມຍຳໃສ່ຂ່າ", "Canh tomyum nêm riềng"),
    ("ຫົວສີໄຄ", "cây sả thơm", "lemongrass", "hua see khai", "noun", "thuc_pham", "ຊອຍຫົວສີໄຄ", "Thái lát sả thơm"),
    ("ໃບຂີ້ຫູດ", "lá chanh kaffir / lá chúc", "kaffir lime leaves", "bai khee hood", "noun", "thuc_pham", "ກິ່ນຫອມໃບຂີ້ຫູດ", "Mùi ngát lá chanh chúc"),
    ("ເກลືອ", "hạt muối mặn", "salt", "kleua", "noun", "thuc_pham", "ເກลືອແກງ", "Muối hạt nêm canh"),
    ("ນ້ຳຕານ", "đường cát ngọt", "sugar", "nam tan", "noun", "thuc_pham", "ນ້ຳຕານຊາຍຂາວ", "Đường cát trắng tinh"),
    ("ນ້ຳປາ", "nước mắm cốt", "fish sauce", "nam pa", "noun", "thuc_pham", "ນ້ຳປາແຊບ", "Nước mắm đậm đà"),
    ("ແປ້ງນົວ", "bột ngọt / mì chính", "MSG (monosodium glutamate)", "paeng nua", "noun", "thuc_pham", "ໃສ່ແປ້ງນົວໜ້ອຍໜຶ່ງ", "Nêm chút bột ngọt"),
    ("ພິກໄທ", "hạt tiêu cay nồng", "black pepper", "phik thai", "noun", "thuc_pham", "ພິກໄທດຳບົດ", "Hạt tiêu đen xay"),
    ("ນ້ຳມັນພືດ", "dầu thực vật ăn", "vegetable cooking oil", "nam man pheud", "noun", "thuc_pham", "ນ້ຳມັນພືດຈືນປາ", "Dầu thực vật chiên cá"),

    # --- HOA QUẢ TRÁI CÂY (FRUITS) ---
    ("ໝາກສີດາ", "quả ổi giòn", "guava", "mak see da", "noun", "thuc_pham", "ໝາກສີດາກອບ", "Ổi giòn ngọt"),
    ("ໝາກທຸລຽນ", "trái sầu riêng vua hoa quả", "durian", "mak thu lian", "noun", "thuc_pham", "ໝາກທຸລຽນກິ່ນແຮງ", "Mùi thơm nức của sầu riêng"),
    ("ໝາກມັງຄຸດ", "trái măng cụt hoàng hậu", "mangosteen", "mak mang khoot", "noun", "thuc_pham", "ໝາກມັງຄຸດລົດຫວານ", "Măng cụt vị ngọt thanh"),
    ("ໝາກລຳໄຍ", "chùm nhãn lồng", "longan", "mak lam yai", "noun", "thuc_pham", "ໝາກລຳໄຍຫວານສ່ຳນ້ຳເຜິ້ງ", "Nhãn ngọt lịm như mật"),
    ("ໝາກຂາມ", "quả me chua", "tamarind", "mak kham", "noun", "thuc_pham", "ໝາກຂາມຫວານ", "Me Thái ngọt"),
    ("ໝາກຍົມ", "chùm ruột chua giòn", "star gooseberry", "mak yom", "noun", "thuc_pham", "ຕຳໝາກຍົມແຊບ", "Chùm ruột giã chua cay"),
    ("ໝາກຂຽບ", "quả na / mãng cầu ta", "custard apple / sugar apple", "mak khiab", "noun", "thuc_pham", "ໝາກຂຽບສຸກຫອມ", "Na chín ngát hương"),
    ("ໝາກສັບປະລົດ", "trái thơm / khóm / dứa", "pineapple", "mak sap pa lod", "noun", "thuc_pham", "ໝາກສັບປະລົດຫວານສົ້ມ", "Dứa chua chua ngọt ngọt"),
    ("ໝາກແຕງໂມ", "quả dưa hấu đỏ", "watermelon", "mak taeng moh", "noun", "thuc_pham", "ກິນແຕງໂມແກ້ຮ້ອນ", "Ăn dưa hấu giải nhiệt"),
    ("ໝາກແຕງກວາ", "quả dưa leo / dưa chuột", "cucumber", "mak taeng kua", "noun", "thuc_pham", "ຊອຍໝາກແຕງກວາ", "Thái lát dưa leo"),

    # --- SẮC MÀU (COLORS) ---
    ("ສີຂາວ", "màu trắng tinh khiết", "white color", "see khao", "noun", "mau_sac", "ລົດສີຂາວ", "Chiếc xe màu trắng"),
    ("ສີດຳ", "màu đen tuyền", "black color", "see dam", "noun", "mau_sac", "ເກີບສີດຳ", "Đôi giày màu đen"),
    ("ສີແດງ", "màu đỏ thắm", "red color", "see daeng", "noun", "mau_sac", "ທຸງຊາດສີແດງ", "Lá cờ đỏ sao vàng"),
    ("ສີເຫຼືອງ", "màu vàng tươi", "yellow color", "see leuang", "noun", "mau_sac", "ດອກໄມ້ສີເຫຼືອງ", "Bông hoa màu vàng rực"),
    ("ສີຂຽວ", "màu xanh lá cây", "green color", "see khiao", "noun", "mau_sac", "ຕົ້ນໄມ້ສີຂຽວສົດ", "Cây cối màu xanh tươi mát"),
    ("ສີຟ້າ", "màu xanh da trời / lam", "blue / sky-blue color", "see fa", "noun", "mau_sac", "ທ້ອງຟ້າສີຟ້າ", "Bầu trời xanh thẳm"),
    ("ສີສົ້ມ", "màu cam tươi tắn", "orange color", "see som", "noun", "mau_sac", "ໝາກກ້ຽງສີສົ້ມ", "Quả cam vỏ màu cam"),
    ("ສີບົວ", "màu hồng phấn hoa sen", "pink color", "see bua", "noun", "mau_sac", "ເສື້ອສີບົວໜ້າຮັກ", "Chiếc áo hồng dễ thương"),
    ("ສີມ່ວງ", "màu tím thủy chung", "purple / violet color", "see muang", "noun", "mau_sac", "ດອກກ້ວຍໄມ້ສີມ່ວງ", "Hoa lan sắc tím"),
    ("ສີນ້ຳຕານ", "màu nâu đất", "brown color", "see nam tan", "noun", "mau_sac", "ໂຕະໄມ້ສີນ້ຳຕານ", "Bàn gỗ màu nâu ấm"),
    ("ສີເທົາ", "màu xám ghi", "gray color", "see thao", "noun", "mau_sac", "ເສື້ອກັນໜາວສີເທົາ", "Áo len xám"),
    ("ສີທອງ", "màu vàng kim óng ánh", "golden color", "see thong", "noun", "mau_sac", "ພຣະພຸດທະຮູບສີທອງ", "Tượng Phật thếp vàng óng"),
    ("ສີເງິນ", "màu bạc sáng ánh kim", "silver color", "see ngen", "noun", "mau_sac", "ລົດໃຫຍ່ສີເງິນ", "Chiếc ô tô ánh bạc"),

    # --- SỐ ĐẾM & ĐƠN VỊ ĐO LƯỜNG (NUMBERS & QUANTIFIERS) ---
    ("ສູນ", "số không (0)", "zero (0)", "soon", "num", "so_dem", "ເລກສູນ", "Con số không"),
    ("ໜຶ່ງ", "số một (1)", "one (1)", "neung", "num", "so_dem", "ໜຶ່ງຄົນ", "Một người"),
    ("ສອງ", "số hai (2)", "two (2)", "song", "num", "so_dem", "ສອງມື້", "Hai ngày"),
    ("ສາມ", "số ba (3)", "three (3)", "sam", "num", "so_dem", "ສາມເດືອນ", "Ba tháng"),
    ("ສີ່", "số bốn (4)", "four (4)", "see", "num", "so_dem", "ສີ່ປີ", "Bốn năm"),
    ("ຫ້າ", "số năm (5)", "five (5)", "ha", "num", "so_dem", "ຫ້າໂມງ", "Năm giờ"),
    ("ຫົກ", "số sáu (6)", "six (6)", "hok", "num", "so_dem", "ຫົກພັນກີບ", "Sáu nghìn kíp"),
    ("ເຈັດ", "số bảy (7)", "seven (7)", "jed", "num", "so_dem", "ເຈັດມື້ຕໍ່ອາທິດ", "Bảy ngày một tuần"),
    ("ແປດ", "số tám (8)", "eight (8)", "paed", "num", "so_dem", "ແປດໂມງເຊົ້າ", "Tám giờ sáng"),
    ("ເກົ້າ", "số chín (9)", "nine (9)", "kao", "num", "so_dem", "ເກົ້າສິບ", "Chín mươi"),
    ("ສິບ", "số mười (10)", "ten (10)", "sib", "num", "so_dem", "ສິບຄະແນນ", "Mười điểm trọn vẹn"),
    ("ຊາວ", "hai mươi (20)", "twenty (20)", "xao", "num", "so_dem", "ຊາວພັນກີບ", "Hai mươi nghìn kíp"),
    ("ສາມສິບ", "ba mươi (30)", "thirty (30)", "sam sib", "num", "so_dem", "ສາມສິບນາທີ", "Ba mươi phút"),
    ("ສີ່ສິບ", "bốn mươi (40)", "forty (40)", "see sib", "num", "so_dem", "ສີ່ສິບກິໂລ", "Bốn mươi cân"),
    ("ຫ້າສິບ", "năm mươi (50)", "fifty (50)", "ha sib", "num", "so_dem", "ຫ້າສິບເປີເຊັນ", "Năm mươi phần trăm"),
    ("ຮ້ອຍ", "một trăm (100)", "hundred (100)", "hoy", "num", "so_dem", "ໜຶ່ງຮ້ອຍ", "Một trăm"),
    ("ພັນ", "một nghìn (1,000)", "thousand (1,000)", "phan", "num", "so_dem", "ໜຶ່ງພັນ", "Một nghìn"),
    ("ໝື່ນ", "mười nghìn (10,000)", "ten thousand (10,000)", "meun", "num", "so_dem", "ໜຶ່ງໝື່ນ", "Mười nghìn kíp"),
    ("ແສນ", "một trăm nghìn (100,000)", "hundred thousand (100,000)", "saen", "num", "so_dem", "ໜຶ່ງແສນກີບ", "Một trăm nghìn kíp"),
    ("ລ້ານ", "một triệu (1,000,000)", "million (1,000,000)", "lan", "num", "so_dem", "ໜຶ່ງລ້ານກີບ", "Một triệu kíp"),
    ("ກີບ", "đồng Kíp (đơn vị tiền tệ Lào)", "Kip (Lao currency)", "keep", "noun", "tien_te", "ລາຄາຫ້າສິບພັນກີບ", "Giá 50.000 Kíp"),
    ("ດົງ", "đồng Việt Nam (VND)", "Dong (Vietnamese currency)", "dong", "noun", "tien_te", "ແລກເງິນດົງ", "Đổi tiền đồng Việt Nam"),
    ("ໂດລາ", "đô la Mỹ (USD)", "Dollar", "doh la", "noun", "tien_te", "ຈ່າຍເປັນໂດລາ", "Thanh toán bằng đô la"),
    ("ບາດ", "đồng Bạt Thái Lan (THB)", "Baht (Thai currency)", "bad", "noun", "tien_te", "ເງິນບາດໄທ", "Đồng bạt Thái"),
    ("ກິໂລກຣາມ", "ki-lô-gam (kg)", "kilogram", "ki loh gram", "noun", "don_vi", "ໜັກຫ້າສິບກິໂລກຣາມ", "Nặng 50 kg"),
    ("ແມັດ", "mét (m)", "meter", "maed", "noun", "don_vi", "ຍາວສອງແມັດ", "Dài hai mét"),
    ("ກິໂລແມັດ", "ki-lô-mét (km)", "kilometer", "ki loh maed", "noun", "don_vi", "ໄລຍະທາງຮ້ອຍກິໂລແມັດ", "Khoảng cách 100 km"),
    ("ລິດ", "lít (l)", "liter", "lit", "noun", "don_vi", "ນ້ຳດື່ມໜຶ່ງລິດ", "Một lít nước uống"),
    ("ໂມງ", "giờ đồng hồ", "hour / o'clock", "mong", "noun", "thoi_gian", "ຈັກໂມງແລ້ວ", "Mấy giờ rồi"),
    ("ນາທີ", "phút", "minute", "na thee", "noun", "thoi_gian", "ລໍຖ້າຫ້ານາທີ", "Chờ trong năm phút"),
    ("ວິນາທີ", "giây", "second", "vi na thee", "noun", "thoi_gian", "ແລ່ນພາຍໃນສິບວິນາທີ", "Chạy trong mười giây"),
    ("ມື້", "ngày", "day", "meu", "noun", "thoi_gian", "ມື້ລະເທື່ອ", "Mỗi ngày một lần"),
    ("ອາທິດ", "tuần lễ", "week", "ar thid", "noun", "thoi_gian", "ອາທິດໜ້າ", "Tuần sau"),
    ("ເດືອນ", "tháng", "month", "deuan", "noun", "thoi_gian", "ເດືອນໜ້າ", "Tháng tới"),
    ("ປີ", "năm", "year", "pee", "noun", "thoi_gian", "ປີໃໝ່", "Năm mới"),

    # --- ĐỊA ĐIỂM, NƠI CHỐN & GIAO THÔNG (LOCATIONS & TRANSPORT) ---
    ("ສະໜາມບິນ", "sân bay / phi trường", "airport", "sa nam bin", "noun", "dia_diem", "ສະໜາມບິນວັດໄຕ", "Sân bay quốc tế Wattay"),
    ("ສະຖານີລົດໄຟ", "ga tàu hỏa", "railway station", "sa tha nee lod fai", "noun", "dia_diem", "ສະຖານີລົດໄຟວຽງຈັນ", "Ga đường sắt Viêng Chăn"),
    ("ຄິວລົດ", "bến xe khách", "bus terminal / station", "khiw lod", "noun", "dia_diem", "ຄິວລົດສາຍໃຕ້", "Bến xe buýt liên tỉnh phía Nam"),
    ("ທ່າເຮືອ", "bến cảng / bến đò", "port / pier / harbor", "tha heua", "noun", "dia_diem", "ທ່າເຮືອທ່າເດື່ອ", "Bến cảng Tha Deua"),
    ("ສະຖານທູດ", "đại sứ quán", "embassy", "sa than thoot", "noun", "dia_diem", "ສະຖານທູດຫວຽດນາມປະຈຳລາວ", "Đại sứ quán Việt Nam tại Lào"),
    ("ທະນາຄານ", "ngân hàng", "bank", "tha na khan", "noun", "dia_diem", "ທະນາຄານການຄ້າຕ່າງປະເທດລາວ", "Ngân hàng Ngoại thương Lào (BCEL)"),
    ("ໄປສະນີ", "bưu điện", "post office", "pai sa nee", "noun", "dia_diem", "ສົ່ງຈົດໝາຍຢູ່ໄປສະນີ", "Gửi thư tại bưu điện"),
    ("ສະຖານີຕຳຫຼວດ", "đồn cảnh sát / công an", "police station", "sa tha nee tam luat", "noun", "dia_diem", "ແຈ້ງຄວາມຢູ່ສະຖານີຕຳຫຼວດ", "Trình báo công an"),
    ("ສວນສາທາລະນະ", "công viên công cộng", "public park", "suan sa tha la na", "noun", "dia_diem", "ຍ່າງຫຼິ້ນສວນສາທາລະນະເຈົ້າອານຸວົງ", "Dạo mát công viên Chao Anouvong"),
    ("ວັດວາອາຮາມ", "chùa chiền tự viện", "temple / pagoda", "vat va ar ham", "noun", "dia_diem", "ໄຫວ້ພຣະຢູ່ວັດ", "Lễ Phật ở chùa"),
    ("ທົ່ງນາ", "cánh đồng lúa bạt ngàn", "rice field / paddy", "thong na", "noun", "dia_diem", "ທົ່ງນາຂຽວງາມ", "Cánh đồng lúa xanh mướt"),
    ("ພູເຂົາ", "ngọn núi cao", "mountain", "phoo khao", "noun", "dia_diem", "ປີນພູເຂົາ", "Leo núi dã ngoại"),
    ("ແມ່ນ້ຳ", "dòng sông quê hương", "river", "mae nam", "noun", "dia_diem", "ແມ່ນ້ຳໄຫຼແຮງ", "Dòng sông chảy xiết"),
    ("ຫາດຊາຍ", "bãi cát bờ biển / bờ sông", "beach / sandbank", "had sai", "noun", "dia_diem", "ຫາດຊາຍແຄມຂອງ", "Bãi cát bồi ven sông Mê Kông"),
    ("ບ້ານນອກ", "nông thôn / làng quê", "countryside / rural area", "ban nork", "noun", "dia_diem", "ກັບໄປຢາມບ້ານນອກ", "Về thăm quê hương thôn dã"),
    ("ຕົວເມືອງ", "thành thị / nội ô phố phường", "city / urban area", "tua meuang", "noun", "dia_diem", "ຊີວິດໃນຕົວເມືອງ", "Đời sống chốn thành thị"),
]

def main():
    print("=" * 65)
    print("💎 CHẠY BỘ NẠP SIÊU TỪ ĐIỂN TIẾNG LÀO ĐỜI SỐNG (ULTRA BUILDER)")
    print("=" * 65)

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

    print(f"[*] Số từ hiện tại: {len(existing_rows)}")

    added = 0
    for item in VOCAB_DATA:
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

    print(f"[+] Đã thêm mới: +{added} mục từ chuẩn hóa.")
    print(f"[+] QUY MÔ TỔNG CỘNG HIỆN NAY: {len(existing_rows)} TỪ VỰNG.")
    print("=" * 65)

if __name__ == "__main__":
    main()
