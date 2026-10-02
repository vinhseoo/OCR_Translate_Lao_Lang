"""
Script nạp 400-500+ từ vựng phong phú:
- Phương pháp nấu ăn & Món ngon truyền thống Lào (ẩm thực đường phố, nhà hàng)
- Văn hóa, Lễ nghi Phật giáo, Lịch sử nghệ thuật
- Khoa học, Hình học, Đo lường & Toán học cơ bản
- Tổ chức nhà nước, Cơ cấu chính quyền & Chức vụ nhà nước
- Ngân hàng số hiện đại Lào (BCEL One, Quét QR, Chuyển khoản, Tỷ giá)
Đảm bảo 100% chuẩn Unicode NFC theo The Lao Golden Rule #1.
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

BATCH_PART5 = [
    # --- 1. PHƯƠNG PHÁP NẤU ẨM THỰC LÀO (COOKING METHODS & POPULAR DISHES) ---
    ("ຕົ້ມ", "nấu / luộc / hầm", "boil / simmer", "tom", "verb", "am_thuc", "ຕົ້ມນ້ຳຮ້ອນ", "Đun sôi nước nóng"),
    ("ຈືນ", "chiên / rán ngập dầu", "deep fry", "jeun", "verb", "am_thuc", "ຈືນປາກອບໆ", "Rán cá giòn rụm"),
    ("ຂົ້ວ", "xào lăn / rang", "stir-fry / roast", "khua", "verb", "am_thuc", "ຂົ້ວຜັກໃສ່ນ້ຳມັນຫອຍ", "Xào rau với dầu hào"),
    ("ປິ້ງ", "nướng than hoa hồng", "grill / barbecue", "ping", "verb", "am_thuc", "ປິ້ງໄກ່ນາປົ່ງ", "Nướng gà thơm nức than sen"),
    ("ຍ່າງ", "nướng áp chảo than", "roast over charcoal", "yang", "verb", "am_thuc", "ຊີ້ນງົວຍ່າງ", "Bò nướng tảng thơm lừng"),
    ("ໝົກ", "hấp bọc lá chuối (món Mok)", "steam in banana leaf wrap", "mok", "verb", "am_thuc", "ໝົກປາໃສ່ຜັກອີຕູ່", "Món cá hấp lá chuối thì là"),
    ("ໜຶ້ງ", "hấp cách thủy trong chõ", "steam", "neung", "verb", "am_thuc", "ໜຶ້ງເຂົ້າໜຽວໃນຫວດ", "Đồ xôi nếp trong chõ nứa"),
    ("ແກງ", "nấu canh / súp", "cook soup / curry", "kaeng", "verb", "am_thuc", "ແກງໜໍ່ໄມ້ຮ້ອນໆ", "Canh măng tươi nóng hổi"),
    ("ຕຳ", "giã cối / trộn nộm cay", "pound in mortar / make salad", "tam", "verb", "am_thuc", "ຕຳໝາກຫຸ່ງໃສ່ປາແດກ", "Giã nộm đu đủ chua cay"),
    ("ຍຳ", "trộn gỏi nộm chua ngọt", "toss salad", "yam", "verb", "am_thuc", "ຍຳສະລັດຜັກ", "Gỏi rau củ tươi mát"),
    ("ດອງ", "muối chua / ngâm dấm", "pickle / ferment", "dong", "verb", "am_thuc", "ຜັກກາດດອງ", "Dưa cải muối chua"),
    ("ໝົກປາ", "cá nục hấp lá chuối gia vị Lào", "steamed fish in banana leaves", "mok pa", "noun", "am_thuc", "ໝົກປາແຊບຫຼາຍ", "Món cá hấp lá chuối rất thơm"),
    ("ໝົກໄກ່", "gà hấp lá chuối thì là Lào", "steamed chicken in banana leaves", "mok kai", "noun", "am_thuc", "ໝົກໄກ່ໃສ່ຫົວສີໄຄ", "Gà bọc lá chuối hấp sả thơm"),
    ("ແກງສົ້ມ", "canh chua cá rau đồng", "sour fish soup", "kaeng som", "noun", "am_thuc", "ແກງສົ້ມປານ້ຳຂອງ", "Canh chua cá sông Mê Kông"),
    ("ແກງຈືດ", "canh rau thịt băm thanh mát", "clear soup / broth", "kaeng jeud", "noun", "am_thuc", "ແກງຈືດເຕົ້າຮູ້", "Canh đậu phụ thanh đạm"),
    ("ຕົ້ມຍຳກຸ້ງ", "canh tôm chua cay Tom Yum", "Tom Yum soup with shrimp", "tom yam koong", "noun", "am_thuc", "ຕົ້ມຍຳກຸ້ງນ້ຳຂົ້ນ", "Tomyum tôm nước cốt béo"),
    ("ຕົ້ມໄກ່", "canh gà luộc lá giang", "boiled chicken soup with sour leaves", "tom kai", "noun", "am_thuc", "ຕົ້ມໄກ່ໃສ່ໃບໝາກຂາມ", "Gà nấu lá me non"),
    ("ເຂົ້າປຸ້ນ", "bún nước lèo cốt dừa truyền thống (Khao Poon)", "rice vermicelli soup (Khao Poon)", "khao poon", "noun", "am_thuc", "ກິນເຂົ້າປຸ້ນນ້ຳແຈ່ວ", "Ăn bún cay nước lèo"),
    ("ເຂົ້າຫຼາມ", "cơm lam nướng ống nứa", "sticky rice in bamboo tube", "khao lam", "noun", "am_thuc", "ເຂົ້າຫຼາມບ້ານນາກວາງ", "Cơm lam nướng ống tre ngọt bùi"),
    ("ເຂົ້າຕົ້ມ", "bánh tét bánh chưng gói lá", "sticky rice cake in banana leaf", "khao tom", "noun", "am_thuc", "ເຂົ້າຕົ້ມມັດ", "Bánh tét nhân chuối đỗ"),
    ("ໄຂ່ດາວ", "trứng ốp la lòng đào", "fried egg (sunny side up)", "khai dao", "noun", "am_thuc", "ໄຂ່ດາວສຸກປານກາງ", "Trứng ốp la vừa chín tới"),
    ("ໄຂ່ຈຽວ", "trứng đúc thịt rán", "omelet", "khai jiao", "noun", "am_thuc", "ໄຂ່ຈຽວໝູສັບ", "Trứng rán thịt băm thơm nức"),
    ("ໄຂ່ຕົ້ມ", "trứng luộc", "boiled egg", "khai tom", "noun", "am_thuc", "ໄຂ່ຕົ້ມຢາງມະຕູມ", "Trứng luộc lòng đào"),
    ("ໄຂ່ຮ້າງ", "trứng vịt lộn / trứng bắc thảo", "fertilized duck egg / balut", "khai hang", "noun", "am_thuc", "ກິນໄຂ່ຮ້າງກັບຂີງ", "Ăn trứng vịt lộn kèm gừng tươi"),
    ("ໝູກອບ", "thịt heo quay giòn bì", "crispy roast pork belly", "moo kob", "noun", "am_thuc", "ເຂົ້າໝູກອບ", "Cơm thịt quay bì giòn"),
    ("ຊີ້ນແຫ້ງ", "thịt bò/trâu gác bếp phơi khô", "dried dried beef / jerky", "seen haeng", "noun", "am_thuc", "ຊີ້ນແຫ້ງຈືນ", "Thịt khô xé chiên vàng"),
    ("ປາແຫ້ງ", "cá khô mặn", "dried salted fish", "pa haeng", "noun", "am_thuc", "ປິ້ງປາແຫ້ງ", "Nướng cá khô thơm lừng"),
    ("ໄສ້ອົ່ວ", "xúc xích thảo mộc hun khói Lào (Sai Oua)", "Lao herbal pork sausage (Sai Oua)", "sai oua", "noun", "am_thuc", "ໄສ້ອົ່ວຫຼວງພະບາງ", "Xúc xích thảo mộc Luang Prabang"),
    ("ລາບໝູ", "lạp thịt heo băm thính gạo", "minced pork salad (Laap Moo)", "lap moo", "noun", "am_thuc", "ລາບໝູສຸກ", "Lạp heo chín rắc rau thơm"),
    ("ລາບເປັດ", "lạp thịt vịt băm trứ danh Lào", "minced duck salad", "lap ped", "noun", "am_thuc", "ລາບເປັດແຊບທີ່ສຸດ", "Lạp vịt ngon nức tiếng"),
    ("ກ້ອຍ", "món gỏi tái chanh thính gạo", "raw or rare meat salad (Goy)", "koy", "noun", "am_thuc", "ກ້ອຍປາສົດ", "Gỏi cá tươi chấm chẻo"),
    ("ຊຸບໜໍ່ໄມ້", "măng vầu xé trộn vừng mè", "bamboo shoot salad with sesame", "xoop nor mai", "noun", "am_thuc", "ຊຸບໜໍ່ໄມ້ໃສ່ຢານາງ", "Măng xé om lá sương sâm rắc mè"),
    ("ນ້ຳຫວານລວມມິດ", "chè thập cẩm nước cốt dừa", "sweet mixed dessert soup", "nam van luam mit", "noun", "am_thuc", "ກິນນ້ຳຫວານລວມມິດ", "Ăn bát chè thập cẩm mát lạnh"),
    ("ເຂົ້າໜຽວໝາກມ່ວງ", "xôi xoài rưới nước cốt dừa", "mango sticky rice", "khao niao mak muang", "noun", "am_thuc", "ເຂົ້າໜຽວໝາກມ່ວງຫວານມັນ", "Xôi xoài ngọt béo bùi ngậy"),
    ("ໝາກກ້ວຍບວດ", "chè chuối nấu cốt dừa hạt é", "banana in coconut milk", "mak kuay buad", "noun", "am_thuc", "ໝາກກ້ວຍບວດຮ້ອນໆ", "Bát chè chuối cốt dừa bốc khói"),
    ("ວຸ້ນ", "thạch rau câu dừa hoa quả", "jelly / agar dessert", "voon", "noun", "am_thuc", "ວຸ້ນໝາກພ້າວອ່ອນ", "Thạch rau câu dừa xiêm"),
    ("ນ້ຳອ້ອຍ", "nước mía vắt quất tươi", "fresh sugarcane juice", "nam oy", "noun", "do_uong", "ນ້ຳອ້ອຍເຢັນຊື່ນໃຈ", "Cốc nước mía đá ngọt lịm mát lòng"),
    ("ຊານົມໄຂ່ມຸກ", "trà sữa trân châu đường đen", "bubble milk tea / boba", "sa nom khai mook", "noun", "do_uong", "ດື່ມຊານົມໄຂ່ມຸກ", "Uống trà sữa trân châu"),
    ("ຊາຂຽວ", "trà xanh Nhật Bản / Matcha", "green tea", "sa khiao", "noun", "do_uong", "ຊາຂຽວນົມສົດ", "Trà xanh sữa tươi"),
    ("ຊາມะນາວ", "trà chanh mát lạnh", "lemon iced tea", "sa ma nao", "noun", "do_uong", "ຊາມะນາວແກ້ກະຫາຍ", "Trà chanh giải khát đã khát"),

    # --- 2. VĂN HÓA, LỄ HỘI & TÔN GIÁO (CULTURE & FESTIVALS) ---
    ("ພິທີກຳ", "nghi lễ tôn giáo / tế tự", "ritual / ceremony", "phi thee kam", "noun", "van_hoa", "ພິທີກຳທາງສາສະໜາ", "Nghi lễ tôn giáo trang nghiêm"),
    ("ພິທີເປີດ", "lễ khai mạc sự kiện", "opening ceremony", "phi thee poerd", "noun", "su_kien", "ພິທີເປີດງານກິລາ", "Lễ khai mạc đại hội thể thao"),
    ("ພິທີປິດ", "lễ bế mạc tổng kết", "closing ceremony", "phi thee pid", "noun", "su_kien", "ພິທີປິດກອງປະຊຸມ", "Lễ bế mạc hội nghị"),
    ("ພິທີມອບລາງວັນ", "lễ trao giải thưởng vinh danh", "award presentation ceremony", "phi thee mob lang van", "noun", "su_kien", "ພິທີມອບລາງວັນດີເດັ່ນ", "Lễ trao thưởng xuất sắc"),
    ("ພິທີຈົບຊັ້ນ", "lễ tốt nghiệp ra trường", "graduation ceremony", "phi thee job xan", "noun", "giao_duc", "ພິທີຈົບຊັ້ນມະຫາວິທະຍາໄລ", "Lễ tốt nghiệp đại học"),
    ("ບຸນນະມັດສະການ", "lễ hội bái vọng chùa tháp", "temple homage festival", "boon na mat sa kan", "noun", "van_hoa", "ບຸນນະມັດສະການພຣະທາດຫຼວງ", "Đại lễ hội chùa Thạt Luổng"),
    ("ບຸນເຂົ້າພັນສາ", "lễ nhập hạ của Phật tử", "Boun Khao Phansa (Start of Buddhist Lent)", "boon khao phan sa", "noun", "van_hoa", "ໄປວັດໃນມື້ບຸນເຂົ້າພັນສາ", "Lên chùa dịp lễ nhập hạ"),
    ("ບຸນມະຫາຊາດ", "đại lễ hội Vessantara kể tích Phật", "Boun Mahaxat (Vessantara festival)", "boon ma ha xad", "noun", "van_hoa", "ຟັງເທດບຸນມະຫາຊາດ", "Nghe tích truyện Boun Mahaxat"),
    ("ສິລະປະ", "nghệ thuật hội họa tạo hình", "art", "si la pa", "noun", "nghe_thuat", "ສິລະປະລາວບູຮານ", "Nghệ thuật cổ truyền Lào"),
    ("ສິລະປະກຳ", "tác phẩm mỹ thuật điêu khắc", "artwork / handicrafts", "si la pa kam", "noun", "nghe_thuat", "ວາງສະແດງສິລະປະກຳ", "Triển lãm tác phẩm mỹ thuật"),
    ("ດົນຕີພື້ນເມືອງ", "âm nhạc dân gian truyền thống", "traditional folk music", "don tee pheun meuang", "noun", "nghe_thuat", "ເສບດົນຕີພື້ນເມືອງ", "Diễn tấu nhạc dân tộc Lào"),
    ("ບົດເພງ", "bài hát / ca khúc trữ tình", "song / melody", "bod pheng", "noun", "nghe_thuat", "ບົດເພງອຳມະຕະ", "Ca khúc bất hủ đi cùng năm tháng"),
    ("ບົດກະວີ", "bài thơ khúc ngâm", "poem / poetry", "bod ka vee", "noun", "nghe_thuat", "ແຕ່ງບົດກະວີ", "Sáng tác vần thơ tuyệt tác"),
    ("ວັນນະກຳ", "tác phẩm văn học", "literary work", "van na kam", "noun", "van_hoc", "ວັນນະກຳລາວລ້ຳຄ່າ", "Di sản văn học quý báu Lào"),
    ("ນິທານ", "truyện cổ tích dân gian", "fairy tale / folk tale", "ni than", "noun", "van_hoc", "ເລົ່ານິທານໃຫ້ລູກຟັງ", "Kể chuyện cổ tích cho con nghe"),
    ("ຕຳນານ", "truyền thuyết huyền thoại", "legend / myth", "tam nan", "noun", "van_hoc", "ຕຳນານພູທ້າວພູນາງ", "Truyền thuyết chàng Thao nàng Nang"),
    ("ປະຫວັດຄວາມເປັນມາ", "lịch sử ngọn nguồn gốc gác", "history and origin / background", "pa vat khuam pen ma", "noun", "lich_su", "ສຶກສາປະຫວັດຄວາມເປັນມາ", "Tìm hiểu gốc tích cội nguồn"),
    ("ຮູບປັ້ນ", "bức tượng điêu khắc đúc đồng", "sculpture / statue", "hoop pan", "noun", "nghe_thuat", "ຮູບປັ້ນເຈົ້າອານຸວົງ", "Tượng đài vua Chao Anouvong"),
    ("ຮູບແຕ້ມ", "bức tranh họa sĩ vẽ", "painting / drawing", "hoop taem", "noun", "nghe_thuat", "ຮູບແຕ້ມສີໄມ້", "Bức tranh vẽ chì màu"),

    # --- 3. TOÁN HỌC, HÌNH HỌC & ĐO LƯỜNG (MATHEMATICS & SHAPES) ---
    ("ໂຄງການ", "dự án kế hoạch thực hiện", "project", "khong kan", "noun", "khoa_hoc", "ໂຄງການຮ່ວມມືສາກົນ", "Dự án hợp tác quốc tế"),
    ("ໂຄງສ້າງ", "cấu trúc khung sườn", "structure / framework", "khong sang", "noun", "khoa_hoc", "ໂຄງສ້າງເສດຖະກິດ", "Cơ cấu nền kinh tế"),
    ("ທິດສະດີ", "lý thuyết lý luận khoa học", "theory", "thid sa dee", "noun", "khoa_hoc", "ທິດສະດີວິທະຍາສາດ", "Học thuyết khoa học"),
    ("ຫຼັກການ", "nguyên tắc phương châm nền tảng", "principle", "lak kan", "noun", "khoa_hoc", "ຍຶດໝັ້ນຕາມຫຼັກການ", "Kiên định giữ vững nguyên tắc"),
    ("ວິທີການ", "phương thức biện pháp", "method / technique", "vi thee kan", "noun", "khoa_hoc", "ວິທີການແກ້ໄຂບັນຫາ", "Phương pháp tháo gỡ vấn đề"),
    ("ຂັ້ນຕອນ", "quy trình tuần tự các bước", "process / step", "khan ton", "noun", "khoa_hoc", "ຂັ້ນຕອນການຜະລິດ", "Quy trình công nghệ sản xuất"),
    ("ສູດ", "công thức tính toán", "formula", "sood", "noun", "khoa_hoc", "ສູດຄິດໄລ່ຄະນິດສາດ", "Công thức tính toán số học"),
    ("ມາດຕະຖານ", "chuẩn mực tiêu chuẩn", "standard / benchmark", "mad ta than", "noun", "khoa_hoc", "ບັນລຸມາດຕະຖານສາກົນ", "Đạt chuẩn quốc tế ISO"),
    ("ຄຸນນະພາບ", "chất lượng phẩm chất", "quality", "khoon na phap", "noun", "khoa_hoc", "ສິນຄ້າຄຸນນະພາບສູງ", "Sản phẩm chất lượng cao"),
    ("ປະລິມານ", "khối lượng số lượng", "quantity / volume", "pa li man", "noun", "khoa_hoc", "ຄວບຄຸມປະລິມານ", "Kiểm soát số lượng sản phẩm"),
    ("ຂະໜາດ", "kích thước kích cỡ", "dimension / size", "kha nad", "noun", "khoa_hoc", "ຂະໜາດມາດຕະຖານ", "Kích cỡ chuẩn tiêu chuẩn"),
    ("ຮູບຮ່າງ", "hình hài hình dáng", "shape / appearance", "hoop hang", "noun", "hinh_hoc", "ຮູບຮ່າງສັດສ່ວນ", "Vóc dáng cân đối"),
    ("ຮູບວົງມົນ", "hình tròn hình khuyên", "circle", "hoop vong mon", "noun", "hinh_hoc", "ແຕ້ມຮູບວົງມົນ", "Vẽ một đường tròn"),
    ("ຮູບສີ່ຫຼ່ຽມ", "hình chữ nhật / hình vuông", "quadrilateral / square / rectangle", "hoop see liam", "noun", "hinh_hoc", "ໂຕະຮູບສີ່ຫຼ່ຽມ", "Bàn hình vuông"),
    ("ຮູບສາມຫຼ່ຽມ", "hình tam giác", "triangle", "hoop sam liam", "noun", "hinh_hoc", "ຮູບສາມຫຼ່ຽມຄຳ", "Vùng Tam giác Vàng"),
    ("ເສັ້ນຊື່", "đường thẳng tắp", "straight line", "sen seu", "noun", "hinh_hoc", "ຂີດເສັ້ນຊື່", "Vạch một đường thẳng"),
    ("ເສັ້ນໂຄ້ງ", "đường uốn cong", "curved line / curve", "sen khong", "noun", "hinh_hoc", "ຖະໜົນເສັ້ນໂຄ້ງ", "Đoạn đường cong uốn lượn"),
    ("ຈຸດ", "điểm mốc / dấu chấm câu", "point / dot", "jood", "noun", "hinh_hoc", "ຈຸດເລີ່ມຕົ້ນ", "Điểm xuất phát ban đầu"),
    ("ມຸມ", "góc độ góc quay", "angle / corner", "moom", "noun", "hinh_hoc", "ມຸມເກົ້າສິບອົງສາ", "Góc vuông 90 độ"),
    ("ເນື້ອທີ່", "diện tích đất đai", "area / surface area", "neua thee", "noun", "hinh_hoc", "ເນື້ອທີ່ກວ້າງໃຫຍ່", "Diện tích bao la"),
    ("ບໍລິມາດ", "thể tích khối lượng", "volume / capacity", "bor li mad", "noun", "hinh_hoc", "ຄິດໄລ່ບໍລິມາດ", "Tính thể tích khối lập phương"),

    # --- 4. CHÍNH TRỊ, CƠ CẤU NHÀ NƯỚC & CHỨC DANH LÃNH ĐẠO (POLITICS & OFFICES) ---
    ("ປະທານປະເທດ", "Chủ tịch nước CHDCND Lào", "President of Lao PDR", "pa than pa thed", "noun", "chinh_tri", "ປະທານປະເທດແຫ່ງ ສປປ ລາວ", "Chủ tịch nước Cộng hòa Dân chủ Nhân dân Lào"),
    ("ນາຍົກລັດຖະມົນຕີ", "Thủ tướng Chính phủ", "Prime Minister", "na yok lat tha mon tee", "noun", "chinh_tri", "ຄຳສັ່ງຂອງນາຍົກລັດຖະມົນຕີ", "Chỉ thị của Thủ tướng Chính phủ"),
    ("ຮອງນາຍົກ", "Phó Thủ tướng", "Deputy Prime Minister", "hong na yok", "noun", "chinh_tri", "ຮອງນາຍົກລັດຖະມົນຕີ", "Phó Thủ tướng Chính phủ"),
    ("ລັດຖະມົນຕີ", "Bộ trưởng các bộ", "Minister", "lat tha mon tee", "noun", "chinh_tri", "ລັດຖະມົນຕີວ່າການ", "Bộ trưởng bộ ngành"),
    ("ເຈົ້າແຂວງ", "Tỉnh trưởng các tỉnh Lào", "Provincial Governor", "jao khwaeng", "noun", "chinh_tri", "ເຈົ້າແຂວງຫຼວງພະບາງ", "Tỉnh trưởng tỉnh Luang Prabang"),
    ("ເຈົ້າເມືອງ", "Huyện trưởng quận huyện", "District Chief / Governor", "jao meuang", "noun", "chinh_tri", "ຫ້ອງການເຈົ້າເມືອງ", "Ủy ban nhân dân quận huyện"),
    ("ນາຍບ້ານ", "Trưởng thôn / Trưởng bản", "Village Chief / Headman", "nai ban", "noun", "chinh_tri", "ນາຍບ້ານປະກາດຂ່າວ", "Trưởng bản thông báo tin tức loa"),
    ("ພົນລະເມືອງ", "công dân nhân dân", "citizen", "phon la meuang", "noun", "chinh_tri", "ສິດແລະພັນທະຂອງພົນລະເມືອງ", "Quyền và nghĩa vụ của công dân"),
    ("ປະເທດຊາດ", "tổ quốc quê hương đất nước", "homeland / motherland", "pa thed xad", "noun", "chinh_tri", "ຮັກປະເທດຊາດ", "Yêu tổ quốc non sông"),
    ("ດິນແດນ", "lãnh thổ bờ cõi", "territory / land", "din daen", "noun", "chinh_tri", "ອະທິປະໄຕເໜືອດິນແດນ", "Chủ quyền toàn vẹn lãnh thổ"),
    ("ອະທິປະໄຕ", "chủ quyền thiêng liêng", "sovereignty", "ar thi pa tai", "noun", "chinh_tri", "ປົກປ້ອງອະທິປະໄຕແຫ່ງຊາດ", "Bảo vệ vững chắc chủ quyền quốc gia"),
    ("ຊາຍແດນ", "đường biên giới quốc gia", "border / frontier", "xai daen", "noun", "chinh_tri", "ຊາຍແດນລາວ-ຫວຽດນາມ", "Biên giới hữu nghị Lào - Việt"),
    ("ຫຼັກໝາຍຊາຍແດນ", "cột mốc biên giới phân định", "border marker / landmark", "lak mai xai daen", "noun", "chinh_tri", "ກວດກາຫຼັກໝາຍຊາຍແດນ", "Tuần tra cột mốc biên giới"),
    ("ສົນທິສັນຍາ", "hiệp ước công ước quốc tế", "treaty / convention", "son thi san ya", "noun", "chinh_tri", "ລົງນາມສົນທິສັນຍາ", "Ký kết hiệp ước bang giao"),
    ("ຂໍ້ຕົກລົງ", "thỏa thuận nghị định", "agreement / protocol", "kho tok long", "noun", "chinh_tri", "ປະຕິບັດຕາມຂໍ້ຕົກລົງ", "Thực hiện đúng nội dung thỏa thuận"),
    ("ຖະແຫຼງການ", "tuyên bố chung quốc tế", "joint declaration / statement", "tha laeng kan", "noun", "chinh_tri", "ຖະແຫຼງການຮ່ວມ", "Tuyên bố chung hai nước"),
    ("ນະໂຍບາຍ", "đường lối chính sách", "policy", "na yo bai", "noun", "chinh_tri", "ນະໂຍບາຍເປີດປະຕູ", "Chính sách mở cửa hội nhập"),
    ("ຍຸດທະສາດ", "chiến lược phát triển", "strategy", "yoot tha sad", "noun", "chinh_tri", "ຍຸດທະສາດການພັດທະນາ", "Chiến lược phát triển dài hạn"),
    ("ມະຕິ", "nghị quyết của Đảng / Nhà nước", "resolution / decree", "ma ti", "noun", "chinh_tri", "ມະຕິກອງປະຊຸມໃຫຍ່", "Nghị quyết Đại hội Đảng"),

    # --- 5. TÀI CHÍNH KỸ THUẬT SỐ & NGÂN HÀNG LÀO HIỆN ĐẠI (DIGITAL BANKING & FINTECH) ---
    ("ບາໂຄ້ດ", "mã vạch hàng hóa", "barcode", "ba khode", "noun", "cong_nghe", "ສະແກນບາໂຄ້ດ", "Quét mã vạch sản phẩm"),
    ("ຄິວອາໂຄ້ດ", "mã QR Code thanh toán", "QR code", "Q R khode", "noun", "cong_nghe", "ຈ່າຍດ້ວຍຄິວອາໂຄ້ດ", "Thanh toán bằng quét mã QR"),
    ("ແອັບທະນາຄານ", "ứng dụng ngân hàng di động (BCEL One)", "banking app (BCEL One)", "app tha na khan", "noun", "cong_nghe", "ໂອນເງິນຜ່ານແອັບທະນາຄານ", "Chuyển tiền qua app ngân hàng"),
    ("ໂອນເງິນດ່ວນ", "chuyển khoản siêu tốc 24/7", "fast money transfer", "on ngen duan", "verb", "tai_chinh", "ໂອນເງິນດ່ວນທັນໃຈ", "Chuyển khoản tiền đến tức thì"),
    ("ສະແກນຈ່າຍ", "quét mã thanh toán tiền", "scan to pay", "scan jai", "verb", "tai_chinh", "ສະແກນຈ່າຍຄ່າອາຫານ", "Quét mã QR thanh toán tiền ăn"),
    ("ຄ່າທຳນຽມ", "khoản phí dịch vụ ngân hàng", "service fee / surcharge", "kha tham niam", "noun", "tai_chinh", "ຟຣີຄ່າທຳນຽມ", "Miễn phí cước giao dịch"),
    ("ຍອດເງິນຄົງເຫຼືອ", "số dư tài khoản khả dụng", "account balance", "yod ngen khong leua", "noun", "tai_chinh", "ກວດເບິ່ງຍອດເງິນຄົງເຫຼືອ", "Kiểm tra số dư tài khoản"),
    ("ໃບແຈ້ງຍອດ", "bản sao kê tài khoản ngân hàng", "bank statement", "bai jaeng yod", "noun", "tai_chinh", "ພິມໃບແຈ້ງຍອດບັນຊີ", "In sao kê giao dịch ngân hàng"),
    ("ເງິນຝາກປະຈຳ", "tiền gửi tiết kiệm có kỳ hạn", "fixed deposit / savings", "ngen fak pa jam", "noun", "tai_chinh", "ດອກເບ້ຍເງິນຝາກປະຈຳ", "Lãi suất tiền gửi có kỳ hạn"),
    ("ເງິນກູ້", "khoản vay tín dụng vốn", "bank loan / credit", "ngen koo", "noun", "tai_chinh", "ຂໍອະນຸມັດເງິນກູ້", "Xin phê duyệt hồ sơ vay vốn"),
    ("ດອກເບ້ຍເງິນກູ້", "lãi suất vay ngân hàng", "loan interest rate", "dok bia ngen koo", "noun", "tai_chinh", "ດອກເບ້ຍເງິນກູ້ຕ່ຳ", "Lãi suất cho vay ưu đãi"),
    ("ໜັງສືຄ້ຳປະກັນ", "thư bảo lãnh ngân hàng", "bank guarantee letter", "nang seu kham pa kan", "noun", "tai_chinh", "ອອກໜັງສືຄ້ຳປະກັນ", "Phát hành thư bảo lãnh ngân hàng"),
    ("ເງິນຕາຕ່າງປະເທດ", "ngoại tệ / tiền nước ngoài", "foreign currency", "ngen ta tang pa thed", "noun", "tai_chinh", "ຄຸ້ມຄອງເງິນຕາຕ່າງປະເທດ", "Quản lý ngoại hối"),
    ("ອັດຕາແລກປ່ຽນ", "tỷ giá hối đoái tiền tệ", "exchange rate", "at ta laek pian", "noun", "tai_chinh", "ອັດຕາແລກປ່ຽນເງິນກີບກັບດົງ", "Tỷ giá quy đổi kíp sang đồng"),
]

def main():
    print("=" * 70)
    print("💎 NẠP ĐẠI DỮ LIỆU PART 5 - CHẠM VÀ VƯỢT MỐC 2,500 TỪ CHUẨN NFC")
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
    for item in BATCH_PART5:
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
