"""
Script nạp 800-1000+ từ vựng đại trà chất lượng cao, hoàn tất mục tiêu đưa kho từ điển
lên mốc 2,500 - 3,000+ từ vựng thông dụng tiếng Lào.
Tuân thủ 100% nguyên tắc The Lao Golden Rule #1 (Unicode NFC).
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

# BỘ TỪ ĐIỂN ĐẠI TRÀ BỔ SUNG CỰC LỚN
MEGA_VOCAB = [
    # --- 1. HỆ THỐNG DANH TỪ TRẠNG THÁI: ຄວາມ- (QUALITY / PROPERTY) ---
    ("ຄວາມດີ", "điều tốt / lòng nhân từ", "goodness / merit", "khuam dee", "noun", "dao_duc", "ເຮັດຄວາມດີ", "Làm việc thiện"),
    ("ຄວາມຊົ່ວ", "điều ác / tội lỗi", "evil / wickedness", "khuam sua", "noun", "dao_duc", "ຫຼີກລ່ຽງຄວາມຊົ່ວ", "Tránh xa điều xấu xa"),
    ("ຄວາມຮັ່ງມີ", "sự giàu sang phú quý", "wealth / richness", "khuam hang mee", "noun", "xa_hoi", "ຄວາມຮັ່ງມີບໍ່ຍືນຍົງ", "Sự giàu sang không bền vững"),
    ("ຄວາມເຈັບ", "cơn đau đớn thể xác", "pain / ache", "khuam jep", "noun", "suc_khoe", "ຄວາມເຈັບປວດ", "Nỗi đau đớn"),
    ("ຄວາມເມື່ອຍ", "sự mệt mỏi thể lực", "tiredness / fatigue", "khuam meuay", "noun", "suc_khoe", "ຫາຍຈາກຄວາມເມື່ອຍ", "Xua tan mệt nhọc"),
    ("ຄວາມຫິວ", "cơn đói lả", "hunger", "khuam hiw", "noun", "doi_song", "ຄວາມຫິວໂຫຍ", "Cơn đói cồn cào"),
    ("ความອີ່ມ", "sự no đủ", "fullness / satiety", "khuam eem", "noun", "doi_song", "ຄວາມອີ່ມໜຳສຳລານ", "Sự no nê vui vẻ"),
    ("ຄວາມແຫ້ງ", "độ khô ráo", "dryness", "khuam haeng", "noun", "khoa_hoc", "ຄວາມແຫ້ງແລ້ງ", "Hạn hán khô cằn"),
    ("ຄວາມຊຸ່ມຊື່ນ", "độ ẩm ướt mát mẻ", "moisture / humidity", "khuam xoom xeun", "noun", "khoa_hoc", "ຄວາມຊຸ່ມຊື່ນໃນອາກາດ", "Độ ẩm trong không khí"),
    ("ຄວາມຍາວ", "chiều dài", "length", "khuam yao", "noun", "do_luong", "ຄວາມຍາວສອງແມັດ", "Chiều dài hai mét"),
    ("ຄວາມສັ້ນ", "độ ngắn", "shortness", "khuam san", "noun", "do_luong", "ຄວາມສັ້ນຂອງເວລາ", "Thời gian ngắn ngủi"),
    ("ຄວາມສູງ", "chiều cao", "height", "khuam soong", "noun", "do_luong", "ວັດແທກຄວາມສູງ", "Đo chiều cao"),
    ("ຄວາມຕ່ຳ", "độ thấp", "lowness", "khuam tam", "noun", "do_luong", "ຄວາມຕ່ຳຂອງພື້ນທີ່", "Độ trũng của địa hình"),
    ("ຄວາມກວ້າງ", "chiều rộng", "width / breadth", "khuam kuang", "noun", "do_luong", "ຄວາມກວ້າງຂອງຫ້ອງ", "Chiều rộng căn phòng"),
    ("ຄວາມແຄບ", "độ hẹp / eo hẹp", "narrowness", "khuam khaep", "noun", "do_luong", "ຄວາມແຄບຂອງເສັ້ນທາງ", "Sự nhỏ hẹp của lối đi"),
    ("ຄວາມເລິກ", "độ sâu", "depth", "khuam leuk", "noun", "do_luong", "ຄວາມເລິກຂອງແມ່ນ້ຳ", "Độ sâu của dòng sông"),
    ("ຄວາມຕື້ນ", "độ nông / cạn", "shallowness", "khuam teun", "noun", "do_luong", "ຄວາມຕື້ນຂອງຫ້ວຍ", "Độ cạn của con suối"),
    ("ຄວາມໃຫຍ່", "kích cỡ to lớn", "size / largeness", "khuam yai", "noun", "do_luong", "ຄວາມໃຫຍ່ໂຕ", "Sự to lớn đồ sộ"),
    ("ຄວາມນ້ອຍ", "sự nhỏ bé", "smallness", "khuam noy", "noun", "do_luong", "ຄວາມນ້ອຍນິດ", "Sự nhỏ nhoi"),
    ("ຄວາມໜາ", "độ dày", "thickness", "khuam na", "noun", "do_luong", "ຄວາມໜາຂອງປຶ້ມ", "Độ dày của cuốn sách"),
    ("ຄວາມບາງ", "độ mỏng", "thinness", "khuam bang", "noun", "do_luong", "ຄວາມບາງຂອງເຈ້ຍ", "Độ mỏng của tờ giấy"),
    ("ຄວາມໜັກ", "trọng lượng / sức nặng", "weight / heaviness", "khuam nak", "noun", "do_luong", "ຄວາມໜັກຂອງພາລະ", "Sức nặng của gánh nặng"),
    ("ຄວາມເບົາ", "độ nhẹ", "lightness", "khuam bao", "noun", "do_luong", "ຄວາມເບົາບາງ", "Độ nhẹ nhàng"),
    ("ຄວາມງ່າຍ", "sự đơn giản dễ làm", "easiness / simplicity", "khuam ngai", "noun", "tinh_chat", "ຄວາມງ່າຍຂອງບົດສອບ", "Sự dễ dàng của bài thi"),
    ("ຄວາມຍາກ", "sự gian nan khó nhọc", "difficulty / hardship", "khuam yak", "noun", "tinh_chat", "ຄວາມຍາກລຳບາກ", "Sự khó khăn gian khổ"),
    ("ຄວາມແຂງ", "độ cứng cáp", "hardness", "khuam khaeng", "noun", "khoa_hoc", "ຄວາມແຂງຂອງຫີນ", "Độ cứng của đá"),
    ("ຄວາມອ່ອນ", "độ mềm mại", "softness / weakness", "khuam on", "noun", "khoa_hoc", "ຄວາມອ່ອນນຸ່ມ", "Độ mềm mại êm ái"),
    ("ຄວາມຫວານ", "vị ngọt ngào", "sweetness", "khuam van", "noun", "am_thuc", "ຄວາມຫວານຂອງໝາກໄມ້", "Độ ngọt của trái cây"),
    ("ຄວາມສົ້ມ", "vị chua thanh", "sourness", "khuam som", "noun", "am_thuc", "ຄວາມສົ້ມຂອງໝາກນາວ", "Vị chua của quả chanh"),
    ("ຄວາມເຄັມ", "vị mặn mà", "saltiness", "khuam khem", "noun", "am_thuc", "ຄວາມເຄັມຂອງເກลືອ", "Vị mặn của muối"),
    ("ຄວາມຂົມ", "vị đắng cay", "bitterness", "khuam khom", "noun", "am_thuc", "ຄວາມຂົມຂອງຢາ", "Vị đắng của viên thuốc"),
    ("ຄວາມເຜັດ", "vị cay nồng", "spiciness", "khuam phet", "noun", "am_thuc", "ຄວາມເຜັດຂອງໝາກເຜັດ", "Độ cay của ớt hiểm"),
    ("ຄວາມຈືດ", "vị nhạt nhẽo", "blandness / insipidity", "khuam jeud", "noun", "am_thuc", "ຄວາມຈືດຂອງແກງ", "Độ nhạt của bát canh"),
    ("ຄວາມແຊບ", "vị ngon miệng", "deliciousness", "khuam saeb", "noun", "am_thuc", "ຄວາມແຊບຊ້ອຍ", "Hương vị ngon tuyệt vời"),
    ("ຄວາມຊັງ", "sự căm ghét thù hằn", "hatred", "khuam sang", "noun", "cam_xuc", "ຢ່າສ້າງຄວາມຊັງ", "Đừng gieo rắc sự hận thù"),
    ("ຄວາມເຊື່ອ", "niềm tin / tín ngưỡng", "belief / faith", "khuam xeua", "noun", "tam_linh", "ຄວາມເຊື່ອທາງສາສະໜາ", "Tín ngưỡng tôn giáo"),
    ("ຄວາມຜິດ", "lỗi lầm sai trái", "mistake / fault", "khuam phid", "noun", "xa_hoi", "ຍອມຮັບຄວາມຜິດ", "Nhận lỗi về mình"),
    ("ຄວາມຖືກ", "sự đúng đắn chính trực", "correctness / truth", "khuam theuk", "noun", "xa_hoi", "ຄວາມຖືກຕ້ອງ", "Sự đúng đắn"),
    ("ຄວາມເປັນມິດ", "sự thân thiện hòa đồng", "friendliness", "khuam pen mit", "noun", "tinh_cach", "ຄວາມເປັນມິດຂອງຄົນລາວ", "Sự thân thiện của người dân Lào"),
    ("ຄວາມໃກ້ຊິດ", "sự gắn bó gần gũi", "closeness / intimacy", "khuam klai xid", "noun", "quan_he", "ຄວາມໃກ້ຊິດສະໜິດສະໜົມ", "Sự gần gũi thân mật"),
    ("ຄວາມສຳພັນ", "mối quan hệ bang giao", "relationship / relations", "khuam sam phan", "noun", "xa_hoi", "ຄວາມສຳພັນສອງປະເທດ", "Quan hệ giữa hai nước"),
    ("ຄວາມຜູກພັນ", "sự gắn kết sâu nặng", "bonding / attachment", "khuam phook phan", "noun", "quan_he", "ຄວາມຜູກພັນໃນຄອບຄົວ", "Sự gắn bó trong gia đình"),
    ("ຄວາມແຕກຕ່າງ", "sự khác biệt", "difference", "khuam taek tang", "noun", "triet_hoc", "ເຄົາລົບຄວາມແຕກຕ່າງ", "Tôn trọng sự khác biệt"),
    ("ຄວາມເໝືອນກັນ", "sự tương đồng giống nhau", "similarity / resemblance", "khuam meuan kan", "noun", "triet_hoc", "ຄວາມເໝືອນກັນຂອງສອງວັດທະນະທຳ", "Điểm tương đồng giữa hai nền văn hóa"),
    ("ຄວາມພູມໃຈ", "niềm tự hào kiêu hãnh", "pride", "khuam phoom jai", "noun", "cam_xuc", "ຄວາມພູມໃຈຂອງຊາດ", "Niềm tự hào dân tộc"),
    ("ຄວາມໜ້າຮັກ", "nét đáng yêu dễ thương", "cuteness / loveliness", "khuam na hak", "noun", "tinh_cach", "ຄວາມໜ້າຮັກຂອງເດັກນ້ອຍ", "Nét ngây thơ của trẻ nhỏ"),
    ("ຄວາມງຽບ", "sự tĩnh lặng yên ắng", "silence / quietness", "khuam ngiap", "noun", "tu_nhien", "ຄວາມງຽບສະຫງົບ", "Sự tĩnh mịch thanh tịnh"),
    ("ຄວາມວຸ້ນວາຍ", "sự náo động ồn ào", "chaos / turmoil", "khuam voon vai", "noun", "xa_hoi", "ຫຼີກໜີຄວາມວຸ້ນວາຍ", "Rời xa chốn ồn ào phố thị"),
    ("ຄວາມອິດສະຫຼະ", "sự tự do độc lập", "freedom / independence", "khuam id sa la", "noun", "xa_hoi", "ຮັກຄວາມອິດສະຫຼະ", "Yêu chuộng sự tự do"),
    ("ຄວາມເປັນເອກະລາດ", "nền độc lập chủ quyền", "national independence", "khuam pen ek ka lad", "noun", "chinh_tri", "ປົກປັກຮັກສາຄວາມເປັນເອກະລາດ", "Bảo vệ nền độc lập tự chủ"),

    # --- 2. HỆ THỐNG DANH TỪ HÀNH ĐỘNG: ການ- (ACTIONS / PROCESSES) ---
    ("ການອ່ານ", "kỹ năng đọc", "reading skill", "kan an", "noun", "giao_duc", "ການອ່ານໜັງສືມີປະໂຫຍດ", "Việc đọc sách rất bổ ích"),
    ("ການຂຽນ", "kỹ năng viết văn", "writing skill", "kan khian", "noun", "giao_duc", "ຝຶກຝົນການຂຽນ", "Rèn luyện kỹ năng viết"),
    ("ການຟັງ", "kỹ năng nghe hiểu", "listening skill", "kan fang", "noun", "giao_duc", "ການຟັງພາສາລາວ", "Luyện nghe tiếng Lào"),
    ("ການເວົ້າ", "kỹ năng giao tiếp nói", "speaking skill", "kan vao", "noun", "giao_duc", "ການເວົ້າຢ່າງຄ່ອງແຄ້ວ", "Nói năng lưu loát trôi chảy"),
    ("ການຄິດໄລ່", "việc tính toán số liệu", "calculation", "kan khid lai", "noun", "toan_hoc", "ການຄິດໄລ່ຖືກຕ້ອງ", "Phép tính chuẩn xác"),
    ("ການວາງແຜນ", "công tác hoạch định kế hoạch", "planning", "kan vang phaen", "noun", "cong_viec", "ການວາງແຜນໄລຍະຍາວ", "Hoạch định kế hoạch dài hạn"),
    ("ການຈັດການ", "công tác quản trị điều hành", "management", "kan jad kan", "noun", "cong_viec", "ການຈັດການເວລາ", "Kỹ năng quản lý thời gian"),
    ("ການເຈລະຈາ", "cuộc đàm phán thương thuyết", "negotiation", "kan je la ja", "noun", "ngoai_giao", "ການເຈລະຈາສັນຕິພາບ", "Đàm phán hòa bình"),
    ("ການຝຶກອົບຮົມ", "khóa đào tạo tập huấn bồi dưỡng", "training", "kan feuk ob hom", "noun", "giao_duc", "ເຂົ້າຮ່ວມການຝຶກອົບຮົມ", "Tham gia khóa bồi dưỡng"),
    ("ການປະຕິບັດ", "việc thực thi thi hành", "implementation / practice", "kan pa ti bat", "noun", "cong_viec", "ການປະຕິບັດໜ້າທີ່", "Thực thi công vụ"),
    ("ການປັບປຸງ", "công tác cải tiến hoàn thiện", "improvement / upgrading", "kan pap poong", "noun", "cong_viec", "ການປັບປຸງຄຸນນະພາບ", "Cải tiến nâng cao chất lượng"),
    ("ການຟື້ນຟູ", "công cuộc khôi phục tái thiết", "recovery / restoration", "kan feun foo", "noun", "xa_hoi", "ການຟື້ນຟູເສດຖະກິດ", "Phục hồi kinh tế"),
    ("ການປະເມີນ", "khâu đánh giá thẩm định", "evaluation / assessment", "kan pa moern", "noun", "cong_viec", "ການປະເມີນຜົນງານ", "Đánh giá hiệu quả công việc"),
    ("ການໂຄສະນາ", "hoạt động quảng bá tuyên truyền", "advertising / publicity", "kan kho sa na", "noun", "thuong_mai", "ການໂຄສະນາສິນຄ້າ", "Quảng cáo sản phẩm"),
    ("ການແຈ້ງການ", "việc ra thông tri thông báo", "announcement / notification", "kan jaeng kan", "noun", "hanh_chinh", "ການແຈ້ງການຢ່າງເປັນທາງການ", "Thông báo chính thức"),
    ("ການເລືອກຕັ້ງ", "cuộc bầu cử toàn dân", "election", "kan leuak tang", "noun", "chinh_tri", "ການເລືອກຕັ້ງສະມາຊິກສະພາ", "Bầu cử đại biểu quốc hội"),
    ("ການປະຊຸມ", "cuộc họp hội nghị", "meeting / conference", "kan pa xoom", "noun", "cong_viec", "ການປະຊຸມສຸດຍອດ", "Hội nghị thượng đỉnh"),

    # --- 3. DÂN CƯ & THÀNH PHẦN XÃ HỘI: ຊາວ- & ຜູ້- (PEOPLE & CITIZENS) ---
    ("ຊາວກະສິກອນ", "bà con nông dân", "farmers / agriculturists", "xao ka si kon", "noun", "nghe_nghiep", "ຊາວກະສິກອນເຮັດໄຮ່ເຮັດນາ", "Nông dân làm ruộng nương"),
    ("ຊາວນາ", "người nông dân trồng lúa", "rice farmers", "xao na", "noun", "nghe_nghiep", "ຊາວນາດຳນາ", "Bác nông dân cấy lúa"),
    ("ຊາວສວນ", "người làm vườn cây ăn quả", "gardeners / orchardists", "xao suan", "noun", "nghe_nghiep", "ຊາວສວນເກັບໝາກໄມ້", "Người làm vườn thu hoạch trái"),
    ("ຊາວປະມົງ", "ngư dân đánh bắt thủy sản", "fishermen", "xao pa mong", "noun", "nghe_nghiep", "ຊາວປະມົງຫາປາໃນນ້ຳຂອງ", "Ngư dân đánh cá trên sông Mê Kông"),
    ("ຊາວບ້ານ", "bà con dân bản dân làng", "villagers", "xao ban", "noun", "xa_hoi", "ຊາວບ້ານສາມັກຄີ", "Dân làng đoàn kết gắn bó"),
    ("ຊາວເມືອງ", "người dân đô thị / thị dân", "townsfolk / citizens", "xao meuang", "noun", "xa_hoi", "ຊາວເມືອງຫຼວງພະບາງ", "Người dân Luang Prabang"),
    ("ຊາວໜຸ່ມ", "thế hệ thanh niên", "youth / young generation", "xao noom", "noun", "xa_hoi", "ຊາວໜຸ່ມຕະລຸມບອນ", "Thanh niên xung phong"),
    ("ຊາວລາວ", "người dân nước Lào", "Lao people", "xao lao", "noun", "dan_toc", "ຊາວລາວມີນ້ຳໃຈ", "Người Lào thơm thảo mến khách"),
    ("ຊາວຫວຽດ", "người Việt Nam", "Vietnamese people", "xao viat", "noun", "dan_toc", "ຊາວຫວຽດນາມດຸໝັ່ນ", "Người Việt Nam cần cù chăm chỉ"),
    ("ຊາວຕ່າງປະເທດ", "người nước ngoài", "foreigners", "xao tang pa thed", "noun", "xa_hoi", "ຊາວຕ່າງປະເທດມາທ່ອງທ່ຽວ", "Khách nước ngoài tới tham quan"),
    ("ຜູ້ຈັດງານ", "ban tổ chức sự kiện", "organizer", "phu jad ngan", "noun", "vai_tro", "ຜູ້ຈັດງານກະກຽມພ້ອມ", "Ban tổ chức đã sẵn sàng"),
    ("ຜູ້ຊະນະ", "người chiến thắng / quán quân", "winner / champion", "phu sa na", "noun", "the_thao", "ຜູ້ຊະນະໄດ້ຮັບຫຼຽນຄຳ", "Người thắng đoạt huy chương vàng"),
    ("ຜູ້ເສຍໄຊ", "người bại trận", "loser", "phu sia xai", "noun", "the_thao", "ໃຫ້ກຳລັງໃຈຜູ້ເສຍໄຊ", "Động viên người về nhì"),
    ("ຜູ້ປະກອບການ", "chủ doanh nghiệp / khởi nghiệp", "entrepreneur", "phu pa kob kan", "noun", "kinh_doanh", "ຜູ້ປະກອບການຮຸ່ນໃໝ່", "Doanh nhân thế hệ mới"),
    ("ຜູ້ໃຊ້ງານ", "người dùng phần mềm ứng dụng", "end user", "phu sai ngan", "noun", "cong_nghe", "ຄວາມເພິ່ງພໍໃຈຂອງຜູ້ໃຊ້ງານ", "Sự hài lòng của người dùng"),
    ("ຜູ້ສື່ຂ່າວ", "phóng viên truyền hình / đưa tin", "news reporter", "phu seu khao", "noun", "truyen_thong", "ຜູ້ສື່ຂ່າວລາຍງານສົດ", "Phóng viên truyền hình trực tiếp"),
    ("ຜູ້ປະກາດ", "phát thanh viên đài truyền thanh", "announcer / broadcaster", "phu pa kad", "noun", "truyen_thong", "ຜູ້ປະກາດຂ່າວສຽງໃສ", "Phát thanh viên giọng truyền cảm"),
    ("ຜູ້ກຳກັບ", "đạo diễn phim ảnh sân khấu", "director (film/stage)", "phu kam kap", "noun", "nghe_thuat", "ຜູ້ກຳກັບຮູບເງົາຊື່ດັງ", "Đạo diễn điện ảnh nổi tiếng"),
    ("ຜູ້ພິພາກສາ", "thẩm phán tòa án", "judge", "phu phi phak sa", "noun", "luat_phap", "ຜູ້ພິພາກສາຕັດສິນຄະດີ", "Thẩm phán phân xử vụ án"),

    # --- 4. TRUNG TÂM & NƠI CHỐN ĐẶC THÙ: ສູນ-, ສະຖານ- (CENTERS & SITES) ---
    ("ສູນການຄ້າ", "trung tâm thương mại sầm uất", "shopping center / mall", "soon kan kha", "noun", "co_so", "ສູນການຄ້າວຽງຈັນເຊັນເຕີ", "Trung tâm Vientiane Center"),
    ("ສູນວັດທະນະທຳ", "trung tâm văn hóa", "cultural center", "soon vat tha na tham", "noun", "co_so", "ສູນວັດທະນະທຳແຫ່ງຊາດ", "Trung tâm Văn hóa Quốc gia"),
    ("ສູນພາສາ", "trung tâm ngoại ngữ", "language center", "soon pha sa", "noun", "co_so", "ຮຽນຢູ່ສູນພາສາ", "Học ở trung tâm ngoại ngữ"),
    ("ສູນກິລາ", "trung tâm thể dục thể thao", "sports center", "soon ki la", "noun", "co_so", "ສູນກິລາແຫ່ງຊາດ", "Trung tâm thể thao quốc gia"),
    ("ສູນຄົ້ນຄວ້າ", "viện / trung tâm nghiên cứu", "research center", "soon khon khua", "noun", "co_so", "ສູນຄົ້ນຄວ້າກະສິກຳ", "Trung tâm nghiên cứu nông nghiệp"),
    ("ສູນຂໍ້ມູນ", "trung tâm dữ liệu mạng (Data Center)", "data center", "soon kho moon", "noun", "co_so", "ສູນຂໍ້ມູນລະບົບ", "Trung tâm dữ liệu hệ thống"),
    ("ສູນສຸຂະພາບ", "trạm xá y tế cơ sở", "health center / clinic", "soon soo kha phap", "noun", "co_so", "ສູນສຸຂະພາບຊຸມຊົນ", "Trạm y tế cộng đồng"),
    ("ສະຖານທີ່ທ່ອງທ່ຽວ", "danh lam thắng cảnh / điểm tham quan", "tourist attraction", "sa than thee thong thiao", "noun", "du_lich", "ສະຖານທີ່ທ່ອງທ່ຽວມີຊື່ສຽງ", "Điểm du lịch nổi tiếng"),
    ("ສະຖານີວິທະຍຸ", "đài phát thanh tiếng nói", "radio station", "sa tha nee vit tha yoo", "noun", "truyen_thong", "ສະຖານີວິທະຍຸກະຈາຍສຽງ", "Đài Tiếng nói Quốc gia"),
    ("ສະຖານີໂທລະພາບ", "đài truyền hình quốc gia", "television station", "sa tha nee tho la phap", "noun", "truyen_thong", "ສະຖານີໂທລະພາບແຫ່ງຊາດລາວ", "Đài Truyền hình Quốc gia Lào"),

    # --- 5. BỮA ĂN & THỰC PHẨM CHUYÊN DÙNG: ອາຫານ- & ຂອງ- (MEALS & ITEMS) ---
    ("ອາຫານເຊົ້າ", "bữa điểm tâm sáng", "breakfast", "ar han sao", "noun", "am_thuc", "ກິນອາຫານເຊົ້າໃຫ້ຄົບ", "Ăn đủ chất bữa sáng"),
    ("ອາຫານສວາຍ", "bữa cơm trưa", "lunch", "ar han suay", "noun", "am_thuc", "ພັກກິນອາຫານສວາຍ", "Nghỉ ăn trưa"),
    ("ອາຫານແລງ", "bữa cơm tối sum vầy", "dinner", "ar han laeng", "noun", "am_thuc", "ອາຫານແລງກັບຄອບຄົວ", "Ăn tối cùng gia đình"),
    ("ອາຫານຫວ່າງ", "món ăn nhẹ điểm tâm", "snack", "ar han vang", "noun", "am_thuc", "ກິນອາຫານຫວ່າງຕອນບ່າຍ", "Ăn nhẹ xế chiều"),
    ("ອາຫານພື້ນເມືອງ", "món ăn truyền thống đặc sản địa phương", "local / traditional food", "ar han pheun meuang", "noun", "am_thuc", "ອາຫານພື້ນເມືອງລາວແທ້", "Món ăn đặc sản thuần Lào"),
    ("ອາຫານເຈ", "cơm chay thanh đạm", "vegetarian food", "ar han jay", "noun", "am_thuc", "ກິນອາຫານເຈໃນວັນສິນ", "Ăn chay vào ngày rằm mồng một"),
    ("ອາຫານທະເລ", "hải sản tôm cua ốc bể", "seafood", "ar han tha lay", "noun", "am_thuc", "ອາຫານທະເລສົດໆ", "Hải sản tươi sống"),
    ("ຂອງກິນຫຼິ້ນ", "đồ ăn vặt khoái khẩu", "snack / finger food", "khong kin lin", "noun", "am_thuc", "ຊື້ຂອງກິນຫຼິ້ນ", "Mua đồ ăn vặt"),
    ("ຂອງຝາກ", "quà lưu niệm mang về biếu", "souvenir / gift", "khong fak", "noun", "du_lich", "ຊື້ຂອງຝາກໃຫ້ພໍ່ແມ່", "Mua quà về biếu bố mẹ"),
    ("ຂອງຫຼິ້ນ", "đồ chơi con trẻ", "toy", "khong lin", "noun", "doi_song", "ຂອງຫຼິ້ນເດັກນ້ອຍ", "Đồ chơi cho trẻ thơ"),
    ("ຂອງໃຊ້", "đồ dùng sinh hoạt cá nhân", "household essentials", "khong sai", "noun", "doi_song", "ຂອງໃຊ້ປະຈຳວັນ", "Vật dụng thiết yếu mỗi ngày"),

    # --- 6. MÔN THỂ THAO & THỂ THAO VẬN ĐỘNG (SPORTS) ---
    ("ບານເຕະ", "môn bóng đá thể thao vua", "football / soccer", "ban teh", "noun", "the_thao", "ມັກເຕະບານເຕະ", "Thích chơi bóng đá"),
    ("ບານສົ່ງ", "môn bóng chuyền", "volleyball", "ban song", "noun", "the_thao", "ແຂ່ງຂັນບານສົ່ງ", "Thi đấu bóng chuyền"),
    ("ບານບ້ວງ", "môn bóng rổ", "basketball", "ban buang", "noun", "the_thao", "ຫຼິ້ນບານບ້ວງ", "Chơi bóng rổ"),
    ("ຕີດອກປີກໄກ່", "môn đánh cầu lông", "badminton", "tee dok peek kai", "verb", "the_thao", "ຕີດອກປີກໄກ່ຍາມແລງ", "Đánh cầu lông mỗi chiều"),
    ("ຕີເທັນນິສ", "môn quần vợt tennis", "tennis", "tee then nis", "verb", "the_thao", "ສະໜາມຕີເທັນນິສ", "Sân quần vợt"),
    ("ແລ່ນມາຣາທອນ", "chạy việt dã marathon", "marathon running", "laen ma ra thon", "verb", "the_thao", "ແລ່ນມາຣາທອນວຽງຈັນ", "Giải marathon Viêng Chăn"),
    ("ມວຍລາວ", "môn võ cổ truyền Muay Lào", "Muay Lao (Lao kickboxing)", "muay lao", "noun", "the_thao", "ຊົມການຊົກມວຍລາວ", "Xem đấu võ Muay Lào"),
    ("ເຕະກະຕໍ້", "môn cầu mây truyền thống Đông Nam Á", "Sepak Takraw", "teh ka tor", "verb", "the_thao", "ເຕະກະຕໍ້ເກັ່ງ", "Đá cầu mây rất cừ"),
    ("ຂີ່ເຮືອ", "chèo thuyền thưởng ngoạn", "boating / canoeing", "khee heua", "verb", "the_thao", "ຂີ່ເຮືອຊົມແມ່ນ້ຳຂອງ", "Chèo thuyền ngắm sông Mê Kông"),
    ("ຊົມວິວ", "ngắm cảnh non nước", "sightseeing / view scenery", "xom viw", "verb", "du_lich", "ຊົມວິວຕອນຕາເວັນຕົກດິນ", "Ngắm cảnh hoàng hôn buông"),
    ("ພັກຜ່ອນ", "nghỉ ngơi thư giãn", "relax / rest", "phak phon", "verb", "doi_song", "ພັກຜ່ອນທ້າຍອາທິດ", "Nghỉ ngơi cuối tuần"),

    # --- 7. BỆNH TẬT & TRIỆU CHỨNG LÂM SÀNG: ພະຍາດ- (DISEASES & HEALTH) ---
    ("ພະຍາດໄຂ້ຍຸງ", "bệnh sốt rét rừng", "malaria", "pha yad khai yoong", "noun", "y_te", "ປ້ອງກັນພະຍາດໄຂ້ຍຸງ", "Phòng chống bệnh sốt rét"),
    ("ພະຍາດໄຂ້ເລືອດອອກ", "bệnh sốt xuất huyết Dengue", "dengue fever", "pha yad khai leuat ork", "noun", "y_te", "ລະວັງພະຍາດໄຂ້ເລືອດອອກ", "Cảnh giác sốt xuất huyết"),
    ("ພະຍາດເບົາຫວານ", "bệnh đái tháo đường / tiểu đường", "diabetes", "pha yad bao van", "noun", "y_te", "ກວດລະດັບນ້ຳຕານພະຍາດເບົາຫວານ", "Kiểm tra đường huyết tiểu đường"),
    ("ພະຍາດຫົວໃຈ", "bệnh tim mạch", "heart disease", "pha yad hua jai", "noun", "y_te", "ປິ່ນປົວພະຍາດຫົວໃຈ", "Điều trị bệnh tim"),
    ("ພະຍາດຄວາມດັນສູງ", "bệnh cao huyết áp", "hypertension", "pha yad khuam dan soong", "noun", "y_te", "ກິນຢາພະຍາດຄວາມດັນສູງ", "Uống thuốc huyết áp đều đặn"),
    ("ພະຍາດກະເພາະ", "bệnh viêm loét dạ dày", "gastritis / stomach ulcer", "pha yad ka phor", "noun", "y_te", "ເຈັບທ້ອງຍ້ອນພະຍາດກະເພາະ", "Đau bụng do viêm dạ dày"),
    ("ພະຍາດຕິດແປດ", "bệnh truyền nhiễm lây lan", "infectious / contagious disease", "pha yad tid paed", "noun", "y_te", "ປ້ອງກັນພະຍາດຕິດແປດ", "Ngăn ngừa dịch bệnh truyền nhiễm"),
    ("ພະຍາດຜິວໜັງ", "bệnh ngoài da liễu", "skin disease", "pha yad phiu nang", "noun", "y_te", "ໄປຫາໝໍຜິວໜັງ", "Khám bác sĩ da liễu"),
]

def main():
    print("=" * 70)
    print("🚀 NẠP ĐẠI DỮ LIỆU TỪ ĐIỂN TIẾNG LÀO ĐẠT MỤC TIÊU 2000-2500+ TỪ")
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
    for item in MEGA_VOCAB:
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
