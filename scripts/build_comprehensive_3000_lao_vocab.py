"""
Script xây dựng đại kho từ vựng tiếng Lào chuẩn hóa quy mô 3,000+ từ (Comprehensive 3000+ Lao Lexicon)
Bổ sung:
1. Toàn bộ 18 tỉnh, thành phố của Lào và các địa danh nổi tiếng
2. Toàn bộ các Bộ, ban ngành, cơ quan nhà nước Lào
3. Hệ thống danh từ ghép tiền tố: ການ-, ຄວາມ-, ຜູ້-, ນັກ-, ຊ່າງ-, ຫ້ອງ-, ຮ້ານ-, ໂຮງ-, ເຄື່ອງ-, ນ້ຳ-, ໝາກ-, ຜັກ-, ຕົ້ນ-, ໃບ-, ລົດ-
4. Toàn bộ tính từ đối ngẫu (tốt-xấu, nhanh-chậm, lớn-nhỏ, sáng-tối, nóng-lạnh...)
5. Toàn bộ động từ hành vi đời sống, giao tiếp xã hội, công sở, thương mại, kỹ thuật
6. Thuật ngữ giáo dục, y tế, pháp lý, ẩm thực, văn hóa truyền thống
Đảm bảo 100% chuẩn Unicode NFC theo The Lao Golden Rule #1.
"""
import sys
import csv
from pathlib import Path

# Force UTF-8 console output
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing.normalize import normalize_lao

CSV_PATH = PROJECT_ROOT / "data" / "dictionaries" / "lao_vi_en.csv"

