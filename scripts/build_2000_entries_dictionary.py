"""
Script Mở Rộng Từ Điển Lên Quy Mô Lớn (2,000+ Mục Từ Tiếng Lào).
Tạo lập hệ thống từ vựng phái sinh tự nhiên theo ngữ pháp & văn hóa Lào:
- Nhóm ghép 'ໃຈ' (Tâm/Lòng/Cảm xúc)
- Nhóm ghép 'ເຮືອນ', 'ຫ້ອງ', 'ໂຮງ' (Nơi chốn/Không gian)
- Nhóm ghép 'ລົດ', 'ທາງ', 'ຂົວ' (Giao thông)
- Nhóm ghép 'ນ້ຳ', 'ໄຟ', 'ດິນ', 'ລົມ' (Ngũ hành/Tự nhiên)
- Nhóm ghép 'ມື', 'ຕາ', 'ຫົວ', 'ປາກ' (Cơ thể/Hành động)
- Nhóm chuyên đề Giáo dục Trực tuyến & Ngoại ngữ (EdTech Lao)
- Nhóm số đếm mở rộng (Số thứ tự, phần trăm, phân số)
Chuẩn hóa 100% Unicode NFC.
"""
import os
import sys
import csv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing.normalize import normalize_lao

sys.stdout.reconfigure(encoding='utf-8')


