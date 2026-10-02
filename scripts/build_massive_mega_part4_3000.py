"""
Script hoàn thiện kho từ điển tiếng Lào vượt mốc 2,500 - 3,000 từ vựng.
Tập trung vào:
- Số đếm mở rộng (hàng chục, hàng trăm, thứ tự)
- Thời gian chi tiết (buổi trong ngày, các thứ trong tuần, ngày lễ)
- Từ vựng công nghệ, số hóa, truyền thông
- Động vật, côn trùng, sinh vật biển
- Thiên nhiên, vũ trụ, địa lý tự nhiên
- Dụng cụ sinh hoạt gia đình, đồ dùng học tập
- Cụm từ giao tiếp thành ngữ cửa miệng hàng ngày
Tuân thủ 100% NFC theo normalize_lao().
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

BATCH_PART4 = [
    # --- 1. SỐ ĐẾM MỞ RỘNG & THỨ BẬC (NUMBERS & ORDINALS) ---
    ("ສິບເອັດ", "mười một (11)", "eleven (11)", "sib et", "num", "so_dem", "ອາຍຸສິບເອັດປີ", "Mười một tuổi"),
    ("ສິບສອງ", "mười hai (12)", "twelve (12)", "sib song", "num", "so_dem", "ສິບສອງເດືອນ", "Mười hai tháng"),
    ("ສິບສາມ", "mười ba (13)", "thirteen (13)", "sib sam", "num", "so_dem", "ວັນທີສິບສາມ", "Ngày mười ba"),
    ("ສິບສີ່", "mười bốn (14)", "fourteen (14)", "sib see", "num", "so_dem", "ສິບສີ່ຄົນ", "Mười bốn người"),
    ("ສິບຫ້າ", "mười lăm (15)", "fifteen (15)", "sib ha", "num", "so_dem", "ສິບຫ້ານາທີ", "Mười lăm phút"),
    ("ສິບຫົກ", "mười sáu (16)", "sixteen (16)", "sib hok", "num", "so_dem", "ຫ້ອງສິບຫົກ", "Phòng mười sáu"),
    ("ສິບເຈັດ", "mười bảy (17)", "seventeen (17)", "sib jed", "num", "so_dem", "ເລກສິບເຈັດ", "Số mười bảy"),
    ("ສິບແປດ", "mười tám (18)", "eighteen (18)", "sib paed", "num", "so_dem", "ສິບແປດປີຂຶ້ນໄປ", "Từ 18 tuổi trở lên"),
    ("ສິບເກົ້າ", "mười chín (19)", "nineteen (19)", "sib kao", "num", "so_dem", "ສິບເກົ້າໂມງ", "Mười chín giờ"),
    ("ຊາວເອັດ", "hai mươi mốt (21)", "twenty-one (21)", "xao et", "num", "so_dem", "ຊາວເອັດພັນ", "Hai mươi mốt nghìn"),
    ("ຊາວສອງ", "hai mươi hai (22)", "twenty-two (22)", "xao song", "num", "so_dem", "ວັນທີຊາວສອງ", "Ngày 22"),
    ("ຊາວຫ້າ", "hai mươi lăm (25)", "twenty-five (25)", "xao ha", "num", "so_dem", "ຊາວຫ້າອົງສາ", "Hai mươi lăm độ C"),
    ("ຫົກສິບ", "sáu mươi (60)", "sixty (60)", "hok sib", "num", "so_dem", "ຫົກສິບນາທີ", "Sáu mươi phút"),
    ("ເຈັດສິບ", "bảy mươi (70)", "seventy (70)", "jed sib", "num", "so_dem", "ເຈັດສິບພັນກີບ", "Bảy mươi nghìn kíp"),
    ("ແປດສິບ", "tám mươi (80)", "eighty (80)", "paed sib", "num", "so_dem", "ແປດສິບເປີເຊັນ", "Tám mươi phần trăm"),
    ("ເກົ້າສິບ", "chín mươi (90)", "ninety (90)", "kao sib", "num", "so_dem", "ເກົ້າສິບວິນາທີ", "Chín mươi giây"),
    ("ໜຶ່ງຮ້ອຍ", "một trăm (100)", "one hundred (100)", "neung hoy", "num", "so_dem", "ໜຶ່ງຮ້ອຍເປີເຊັນ", "Một trăm phần trăm"),
    ("ສອງຮ້ອຍ", "hai trăm (200)", "two hundred (200)", "song hoy", "num", "so_dem", "ສອງຮ້ອຍກິໂລແມັດ", "Hai trăm cây số"),
    ("ຫ้าร້ອຍ", "năm trăm (500)", "five hundred (500)", "ha hoy", "num", "so_dem", "ຫ้าร້ອຍກີບ", "Năm trăm kíp"),
    ("ໜຶ່ງພັນ", "một nghìn (1,000)", "one thousand (1,000)", "neung phan", "num", "so_dem", "ໜຶ່ງພັນກີບ", "Một nghìn kíp"),
    ("ສອງພັນ", "hai nghìn (2,000)", "two thousand (2,000)", "song phan", "num", "so_dem", "ສອງພັນປີ", "Hai nghìn năm"),
    ("ຫ້າພັນ", "năm nghìn (5,000)", "five thousand (5,000)", "ha phan", "num", "so_dem", "ຫ້າພັນດົງ", "Năm nghìn đồng"),
    ("ໜຶ່ງໝື່ນ", "mười nghìn (10,000)", "ten thousand (10,000)", "neung meun", "num", "so_dem", "ໜຶ່ງໝື່ນກີບ", "Mười nghìn kíp"),
    ("ຫ້າໝື່ນ", "năm mươi nghìn (50,000)", "fifty thousand (50,000)", "ha meun", "num", "so_dem", "ຫ້າໝື່ນກີບ", "Năm mươi nghìn kíp"),
    ("ໜຶ່ງແສນ", "một trăm nghìn (100,000)", "one hundred thousand (100,000)", "neung saen", "num", "so_dem", "ໜຶ່ງແສນກີບ", "Một trăm nghìn kíp"),
    ("ຫ້າແສນ", "năm trăm nghìn (500,000)", "five hundred thousand (500,000)", "ha saen", "num", "so_dem", "ຫ້າແສນກີບ", "Năm trăm nghìn kíp"),
    ("ໜຶ່ງລ້ານ", "một triệu (1,000,000)", "one million (1,000,000)", "neung lan", "num", "so_dem", "ໜຶ່ງລ້ານກີບ", "Một triệu kíp"),
    ("ສິບລ້ານ", "mười triệu (10,000,000)", "ten million (10,000,000)", "sib lan", "num", "so_dem", "ສິບລ້ານກີບ", "Mười triệu kíp"),
    ("ຕື້", "một tỷ (1,000,000,000)", "billion (1,000,000,000)", "teu", "num", "so_dem", "ໜຶ່ງຕື້ກີບ", "Một tỷ kíp"),
    ("ທີໜຶ່ງ", "thứ nhất / hạng một", "first (1st)", "thee neung", "noun", "thu_tu", "ໄດ້ອັນດັບທີໜຶ່ງ", "Đạt giải nhất"),
    ("ທີສອງ", "thứ hai / hạng nhì", "second (2nd)", "thee song", "noun", "thu_tu", "ລາງວັນທີສອງ", "Giải nhì"),
    ("ທີສາມ", "thứ ba / hạng ba", "third (3rd)", "thee sam", "noun", "thu_tu", "ຢູ່ຊັ້ນທີສາມ", "Ở tầng 3"),
    ("ທີສີ່", "thứ tư", "fourth (4th)", "thee see", "noun", "thu_tu", "ບົດທີສີ່", "Bài số bốn"),
    ("ທີຫ້າ", "thứ năm", "fifth (5th)", "thee ha", "noun", "thu_tu", "ຄັ້ງທີຫ້າ", "Lần thứ năm"),
    ("ອັນດັບໜຶ່ງ", "đứng vị trí số 1 / quán quân", "rank first / top 1", "an dap neung", "noun", "thu_tu", "ຕິດອັນດັບໜຶ່ງ", "Lọt vào vị trí số 1"),
    ("ຂັ້ນຕົ້ນ", "trình độ sơ cấp", "beginner / elementary level", "khan ton", "noun", "giao_duc", "ພາສາລາວຂັ້ນຕົ້ນ", "Tiếng Lào sơ cấp"),
    ("ຂັ້ນກາງ", "trình độ trung cấp", "intermediate level", "khan kang", "noun", "giao_duc", "ຫຼັກສູດຂັ້ນກາງ", "Giáo trình trung cấp"),
    ("ຂັ້ນສູງ", "trình độ nâng cao / cao cấp", "advanced level", "khan soong", "noun", "giao_duc", "ການຝຶກອົບຮົມຂັ້ນສູງ", "Đào tạo nâng cao"),

    # --- 2. THỜI GIAN, CÁC BUỔI & CÁC NGÀY TRONG TUẦN (TIME & DAYS) ---
    ("ຕອນເຊົ້າໆ", "sáng sớm tinh mơ", "early morning", "ton sao sao", "adv", "thoi_gian", "ຕື່ນແຕ່ຕອນເຊົ້າໆ", "Dậy từ lúc sáng sớm"),
    ("ຕອນສວາຍໆ", "giữa trưa đứng bóng", "midday / noon", "ton suay suay", "adv", "thoi_gian", "ຕອນສວາຍໆແດດຮ້ອນ", "Buổi trưa nắng gắt"),
    ("ຕອນບ່າຍໆ", "xế chiều", "late afternoon", "ton bai bai", "adv", "thoi_gian", "ພົບກັນຕອນບ່າຍໆ", "Gặp nhau lúc xế chiều"),
    ("ຕອນຫົວຄ່ຳ", "chập tối lúc lên đèn", "dusk / twilight", "ton hua kham", "adv", "thoi_gian", "ຕອນຫົວຄ່ຳເປີດໄຟ", "Chập tối bật đèn"),
    ("ຕອນເດິກ", "đêm khuya thanh vắng", "late night", "ton deuk", "adv", "thoi_gian", "ນອນຕອນເດິກ", "Thức khuya ngủ muộn"),
    ("ທ່ຽງຄືນ", "nửa đêm đúng 12 giờ", "midnight (12:00 AM)", "thiang kheun", "noun", "thoi_gian", "ຮອດທ່ຽງຄືນແລ້ວ", "Đã đến nửa đêm rồi"),
    ("ທ່ຽງວັນ", "giữa trưa đúng 12 giờ", "noon (12:00 PM)", "thiang van", "noun", "thoi_gian", "ກິນເຂົ້າຕອນທ່ຽງວັນ", "Ăn cơm trưa lúc 12 giờ"),
    ("ໂມງເຄິ່ງ", "rưỡi (30 phút)", "half past / thirty", "mong khoerng", "noun", "thoi_gian", "ແປດໂມງເຄິ່ງ", "Tám giờ rưỡi"),
    ("ເຄິ່ງຊົ່ວໂມງ", "nửa tiếng đồng hồ", "half an hour", "khoerng xua mong", "noun", "thoi_gian", "ລໍຖ້າເຄິ່ງຊົ່ວໂມງ", "Chờ nửa tiếng đồng hồ"),
    ("ວັນທຳມະດາ", "ngày làm việc bình thường", "weekday", "van tham ma da", "noun", "thoi_gian", "ເຮັດວຽກວັນທຳມະດາ", "Làm việc ngày thường"),
    ("ວັນພັກທ້າຍອາທິດ", "kỳ nghỉ cuối tuần thứ 7 - chủ nhật", "weekend", "van phak thai ar thid", "noun", "thoi_gian", "ພັກຜ່ອນວັນພັກທ້າຍອາທິດ", "Nghỉ ngơi ngày cuối tuần"),
    ("ວັນພັກລັດຖະການ", "ngày nghỉ lễ chính thức của nhà nước", "official public holiday", "van phak lat tha kan", "noun", "thoi_gian", "ວັນພັກລັດຖະການແຫ່ງຊາດ", "Nghỉ lễ công quyền"),
    ("ວັນຊາດ", "ngày Quốc khánh nước CHDCND Lào (2/12)", "National Day", "van xad", "noun", "le_hoi", "ສະເຫຼີມສະຫຼອງວັນຊາດ", "Kỷ niệm ngày Quốc khánh"),
    ("ວັນຄູ", "ngày Nhà giáo tri ân thầy cô", "Teacher's Day", "van khoo", "noun", "le_hoi", "ອວຍພອນວັນຄູ", "Chúc mừng ngày Nhà giáo"),
    ("ວັນແມ່ຍິງ", "ngày Quốc tế Phụ nữ", "Women's Day", "van mae ying", "noun", "le_hoi", "ມອບດອກໄມ້ວັນແມ່ຍິງ", "Tặng hoa ngày Phụ nữ"),

    # --- 3. ĐỘNG VẬT, CÔN TRÙNG & THẾ GIỚI TỰ NHIÊN (FAUNA & NATURE) ---
    ("ນົກ", "con chim trên trời", "bird", "nok", "noun", "dong_vat", "ນົກບິນເທິງຟ້າ", "Chim bay lượn trên trời"),
    ("ນົກເຂົາ", "chim bồ câu bồ nông", "dove / pigeon", "nok khao", "noun", "dong_vat", "ນົກເຂົາສັນຕິພາບ", "Bồ câu biểu tượng hòa bình"),
    ("ນົກຍູງ", "con công xòe đuôi", "peacock", "nok yoong", "noun", "dong_vat", "ນົກຍູງລຳແພນ", "Công xòe cánh múa"),
    ("ນົກອິນຊີ", "chim đại bàng dũng mãnh", "eagle", "nok in see", "noun", "dong_vat", "ນົກອິນຊີຕາແຫຼມ", "Đại bàng mắt sắc như dao"),
    ("ເປັດ", "con vịt bơi dưới ao", "duck", "ped", "noun", "dong_vat", "ລ້ຽງເປັດ", "Nuôi vịt lấy trứng"),
    ("ໄກ່", "con gà trống mái", "chicken", "kai", "noun", "dong_vat", "ໄກ່ຂັນຍາມເຊົ້າ", "Gà gáy sáng"),
    ("ໝູ", "con lợn / heo", "pig / swine", "moo", "noun", "dong_vat", "ລ້ຽງໝູໃນຄອກ", "Nuôi lợn trong chuồng"),
    ("ແບ້", "con dê núi", "goat", "bae", "noun", "dong_vat", "ແບ້ກິນຫຍ້າ", "Dê gặm cỏ trên đồi"),
    ("ແກະ", "con cừu lông trắng", "sheep", "kae", "noun", "dong_vat", "ຂົນແກະນຸ່ມ", "Lông cừu êm ấm"),
    ("ກວາງ", "con hươu / nai rừng", "deer", "kuang", "noun", "dong_vat", "ກວາງແລ່ນໃນປ່າ", "Hươu chạy trong rừng"),
    ("ກະຕ່າຍ", "con thỏ ngọc trắng", "rabbit / hare", "ka tai", "noun", "dong_vat", "ກະຕ່າຍກິນຜັກກາດ", "Thỏ ăn bắp cải"),
    ("ກະຮອກ", "con sóc chuyền cành", "squirrel", "ka hok", "noun", "dong_vat", "ກະຮອກປີນຕົ້ນໄມ້", "Sóc thoăn thoắt chuyền cành"),
    ("ເຈຍ", "con dơi bay đêm", "bat", "jia", "noun", "dong_vat", "ເຈຍຢູ່ໃນຖ້ຳ", "Dơi làm tổ trong hang"),
    ("ຈິ້ງຈົກ", "con thằn lằn / thạch sùng", "gecko / lizard", "jing jok", "noun", "dong_vat", "ຈິ້ງຈົກຕິດຝາ", "Thằn lằn bám trên tường"),
    ("ກັບແກ້", "con tắc kè hoa kêu to", "tokay gecko", "kap kae", "noun", "dong_vat", "ກັບແກ້ຮ້ອງ", "Tắc kè kêu đêm"),
    ("ປານິນ", "con cá rô phi", "tilapia fish", "pa nin", "noun", "dong_vat", "ປານິນປິ້ງ", "Cá rô phi nướng mỡ hành"),
    ("ປາດຸກ", "con cá trê sông", "catfish", "pa dook", "noun", "dong_vat", "ປາດຸກຍ່າງ", "Cá trê nướng rơm"),
    ("ປາຄໍ່", "con cá quả / cá chuối / cá lóc", "snakehead fish", "pa khor", "noun", "dong_vat", "ຕົ້ມສົ້ມປາຄໍ່", "Canh chua cá lóc"),
    ("ປາແຊວມອນ", "cá hồi đại dương", "salmon", "pa sal mon", "noun", "dong_vat", "ກິນປາແຊວມອນ", "Ăn cá hồi fillet"),
    ("ປາສະຫຼາມ", "cá mập hung dữ", "shark", "pa sa lam", "noun", "dong_vat", "ປາສະຫຼາມໃນທະເລ", "Cá mập ngoài đại dương"),
    ("ປາວານ", "cá voi khổng lồ", "whale", "pa van", "noun", "dong_vat", "ປາວານໃຫຍ່", "Cá voi xanh khổng lồ"),
    ("ປາໂລມາ", "cá heo thân thiện", "dolphin", "pa loh ma", "noun", "dong_vat", "ປາໂລມາສະຫຼາດ", "Cá heo rất thông minh"),
    ("ແມງມຸມ", "con nhện giăng tơ", "spider", "maeng moom", "noun", "dong_vat", "ແມງມຸມຊັກໃຍ", "Nhện chăng tơ bắt mồi"),
    ("ຂີ້ເຂັບ", "con rết độc", "centipede", "khee khep", "noun", "dong_vat", "ລະວັງຂີ້ເຂັບຕອດ", "Cẩn thận rết cắn"),
    ("ແມງງອດ", "con bọ cạp đuôi cong", "scorpion", "maeng ngod", "noun", "dong_vat", "ແມງງອດມີພິດ", "Bọ cạp có nọc độc"),
    ("ປວກ", "con mối mọt gỗ", "termite", "puak", "noun", "dong_vat", "ປວກກິນໄມ້", "Mối ăn rỗng thanh gỗ"),

    # --- 4. THIÊN NHIÊN, VŨ TRỤ & ĐỊA LÝ (UNIVERSE & GEOGRAPHY) ---
    ("ດວງອາທິດ", "mặt trời chói chang", "sun", "duang ar thid", "noun", "vu_tru", "ດວງອາທິດສ່ອງແສງ", "Mặt trời tỏa ánh nắng rạng rỡ"),
    ("ດວງຈັນ", "mặt trăng tròn vằng vặc", "moon", "duang jan", "noun", "vu_tru", "ດວງຈັນວັນເພັງ", "Mặt trăng ngày rằm"),
    ("ດວງດາວ", "ngôi sao lấp lánh", "star", "duang dao", "noun", "vu_tru", "ດວງດາວເຕັມທ້ອງຟ້າ", "Muôn vì sao sáng ngập trời"),
    ("ທ້ອງຟ້າ", "bầu trời bao la", "sky", "thong fa", "noun", "vu_tru", "ທ້ອງຟ້າແຈ່ມໃສ", "Bầu trời trong xanh khoáng đạt"),
    ("ຂອບຟ້າ", "đường chân trời xa xôi", "horizon", "khob fa", "noun", "vu_tru", "ແນມເບິ່ງຂອບຟ້າ", "Dõi mắt nhìn về phía chân trời"),
    ("ເມກ", "đám mây trôi bồng bềnh", "cloud", "mek", "noun", "tu_nhien", "ເມກສີຂາວ", "Những đám mây trắng xốp"),
    ("ນ້ຳຄ້າງ", "hạt sương đêm đọng trên lá", "dew", "nam khang", "noun", "tu_nhien", "ນ້ຳຄ້າງຍາມເຊົ້າ", "Hạt sương mai tinh khôi"),
    ("ຫິມະ", "tuyết trắng rơi", "snow", "hi ma", "noun", "thoi_tiet", "ຫິມະຕົກ", "Tuyết rơi mùa đông"),
    ("ລົມບ້າໝູ", "cơn lốc xoáy cuồng phong", "tornado / whirlwind", "lom ba moo", "noun", "thoi_tiet", "ລົມບ້າໝູພັດ", "Lốc xoáy dữ dội quét qua"),
    ("ພູເຂົາໄຟ", "ngọn núi lửa phun trào", "volcano", "phoo khao fai", "noun", "dia_ly", "ພູເຂົາໄຟລະເບີດ", "Núi lửa phun trào nham thạch"),
    ("ແຜ່ນດິນໄຫວ", "trận động đất rung chuyển", "earthquake", "phaen din vai", "noun", "dia_ly", "ເກີດແຜ່ນດິນໄຫວ", "Xảy ra cơn địa chấn động đất"),
    ("ຄື້ນສຸນາມິ", "sóng thần khổng lồ", "tsunami", "kheun su na mi", "noun", "dia_ly", "ໄພພິບັດຄື້ນສຸນາມິ", "Thảm họa sóng thần"),
    ("ມະຫາສະໝຸດ", "đại dương mênh mông", "ocean", "ma ha sa mood", "noun", "dia_ly", "ມະຫາສະໝຸດປາຊີຟິກ", "Thái Bình Dương mênh mông"),
    ("ທະເລ", "biển cả", "sea", "tha lay", "noun", "dia_ly", "ໄປທ່ຽວທະເລ", "Đi nghỉ mát bãi biển"),
    ("ອ່າວ", "vịnh biển kín gió", "bay / gulf", "ao", "noun", "dia_ly", "ອ່າວທະເລງາມ", "Vịnh biển tuyệt đẹp"),
    ("ເກາະ", "hòn đảo giữa sông/biển", "island", "kor", "noun", "dia_ly", "ເກາະດອນໃນແມ່ນ້ຳຂອງ", "Cù lao giữa dòng sông Mê Kông"),
    ("ແຫຼມ", "mũi đất / bán đảo nhô ra", "peninsula / cape", "laem", "noun", "dia_ly", "ແຫຼມອິນດູຈີນ", "Bán đảo Đông Dương"),
    ("ນ້ຳພຸຮ້ອນ", "suối nước khoáng nóng", "hot spring", "nam phoo hon", "noun", "du_lich", "ອາບນ້ຳພຸຮ້ອນ", "Tắm suối khoáng nóng"),
    ("ຫ້ວຍນ້ຳ", "con suối nhỏ róc rách", "stream / creek", "huay nam", "noun", "tu_nhien", "ສຽງຫ້ວຍນ້ຳໄຫຼ", "Tiếng suối róc rách"),
    ("ໜອງນ້ຳ", "ao đầm nước ngọt", "pond / pool", "nong nam", "noun", "tu_nhien", "ໜອງນ້ຳບົວ", "Ao sen ngát hương"),
    ("ບຶງ", "đầm lầy ngập nước", "swamp / marsh", "beung", "noun", "tu_nhien", "ບຶງທາດຫຼວງ", "Đầm That Luang Viêng Chăn"),
    ("ທະເລສາບ", "hồ nước ngọt tự nhiên lớn", "lake", "tha lay sab", "noun", "dia_ly", "ທະເລສາບນ້ຳງື່ມ", "Hồ thủy điện Nam Ngum"),
    ("ປ່າດົງ", "rừng rậm nhiệt đới hoang sơ", "jungle / tropical rainforest", "pa dong", "noun", "tu_nhien", "ປ່າດົງດິບ", "Khu rừng nguyên sinh"),
    ("ປ່າສະຫງວນ", "khu bảo tồn thiên nhiên quốc gia", "national protected forest", "pa sa nguan", "noun", "tu_nhien", "ປ່າສະຫງວນແຫ່ງຊາດພູເຂົາຄວາຍ", "Vườn quốc gia Phou Khao Khouay"),

    # --- 5. VẬT DỤNG SINH HOẠT, DỤNG CỤ HỌC TẬP & NHÀ BẾP (UTENSILS & STATIONERY) ---
    ("ກະຕ່າ", "cái rổ / giỏ mây tre đan", "basket", "ka ta", "noun", "do_dung", "ກະຕ່າໃສ່ເຄື່ອງ", "Giỏ đựng hoa quả"),
    ("ຖັງ", "cái xô / thùng chứa", "bucket / bin", "thang", "noun", "do_dung", "ຖັງນ້ຳ", "Thùng đựng nước"),
    ("ຖັງຂີ້ເຫຍື້ອ", "thùng chứa rác thải", "trash can / dustbin", "thang khee yua", "noun", "do_dung", "ຖິ້ມຂີ້ເຫຍື້ອໃສ່ຖັງ", "Vứt rác vào thùng"),
    ("ຂີ້ເຫຍື້ອ", "rác rưởi phế thải", "garbage / trash", "khee yua", "noun", "do_dung", "ເກັບຂີ້ເຫຍື້ອ", "Thu gom rác"),
    ("ຟອຍກວາດເຮືອນ", "cây chổi đót quét nhà", "broom", "foy kuat heuan", "noun", "do_dung", "ຈັບຟອຍກວາດເຮືອນ", "Cầm chổi quét sạch nhà"),
    ("ໄມ້ຖູພື້ນ", "cây lau sàn nhà", "mop", "mai thoo pheun", "noun", "do_dung", "ຊັກໄມ້ຖູພື້ນ", "Giặt cây lau nhà"),
    ("ຄຸ", "cái xô múc nước xách tay", "pail / water bucket", "khoo", "noun", "do_dung", "ຄຸນ້ຳ", "Xô nước sinh hoạt"),
    ("ຂັນ", "cái ca / gáo múc nước tắm", "dipper / bowl", "khan", "noun", "do_dung", "ຂັນຕັກນ້ຳ", "Ca múc nước dội mát"),
    ("ກະເປົາເດີນທາງ", "va li hành lý du lịch", "travel suitcase / luggage", "ka pao dern thang", "noun", "do_dung", "ຈັດກະເປົາເດີນທາງ", "Sắp xếp va li du lịch"),
    ("ກະແຈລົດ", "chìa khóa xe máy / ô tô", "car/bike key", "ka jae lod", "noun", "do_dung", "ກະແຈລົດຈັກ", "Chìa khóa xe gắn máy"),
    ("ໂຄມໄຟ", "đèn chụp để bàn / lồng đèn", "desk lamp / lantern", "khom fai", "noun", "do_dung", "ເປີດໂຄມໄຟອ່ານປຶ້ມ", "Bật đèn bàn đọc sách"),
    ("ສາຍໄຟ", "dây dẫn điện", "electric wire", "sai fai", "noun", "do_dung", "ສາຍໄຟປອດໄພ", "Dây điện an toàn"),
    ("ປລັກໄຟ", "ổ cắm điện / phích cắm", "power plug / socket", "pluk fai", "noun", "do_dung", "ສຽບປລັກໄຟ", "Cắm phích vào ổ điện"),
    ("ສະວິດໄຟ", "công tắc bật tắt đèn", "light switch", "sa vit fai", "noun", "do_dung", "ກົດສະວິດໄຟ", "Bấm công tắc đèn"),
    ("ເຂ็ม", "cây kim may vá", "needle", "khem", "noun", "do_dung", "ສົ້ນເຂ็ม", "Đầu mũi kim"),
    ("ດ້າຍ", "cuộn chỉ may vá", "thread / yarn", "dai", "noun", "do_dung", "ດ້າຍຫຍິບເຄື່ອງ", "Chỉ khâu áo quần"),
    ("ມີດຕັດ", "cái kéo cắt giấy / vải", "scissors", "meed tad", "noun", "do_dung", "ມີດຕັດແຫຼມ", "Cây kéo sắc ngọt"),
    ("ເທບກາວ", "cuộn băng dính dán", "adhesive tape", "thep kao", "noun", "do_dung", "ຕິດເທບກາວ", "Dán băng dính lại"),
    ("ກາວ", "keo dán dính", "glue", "kao", "noun", "do_dung", "ທາກາວ", "Bôi keo dán giấy"),
    ("ເຈ້ຍ", "tờ giấy trắng", "paper", "jia", "noun", "van_phong", "ເຈ້ຍຂຽນໜັງສື", "Tờ giấy viết bài"),
    ("ປາກກາ", "cây bút bi / bút mực", "pen", "pak ka", "noun", "van_phong", "ປາກກາສີຟ້າ", "Bút bi xanh"),
    ("ສໍດຳ", "cây bút chì gỗ", "pencil", "sor dam", "noun", "van_phong", "ເຫຼົາສໍດຳ", "Gọt bút chì nhọn"),
    ("ຢາງລຶບ", "cục tẩy gôm bút chì", "eraser / rubber", "yang leub", "noun", "van_phong", "ລຶບດ້ວຍຢາງລຶບ", "Tẩy bằng cục gôm"),
    ("ໄມ້ບັນທັດ", "cây thước kẻ đo ly", "ruler", "mai ban thad", "noun", "van_phong", "ຂີດເສັ້ນດ້ວຍໄມ້ບັນທັດ", "Kẻ đường thẳng bằng thước"),
    ("ນ້ຳມຶກ", "lọ mực viết", "ink", "nam meuk", "noun", "van_phong", "ນ້ຳມຶກສີດຳ", "Lọ mực màu đen"),
    ("ປຶ້ມບັນທຶກ", "sổ tay ghi chép nhật ký", "notebook / diary", "peum ban theuk", "noun", "van_phong", "ຈົດໃສ່ປຶ້ມບັນທຶກ", "Ghi vào cuốn sổ tay"),
    ("ປະຕິທິນ", "cuốn lịch để bàn / treo tường", "calendar", "pa ti thin", "noun", "van_phong", "ເບິ່ງວັນທີໃນປະຕິທິນ", "Xem ngày trên lịch"),

    # --- 6. MẪU CÂU GIAO TIẾP VÀ KHẨU NGỮ HÀNG NGÀY (DAILY PHRASES & COLLOQUIAL) ---
    ("ບໍ່ມີບັນຫາເລີຍ", "hoàn toàn không có vấn đề gì cả", "no problem at all", "bor mee ban ha loey", "phrase", "giao_tiep", "ເລື່ອງນີ້ບໍ່ມີບັນຫາເລີຍ", "Việc này không có vấn đề gì cả"),
    ("ແລ້ວແຕ່ເຈົ້າ", "tùy bạn / do bạn quyết định đấy", "it's up to you", "laew tae jao", "phrase", "giao_tiep", "ກິນຫຍັງກໍໄດ້ ແລ້ວແຕ່ເຈົ້າ", "Ăn gì cũng được, tùy bạn đấy"),
    ("ຕາມສະບາຍ", "cứ tự nhiên / thoải mái nhé", "make yourself at home", "tam sa bai", "phrase", "giao_tiep", "ເຊີນນັ່ງຕາມສະບາຍເດີ້", "Mời ngồi chơi tự nhiên nhé"),
    ("ຢ່າຄິດຫຼາຍ", "đừng nghĩ ngợi nhiều / đừng bận tâm", "don't overthink", "ya khid lai", "phrase", "giao_tiep", "ຢ່າຄິດຫຼາຍ ບໍ່ເປັນຫຍັງດອກ", "Đừng nghĩ nhiều, không sao đâu"),
    ("ຂໍໃຫ້ສຸຂະພາບແຂງແຮງ", "chúc dồi dào sức khỏe", "wish you good health", "kho hai soo kha phap khaeng haeng", "phrase", "chuc_mung", "ຂໍໃຫ້ສຸຂະພາບແຂງແຮງຕະຫຼອດປີ", "Chúc sức khỏe dồi dào cả năm"),
    ("ຂໍໃຫ້ມີຄວາມສຸກ", "chúc luôn ngập tràn niềm vui hạnh phúc", "wish you happiness", "kho hai mee khuam sook", "phrase", "chuc_mung", "ຂໍໃຫ້ມີຄວາມສຸກຫຼາຍໆ", "Chúc bạn nhiều niềm vui hạnh phúc"),
    ("ເດີນທາງໂດຍສະຫວັດດີພາບ", "thượng lộ bình an / đi đường bình an", "have a safe journey", "dern thang doy sa vat dee phap", "phrase", "chuc_mung", "ຂໍໃຫ້ເດີນທາງໂດຍສະຫວັດດີພາບ", "Chúc bạn thượng lộ bình an"),
    ("ຍິນດີທີ່ໄດ້ຊ່ວຍ", "rất vinh hạnh được giúp đỡ bạn", "my pleasure to help", "yin dee thee dai suay", "phrase", "giao_tiep", "ບໍ່ເປັນຫຍັງ ຍິນດີທີ່ໄດ້ຊ່ວຍ", "Không có chi, rất vui được giúp bạn"),
    ("ຮັກເຈົ້າຫຼາຍ", "yêu thương bạn rất nhiều", "love you so much", "hak jao lai", "phrase", "cam_xuc", "ຂ້ອຍຮັກເຈົ້າຫຼາຍເດີ້", "Tôi thương yêu bạn nhiều lắm đấy"),
    ("ຄິດຮອດຫຼາຍ", "nhớ nhung da diết rất nhiều", "miss you so much", "khid hod lai", "phrase", "cam_xuc", "ຄິດຮອດຫຼາຍເດີ້ເພື່ອນ", "Nhớ bạn nhiều lắm người bạn ơi"),
    ("ຢູ່ດີມີແຮງ", "chúc mạnh khỏe an khang", "stay healthy and well", "yoo dee mee haeng", "phrase", "chuc_mung", "ຂໍໃຫ້ຢູ່ດີມີແຮງເດີ້", "Chúc bác mạnh giỏi bình an nhé"),
    ("ໄປໃສມານໍ", "đi đâu về đấy bạn ơi", "where have you been?", "pai sai ma nor", "phrase", "giao_tiep", "ສະບາຍດີ ໄປໃສມານໍ", "Chào bạn, đi đâu về thế?"),
    ("ສະບາຍດີບໍ່", "bạn có khỏe không", "how are you?", "sa bai dee bor", "phrase", "giao_tiep", "ສະບາຍດີບໍ່ ສະບາຍດີ", "Bạn khỏe không? Tôi khỏe"),
    ("ເວົ້າອີກເທື່ອໜຶ່ງແດ່", "xin hãy nói lại một lần nữa", "please say it again", "vao eek theua neung dae", "phrase", "giao_tiep", "ກະລຸນາເວົ້າອີກເທື່ອໜຶ່ງແດ່", "Làm ơn nhắc lại giùm một lần nữa"),
    ("ຂ້ອຍບໍ່ເຂົ້າໃຈ", "tôi không hiểu ý bạn", "I don't understand", "khoy bor khao jai", "phrase", "giao_tiep", "ຂໍໂທດ ຂ້ອຍບໍ່ເຂົ້າໃຈ", "Xin lỗi, tôi chưa hiểu rõ"),
    ("ຊ່ວຍແປໃຫ້ແດ່", "làm ơn dịch giúp tôi với", "please translate for me", "suay pae hai dae", "phrase", "giao_tiep", "ຄຳນີ້ຊ່ວຍແປໃຫ້ແດ່", "Từ này xin dịch giúp tôi với"),
    ("ອັນນີ້ພາສາລາວເອີ້ນວ່າແນວໃດ", "cái này tiếng Lào gọi là gì?", "what is this called in Lao?", "an nee pha sa lao oern va naew dai", "phrase", "giao_tiep", "ອັນນີ້ພາສາລາວເອີ້ນວ່າແນວໃດນໍ", "Cái này trong tiếng Lào gọi là gì nhỉ?"),
    ("ອ່ານວ່າແນວໃດ", "từ này đọc phát âm thế nào?", "how to pronounce this?", "an va naew dai", "phrase", "giao_tiep", "ຄຳສັບນີ້ອ່ານວ່າແນວໃດ", "Từ vựng này đọc như thế nào?"),
]

def main():
    print("=" * 70)
    print("🚀 BÙNG NỔ KHO TỪ ĐIỂN TIẾNG LÀO: CỘT MỐC 2500 - 3000 TỪ (PART 4)")
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
    for item in BATCH_PART4:
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
    print(f"[+] QUY MÔ CHÍNH THỨC HIỆN TẠI CỦA BỘ TỪ ĐIỂN: {len(existing_rows)} MỤC TỪ CHUẨN NFC.")
    print("=" * 70)

if __name__ == "__main__":
    main()