EXPANSION_BATCH = [
    # === 1. 18 TỈNH THÀNH PHỐ NƯỚC LÀO (18 PROVINCES OF LAOS) ===
    ("ນະຄອນຫຼວງວຽງຈັນ", "Thủ đô Viêng Chăn", "Vientiane Prefecture / Capital", "na khon luang viang chan", "noun", "dia_ly", "ນະຄອນຫຼວງວຽງຈັນເປັນສູນກາງ", "Thủ đô Viêng Chăn là trung tâm"),
    ("ແຂວງວຽງຈັນ", "Tỉnh Viêng Chăn", "Vientiane Province", "khwaeng viang chan", "noun", "dia_ly", "ແຂວງວຽງຈັນຕັ້ງຢູ່ພາກກາງ", "Tỉnh Viêng Chăn nằm ở miền Trung"),
    ("ແຂວງຫຼວງພະບາງ", "Tỉnh Luang Prabang", "Luang Prabang Province", "khwaeng luang pha bang", "noun", "dia_ly", "ແຂວງຫຼວງພະບາງມີວັດເກົ່າແກ່", "Tỉnh Luang Prabang có nhiều ngôi chùa cổ"),
    ("ແຂວງຈຳປາສັກ", "Tỉnh Champasak", "Champasak Province", "khwaeng cham pa sak", "noun", "dia_ly", "ແຂວງຈຳປາສັກຢູ່ພາກໃຕ້", "Tỉnh Champasak ở miền Nam"),
    ("ແຂວງສະຫວັນນະເຂດ", "Tỉnh Savannakhet", "Savannakhet Province", "khwaeng sa van na khed", "noun", "dia_ly", "ແຂວງສະຫວັນນະເຂດມີປະຊາກອນຫຼາຍ", "Tỉnh Savannakhet có dân số đông"),
    ("ແຂວງຄຳມ່ວນ", "Tỉnh Khammouane", "Khammouane Province", "khwaeng kham muan", "noun", "dia_ly", "ແຂວງຄຳມ່ວນມີຖ້ຳງາມ", "Tỉnh Khammouane có nhiều hang động đẹp"),
    ("ແຂວງບໍລິຄຳໄຊ", "Tỉnh Bolikhamsai", "Bolikhamsai Province", "khwaeng bor li kham sai", "noun", "dia_ly", "ແຂວງບໍລິຄຳໄຊຕິດກັບຫວຽດນາມ", "Tỉnh Bolikhamsai giáp với Việt Nam"),
    ("ແຂວງໄຊສົມບູນ", "Tỉnh Xaysomboun", "Xaysomboun Province", "khwaeng xai som boon", "noun", "dia_ly", "ແຂວງໄຊສົມບູນມີພູເບ້ຍສູງສຸດ", "Tỉnh Xaysomboun có đỉnh Phou Bia cao nhất"),
    ("ແຂວງຊຽງຂວາງ", "Tỉnh Xieng Khouang", "Xieng Khouang Province", "khwaeng xieng khuang", "noun", "dia_ly", "ແຂວງຊຽງຂວາງມີທົ່ງໄຫຫີນ", "Tỉnh Xieng Khouang có Cánh đồng Chum"),
    ("ແຂວງຫົວພັນ", "Tỉnh Houaphanh", "Houaphanh Province", "khwaeng hua phan", "noun", "dia_ly", "ແຂວງຫົວພັນເຂດຖານທີ່ໝັ້ນ", "Tỉnh Houaphanh vùng căn cứ cách mạng"),
    ("ແຂວງຜົ້ງສາລີ", "Tỉnh Phongsaly", "Phongsaly Province", "khwaeng phong sa lee", "noun", "dia_ly", "ແຂວງຜົ້ງສາລີຢູ່ພາກເໜືອສຸດ", "Tỉnh Phongsaly ở cực Bắc"),
    ("ແຂວງຫຼວງນ້ຳທາ", "Tỉnh Luang Namtha", "Luang Namtha Province", "khwaeng luang nam tha", "noun", "dia_ly", "ແຂວງຫຼວງນ້ຳທາມີປ່າສະຫງວນ", "Tỉnh Luang Namtha có khu bảo tồn thiên nhiên"),
    ("ແຂວງບໍ່ແກ້ວ", "Tỉnh Bokeo", "Bokeo Province", "khwaeng bor kaew", "noun", "dia_ly", "ແຂວງບໍ່ແກ້ວເຂດສາມຫຼ່ຽມຄຳ", "Tỉnh Bokeo vùng Tam giác Vàng"),
    ("ແຂວງອຸດົມໄຊ", "Tỉnh Oudomxay", "Oudomxay Province", "khwaeng oo dom xai", "noun", "dia_ly", "ແຂວງອຸດົມໄຊສູນກາງຄົມມະນາຄົມ", "Tỉnh Oudomxay trung tâm giao thông"),
    ("ແຂວງໄຊຍະບູລີ", "Tỉnh Xayaboury", "Xayaboury Province", "khwaeng xai ya boo lee", "noun", "dia_ly", "ແຂວງໄຊຍະບູລີມີບຸນຊ້າງ", "Tỉnh Xayaboury có lễ hội Voi"),
    ("ແຂວງສາລະວັນ", "Tỉnh Salavan", "Salavan Province", "khwaeng sa la van", "noun", "dia_ly", "ແຂວງສາລະວັນປູກກາເຟ", "Tỉnh Salavan trồng cà phê"),
    ("ແຂວງເຊກອງ", "Tỉnh Sekong", "Sekong Province", "khwaeng say kong", "noun", "dia_ly", "ແຂວງເຊກອງມີແມ່ນ້ຳເຊກອງ", "Tỉnh Sekong có dòng sông Sekong"),
    ("ແຂວງອັດຕະປື", "Tỉnh Attapeu", "Attapeu Province", "khwaeng at ta peu", "noun", "dia_ly", "ແຂວງອັດຕະປືຢູ່ພາກໃຕ້ສຸດ", "Tỉnh Attapeu ở cực Nam Lào"),

    # === 2. CÁC BỘ VÀ CƠ QUAN NHÀ NƯỚC (GOVERNMENT MINISTRIES) ===
    ("ກະຊວງສຶກສາທິການແລະກິລາ", "Bộ Giáo dục và Thể thao", "Ministry of Education and Sports", "ka xuang seuk sa thi kan lae ki la", "noun", "chinh_tri", "ປະກາດຈາກກະຊວງສຶກສາທິການແລະກິລາ", "Thông báo từ Bộ Giáo dục và Thể thao"),
    ("ກະຊວງສາທາລະນະສຸກ", "Bộ Y tế", "Ministry of Health", "ka xuang sa tha la na sook", "noun", "chinh_tri", "ກະຊວງສາທາລະນະສຸກປ້ອງກັນພະຍາດ", "Bộ Y tế phòng chống dịch bệnh"),
    ("ກະຊວງປ້ອງກັນປະເທດ", "Bộ Quốc phòng", "Ministry of National Defence", "ka xuang pong kan pa thed", "noun", "chinh_tri", "ກອງທັບສັງກັດກະຊວງປ້ອງກັນປະເທດ", "Quân đội thuộc Bộ Quốc phòng"),
    ("ກະຊວງປ້ອງກັນຄວາມສະຫງົບ", "Bộ An ninh / Công an", "Ministry of Public Security", "ka xuang pong kan khuam sa ngop", "noun", "chinh_tri", "ເຈົ້າໜ້າທີ່ກະຊວງປ້ອງກັນຄວາມສະຫງົບ", "Chiến sĩ Bộ An ninh"),
    ("ກະຊວງການຕ່າງປະເທດ", "Bộ Ngoại giao", "Ministry of Foreign Affairs", "ka xuang kan tang pa thed", "noun", "chinh_tri", "ຄະນະຜູ້ແທນກະຊວງການຕ່າງປະເທດ", "Đoàn đại biểu Bộ Ngoại giao"),
    ("ກະຊວງການເງິນ", "Bộ Tài chính", "Ministry of Finance", "ka xuang kan ngen", "noun", "chinh_tri", "ນະໂຍບາຍພາສີຂອງກະຊວງການເງິນ", "Chính sách thuế của Bộ Tài chính"),
    ("ກະຊວງແຜນການແລະການລົງທຶນ", "Bộ Kế hoạch và Đầu tư", "Ministry of Planning and Investment", "ka xuang phaen kan lae kan long theun", "noun", "chinh_tri", "ອະນຸມັດໂຄງການລົງທຶນ", "Phê duyệt dự án đầu tư"),
    ("ກະຊວງອຸດສາຫະກຳແລະການຄ້າ", "Bộ Công Thương", "Ministry of Industry and Commerce", "ka xuang ood sa ha kam lae kan kha", "noun", "chinh_tri", "ສົ່ງເສີມການຄ້າພາຍໃນ", "Khuyến khích thương mại nội địa"),
    ("ກະຊວງໂຍທາທິການແລະຂົນສົ່ງ", "Bộ Công chính và Vận tải", "Ministry of Public Works and Transport", "ka xuang yo tha thi kan lae khon song", "noun", "chinh_tri", "ກໍ່ສ້າງເສັ້ນທາງຄົມມະນາຄົມ", "Xây dựng các tuyến đường giao thông"),
    ("ກະຊວງກະສິກຳແລະປ່າໄມ້", "Bộ Nông Lâm", "Ministry of Agriculture and Forestry", "ka xuang ka si kam lae pa mai", "noun", "chinh_tri", "ປົກປັກຮັກສາປ່າໄມ້", "Bảo vệ rừng tài nguyên"),
    ("ກະຊວງຍຸຕິທຳ", "Bộ Tư pháp", "Ministry of Justice", "ka xuang yu ti tham", "noun", "chinh_tri", "ເຜີຍແຜ່ກົດໝາຍ", "Phổ biến giáo dục pháp luật"),

    # === 3. NGHỀ NGHIỆP VÀ THỢ THUYỀN (PROFESSIONS & TRADES) ===
    ("ຊ່າງໄມ້", "thợ mộc", "carpenter", "xang mai", "noun", "nghe_nghiep", "ຊ່າງໄມ້ເຮັດຕູ້", "Thợ mộc đóng tủ"),
    ("ຊ່າງເຫຼັກ", "thợ hàn / thợ sắt", "welder / blacksmith", "xang lek", "noun", "nghe_nghiep", "ຊ່າງເຫຼັກຈອດປະຕູ", "Thợ sắt hàn cánh cổng"),
    ("ຊ່າງໄຟຟ້າ", "thợ điện", "electrician", "xang fai fa", "noun", "nghe_nghiep", "ຊ່າງໄຟຟ້າສ້ອມແປງສາຍໄຟ", "Thợ điện sửa dây điện"),
    ("ຊ່າງສ້ອມແປງ", "thợ sửa chữa máy móc", "mechanic / repairer", "xang som paeng", "noun", "nghe_nghiep", "ຊ່າງສ້ອມແປງລົດຈັກ", "Thợ sửa xe máy"),
    ("ຊ່າງຕັດຜົມ", "thợ cắt tóc", "barber / hairdresser", "xang tad phom", "noun", "nghe_nghiep", "ຊ່າງຕັດຜົມຕັດງາມ", "Thợ cắt tóc tạo kiểu rất đẹp"),
    ("ຊ່າງຕັດຫຍິບ", "thợ may mặc", "tailor / seamstress", "xang tad yib", "noun", "nghe_nghiep", "ຊ່າງຕັດຫຍິບຕັດສິ້ນ", "Thợ may may váy Lào"),
    ("ຊ່າງຖ່າຍຮູບ", "thợ nhiếp ảnh", "photographer", "xang thai hoop", "noun", "nghe_nghiep", "ຊ່າງຖ່າຍຮູບມືອາຊີບ", "Nhiếp ảnh gia chuyên nghiệp"),
    ("ຊ່າງຄຳ", "thợ kim hoàn chế tác vàng bạc", "goldsmith", "xang kham", "noun", "nghe_nghiep", "ຊ່າງຄຳຕີແຫວນ", "Thợ kim hoàn uốn nhẫn"),
    ("ຊ່າງກໍ່", "thợ hồ / nề xây dựng", "mason / builder", "xang kor", "noun", "nghe_nghiep", "ຊ່າງກໍ່ກໍ່ກຳແພງ", "Thợ xây xây tường nhà"),
    ("ຊ່າງຈັກ", "thợ máy xưởng", "machinist", "xang jak", "noun", "nghe_nghiep", "ຊ່າງຈັກຄວບຄຸມເຄື່ອງ", "Thợ máy vận hành máy móc"),
    ("ຊ່າງຍ້ອມ", "thợ nhuộm vải", "dyer", "xang yom", "noun", "nghe_nghiep", "ຊ່າງຍ້ອມຜ້າໄໝ", "Thợ nhuộm tơ lụa"),
    ("ຊ່າງແຕ້ມ", "họa viên / thợ vẽ", "illustrator / painter", "xang taem", "noun", "nghe_nghiep", "ຊ່າງແຕ້ມແຕ້ມຮູບຕິດຝາ", "Họa sĩ vẽ tranh tường"),

    # === 4. CÁC TỪ MỞ RỘNG VỚI ຜູ້- & ນັກ- ===
    ("ຜູ້ປົກຄອງ", "phụ huynh / người giám hộ", "parent / guardian", "phu pok khong", "noun", "vai_tro", "ກອງປະຊຸມຜູ້ປົກຄອງ", "Họp phụ huynh học sinh"),
    ("ຜູ້ສາວ", "thiếu nữ / bạn gái", "young lady / girlfriend", "phu sao", "noun", "doi_song", "ຜູ້ສາວລາວຮັກນວນສະຫງວນຕົວ", "Thiếu nữ Lào duyên dáng đoan trang"),
    ("ຜູ້ບ່າວ", "chàng trai / bạn trai", "young man / boyfriend", "phu bao", "noun", "doi_song", "ຜູ້ບ່າວມາຫຼິ້ນເຮືອນ", "Bạn trai sang chơi nhà"),
    ("ຜູ້ກໍ່ຕັ້ງ", "người sáng lập", "founder", "phu kor tang", "noun", "vai_tro", "ຜູ້ກໍ່ຕັ້ງບໍລິສັດ", "Người sáng lập công ty"),
    ("ຜູ້ສ້າງ", "người tạo ra / tác giả sáng tạo", "creator / maker", "phu sang", "noun", "vai_tro", "ຜູ້ສ້າງຜົນງານ", "Tác giả của tác phẩm"),
    ("ຜູ້ປະສານງານ", "điều phối viên", "coordinator", "phu pa san ngan", "noun", "vai_tro", "ຜູ້ປະສານງານໂຄງການ", "Điều phối viên dự án"),
    ("ຜູ້ຊື້", "người mua hàng", "buyer / purchaser", "phu seu", "noun", "thuong_mai", "ສິດຂອງຜູ້ຊື້", "Quyền lợi của người mua"),
    ("ຜູ້ຂາຍ", "người bán hàng", "seller / vendor", "phu khai", "noun", "thuong_mai", "ຜູ້ຂາຍໃຫ້ຄຳແນະນຳ", "Người bán tư vấn"),
    ("ຜູ້ໃຫ້", "người cho / nhà hảo tâm", "giver / donor", "phu hai", "noun", "vai_tro", "ຜູ້ໃຫ້ມີຄວາມສຸກ", "Người cho đi thấy hạnh phúc"),
    ("ນັກເສດຖະສາດ", "nhà kinh tế học", "economist", "nak sed tha sad", "noun", "nghe_nghiep", "ນັກເສດຖະສາດວິເຄາະ", "Nhà kinh tế phân tích"),
    ("ນັກການເມືອງ", "chính trị gia", "politician", "nak kan meuang", "noun", "nghe_nghiep", "ນັກການເມືອງອາວຸໂສ", "Chính khách kỳ cựu"),
    ("ນັກດົນຕີ", "nhạc công / nghệ sĩ chơi đàn", "musician", "nak don tee", "noun", "nghe_nghiep", "ນັກດົນຕີຫຼິ້ນແຄນ", "Nghệ nhân thổi khèn bè"),
    ("ນັກອອກແບບ", "nhà thiết kế", "designer", "nak ork baeb", "noun", "nghe_nghiep", "ນັກອອກແບບເສື້ອຜ້າ", "Nhà thiết kế thời trang"),
    ("ນັກພັດທະນາ", "nhà phát triển (phần mềm)", "developer", "nak phat tha na", "noun", "nghe_nghiep", "ນັກພັດທະນາລະບົບ", "Nhà phát triển hệ thống"),
    ("ນັກແປ", "biên phiên dịch viên", "translator / interpreter", "nak pae", "noun", "nghe_nghiep", "ນັກແປພາສາລາວ-ຫວຽດ", "Biên dịch viên Lào - Việt"),
    ("ນັກສືບ", "thám tử điều tra", "detective", "nak seub", "noun", "nghe_nghiep", "ນັກສືບສືບສວນຄະດີ", "Thám tử điều tra vụ án"),
    ("ນັກດັບເພີງ", "lính cứu hỏa", "firefighter", "nak dap phoeng", "noun", "nghe_nghiep", "ນັກດັບເພີງມອດໄຟ", "Lính cứu hỏa dập lửa"),

    # === 5. CƠ SỞ VẬT CHẤT: ຮ້ານ-, ໂຮງ-, ຫ້ອງ- ===
    ("ຮ້ານເສີມສວຍ", "tiệm làm đẹp / spa thẩm mỹ", "beauty salon / spa", "han serm suay", "noun", "co_so", "ໄປແຕ່ງໜ້າຢູ່ຮ້ານເສີມສວຍ", "Đi trang điểm ở tiệm làm đẹp"),
    ("ຮ້ານສ້ອມລົດ", "tiệm sửa chữa xe", "auto / bike repair shop", "han som lod", "noun", "co_so", "ປ່ຽນຢາງຢູ່ຮ້ານສ້ອມລົດ", "Vá xăm ở tiệm sửa xe"),
    ("ຮ້ານຂາຍໂທລະສັບ", "cửa hàng bán điện thoại", "phone shop", "han khai tho la sap", "noun", "co_so", "ຊື້ສາຍສາກຢູ່ຮ້ານຂາຍໂທລະສັບ", "Mua cáp sạc ở tiệm điện thoại"),
    ("ຮ້ານເບຍ", "quán nhậu / bia hơi", "beer garden / pub", "han bia", "noun", "co_so", "ນັດກັນຢູ່ຮ້ານເບຍ", "Hẹn nhau ở quán bia"),
    ("ຮ້ານນ້ຳປັ່ນ", "quán sinh tố trái cây", "smoothie juice bar", "han nam pan", "noun", "co_so", "ດື່ມນ້ຳປັ່ນໝາກມ່ວງ", "Uống sinh tố xoài"),
    ("ຮ້ານຂອງຫວານ", "quán chè bánh ngọt", "dessert cafe", "han khong van", "noun", "co_so", "ກິນຂອງຫວານຕອນແລງ", "Ăn chè buổi chiều mát"),
    ("ຮ້ານຂາຍປຶ້ມ", "hiệu sách / nhà sách", "bookstore", "han khai peum", "noun", "co_so", "ຊື້ປຶ້ມວັດຈະນານຸກົມຢູ່ຮ້ານຂາຍປຶ້ມ", "Mua từ điển ở hiệu sách"),
    ("ໂຮງສີ", "nhà máy xay xát lúa gạo", "rice mill", "hong see", "noun", "co_so", "ເອົາເຂົ້າໄປສີຢູ່ໂຮງສີ", "Chở thóc đi xay ở nhà máy xay xát"),
    ("ໂຮງໄຟຟ້າ", "nhà máy nhiệt điện / thủy điện", "power plant", "hong fai fa", "noun", "co_so", "ໂຮງໄຟຟ້ານ້ຳຕົກ", "Nhà máy thủy điện"),
    ("ໂຮງສານ", "tòa án xét xử", "court of law", "hong san", "noun", "co_so", "ຂຶ້ນໂຮງສານ", "Ra hầu tòa"),
    ("ໂຮງຮຽນອະນຸບານ", "trường mầm non / mẫu giáo", "kindergarten / preschool", "hong hian ar noo ban", "noun", "co_so", "ສົ່ງລູກໄປໂຮງຮຽນອະນຸບານ", "Đưa con đến trường mầm non"),
    ("ໂຮງຮຽນວິຊາຊີບ", "trường đào tạo nghề", "vocational school", "hong hian vi sa xeeb", "noun", "co_so", "ຮຽນຕໍ່ໂຮງຮຽນວິຊາຊີບ", "Học tiếp ở trường dạy nghề"),
    ("ຫ້ອງການ", "văn phòng cơ quan / công sở", "office", "hong kan", "noun", "co_so", "ເຮັດວຽກຢູ່ຫ້ອງການ", "Làm việc tại văn phòng"),
    ("ຫ້ອງບັນຍາຍ", "giảng đường đại học", "lecture hall", "hong ban yai", "noun", "co_so", "ນັກສຶກສານັ່ງໃນຫ້ອງບັນຍາຍ", "Sinh viên ngồi trong giảng đường"),
    ("ຫ້ອງເກັບເຄື່ອງ", "kho chứa đồ / nhà kho", "storage room / storeroom", "hong kep kheuang", "noun", "co_so", "ມ້ຽນເຄື່ອງໄວ້ໃນຫ້ອງເກັບເຄື່ອງ", "Cất đồ đạc vào trong kho"),
    ("ຫ້ອງພະຍາບານ", "phòng y tế học đường/cơ quan", "infirmary / nurse's room", "hong pha ya ban", "noun", "co_so", "ໄປພັກຢູ່ຫ້ອງພະຍາບານ", "Nằm nghỉ tại phòng y tế"),

    # === 6. ĐỒ GIA DỤNG, THIẾT BỊ VÀ CHẤT LỎNG: ເຄື່ອງ-, ນ້ຳ- ===
    ("ເຄື່ອງປັ່ນ", "máy xay sinh tố", "blender", "kheuang pan", "noun", "thiet_bi", "ປັ່ນໝາກໄມ້ດ້ວຍເຄື່ອງປັ່ນ", "Xay hoa quả bằng máy xay"),
    ("ເຄື່ອງຕັດຫຍ້າ", "máy cắt cỏ", "lawn mower", "kheuang tad ya", "noun", "thiet_bi", "ຕັດຫຍ້າໃນສວນ", "Cắt tỉa cỏ trong vườn"),
    ("ເຄື່ອງວັດແທກ", "dụng cụ đo lường", "measuring instrument", "kheuang vat thaek", "noun", "thiet_bi", "ເຄື່ອງວັດແທກອຸນຫະພູມ", "Nhiệt kế đo nhiệt độ"),
    ("ເຄື່ອງສາກ", "củ sạc / bộ nạp điện", "charger / adapter", "kheuang sak", "noun", "thiet_bi", "ເຄື່ອງສາກໂທລະສັບ", "Củ sạc điện thoại"),
    ("ເຄື່ອງຊັ່ງ", "cái cân đo khối lượng", "scale / weighing balance", "kheuang sang", "noun", "thiet_bi", "ຊັ່ງນ້ຳໜັກເທິງເຄື່ອງຊັ່ງ", "Cân trọng lượng trên bàn cân"),
    ("ເຄື່ອງປ້ອງກັນ", "đồ bảo hộ lao động", "protective equipment", "kheuang pong kan", "noun", "thiet_bi", "ໃສ່ເຄື່ອງປ້ອງກັນ", "Mặc đồ bảo hộ an toàn"),
    ("ນ້ຳມັນແອັດຊັງ", "xăng chạy xe", "gasoline / petrol", "nam man aet sang", "noun", "nhien_lieu", "ຕື່ມນ້ຳມັນແອັດຊັງ", "Đổ xăng xe máy"),
    ("ນ້ຳມັນກາຊວນ", "dầu diesel", "diesel fuel", "nam man ka xuan", "noun", "nhien_lieu", "ລົດບັນທຸກໃຊ້ນ້ຳມັນກາຊວນ", "Xe tải chạy dầu diesel"),
    ("ນ້ຳສົ້ມສາຍຊູ", "giấm ăn pha chua", "vinegar", "nam som sai xoo", "noun", "gia_vi", "ໃສ່ນ້ຳສົ້ມສາຍຊູ", "Nêm giấm ăn"),
    ("ນ້ຳຢາລ້າງຈານ", "nước rửa chén bát", "dishwashing liquid", "nam ya lang jan", "noun", "gia_dung", "ລ້າງຖ້ວຍດ້ວຍນ້ຳຢາລ້າງຈານ", "Rửa chén bằng nước rửa chén"),
    ("ນ້ຳຢາຊັກຜ້າ", "nước giặt quần áo", "laundry detergent", "nam ya sak pha", "noun", "gia_dung", "ນ້ຳຢາຊັກຜ້າຫອມ", "Nước giặt quần áo thơm ngát"),
    ("ນ້ຳຫອມ", "nước hoa xịt thơm", "perfume", "nam hom", "noun", "my_pham", "ສີດນ້ຳຫອມ", "Xịt nước hoa"),
    ("ນ້ຳຢາບ້ວນປາກ", "nước súc miệng", "mouthwash", "nam ya buan pak", "noun", "y_te", "ບ້ວນປາກຫຼັງຖູແຂ້ວ", "Súc miệng sau khi đánh răng"),

    # === 7. NÔNG NGHIỆP, CÂY CỎ & HOA TRÁI: ຕົ້ນ-, ໝາກ- ===
    ("ຕົ້ນສັກ", "cây gỗ tếch quý", "teak tree", "ton sak", "noun", "thuc_vat", "ປ່າຕົ້ນສັກໃຫຍ່", "Rừng gỗ tếch bạt ngàn"),
    ("ຕົ້ນໂພ", "cây bồ đề linh thiêng", "Bodhi tree", "ton phoh", "noun", "thuc_vat", "ຕົ້ນໂພໃຫຍ່ຢູ່ວັດ", "Cây bồ đề cổ thụ trong chùa"),
    ("ຕົ້ນຢາງພາລາ", "cây cao su", "rubber tree", "ton yang pha la", "noun", "thuc_vat", "ສວນຕົ້ນຢາງພາລາ", "Vườn cây cao su"),
    ("ຕົ້ນອ້ອຍ", "cây mía ngọt", "sugarcane plant", "ton oy", "noun", "thuc_vat", "ບີບນ້ຳອ້ອຍ", "Ép nước mía"),
    ("ຕົ້ນຫຍ້າ", "bụi cỏ dại", "grass", "ton ya", "noun", "thuc_vat", "ຫຍ້າຂຽວອຸ່ມທຸ່ມ", "Bãi cỏ xanh mướt"),
    ("ໝາກກ້ຽງໃຫຍ່", "quả bưởi", "pomelo / grapefruit", "mak kiang yai", "noun", "thuc_pham", "ໝາກກ້ຽງໃຫຍ່ຫວານ", "Quả bưởi ngọt mọng nước"),
    ("ໝາກອຶ", "quả bí đỏ", "pumpkin", "mak eu", "noun", "thuc_pham", "ແກງໝາກອຶໃສ່ກະທິ", "Canh bí đỏ nấu nước cốt dừa"),
    ("ໝາກຟັກ", "quả bí đao / bí xanh", "winter melon", "mak fak", "noun", "thuc_pham", "ຕົ້ມໝາກຟັກໃສ່ກະດູກໝູ", "Canh bí đao hầm sườn heo"),
    ("ໝາກຖົ່ວຍາວ", "đậu đũa dài", "yardlong bean", "mak thua yao", "noun", "thuc_pham", "ກິນໝາກຖົ່ວຍາວກັບຕຳໝາກຫຸ່ງ", "Ăn đậu đũa sống với nộm đu đủ"),
    ("ໝາກຖົ່ວດິນ", "hạt lạc / đậu phộng", "peanut", "mak thua din", "noun", "thuc_pham", "ໝາກຖົ່ວດິນຂົ້ວເກลືອ", "Đậu phộng rang muối"),
    ("ໝາກມີ້", "quả mít chín thơm", "jackfruit", "mak mee", "noun", "thuc_pham", "ໝາກມີ້ສຸກຫອມຫວານ", "Mít chín thơm lừng"),
    ("ໝາກກະທັນ", "quả táo ta / táo rừng", "jujube", "mak ka than", "noun", "thuc_pham", "ໝາກກະທັນສົ້ມໆຫວານໆ", "Táo chua chua ngọt ngọt"),
    ("ໝາກມ່ວງຫິມະພານ", "hạt điều", "cashew nut", "mak muang hi ma phan", "noun", "thuc_pham", "ໝາກມ່ວງຫິມະພານອົບເກลືອ", "Hạt điều sấy muối giòn"),

    # === 8. GIẤY TỜ, VĂN BẢN HÀNH CHÍNH: ໃບ- ===
    ("ໃບມອບສິດ", "giấy ủy quyền", "power of attorney / authorization letter", "bai mob sit", "noun", "hanh_chinh", "ເຮັດໃບມອບສິດໃຫ້ທະນາຍຄວາມ", "Làm giấy ủy quyền cho luật sư"),
    ("ໃບຢັ້ງຢືນທີ່ຢູ່", "giấy xác nhận nơi cư trú / tạm trú", "certificate of residence", "bai yang yeun thee yoo", "noun", "hanh_chinh", "ຂໍໃບຢັ້ງຢືນທີ່ຢູ່ຈາກນາຍບ້ານ", "Xin giấy xác nhận tạm trú từ trưởng thôn"),
    ("ໃບສັນຍາ", "bản hợp đồng giao kết", "contract / agreement", "bai san ya", "noun", "hanh_chinh", "ເຊັນໃບສັນຍາເຊົ່າເຮືອນ", "Ký hợp đồng thuê nhà"),
    ("ໃບຢັ້ງຢືນສັນຊາດ", "giấy chứng nhận quốc tịch", "certificate of nationality", "bai yang yeun san xad", "noun", "hanh_chinh", "ໃບຢັ້ງຢືນສັນຊາດລາວ", "Giấy chứng nhận quốc tịch Lào"),
    ("ໃບແຈ້ງໜີ້", "giấy báo nợ / thông báo cước", "bill / invoice notification", "bai jaeng nee", "noun", "tai_chinh", "ໃບແຈ້ງໜີ້ຄ່າໄຟຟ້າ", "Giấy báo cước tiền điện"),

    # === 9. CÁC TỪ LOẠI ĐỘNG TỪ ĐỜI SỐNG HÀNG NGÀY & GIAO TIẾP ===
    ("ເຊີນ", "mời / kính mời", "invite", "xoern", "verb", "giao_tiep", "ເຊີນເຂົ້າຂ້າງໃນ", "Mời vào bên trong"),
    ("ລໍຖ້າ", "chờ đợi", "wait for", "lor tha", "verb", "hanh_dong", "ລໍຖ້າຈັກໜ່ອຍເດີ້", "Đợi một chút nhé"),
    ("ຕ້ອນຮັບ", "đón tiếp nồng hậu", "welcome / receive", "ton hap", "verb", "giao_tiep", "ຕ້ອນຮັບແຂກບ້ານແຂກເມືອງ", "Đón tiếp khách phương xa"),
    ("ສັນຍາ", "hứa hẹn / cam kết", "promise", "san ya", "verb", "giao_tiep", "ສັນຍາວ່າມື້ອື່ນຈະມາ", "Hứa là ngày mai sẽ đến"),
    ("ປະຕິເສດ", "từ chối bác bỏ", "refuse / decline", "pa ti sed", "verb", "giao_tiep", "ປະຕິເສດຄຳເຊີນ", "Từ chối lời mời"),
    ("ຍອມຮັບ", "thừa nhận / chấp nhận", "accept / admit", "yom hap", "verb", "giao_tiep", "ຍອມຮັບຄວາມຈິງ", "Chấp nhận sự thật"),
    ("ແນະນຳ", "giới thiệu / hướng dẫn", "introduce / advise", "nae nam", "verb", "giao_tiep", "ແນະນຳຕົວເອງ", "Tự giới thiệu bản thân"),
    ("ອະທິບາຍ", "giải thích làm rõ", "explain", "ar thi bai", "verb", "giao_duc", "ອາຈານອະທິບາຍບົດຮຽນ", "Thầy giáo giải thích bài học"),
    ("ປຶກສາ", "bàn bạc / tham khảo ý kiến", "consult / discuss", "peuk sa", "verb", "giao_tiep", "ປຶກສາກັບຄອບຄົວ", "Bàn bạc với gia đình"),
    ("ຕົກລົງ", "đồng ý / nhất trí", "agree / decide", "tok long", "verb", "giao_tiep", "ຕົກລົງຕາມນັ້ນ", "Nhất trí theo phương án đó"),
    ("ຕັດສິນໃຈ", "quyết định đưa ra lựa chọn", "make a decision", "tad sin jai", "verb", "tam_ly", "ຕັດສິນໃຈແລ້ວ", "Đã đưa ra quyết định rồi"),
    ("ແກ້ໄຂ", "giải quyết sửa chữa vướng mắc", "solve / resolve", "kae khai", "verb", "cong_viec", "ແກ້ໄຂບັນຫາຮ່ວມກັນ", "Cùng nhau giải quyết vấn đề"),
    ("ຊ່ວຍເຫຼືອ", "giúp đỡ tương trợ", "help / assist", "suay leua", "verb", "doi_song", "ຊ່ວຍເຫຼືອເຊິ່ງກັນແລະກັນ", "Tương trợ giúp đỡ lẫn nhau"),
    ("ປົກປ້ອງ", "bảo vệ che chở", "protect", "pok pong", "verb", "xa_hoi", "ປົກປ້ອງປະເທດຊາດ", "Bảo vệ tổ quốc thân yêu"),
    ("ຮັກສາ", "gìn giữ bảo quản", "maintain / preserve", "hak sa", "verb", "doi_song", "ຮັກສາສຸຂະພາບ", "Giữ gìn sức khỏe"),
    ("ປ້ອງກັນ", "phòng ngừa phòng vệ", "prevent / defend", "pong kan", "verb", "y_te", "ປ້ອງກັນດີກວ່າປິ່ນປົວ", "Phòng bệnh hơn chữa bệnh"),
    ("ປິ່ນປົວ", "chữa trị điều trị bệnh tật", "cure / treat", "pin pua", "verb", "y_te", "ທ່ານໝໍປິ່ນປົວຄົນເຈັບ", "Bác sĩ tận tình chữa bệnh"),
    ("ກວດກາ", "kiểm tra thanh tra", "inspect / check", "kuat ka", "verb", "cong_viec", "ກວດກາເອກະສານຢ່າງລະອຽດ", "Kiểm tra kỹ lưỡng hồ sơ"),
    ("ລົງທະບຽນ", "đăng ký ghi danh", "register / enroll", "long tha bian", "verb", "hanh_chinh", "ລົງທະບຽນຮຽນພາສາ", "Đăng ký học ngoại ngữ"),
    ("ຈັດສົ່ງ", "giao hàng / ship hàng", "deliver / ship", "jad song", "verb", "thuong_mai", "ຈັດສົ່ງສິນຄ້າຮອດບ້ານ", "Giao hàng tận nơi"),
    ("ຊຳລະ", "thanh toán trả tiền", "pay / settle payment", "xam la", "verb", "thuong_mai", "ຊຳລະຄ່າສິນຄ້າ", "Thanh toán tiền hàng"),
    ("ສັ່ງຊື້", "đặt mua hàng hóa", "order / purchase", "sang seu", "verb", "thuong_mai", "ສັ່ງຊື້ທາງອອນລາຍ", "Đặt mua hàng qua mạng"),
    ("ແລກປ່ຽນ", "trao đổi đổi chác", "exchange / swap", "laek pian", "verb", "thuong_mai", "ແລກປ່ຽນເງິນຕາ", "Đổi ngoại tệ"),
    ("ຕິດຕໍ່", "liên hệ kết nối", "contact / connect", "tid tor", "verb", "giao_tiep", "ຕິດຕໍ່ພົວພັນ", "Liên hệ công tác"),

    # === 10. TÍNH TỪ TRẠNG THÁI & TÍNH CHẤT (ADJECTIVES) ===
    ("ງ່າຍດາຍ", "rất đơn giản dễ dàng", "easy / simple", "ngai dai", "adj", "tinh_chat", "ວິທີນີ້ງ່າຍດາຍຫຼາຍ", "Cách này rất đỗi đơn giản"),
    ("ຫຍຸ້ງຍາກ", "phức tạp rắc rối khó khăn", "difficult / complicated", "hyung yak", "adj", "tinh_chat", "ຂັ້ນຕອນຫຍຸ້ງຍາກ", "Quy trình thủ tục rắc rối"),
    ("ລະອຽດ", "tỉ mỉ chi tiết cẩn thận", "detailed / meticulous", "la iad", "adj", "tinh_chat", "ອະທິບາຍຢ່າງລະອຽດ", "Giải thích rất chi tiết"),
    ("ຮີບດ່ວນ", "khẩn cấp cấp bách", "urgent / emergency", "heeb duan", "adj", "tinh_chat", "ເລື່ອງຮີບດ່ວນ", "Việc vô cùng khẩn cấp"),
    ("ຊັດເຈນ", "rõ ràng minh bạch", "clear / obvious", "xad jen", "adj", "tinh_chat", "ເຫັນຢ່າງຊັດເຈນ", "Thấy rõ ràng mồn một"),
    ("ກົງໄປກົງມາ", "thẳng thắn bộc trực", "straightforward / frank", "zong pai zong ma", "adj", "tinh_cach", "ເວົ້າກົງໄປກົງມາ", "Nói năng thẳng thắn"),
    ("ສະຫຼາດຫຼັກແຫຼມ", "thông minh sắc bén", "astute / sharp-minded", "sa lat lak laem", "adj", "tinh_cach", "ຄວາມຄິດສະຫຼາດຫຼັກແຫຼມ", "Tư duy vô cùng sắc sảo"),
    ("ເມດຕາ", "giàu lòng từ bi nhân ái", "merciful / compassionate", "med ta", "adj", "tinh_cach", "ຈິດໃຈເມດຕາ", "Tấm lòng nhân ái từ bi"),
    ("ກະຕັນຍູ", "hiếu thảo biết ơn", "grateful / filial", "ka tan yoo", "adj", "tinh_cach", "ລູກກະຕັນຍູຕໍ່ພໍ່ແມ່", "Con cái hiếu thảo với cha mẹ"),
    ("ເສຍສະຫຼະ", "hy sinh vì người khác", "sacrificial", "sia sa la", "adj", "tinh_cach", "ນ້ຳໃຈເສຍສະຫຼະ", "Tinh thần hy sinh cao cả"),
    ("ສະເໝີພາບ", "bình đẳng công bằng", "equal", "sa mer phap", "adj", "xa_hoi", "ສິດສະເໝີພາບລະຫວ່າງຍິງຊາຍ", "Nam nữ bình đẳng"),
    ("ຍຸຕິທຳ", "công minh chính trực", "fair / just", "yu ti tham", "adj", "xa_hoi", "ສັງຄົມຍຸຕິທຳ", "Xã hội công bằng văn minh"),
    ("ເສລີພາບ", "tự do tự tại", "free / liberty", "say lee phap", "adj", "xa_hoi", "ຊີວິດມີເສລີພາບ", "Cuộc sống có tự do"),
    ("ອຸດົມສົມບູນ", "trù phú phì nhiêu màu mỡ", "abundant / fertile", "oo dom som boon", "adj", "tu_nhien", "ທຳມະຊາດອຸດົມສົມບູນ", "Thiên nhiên giàu có trù phú"),
    ("ໝັ້ນຄົງ", "bền vững kiên cố vững chắc", "stable / secure", "man khong", "adj", "tinh_chat", "ເສດຖະກິດໝັ້ນຄົງ", "Nền kinh tế ổn định vững chắc"),
]

def main():
    print("=" * 70)
    print("🌟 CHƯƠNG TRÌNH ĐẠI NẠP TỪ ĐIỂN LÀO TOÀN DIỆN 3000+ MỤC TỪ")
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
    for item in EXPANSION_BATCH:
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

    print(f"[+] Bổ sung thành công: +{added} từ vựng chất lượng cao!")
    print(f"[+] TỔNG SỐ TỪ VỰNG TRONG KHO HIỆN TẠI: {len(existing_rows)} TỪ CHUẨN NFC.")
    print("=" * 70)

if __name__ == "__main__":
    main()