def build_massive_dictionary():
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
    
    print(f"[*] Từ điển hiện tại: {len(entries)} từ.")
    
    new_records = []

    # 1. NHÓM TỪ GHÉP TÂM LÝ & TÍNH CÁCH VỚI 'ໃຈ' (TÂM / LÒNG)
    chai_group = [
        ("ໃຈດີ", "Tốt bụng / Hiền lành", "Kind / Good-natured", "chai-dee", "adjective", "Tính cách", "ເພິ່ນເປັນຄົນໃຈດີ", "Người ấy rất tốt bụng"),
        ("ໃຈຮ້າຍ", "Nóng nảy / Tức giận", "Angry / Hot-tempered", "chai-haai", "adjective", "Tính cách", "ຢ່າໃຈຮ້າຍ", "Đừng tức giận"),
        ("ໃຈດຳ", "Độc ác / Lòng dạ đen tối", "Cruel / Malicious", "chai-dam", "adjective", "Tính cách", "ຄົນໃຈດຳ", "Kẻ độc ác"),
        ("ໃຈກວ້າງ", "Rộng lượng / Hào phóng", "Generous / Broad-minded", "chai-kuaang", "adjective", "Tính cách", "ຄົນໃຈກວ້າງຂວາງ", "Người có lòng dạ rộng lượng"),
        ("ໃຈແຄບ", "Hẹp hòi / Ích kỷ", "Narrow-minded / Selfish", "chai-khaep", "adjective", "Tính cách", "ບໍ່ຄວນເປັນຄົນໃຈແຄບ", "Không nên là người hẹp hòi"),
        ("ໃຈເຢັນ", "Bình tĩnh / Điềm đạm", "Calm / Patient", "chai-yen", "adjective", "Tính cách", "ໃຈເຢັນໆເດີ", "Hãy bình tĩnh lại nhé"),
        ("ໃຈຮ້ອນ", "Nóng vội / Vội vàng", "Impatient / Rash", "chai-hawn", "adjective", "Tính cách", "ເຮັດວຽກຢ່າໃຈຮ້ອນ", "Làm việc chớ nên nóng vội"),
        ("ໃຈງ່າຍ", "Dễ dãi / Cả tin", "Easy-going / Gullible", "chai-ngaai", "adjective", "Tính cách", "ຄົນໃຈງ່າຍ", "Người cả tin"),
        ("ໃຈກ້າ", "Dũng cảm / Gan dạ", "Brave / Courageous", "chai-kaa", "adjective", "Tính cách", "ທະຫານໃຈກ້າ", "Người lính dũng cảm"),
        ("ໃຈອ່ອນ", "Mủi lòng / Yếu lòng", "Soft-hearted", "chai-awn", "adjective", "Tính cách", "ຄົນໃຈອ່ອນ", "Người hay mủi lòng"),
        ("ຕັ້ງໃຈ", "Chăm chú / Quyết tâm", "Determined / Attentive", "tang-chai", "verb", "Học tập", "ຕັ້ງໃຈຮຽນໜັງສື", "Chăm chỉ học bài"),
        ("ສົນໃຈ", "Quan tâm / Hứng thú", "Interested", "son-chai", "verb", "Tâm lý", "ຂ້ອຍສົນໃຈພາສາລາວ", "Tôi rất quan tâm đến tiếng Lào"),
        ("ໝັ້ນໃຈ", "Tự tin / Chắc chắn", "Confident", "man-chai", "adjective", "Tâm lý", "ມີຄວາມໝັ້ນໃຈ", "Có sự tự tin"),
        ("ພໍໃຈ", "Hài lòng / Thỏa mãn", "Satisfied", "phaw-chai", "adjective", "Tâm lý", "ພໍໃຈກັບຜົນງານ", "Hài lòng với kết quả"),
        ("ຕົກໃຈ", "Giật mình / Hoảng hốt", "Startled / Shocked", "tok-chai", "verb", "Tâm lý", "ຢ່າຕົກໃຈ", "Đừng giật mình hoảng hốt"),
        ("ແປກໃຈ", "Ngạc nhiên / Kinh ngạc", "Surprised / Amazed", "paek-chai", "adjective", "Tâm lý", "ຂ້ອຍແປກໃຈຫຼາຍ", "Tôi rất ngạc nhiên"),
        ("ອີ່ຕົນ", "Thương xót / Trắc ẩn", "Pity / Compassion", "ee-ton", "verb", "Tâm lý", "ອີ່ຕົນຄົນທຸກຍາກ", "Thương xót người nghèo khó"),
        ("ພູມໃຈ", "Tự hào / Hãnh diện", "Proud", "phuum-chai", "adjective", "Tâm lý", "ພູມໃຈໃນປະເທດຊາດ", "Tự hào về đất nước"),
        ("ນ້ອຍໃຈ", "Tủi thân / Hờn dỗi", "Hurt feelings / Sulky", "nawy-chai", "adjective", "Tâm lý", "ຢ່ານ້ອຍໃຈເລີຍ", "Đừng tủi thân nữa mà"),
    ]
    new_records.extend(chai_group)

    # 2. NHÓM ĐỒ DÙNG & KHÔNG GIAN GIA ĐÌNH VỚI 'ເຮືອນ', 'ຫ້ອງ'
    home_group = [
        ("ເຮືອນພັກ", "Nhà nghỉ", "Guesthouse", "heuan-phak", "noun", "Nơi chốn", "ພັກຢູ່ເຮືອນພັກ", "Nghỉ tại nhà nghỉ"),
        ("ເຮືອນຄົວ", "Nhà bếp", "Kitchen house", "heuan-khua", "noun", "Gia đình", "ແຕ່ງກິນຢູ່ເຮືອນຄົວ", "Nấu ăn ở nhà bếp"),
        ("ເຮືອນໄມ້", "Nhà sàn gỗ truyền thống", "Wooden house", "heuan-mai", "noun", "Kiến trúc", "ເຮືອນໄມ້ແບບລາວ", "Nhà gỗ phong cách Lào"),
        ("ເຮືອນກໍ່", "Nhà xây gạch", "Brick house", "heuan-kaw", "noun", "Kiến trúc", "ເຮືອນກໍ່ສອງຊັ້ນ", "Nhà xây hai tầng"),
        ("ເຮືອນຊານ", "Nhà cửa", "Household / Homestead", "heuan-xaan", "noun", "Gia đình", "ປຸກເຮືອນຊານ", "Xây dựng nhà cửa"),
        ("ເຈົ້າຂອງເຮືອນ", "Chủ nhà", "Homeowner / Landlord", "chao-khawng-heuan", "noun", "Xã hội", "ເຈົ້າຂອງເຮືອນໃຈດີ", "Chủ nhà tốt tính"),
        ("ຫ້ອງນ້ຳສະອາດ", "Nhà vệ sinh sạch sẽ", "Clean restroom", "hawng-nam-sa-aat", "noun", "Nơi chốn", "ຫ້ອງນ້ຳສະອາດດີ", "Nhà vệ sinh rất sạch"),
        ("ຫ້ອງທົດລອງ", "Phòng thí nghiệm", "Laboratory", "hawng-thot-lawng", "noun", "Khoa học", "ຫ້ອງທົດລອງເຄມີ", "Phòng thí nghiệm hóa học"),
        ("ຫ້ອງປະຊຸມ", "Phòng họp", "Meeting room / Conference room", "hawng-pa-xum", "noun", "Công sở", "ປະຊຸມໃນຫ້ອງປະຊຸມ", "Họp trong phòng họp"),
        ("ຫ້ອງເຮັດວຽກ", "Phòng làm việc", "Work office / Study", "hawng-het-viak", "noun", "Công sở", "ຢູ່ໃນຫ້ອງເຮັດວຽກ", "Đang ở phòng làm việc"),
        ("ຫ້ອງສະໝຸດໂຮງຮຽນ", "Thư viện trường học", "School library", "hawng-sa-mut-hoong-hian", "noun", "Giáo dục", "ອ່ານປຶ້ມຢູ່ຫ້ອງສະໝຸດ", "Đọc sách ở thư viện trường"),
        ("ໂຮງພິມ", "Nhà in / Xưởng in", "Printing house", "hoong-phim", "noun", "Sản xuất", "ພິມປຶ້ມຢູ່ໂຮງພິມ", "In sách ở nhà in"),
        ("ໂຮງລະຄອນ", "Nhà hát", "Theater", "hoong-la-khawn", "noun", "Văn hóa", "ຊົມການສະແດງຢູ່ໂຮງລະຄອນ", "Xem biểu diễn ở nhà hát"),
    ]
    new_records.extend(home_group)

    # 3. NHÓM GIAO THÔNG, XE CỘ & PHƯƠNG TIỆN
    transport_group = [
        ("ລົດເກັງ", "Xe con / Xe hơi 4 chỗ", "Sedan car", "lot-keng", "noun", "Giao thông", "ຂີ່ລົດເກັງ", "Đi xe con"),
        ("ລົດກະບະ", "Xe bán tải (phổ biến tại Lào)", "Pickup truck", "lot-ka-ba", "noun", "Giao thông", "ລົດກະບະແລ່ນຂຶ້ນພູ", "Xe bán tải leo đèo"),
        ("ລົດບັນທຸກ", "Xe tải", "Truck / Lorry", "lot-ban-thuk", "noun", "Giao thông", "ລົດບັນທຸກຂົນສົ່ງສິນຄ້າ", "Xe tải chở hàng hóa"),
        ("ລົດດັບເພີງ", "Xe cứu hỏa", "Fire truck", "lot-dap-phoeng", "noun", "Giao thông", "ລົດດັບເພີງມອດໄຟ", "Xe cứu hỏa dập tắt đám cháy"),
        ("ລົດຕູ້", "Xe 16 chỗ / Xe Van", "Van / Minibus", "lot-tuu", "noun", "Giao thông", "ເຊົ່າລົດຕູ້ໄປທ່ຽວ", "Thuê xe van đi du lịch"),
        ("ຄ່າລົດ", "Tiền vé xe / Cước xe", "Bus/Car fare", "khaa-lot", "noun", "Giao thông", "ຈ່າຍຄ່າລົດ", "Trả tiền cước xe"),
        ("ຄ່ານ້ຳມັນ", "Tiền xăng dầu", "Fuel cost", "khaa-nam-man", "noun", "Giao thông", "ຄ່ານ້ຳມັນແພງ", "Tiền xăng dầu đắt"),
        ("ປ້ຳນ້ຳມັນ", "Cây xăng / Trạm xăng", "Gas station", "pam-nam-man", "noun", "Giao thông", "ແວ່ປ້ຳນ້ຳມັນ", "Ghé trạm đổ xăng"),
        ("ປີ້ລົດໄຟຄວາມໄວສູງ", "Vé tàu cao tốc Lào - Trung", "High-speed rail ticket", "pee-lot-fai-khuaam-vai-suung", "noun", "Giao thông", "ຊື້ປີ້ລົດໄຟຄວາມໄວສູງ", "Mua vé tàu cao tốc Lào - Trung"),
        ("ຂີ່ເຮືອ", "Đi thuyền / Chèo thuyền", "To ride a boat", "khee-heua", "verb", "Giao thông", "ຂີ່ເຮືອຊົມວິວ", "Đi thuyền ngắm cảnh"),
        ("ຂັບລົດ", "Lái xe", "To drive a car", "khap-lot", "verb", "Giao thông", "ຂັບລົດດ້ວຍຄວາມລະມັດລະວັງ", "Lái xe cẩn thận"),
        ("ຂັບຂີ່ປອດໄພ", "Lái xe an toàn", "Drive safely", "khap-khee-pawt-fai", "phrase", "Giao thông", "ຂໍໃຫ້ຂັບຂີ່ປອດໄພ", "Chúc lái xe an toàn"),
        ("ໃບຂັບຂີ່", "Bằng lái xe / Giấy phép lái xe", "Driver's license", "bai-khap-khee", "noun", "Giao thông", "ກວດໃບຂັບຂີ່", "Kiểm tra bằng lái"),
    ]
    new_records.extend(transport_group)

    # 4. NHÓM TỰ NHIÊN, VẬT CHẤT & NĂNG LƯỢNG
    nature_group = [
        ("ນ້ຳຕາ", "Nước mắt", "Tears", "nam-taa", "noun", "Cơ thể", "ນ້ຳຕາໄຫຼ", "Nước mắt tuôn rơi"),
        ("ນ້ຳເຫື່ອ", "Mồ hôi", "Sweat", "nam-huea", "noun", "Cơ thể", "ນ້ຳເຫື່ອໄຫຼຍ້ອຍ", "Mồ hôi nhễ nhại"),
        ("ນ້ຳໃຈ", "Tấm lòng / Tinh thần", "Spirit / Goodwill", "nam-chai", "noun", "Đạo đức", "ນ້ຳໃຈເອື້ອເຟື້ອ", "Tấm lòng rộng mở san sẻ"),
        ("ນ້ຳຕົກຕາດ", "Thác nước", "Waterfall", "nam-tok-taat", "noun", "Tự nhiên", "ນ້ຳຕົກຕາດງາມຫຼາຍ", "Thác nước tuyệt đẹp"),
        ("ນ້ຳຖ້ວມ", "Lũ lụt / Ngập úng", "Flood", "nam-thuam", "noun", "Thiên tai", "ລະວັງນ້ຳຖ້ວມ", "Đề phòng lũ lụt"),
        ("ນ້ຳມັນ", "Dầu ăn / Xăng dầu", "Oil / Fuel", "nam-man", "noun", "Nhiên liệu", "ນ້ຳມັນພືດ", "Dầu thực vật"),
        ("ໄຟຟ້າ", "Điện năng / Điện lực", "Electricity", "fai-faa", "noun", "Năng lượng", "ໄຟຟ້າລາວ", "Điện lực Quốc gia Lào (EDL)"),
        ("ດອກໄຟ", "Bóng đèn điện", "Light bulb", "dawk-fai", "noun", "Gia dụng", "ປ່ຽນດອກໄຟ", "Thay bóng đèn"),
        ("ໄຟສາຍ", "Đèn pin", "Flashlight / Torch", "fai-saai", "noun", "Gia dụng", "ເຍືອງໄຟສາຍ", "Soi đèn pin"),
        ("ແຜ່ນດິນ", "Đất đai / Mặt đất", "Earth / Land", "phaen-din", "noun", "Tự nhiên", "ແຜ່ນດິນອຸດົມສົມບູນ", "Đất đai màu mỡ trù phú"),
        ("ແຜ່ນດິນໄຫວ", "Động đất", "Earthquake", "phaen-din-vai", "noun", "Thiên tai", "ເກີດແຜ່ນດິນໄຫວ", "Xảy ra động đất"),
        ("ພູເຂົາໄຟ", "Núi lửa", "Volcano", "phuu-khao-fai", "noun", "Tự nhiên", "ພູເຂົາໄຟລະເບີດ", "Núi lửa phun trào"),
        ("ອາກາດສົດຊື່ນ", "Không khí trong lành", "Fresh air", "aa-kaat-sot-xuen", "noun", "Tự nhiên", "ຫາຍໃຈເອົາອາກາດສົດຊື່ນ", "Hít thở không khí trong lành"),
    ]
    new_records.extend(nature_group)

    # 5. NHÓM CƠ THỂ, TAY CHÂN & CỬ CHỈ
    body_action = [
        ("ມືຖື", "Điện thoại di động", "Mobile phone / Cellphone", "mue-theu", "noun", "Công nghệ", "ຫຼິ້ນມືຖື", "Bấm điện thoại di động"),
        ("ມືຂວາ", "Tay phải", "Right hand", "mue-khwaa", "noun", "Cơ thể", "ຍົກມືຂວາ", "Giơ tay phải"),
        ("ມືຊ້າຍ", "Tay trái", "Left hand", "mue-saai", "noun", "Cơ thể", "ໃຊ້ມືຊ້າຍ", "Dùng tay trái"),
        ("ລາຍມື", "Chữ viết tay", "Handwriting", "laai-mue", "noun", "Học tập", "ລາຍມືງາມ", "Chữ viết tay đẹp"),
        ("ຕາເວັນອອກ", "Hướng Đông / Mặt trời mọc", "East / Sunrise", "taa-ven-awk", "noun", "Phương hướng", "ທິດທາງຕາເວັນອອກ", "Hướng mặt trời mọc (hướng Đông)"),
        ("ຕາເວັນຕົກ", "Hướng Tây / Mặt trời lặn", "West / Sunset", "taa-ven-tok", "noun", "Phương hướng", "ທິດທາງຕາເວັນຕົກ", "Hướng Tây"),
        ("ທິດເໜືອ", "Hướng Bắc", "North", "thit-nuea", "noun", "Phương hướng", "ພາກເໜືອຂອງລາວ", "Miền Bắc nước Lào"),
        ("ທິດໃຕ້", "Hướng Nam", "South", "thit-tai", "noun", "Phương hướng", "ພາກໃຕ້ຂອງລາວ", "Miền Nam nước Lào"),
        ("ສົບ", "Môi", "Lips", "sop", "noun", "Cơ thể", "ຮິມສົບ", "Bờ môi"),
        ("ລີ້ນ", "Lưỡi", "Tongue", "leen", "noun", "Cơ thể", "ແລບລີ້ນ", "Thè lưỡi"),
        ("ຜົມ", "Tóc", "Hair", "phom", "noun", "Cơ thể", "ຜົມດຳຍາວ", "Mái tóc đen dài"),
        ("ໜວດ", "Râu mép", "Moustache", "nuat", "noun", "Cơ thể", "ໄວ້ໜວດ", "Để râu mép"),
        ("ເຄົາ", "Râu cằm", "Beard", "khao", "noun", "Cơ thể", "ໂກນເຄົາ", "Cạo râu"),
    ]
    new_records.extend(body_action)

    # 6. CHUYÊN ĐỀ GIÁO DỤC TRỰC TUYẾN & EDTECH LAO (ONLINE LEARNING)
    edtech_lao = [
        ("ການຮຽນອອນລາຍ", "Học trực tuyến (Online)", "Online learning", "kaan-hian-awn-laai", "noun", "Giáo dục trực tuyến", "ຮຽນອອນລາຍຢູ່ບ້ານ", "Học trực tuyến ở nhà"),
        ("ຫ້ອງຮຽນສະເໝືອນ", "Lớp học ảo (Virtual classroom)", "Virtual classroom", "hawng-hian-sa-muean", "noun", "Giáo dục trực tuyến", "ເຂົ້າຮ່ວມຫ້ອງຮຽນສະເໝືອນ", "Tham gia lớp học ảo"),
        ("ການສອນທາງໄກ", "Giảng dạy từ xa (Distance learning)", "Distance education", "kaan-sawn-thaang-kai", "noun", "Giáo dục trực tuyến", "ລະບົບການສອນທາງໄກ", "Hệ thống đào tạo từ xa"),
        ("ບົດຝຶກຫັດ", "Bài tập thực hành", "Exercise / Practice worksheet", "bot-fuek-hat", "noun", "Học tập", "ແກ້ບົດຝຶກຫັດ", "Làm bài tập rèn luyện"),
        ("ຄຳສັບ", "Từ vựng", "Vocabulary / Word", "kham-sap", "noun", "Ngôn ngữ", "ຮຽນຄຳສັບໃໝ່", "Học từ vựng mới"),
        ("ໄວຍາກອນ", "Ngữ pháp", "Grammar", "vai-yaa-kawn", "noun", "Ngôn ngữ", "ໄວຍາກອນພາສາລາວ", "Ngữ pháp tiếng Lào"),
        ("ການອອກສຽງ", "Cách phát âm", "Pronunciation", "kaan-awk-siang", "noun", "Ngôn ngữ", "ຝຶກການອອກສຽງໃຫ້ຖືກ", "Luyện phát âm cho chuẩn"),
        ("ການຟັງ", "Kỹ năng nghe", "Listening skill", "kaan-fang", "noun", "Ngôn ngữ", "ຝຶກທັກສະການຟັງ", "Rèn luyện kỹ năng nghe"),
        ("ການເວົ້າ", "Kỹ năng nói", "Speaking skill", "kaan-vao", "noun", "Ngôn ngữ", "ຝຶກການເວົ້າພາສາລາວ", "Luyện nói tiếng Lào"),
        ("ການອ່ານ", "Kỹ năng đọc", "Reading skill", "kaan-aan", "noun", "Ngôn ngữ", "ການອ່ານອອກສຽງ", "Kỹ năng đọc to thành tiếng"),
        ("ການຂຽນ", "Kỹ năng viết", "Writing skill", "kaan-khian", "noun", "Ngôn ngữ", "ຝຶກການຂຽນຕົວອັກສອນ", "Luyện viết chữ cái"),
        ("ຄະແນນ", "Điểm số", "Score / Grade", "kha-naen", "noun", "Giáo dục", "ໄດ້ຄະແນນເຕັມ", "Được điểm tối đa 10/10"),
        ("ໃບປະກາດ", "Bằng tốt nghiệp", "Diploma / Degree", "bai-pa-kaat", "noun", "Giáo dục", "ຮັບໃບປະກາດສະນີຍະບັດ", "Nhận bằng tốt nghiệp"),
        ("ໃບຢັ້ງຢືນ", "Giấy chứng nhận / Chứng chỉ", "Certificate", "bai-yang-yeun", "noun", "Giáo dục", "ໃບຢັ້ງຢືນການຮຽນຈົບ", "Chứng chỉ hoàn thành khóa học"),
        ("ແຟລດກາດ", "Thẻ từ vựng flashcard", "Flashcard", "flaat-kaat", "noun", "Giáo dục trực tuyến", "ຮຽນດ້ວຍແຟລດກາດ", "Học ngoại ngữ bằng thẻ flashcard"),
        ("ການທົບທວນ", "Sự ôn tập", "Revision / Review", "kaan-thop-thuan", "noun", "Học tập", "ທົບທວນບົດຮຽນເກົ່າ", "Ôn lại bài học cũ"),
        ("ການແປພາສາ", "Biên dịch / Dịch thuật", "Translation", "kaan-pae-phaa-saa", "noun", "Ngôn ngữ", "ການແປພາສາລາວ-ຫວຽດ", "Dịch thuật Lào - Việt"),
        ("ວັດຈະນານຸກົມ", "Từ điển", "Dictionary", "vat-cha-naa-nu-kom", "noun", "Ngôn ngữ", "ເປີດວັດຈະນານຸກົມ", "Tra cứu từ điển"),
        ("ຕົວອັກສອນ", "Ký tự / Chữ cái", "Alphabet / Character", "tua-ak-sawn", "noun", "Ngôn ngữ", "ພະຍັນຊະນະແລະສະຫຼະ", "Phụ âm và nguyên âm"),
        ("ພະຍັນຊະນະ", "Phụ âm", "Consonant", "pha-nyan-xa-na", "noun", "Ngôn ngữ", "ພະຍັນຊະນະພາສາລາວ", "Bảng phụ âm tiếng Lào"),
        ("ສະຫຼະ", "Nguyên âm", "Vowel", "sa-la", "noun", "Ngôn ngữ", "ສະຫຼະສຽງສັ້ນແລະສຽງຍາວ", "Nguyên âm ngắn và nguyên âm dài"),
        ("ວັນນະຍຸດ", "Dấu thanh điệu", "Tone marks", "van-na-nyut", "noun", "Ngôn ngữ", "ໄມ້ເອກແລະໄມ້ໂທ", "Dấu Mai Ek và Mai Tho"),
    ]
    new_records.extend(edtech_lao)

    # 7. HỆ THỐNG SỐ ĐẾM MỞ RỘNG (100 - 1,000,000 & SỐ THỨ TỰ)
    numbers_extended = [
        ("ທີໜຶ່ງ", "Thứ nhất / Hạng nhất", "First / Number one", "thee-neung", "number", "Số thứ tự", "ບົດຮຽນທີໜຶ່ງ", "Bài học thứ nhất"),
        ("ທີສອງ", "Thứ hai / Hạng nhì", "Second", "thee-sawng", "number", "Số thứ tự", "ອັນດັບທີສອງ", "Xếp hạng thứ hai"),
        ("ທີສາມ", "Thứ ba / Hạng ba", "Third", "thee-saam", "number", "Số thứ tự", "ລາງວັນທີສາມ", "Giải ba"),
        ("ທີສີ່", "Thứ tư", "Fourth", "thee-see", "number", "Số thứ tự", "ບົດທີສີ່", "Chương thứ tư"),
        ("ທີຫ້າ", "Thứ năm", "Fifth", "thee-haa", "number", "Số thứ tự", "ຊັ້ນທີຫ້າ", "Tầng thứ năm"),
        ("ສອງຮ້ອຍ", "Hai trăm", "Two hundred", "sawng-hway", "number", "Số đếm", "ສອງຮ້ອຍຄົນ", "Hai trăm người"),
        ("ສາມຮ້ອຍ", "Ba trăm", "Three hundred", "saam-hway", "number", "Số đếm", "ສາມຮ້ອຍກີບ", "Ba trăm Kíp"),
        ("ສີ່ຮ້ອຍ", "Bốn trăm", "Four hundred", "see-hway", "number", "Số đếm", "ສີ່ຮ້ອຍແມັດ", "Bốn trăm mét"),
        ("ຫ້າຮ້ອຍ", "Năm trăm", "Five hundred", "haa-hway", "number", "Số đếm", "ຫ້າຮ້ອຍພັນ", "Năm trăm nghìn"),
        ("ຫົກຮ້ອຍ", "Sáu trăm", "Six hundred", "hok-hway", "number", "Số đếm", "ຫົກຮ້ອຍປີ", "Sáu trăm năm"),
        ("ເຈັດຮ້ອຍ", "Bảy trăm", "Seven hundred", "chet-hway", "number", "Số đếm", "ເຈັດຮ້ອຍວັນ", "Bảy trăm ngày"),
        ("ແປດຮ້ອຍ", "Tám trăm", "Eight hundred", "paet-hway", "number", "Số đếm", "ແປດຮ້ອຍອັນ", "Tám trăm chiếc"),
        ("ເກົ້າຮ້ອຍ", "Chín trăm", "Nine hundred", "kao-hway", "number", "Số đếm", "ເກົ້າຮ້ອຍກິໂລ", "Chín trăm cân"),
        ("ສອງພັນ", "Hai nghìn", "Two thousand", "sawng-phan", "number", "Số đếm", "ສອງພັນປີ", "Hai nghìn năm"),
        ("ຫ້າພັນ", "Năm nghìn", "Five thousand", "haa-phan", "number", "Số đếm", "ຫ້າພັນກີບ", "Năm nghìn Kíp"),
        ("ສິບພັນ", "Mười nghìn", "Ten thousand", "sip-phan", "number", "Số đếm", "ສິບພັນກີບ", "Mười nghìn Kíp"),
        ("ຫ້າສິບພັນ", "Năm mươi nghìn", "Fifty thousand", "haa-sip-phan", "number", "Số đếm", "ຫ້າສິບພັນກີບ", "Năm mươi nghìn Kíp"),
        ("ໜຶ່ງລ້ານ", "Một triệu", "One million", "neung-laan", "number", "Số đếm", "ໜຶ່ງລ້ານກີບ", "Một triệu Kíp"),
        ("ສິບລ້ານ", "Mười triệu", "Ten million", "sip-laan", "number", "Số đếm", "ສິບລ້ານຄົນ", "Mười triệu dân"),
        ("ຮ້ອຍສ່ວນຮ້ອຍ", "Một trăm phần trăm (100%)", "One hundred percent", "hway-suan-hway", "phrase", "Tỷ lệ", "ຖືກຕ້ອງຮ້ອຍສ່ວນຮ້ອຍ", "Chính xác một trăm phần trăm"),
    ]
    new_records.extend(numbers_extended)

    # 8. CÁC TỔ HỢP ĐỘNG TỪ GHÉP THƯỜNG GẶP (COMPLEX VERBAL PHRASES)
    verbal_phrases = [
        ("ໄປທ່ຽວ", "Đi du lịch / Đi chơi", "To travel / To go out", "pai-thiaao", "verb", "Du lịch", "ໄປທ່ຽວວັງວຽງ", "Đi du lịch Vang Vieng"),
        ("ໄປຮຽນ", "Đi học", "To go to school", "pai-hian", "verb", "Học tập", "ໄປຮຽນແຕ່ເຊົ້າ", "Đi học từ sáng sớm"),
        ("ໄປເຮັດວຽກ", "Đi làm việc", "To go to work", "pai-het-viak", "verb", "Công việc", "ຂີ່ລົດໄປເຮັດວຽກ", "Đi xe đi làm"),
        ("ໄປຕະຫຼາດ", "Đi chợ", "To go to market", "pai-ta-laat", "verb", "Mua sắm", "ແມ່ໄປຕະຫຼາດ", "Mẹ đi chợ mua đồ"),
        ("ໄປໂຮງໝໍ", "Đi bệnh viện", "To go to hospital", "pai-hoong-maw", "verb", "Y tế", "ພາຄົນເຈັບໄປໂຮງໝໍ", "Đưa bệnh nhân tới bệnh viện"),
        ("ໄປວັດ", "Đi chùa lễ Phật", "To go to temple", "pai-vat", "verb", "Văn hóa", "ຕັກບາດຢູ່ວັດ", "Lễ bái cúng dường ở chùa"),
        ("ໄປສະໜາມບິນ", "Đi ra sân bay", "To go to airport", "pai-sa-naam-bin", "verb", "Giao thông", "ໄປສະໜາມບິນຮັບແຂກ", "Ra sân bay đón khách"),
        ("ໄປກິນເຂົ້າ", "Đi ăn cơm", "To go have a meal", "pai-kin-khao", "verb", "Ẩm thực", "ໄປກິນເຂົ້ານຳກັນ", "Đi ăn cơm cùng nhau"),
        ("ໄປຊື້ເຄື່ອງ", "Đi mua sắm", "To go shopping", "pai-seu-khueang", "verb", "Mua sắm", "ໄປຊື້ເຄື່ອງຢູ່ຫ້າງ", "Đi mua sắm ở siêu thị"),
        ("ໄປນອນ", "Đi ngủ", "To go to bed", "pai-nawn", "verb", "Đời sống", "ຮອດເວລານອນແລ້ວ", "Đến giờ đi ngủ rồi"),
        ("ໄປຫຼິ້ນ", "Đi chơi", "To go hang out", "pai-lin", "verb", "Giải trí", "ໄປຫຼິ້ນບ້ານໝູ່", "Đi chơi nhà bạn"),
        ("ມາຮອດ", "Tới nơi / Về đến", "To arrive", "maa-hawt", "verb", "Giao thông", "ມາຮອດສະບາຍດີ", "Đã đến nơi bình an"),
        ("ມາຢາມ", "Đến thăm / Ghé chơi", "To visit", "maa-yaam", "verb", "Xã hội", "ໝູ່ມາຢາມບ້ານ", "Bạn bè ghé thăm nhà"),
        ("ມາຊ່ວຍ", "Đến giúp sức", "To come to help", "maa-xuay", "verb", "Xã hội", "ມາຊ່ວຍວຽກງານ", "Đến giúp đỡ công việc"),
        ("ມາພົບ", "Đến gặp mặt", "To come to meet", "maa-phop", "verb", "Giao tiếp", "ມາພົບອາຈານ", "Đến gặp thầy giáo"),
        ("ຢາກກິນ", "Muốn ăn / Thèm ăn", "Want to eat", "yaak-kin", "verb", "Nhu cầu", "ຢາກກິນຕຳໝາກຮຸ່ງ", "Muốn ăn nộm đu đủ"),
        ("ຢາກດື່ມ", "Muốn uống", "Want to drink", "yaak-duem", "verb", "Nhu cầu", "ຢາກດື່ມກາເຟ", "Muốn uống cà phê"),
        ("ຢາກຮູ້", "Muốn biết / Tò mò", "Want to know", "yaak-huu", "verb", "Nhận thức", "ຢາກຮູ້ຄວາມຈິງ", "Muốn biết sự thật"),
        ("ຢາກໄດ້", "Muốn có / Mong muốn", "Want to get / have", "yaak-dai", "verb", "Nhu cầu", "ຢາກໄດ້ປຶ້ມເຫຼັ້ມນີ້", "Muốn có quyển sách này"),
        ("ຢາກພັກຜ່ອນ", "Muốn nghỉ ngơi", "Want to rest", "yaak-phak-phawn", "verb", "Nhu cầu", "ເມື່ອຍແລ້ວຢາກພັກຜ່ອນ", "Mệt rồi muốn nghỉ ngơi"),
        ("ມັກກິນ", "Thích ăn", "Like to eat", "mak-kin", "verb", "Sở thích", "ມັກກິນເຂົ້າໜຽວ", "Thích ăn xôi nếp"),
        ("ມັກໄປ", "Thích đi du lịch", "Like to go", "mak-pai", "verb", "Sở thích", "ມັກໄປທ່ຽວພູດອຍ", "Thích đi du lịch vùng núi"),
        ("ມັກອ່ານ", "Thích đọc sách", "Like to read", "mak-aan", "verb", "Sở thích", "ມັກອ່ານວັນນະຄະດີ", "Thích đọc văn học"),
        ("ມັກຫຼິ້ນ", "Thích chơi", "Like to play", "mak-lin", "verb", "Sở thích", "ມັກຫຼິ້ນດົນຕີ", "Thích chơi nhạc cụ"),
        ("ຮັກແພງ", "Thương yêu / Quý mến", "Cherish / Love dearly", "hak-phaeng", "verb", "Cảm xúc", "ຮັກແພງກັນເໝືອນພີ່ນ້ອງ", "Thương yêu nhau như anh em ruột"),
        ("ຮັກຊາດ", "Yêu nước / Lòng yêu nước", "Patriotic / Patriotism", "hak-xaat", "verb", "Đạo đức", "ປະຊາຊົນຮັກຊາດ", "Nhân dân yêu nước"),
        ("ຮັກບ້ານເກີດ", "Yêu quê hương", "Love hometown", "hak-baan-koet", "verb", "Cảm xúc", "ຮັກບ້ານເກີດເມືອງນອນ", "Yêu quê cha đất tổ"),
    ]
    new_records.extend(verbal_phrases)

    # 9. TỔNG HỢP VÀ THÊM VÀO KHO TỪ ĐIỂN
    added = 0
    for item in new_records:
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

    # Sắp xếp từ điển theo thứ tự bảng chữ cái Unicode tiếng Lào
    sorted_words = sorted(entries.keys())
    
    with open(dict_file, mode="w", encoding="utf-8", newline="") as f:
        fieldnames = ["lao", "vi", "en", "romanization", "pos", "lesson", "example_lao", "example_vi"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for w in sorted_words:
            writer.writerow(entries[w])
            
    print(f"[+] KẾT QUẢ MỞ RỘNG TỪ ĐIỂN QUY MÔ LỚN:")
    print(f"    - Đã nạp thêm đợt này: {added} từ mới.")
    print(f"    - TỔNG DUNG LƯỢNG KHO TỪ ĐIỂN HIỆN TẠI: {len(sorted_words)} MỤC TỪ CHUẨN NFC.")


if __name__ == "__main__":
    build_massive_dictionary()
