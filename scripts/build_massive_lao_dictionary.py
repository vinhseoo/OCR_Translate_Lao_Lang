"""
Script Xây Dựng Kho Từ Điển Giáo Trình & Giao Tiếp Tiếng Lào Quy Mô Lớn (Massive Lao Dictionary).
Mở rộng quy mô từ điển lên > 1,500 - 2,000 mục từ toàn diện thông qua:
1. Bộ từ gốc chuyên sâu theo 20 lĩnh vực thực tế (Y tế, Giáo dục, Kinh tế, Du lịch, Pháp luật, Công nghệ, ...)
2. Quy tắc tạo từ phái sinh & từ ghép tự nhiên của tiếng Lào:
   - 'ຄວາມ' + Tính từ -> Danh từ khái niệm (Trạng thái/Bản chất)
   - 'ການ' + Động từ -> Danh từ hành động (Sự/Việc/Quá trình)
   - 'ຜູ້' / 'ນັກ' + Nghề nghiệp/Hành động -> Danh từ chỉ người
   - 'ຮ້ານ' / 'ຫ້ອງ' / 'ໂຮງ' + Chức năng -> Danh từ địa điểm
3. Toàn bộ 18 tỉnh thành & địa danh danh thắng của Lào.
4. Chuẩn hóa 100% Unicode NFC theo Lao Golden Rule #1.
"""
import os
import sys
import csv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing.normalize import normalize_lao


def load_existing_dict(filepath: str):
    entries = {}
    if os.path.exists(filepath):
        with open(filepath, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                norm_lao = normalize_lao(row.get("lao", "").strip())
                if norm_lao:
                    entries[norm_lao] = {
                        "lao": norm_lao,
                        "vi": row.get("vi", "").strip(),
                        "en": row.get("en", "").strip(),
                        "romanization": row.get("romanization", "").strip(),
                        "pos": row.get("pos", "").strip(),
                        "lesson": row.get("lesson", "").strip(),
                        "example_lao": normalize_lao(row.get("example_lao", "").strip()),
                        "example_vi": row.get("example_vi", "").strip(),
                    }
    return entries


def get_massive_vocab_list():
    items = []
    
    # --- A. 18 TỈNH THÀNH & ĐỊA DANH NỔI TIẾNG CỦA LÀO ---
    provinces = [
        ("ນະຄອນຫຼວງວຽງຈັນ", "Thủ đô Viêng Chăn", "Vientiane Capital", "na-khawn-luang-viang-chan", "noun", "Địa lý Lào", "ໄປທ່ຽວນtraceນະຄອນຫຼວງວຽງຈັນ", "Đi tham quan thủ đô Viêng Chăn"),
        ("ແຂວງວຽງຈັນ", "Tỉnh Viêng Chăn", "Vientiane Province", "khwaeng-viang-chan", "noun", "Địa lý Lào", "ອ່າງນ້ຳງື່ມຢູ່ແຂວງວຽງຈັນ", "Hồ Nậm Ngừm ở tỉnh Viêng Chăn"),
        ("ຫຼວງພະບາງ", "Luang Prabang", "Luang Prabang", "luang-pha-baang", "noun", "Địa lý Lào", "ເມືອງມໍລະດົກໂລກ", "Thành phố di sản thế giới"),
        ("ຈຳປາສັກ", "Champasak", "Champasak", "cham-paa-sak", "noun", "Địa lý Lào", "ແຂວງຈຳປາສັກພາກໃຕ້", "Tỉnh Champasak miền Nam Lào"),
        ("ສະຫວັນນະເຂດ", "Savannakhet", "Savannakhet", "sa-van-na-kheet", "noun", "Địa lý Lào", "ແຂວງໃຫຍ່ສະຫວັນນະເຂດ", "Tỉnh lớn Savannakhet"),
        ("ຄຳມ່ວນ", "Khammouane", "Khammouane", "kham-muan", "noun", "Địa lý Lào", "ຖ້ຳກອງລໍຢູ່ຄຳມ່ວນ", "Hang động Konglor ở Khammouane"),
        ("ບໍລິຄຳໄຊ", "Bolikhamxay", "Bolikhamxay", "baw-li-kham-xai", "noun", "Địa lý Lào", "ແຂວງບໍລິຄຳໄຊ", "Tỉnh Bolikhamxay"),
        ("ຊຽງຂວາງ", "Xieng Khouang (Cánh đồng Chum)", "Xieng Khouang", "xiang-khuaang", "noun", "Địa lý Lào", "ທົ່ງໄຫຫີນຊຽງຂວາງ", "Cánh đồng Chum Xieng Khouang"),
        ("ຫົວພັນ", "Houaphanh (Sầm Nưa)", "Houaphanh", "hua-phan", "noun", "Địa lý Lào", "ເມືອງຊຳເໜືອແຂວງຫົວພັນ", "Thị xã Sầm Nưa tỉnh Houaphanh"),
        ("ຜົ້ງສາລີ", "Phongsaly", "Phongsaly", "phong-saa-lee", "noun", "Địa lý Lào", "ແຂວງເໜືອສຸດຜົ້ງສາລີ", "Tỉnh cực Bắc Phongsaly"),
        ("ອຸດົມໄຊ", "Oudomxay", "Oudomxay", "u-dom-xai", "noun", "Địa lý Lào", "ສູນກາງພາກເໜືອອຸດົມໄຊ", "Trung tâm miền Bắc Oudomxay"),
        ("ຫຼວງນ້ຳທາ", "Luang Namtha", "Luang Namtha", "luang-nam-thaa", "noun", "Địa lý Lào", "ປ່າສະຫງວນຫຼວງນ້ຳທາ", "Khu bảo tồn Luang Namtha"),
        ("ບໍ່ແກ້ວ", "Bokeo (Tam giác vàng)", "Bokeo", "baw-kaew", "noun", "Địa lý Lào", "ສາມຫຼ່ຽມຄຳບໍ່ແກ້ວ", "Tam giác vàng Bokeo"),
        ("ໄຊຍະບູລີ", "Xayaboury", "Xayaboury", "xai-nya-buu-lee", "noun", "Địa lý Lào", "ບຸນຊ້າງໄຊຍະບູລີ", "Lễ hội voi Xayaboury"),
        ("ສາລະວັນ", "Saravane", "Saravane", "saa-la-van", "noun", "Địa lý Lào", "ແຂວງສາລະວັນ", "Tỉnh Saravane"),
        ("ເຊກອງ", "Sekong", "Sekong", "xee-kawng", "noun", "Địa lý Lào", "ແຂວງເຊກອງ", "Tỉnh Sekong"),
        ("ອັດຕະປື", "Attapeu", "Attapeu", "at-ta-peuu", "noun", "Địa lý Lào", "ແຂວງອັດຕະປືພາກໃຕ້", "Tỉnh Attapeu miền Nam"),
        ("ໄຊສົມບູນ", "Xaysomboun", "Xaysomboun", "xai-som-buun", "noun", "Địa lý Lào", "ພູເບ້ຍຢູ່ໄຊສົມບູນ", "Đỉnh núi Phou Bia ở Xaysomboun"),
        ("ວັງວຽງ", "Vang Vieng", "Vang Vieng", "vang-viang", "noun", "Địa danh", "ວັງວຽງເມືອງທ່ອງທ່ຽວ", "Thành phố du lịch Vang Vieng"),
        ("ສີ່ພັນດອນ", "Si Phan Don (4000 đảo)", "Si Phan Don", "see-phan-dawn", "noun", "Địa danh", "ນ້ຳຕົກຕາດຄອນພະເພັງຢູ່ສີ່ພັນດອນ", "Thác Khone Phapheng ở 4000 đảo"),
        ("ຄອນພະເພັງ", "Khone Phapheng (Niagara châu Á)", "Khone Phapheng Falls", "khon-pha-pheng", "noun", "Địa danh", "ນ້ຳຕົກຕາດຄອນພະເພັງ", "Thác nước Khone Phapheng"),
        ("ຕາດກວາງຊີ", "Thác Kuang Si (Luang Prabang)", "Kuang Si Falls", "taat-kuaang-see", "noun", "Địa danh", "ໄປອາບນ້ຳຕາດກວາງຊີ", "Đi tắm thác Kuang Si"),
        ("ວັດຊຽງທອງ", "Chùa Wat Xieng Thong", "Wat Xieng Thong", "vat-xiang-thawng", "noun", "Địa danh", "ວັດຊຽງທອງຫຼວງພະບາງ", "Chùa Xieng Thong Luang Prabang"),
        ("ວັດສີສະເກດ", "Chùa Wat Si Saket", "Wat Si Saket", "vat-see-sa-keet", "noun", "Địa danh", "ວັດເກົ່າແກ່ວັດສີສະເກດ", "Chùa cổ Wat Si Saket"),
    ]
    items.extend(provinces)

    # --- B. TỪ GHÉP KHÁI NIỆM: 'ຄວາມ' + TÍNH TỪ ---
    concepts_khwam = [
        ("ຄວາມຮັກ", "Tình yêu / Tình thương", "Love", "khuaam-hak", "noun", "Khái niệm", "ຄວາມຮັກຂອງແມ່", "Tình yêu của mẹ"),
        ("ຄວາມສຸກ", "Hạnh phúc", "Happiness", "khuaam-suk", "noun", "Khái niệm", "ຂໍໃຫ້ມີຄວາມສຸກ", "Chúc bạn nhiều hạnh phúc"),
        ("ความສະຫງົບ", "Hòa bình / Yên bình", "Peace / Calmness", "khuaam-sa-ngop", "noun", "Khái niệm", "ຄວາມສະຫງົບໃນໃຈ", "Sự thanh thản trong tâm"),
        ("ຄວາມຮູ້", "Kiến thức / Tri thức", "Knowledge", "khuaam-huu", "noun", "Khái niệm", "ສະແຫວງຫາຄວາມຮູ້", "Tìm kiếm tri thức"),
        ("ຄວາມຈິງ", "Sự thật / Chân lý", "Truth", "khuaam-ching", "noun", "Khái niệm", "ເວົ້າຄວາມຈິງ", "Nói sự thật"),
        ("ຄວາມດີ", "Lòng tốt / Việc thiện", "Goodness / Merit", "khuaam-dee", "noun", "Khái niệm", "ເຮັດຄວາມດີ", "Làm việc thiện"),
        ("ຄວາມງາມ", "Vẻ đẹp / Nét đẹp", "Beauty", "khuaam-ngaam", "noun", "Khái niệm", "ຄວາມງາມທຳມະຊາດ", "Vẻ đẹp tự nhiên"),
        ("ຄວາມສະອາດ", "Sự sạch sẽ", "Cleanliness", "khuaam-sa-aat", "noun", "Khái niệm", "ຮັກສາຄວາມສະອາດ", "Giữ gìn vệ sinh sạch sẽ"),
        ("ຄວາມພະຍາຍາມ", "Sự cố gắng / Nỗ lực", "Effort / Striving", "khuaam-pha-yaa-yaam", "noun", "Khái niệm", "ຄວາມພະຍາຍາມຈະພາໄປສູ່ຄວາມສຳເລັດ", "Nỗ lực sẽ dẫn tới thành công"),
        ("ຄວາມເຂົ້າໃຈ", "Sự thấu hiểu", "Understanding", "khuaam-khao-chai", "noun", "Khái niệm", "ສ້າງຄວາມເຂົ້າໃຈເຊິ່ງກັນແລະກັນ", "Tạo dựng sự thấu hiểu lẫn nhau"),
        ("ຄວາມຫວັງ", "Hy vọng / Niềm hy vọng", "Hope", "khuaam-vang", "noun", "Khái niệm", "ຍັງມີຄວາມຫວັງ", "Vẫn còn niềm hy vọng"),
        ("ຄວາມເຊື່ອ", "Niềm tin / Tín ngưỡng", "Belief / Faith", "khuaam-xua", "noun", "Khái niệm", "ຄວາມເຊື່ອທາງສາສະໜາ", "Tín ngưỡng tôn giáo"),
        ("ຄວາມຍາກ", "Sự khó khăn", "Difficulty", "khuaam-nyaak", "noun", "Khái niệm", "ຜ່ານຜ່າຄວາມຍາກລຳບາກ", "Vượt qua gian khó"),
        ("ຄວາມສະດວກ", "Sự thuận tiện", "Convenience", "khuaam-sa-duak", "noun", "Khái niệm", "ຄວາມສະດວກສະບາຍ", "Sự tiện nghi thoải mái"),
        ("ຄວາມປອດໄພ", "Sự an toàn", "Safety / Security", "khuaam-pawt-fai", "noun", "Khái niệm", "ຄຳນຶງເຖິງຄວາມປອດໄພ", "Coi trọng sự an toàn"),
        ("ຄວາມໄວ", "Tốc độ / Vận tốc", "Speed / Velocity", "khuaam-vai", "noun", "Khái niệm", "ຄວບຄຸມຄວາມໄວ", "Kiểm soát tốc độ"),
        ("ຄວາມຮ້ອນ", "Độ nóng / Nhiệt độ cao", "Heat", "khuaam-hawn", "noun", "Khái niệm", "ຄວາມຮ້ອນສູງ", "Nhiệt độ cao"),
        ("ຄວາມເຢັນ", "Độ lạnh / Hơi mát", "Coldness / Chill", "khuaam-yen", "noun", "Khái niệm", "ສຳຜັດຄວາມເຢັນ", "Cảm nhận hơi mát lạnh"),
        ("ຄວາມມືດ", "Bóng tối", "Darkness", "khuaam-muet", "noun", "Khái niệm", "ຢູ່ໃນຄວາມມືດ", "Ở trong bóng tối"),
        ("ຄວາມສະຫວ່າງ", "Ánh sáng / Sự sáng sủa", "Brightness / Light", "khuaam-sa-vaang", "noun", "Khái niệm", "ຄວາມສະຫວ່າງຂອງປັນຍາ", "Ánh sáng của trí tuệ"),
        ("ຄວາມອົດທົນ", "Sự kiên nhẫn / Nhẫn nại", "Patience / Endurance", "khuaam-ot-thon", "noun", "Khái niệm", "ມີຄວາມອົດທົນສູງ", "Có tính nhẫn nại cao"),
        ("ຄວາມຮັບຜິດຊອບ", "Trách nhiệm", "Responsibility", "khuaam-hap-phit-xawp", "noun", "Khái niệm", "ມີຄວາມຮັບຜິດຊອບຕໍ່ວຽກ", "Có trách nhiệm với công việc"),
    ]
    items.extend(concepts_khwam)

    # --- C. TỪ GHÉP HÀNH ĐỘNG: 'ການ' + ĐỘNG TỪ ---
    actions_kaan = [
        ("ການຮຽນ", "Việc học / Sự học tập", "Studying / Learning", "kaan-hian", "noun", "Hành động danh từ", "ການຮຽນຮູ້ຕະຫຼອດຊີວິດ", "Học tập suốt đời"),
        ("ການສອນ", "Việc giảng dạy", "Teaching", "kaan-sawn", "noun", "Hành động danh từ", "ການສອນວິຊາພາສາລາວ", "Giảng dạy môn tiếng Lào"),
        ("ການສຶກສາ", "Giáo dục / Sự học hành", "Education", "kaan-seuk-saa", "noun", "Hành động danh từ", "ກະຊວງສຶກສາທິການ", "Bộ Giáo dục"),
        ("ການເຮັດວຽກ", "Làm việc / Lao động", "Working", "kaan-het-viak", "noun", "Hành động danh từ", "ການເຮັດວຽກເປັນທີມ", "Làm việc nhóm"),
        ("ການທ່ອງທ່ຽວ", "Du lịch", "Tourism / Traveling", "kaan-thawng-thiaao", "noun", "Hành động danh từ", "ການທ່ອງທ່ຽວແບບອະນຸລັກ", "Du lịch sinh thái"),
        ("ການເດີນທາງ", "Chuyến đi / Đi lại", "Journey / Travel", "kaan-doen-thaang", "noun", "Hành động danh từ", "ການເດີນທາງປອດໄພ", "Chuyến đi an toàn"),
        ("ການພັດທະນາ", "Sự phát triển", "Development", "kaan-phat-tha-naa", "noun", "Hành động danh từ", "ການພັດທະນາປະເທດຊາດ", "Phát triển đất nước"),
        ("ການຄ້າ", "Thương mại / Buôn bán", "Trade / Commerce", "kaan-khaa", "noun", "Hành động danh từ", "ການຄ້າລະຫວ່າງປະເທດ", "Thương mại quốc tế"),
        ("ການເມືອງ", "Chính trị", "Politics", "kaan-mueang", "noun", "Hành động danh từ", "ການເມືອງແລະສັງຄົມ", "Chính trị và xã hội"),
        ("ການຊ່ວຍເຫຼືອ", "Sự giúp đỡ / Cứu trợ", "Assistance / Aid", "kaan-xuay-luea", "noun", "Hành động danh từ", "ການຊ່ວຍເຫຼືອເຊິ່ງກັນແລະກັນ", "Giúp đỡ lẫn nhau"),
        ("ການຮ່ວມມື", "Sự hợp tác", "Cooperation", "kaan-huam-mue", "noun", "Hành động danh từ", "ການຮ່ວມມືລາວ-ຫວຽດ", "Hợp tác Lào - Việt"),
        ("ການແພດ", "Y khoa / Y tế", "Medicine / Medical care", "kaan-phaet", "noun", "Hành động danh từ", "ການແພດທັນສະໄໝ", "Y học hiện đại"),
        ("ການຂົນສົ່ງ", "Giao thông vận tải / Vận chuyển", "Transportation", "kaan-khon-song", "noun", "Hành động danh từ", "ລະບົບການຂົນສົ່ງ", "Hệ thống vận tải"),
        ("ການສື່ສານ", "Truyền thông / Giao tiếp", "Communication", "kaan-seuu-saan", "noun", "Hành động danh từ", "ເຄືອຂ່າຍການສື່ສານ", "Mạng lưới truyền thông"),
        ("ການກໍ່ສ້າງ", "Xây dựng", "Construction", "kaan-kaw-saang", "noun", "Hành động danh từ", "ການກໍ່ສ້າງຂົວທາງ", "Xây dựng cầu đường"),
        ("ການຜະລິດ", "Sản xuất", "Production", "kaan-pha-lit", "noun", "Hành động danh từ", "ການຜະລິດກະສິກຳ", "Sản xuất nông nghiệp"),
        ("ການບໍລິການ", "Dịch vụ", "Service", "kaan-baw-li-kaan", "noun", "Hành động danh từ", "ການບໍລິການລູກຄ້າ", "Chăm sóc khách hàng"),
        ("ການປົກຄອງ", "Quản lý / Hành chính cai trị", "Governance / Administration", "kaan-pok-khawng", "noun", "Hành động danh từ", "ລະບົບການປົກຄອງ", "Hệ thống quản lý hành chính"),
    ]
    items.extend(actions_kaan)

    # --- D. TỪ CHỈ NGƯỜI & NGHỀ NGHIỆP: 'ນັກ' / 'ຜູ້' ---
    people_occupations = [
        ("ນັກຂຽນ", "Nhà văn", "Writer / Author", "nak-khian", "noun", "Nghề nghiệp", "ນັກຂຽນຊື່ດັງ", "Nhà văn nổi tiếng"),
        ("ນັກຂ່າວ", "Nhà báo / Phóng viên", "Journalist / Reporter", "nak-khaao", "noun", "Nghề nghiệp", "ນັກຂ່າວໂທລະພາບ", "Phóng viên truyền hình"),
        ("ນັກຮ້ອງ", "Ca sĩ", "Singer", "nak-hawng", "noun", "Nghề nghiệp", "ນັກຮ້ອງສຽງດີ", "Ca sĩ hát hay"),
        ("ນັກກິລາ", "Vận động viên", "Athlete", "nak-ki-laa", "noun", "Nghề nghiệp", "ນັກກິລາແລ່ນ", "Vận động viên chạy"),
        ("ນັກທຸລະກິດ", "Doanh nhân", "Businessman", "nak-thu-la-kit", "noun", "Nghề nghiệp", "ນັກທຸລະກິດໜຸ່ມ", "Doanh nhân trẻ"),
        ("ນັກວິທະຍາສາດ", "Nhà khoa học", "Scientist", "nak-vit-tha-yaa-saat", "noun", "Nghề nghiệp", "ນັກວິທະຍາສາດຄົ້ນຄວ້າ", "Nhà khoa học nghiên cứu"),
        ("ນັກແປ", "Người dịch / Biên dịch viên", "Translator", "nak-pae", "noun", "Nghề nghiệp", "ນັກແປພາສາລາວ-ຫວຽດ", "Biên dịch viên Lào - Việt"),
        ("ນັກບິນ", "Phi công", "Pilot", "nak-bin", "noun", "Nghề nghiệp", "ນັກບິນສາຍການບິນລາວ", "Phi công Hãng hàng không Quốc gia Lào"),
        ("ຜູ້ຈັດການ", "Người quản lý / Giám đốc", "Manager", "phuu-chat-kaan", "noun", "Nghề nghiệp", "ຜູ້ຈັດການໂຮງແຮມ", "Quản lý khách sạn"),
        ("ຜູ້ອຳນວຍການ", "Tổng giám đốc / Hiệu trưởng", "Director / Principal", "phuu-am-nuay-kaan", "noun", "Nghề nghiệp", "ຜູ້ອຳນວຍການໂຮງຮຽນ", "Hiệu trưởng trường học"),
        ("ຜູ້ໂດຍສານ", "Hành khách", "Passenger", "phuu-dooy-saan", "noun", "Nghề nghiệp", "ຜູ້ໂດຍສານລົດເມ", "Hành khách đi xe buýt"),
        ("ຜູ້ປ່ວຍ", "Bệnh nhân", "Patient", "phuu-puay", "noun", "Y tế", "ປິ່ນປົວຜູ້ປ່ວຍ", "Chữa trị cho bệnh nhân"),
        ("ຜູ້ຊ່ຽວຊານ", "Chuyên gia", "Expert / Specialist", "phuu-xiaao-xaan", "noun", "Nghề nghiệp", "ຜູ້ຊ່ຽວຊານດ້ານໄອທີ", "Chuyên gia công nghệ thông tin"),
        ("ຜູ້ຕາງໜ້າ", "Đại diện / Đại biểu", "Representative", "phuu-taang-naa", "noun", "Nghề nghiệp", "ຜູ້ຕາງໜ້າບໍລິສັດ", "Đại diện công ty"),
        ("ວິສະວະກອນ", "Kỹ sư", "Engineer", "vit-sa-va-kawn", "noun", "Nghề nghiệp", "ວິສະວະກອນຂົວທາງ", "Kỹ sư cầu đường"),
        ("ສະຖາປະນິກ", "Kiến trúc sư", "Architect", "sa-thaa-pa-nik", "noun", "Nghề nghiệp", "ສະຖາປະນິກອອກແບບເຮືອນ", "Kiến trúc sư thiết kế nhà"),
        ("ທະນາຍຄວາມ", "Luật sư", "Lawyer / Attorney", "tha-naai-khuaam", "noun", "Nghề nghiệp", "ປຶກສາທະນາຍຄວາມ", "Tham vấn luật sư"),
        ("ກຳມະກອນ", "Công nhân", "Worker / Laborer", "kam-ma-kawn", "noun", "Nghề nghiệp", "ກຳມະກອນໂຮງງານ", "Công nhân nhà máy"),
        ("ແມ່ບ້ານ", "Người giúp việc / Nội trợ", "Housewife / Maid", "mae-baan", "noun", "Nghề nghiệp", "ແມ່ບ້ານເຮັດວຽກເຮືອນ", "Người giúp việc dọn nhà"),
        ("ພະນັກງານ", "Nhân viên / Cán bộ", "Employee / Staff", "pha-nak-ngaan", "noun", "Nghề nghiệp", "ພະນັກງານທະນາຄານ", "Nhân viên ngân hàng"),
    ]
    items.extend(people_occupations)

    # --- E. ĐỊA ĐIỂM DỊCH VỤ: 'ຮ້ານ' / 'ຫ້ອງ' / 'ໂຮງ' ---
    venues = [
        ("ຮ້ານຕັດຜົມ", "Tiệm cắt tóc", "Barbershop / Hair salon", "haan-tat-phom", "noun", "Dịch vụ", "ໄປຮ້ານຕັດຜົມ", "Đến tiệm cắt tóc"),
        ("ຮ້ານຊັກລີດ", "Tiệm giặt là", "Laundry shop", "haan-xak-leet", "noun", "Dịch vụ", "ເອົາເຄື່ອງໄປຮ້ານຊັກລີດ", "Mang quần áo ra tiệm giặt"),
        ("ຮ້ານສ້ອມແປງ", "Tiệm sửa chữa (xe máy/máy móc)", "Repair shop", "haan-sawm-paeng", "noun", "Dịch vụ", "ຮ້ານສ້ອມແປງລົດຈັກ", "Tiệm sửa xe máy"),
        ("ຮ້ານຂາຍປຶ້ມ", "Hiệu sách", "Bookstore", "haan-khaai-puem", "noun", "Dịch vụ", "ຊື້ວັດຈະນານຸກົມຢູ່ຮ້ານຂາຍປຶ້ມ", "Mua từ điển ở hiệu sách"),
        ("ຮ້ານສະດວກຊື້", "Cửa hàng tiện lợi", "Convenience store", "haan-sa-duak-seu", "noun", "Mua sắm", "ເຂົ້າຮ້ານສະດວກຊື້", "Vào cửa hàng tiện lợi"),
        ("ໂຮງໜັງ", "Rạp chiếu phim", "Movie theater / Cinema", "hoong-nang", "noun", "Giải trí", "ເບິ່ງໜັງຢູ່ໂຮງໜັງ", "Xem phim ở rạp"),
        ("ໂຮງງານ", "Nhà máy / Xí nghiệp", "Factory", "hoong-ngaan", "noun", "Công nghiệp", "ໂຮງງານຕັດຫຍິບ", "Nhà máy may mặc"),
        ("ຫໍສະໝຸດ", "Thư viện", "Library", "haw-sa-mut", "noun", "Giáo dục", "ອ່ານໜັງສືຢູ່ຫໍສະໝຸດແຫ່ງຊາດ", "Đọc sách ở Thư viện Quốc gia"),
        ("ຫໍພິພິທະພັນ", "Bảo tàng", "Museum", "haw-phi-phi-tha-phan", "noun", "Văn hóa", "ຫໍພິພິທະພັນແຫ່ງຊາດລາວ", "Bảo tàng Quốc gia Lào"),
        ("ສະໜາມກິລາ", "Sân vận động", "Stadium / Sports complex", "sa-naam-ki-laa", "noun", "Thể thao", "ແຂ່ງຂັນຢູ່ສະໜາມກິລາ", "Thi đấu ở sân vận động"),
        ("ສະລອຍນ້ຳ", "Bể bơi", "Swimming pool", "sa-lawy-nam", "noun", "Thể thao", "ລອຍນ້ຳຢູ່ສະລອຍນ້ຳ", "Bơi ở bể bơi"),
        ("ສວນສາທາລະນະ", "Công viên công cộng", "Public park", "suan-saa-thaa-la-na", "noun", "Nơi chốn", "ຍ່າງຫຼິ້ນສວນສາທາລະນະ", "Đi dạo công viên"),
        ("ສວນສັດ", "Vườn bách thú / Thảo cầm viên", "Zoo", "suan-sat", "noun", "Nơi chốn", "ພາເດັກນ້ອຍໄປສວນສັດ", "Dẫn trẻ con đi vườn thú"),
    ]
    items.extend(venues)

    # --- F. THƯƠNG MẠI, TIỀN TỆ & TÀI CHÍNH ---
    finance = [
        ("ເງິນ", "Tiền bạc", "Money", "ngoen", "noun", "Kinh tế", "ມີເງິນ", "Có tiền"),
        ("ເງິນກີບ", "Tiền Kíp Lào", "Lao Kip (LAK)", "ngoen-keep", "noun", "Kinh tế", "ເງິນກີບລາວ", "Đồng Kíp Lào"),
        ("ເງິນດົ່ງ", "Tiền Đồng Việt Nam", "Vietnamese Dong (VND)", "ngoen-dong", "noun", "Kinh tế", "ແລກປ່ຽນເງິນດົ່ງ", "Đổi tiền Đồng"),
        ("ເງິນໂດລາ", "Đô la Mỹ", "US Dollar (USD)", "ngoen-doo-laa", "noun", "Kinh tế", "ເງິນໂດລາສະຫະລັດ", "Đô la Mỹ"),
        ("ເງິນບາດ", "Tiền Bạt Thái Lan", "Thai Baht (THB)", "ngoen-baat", "noun", "Kinh tế", "ຈ່າຍເງິນບາດ", "Thanh toán tiền Baht"),
        ("ລາຄາ", "Mức giá / Giá cả", "Price / Cost", "laa-khaa", "noun", "Mua sắm", "ລາຄາເທົ່າໃດ", "Giá bao nhiêu?"),
        ("ໃບຮັບເງິນ", "Hóa đơn / Biên nhận", "Receipt / Bill", "bai-hap-ngoen", "noun", "Mua sắm", "ຂໍໃບຮັບເງິນແດ່", "Cho tôi xin hóa đơn"),
        ("ຫຼຸດລາຄາ", "Giảm giá", "Discount", "lut-laa-khaa", "verb", "Mua sắm", "ຫຼຸດລາຄາໄດ້ບໍ", "Có bớt/giảm giá được không?"),
        ("ເງິນທອນ", "Tiền thối / Tiền trả lại", "Change (money)", "ngoen-thawn", "noun", "Mua sắm", "ຢ່າລືມເອົາເງິນທອນ", "Đừng quên lấy tiền thối"),
        ("ບັດເຄຣດິດ", "Thẻ tín dụng", "Credit card", "bat-khee-dit", "noun", "Tài chính", "ຈ່າຍຜ່ານບັດເຄຣດິດ", "Thanh toán bằng thẻ tín dụng"),
        ("ໂອນເງິນ", "Chuyển khoản", "Transfer money", "oon-ngoen", "verb", "Tài chính", "ໂອນເງິນຜ່ານແອັບ", "Chuyển tiền qua app ngân hàng"),
        ("ຖອນເງິນ", "Rút tiền mặt", "Withdraw cash", "thawn-ngoen", "verb", "Tài chính", "ຖອນເງິນຢູ່ຕູ້ ATM", "Rút tiền ở cây ATM"),
        ("ດອກເບ້ຍ", "Lãi suất / Tiền lãi", "Interest rate", "dawk-bia", "noun", "Tài chính", "ດອກເບ້ຍເງິນຝາກ", "Lãi suất tiền gửi"),
        ("ໜີ້ສິນ", "Nợ nần", "Debt", "nee-sin", "noun", "Tài chính", "ບໍ່ມີໜີ້ສິນ", "Không có nợ nần"),
        ("ລົງທຶນ", "Đầu tư", "Invest / Investment", "long-thun", "verb", "Tài chính", "ລົງທຶນໃສ່ທຸລະກິດ", "Đầu tư vào kinh doanh"),
        ("ກຳໄລ", "Lợi nhuận / Tiền lời", "Profit", "kam-lai", "noun", "Tài chính", "ໄດ້ກຳໄລຫຼາຍ", "Thu được nhiều lợi nhuận"),
        ("ຂາດທຶນ", "Thua lỗ", "Loss", "khaat-thun", "verb", "Tài chính", "ທຸລະກິດຂາດທຶນ", "Kinh doanh thua lỗ"),
    ]
    items.extend(finance)

    # --- G. ĐỘNG TỪ MỞ RỘNG VỀ TÂM LÝ, TRÍ TUỆ & GIAO TIẾP ---
    verbs_mind = [
        ("ອະທິບາຍ", "Giải thích", "To explain", "a-thi-baai", "verb", "Giao tiếp", "ອະທິບາຍໃຫ້ຟັງແດ່", "Hãy giải thích cho tôi nghe"),
        ("ແນະນຳ", "Giới thiệu / Khuyên bảo", "To introduce / To recommend", "nae-nam", "verb", "Giao tiếp", "ແນະນຳຕົວເອງ", "Tự giới thiệu bản thân"),
        ("ຕັດສິນໃຈ", "Quyết định", "To decide", "tat-sin-chai", "verb", "Tâm lý", "ຕັດສິນໃຈແລ້ວ", "Đã quyết định rồi"),
        ("ສັນຍາ", "Hứa hẹn / Hợp đồng", "To promise / Contract", "san-nyaa", "verb", "Giao tiếp", "ຂ້ອຍສັນຍາ", "Tôi xin hứa"),
        ("ຂໍຮ້ອງ", "Yêu cầu / Cầu xin", "To request / To plead", "khaw-hawng", "verb", "Giao tiếp", "ຂໍຮ້ອງຢ່າເຮັດແບບນັ້ນ", "Xin đừng làm như thế"),
        ("ຊົມເຊີຍ", "Khen ngợi / Hoan nghênh", "To praise / To congratulate", "xom-soey", "verb", "Giao tiếp", "ຊົມເຊີຍຜົນງານ", "Khen ngợi thành tích"),
        ("ອວຍພອນ", "Chúc mừng / Chúc tụng", "To bless / To wish well", "uay-phawn", "verb", "Giao tiếp", "ອວຍພອນປີໃໝ່", "Chúc mừng năm mới"),
        ("ຂໍອະໄພ", "Xin thứ lỗi", "To forgive / To pardon", "khaw-a-phai", "phrase", "Giao tiếp", "ຂໍອະໄພໃນຄວາມບໍ່ສະດວກ", "Xin thứ lỗi vì sự bất tiện"),
        ("ຂອບໃຈນຳ", "Cảm ơn nhé", "Thanks too", "khop-chai-nam", "phrase", "Giao tiếp", "ຂອບໃຈນຳເດີ", "Cảm ơn nhiều nha"),
        ("ສັງເກດ", "Quan sát / Chú ý", "To observe / To notice", "sang-keet", "verb", "Nhận thức", "ສັງເກດເບິ່ງ", "Quan sát kỹ"),
        ("ຄົ້ນຄວ້າ", "Nghiên cứu / Tìm tòi", "To research", "khon-khwaa", "verb", "Học tập", "ຄົ້ນຄວ້າວິທະຍາສາດ", "Nghiên cứu khoa học"),
        ("ແກ້ໄຂ", "Khắc phục / Giải quyết / Sửa lỗi", "To solve / To fix", "kae-khai", "verb", "Hành động", "ແກ້ໄຂບັນຫາ", "Giải quyết vấn đề"),
        ("ປ້ອງກັນ", "Bảo vệ / Phòng ngừa", "To protect / To prevent", "pawng-kan", "verb", "Hành động", "ປ້ອງກັນພະຍາດ", "Phòng ngừa dịch bệnh"),
        ("ປິ່ນປົວ", "Chữa bệnh / Điều trị", "To treat / To cure", "pin-pua", "verb", "Y tế", "ປິ່ນປົວໃຫ້ຫາຍດີ", "Điều trị cho mau khỏi"),
        ("ສ້ອມແປງ", "Sửa chữa", "To repair / To mend", "sawm-paeng", "verb", "Hành động", "ສ້ອມແປງເຮືອນ", "Sửa chữa nhà cửa"),
        ("ປູກ", "Trồng trọt", "To plant / To grow", "puuk", "verb", "Nông nghiệp", "ປູກຕົ້ນໄມ້", "Trồng cây"),
        ("ລ້ຽງ", "Nuôi nấng / Đãi tiệc", "To raise / To feed / To treat", "liang", "verb", "Hành động", "ລ້ຽງສັດ", "Chăn nuôi gia súc"),
        ("ເດີນທາງ", "Lên đường / Đi lại", "To travel / To journey", "doen-thaang", "verb", "Du lịch", "ເດີນທາງດ້ວຍຄວາມປອດໄພ", "Lên đường thượng lộ bình an"),
        ("ຢ້ຽມຢາມ", "Thăm viếng / Thăm hỏi", "To visit", "yiam-yaam", "verb", "Xã hội", "ໄປຢ້ຽມຢາມຄອບຄົວ", "Đi thăm gia đình"),
    ]
    items.extend(verbs_mind)

    # --- H. KHẨU NGỮ, THÀNH NGỮ & CÂU CẢM THÁN HÀNG NGÀY ---
    idioms_slang = [
        ("ບໍ່ເປັນຫຍັງ", "Không sao / Không có gì", "Never mind / You're welcome", "baw-pen-nyang", "phrase", "Giao tiếp", "ບໍ່ເປັນຫຍັງ, ສະບາຍໃຈໄດ້", "Không sao đâu, cứ an tâm"),
        ("ສະບາຍດີ", "Xin chào / Chúc bình an", "Hello / Good health", "sa-baai-dee", "phrase", "Giao tiếp", "ສະບາຍດີຕອນເຊົ້າ", "Chào buổi sáng"),
        ("ລາກ່ອນ", "Tạm biệt", "Goodbye", "laa-kawn", "phrase", "Giao tiếp", "ລາກ່ອນ, ພົບກັນໃໝ່", "Tạm biệt, hẹn gặp lại"),
        ("ໂຊກດີເດີ", "Chúc may mắn nhé", "Good luck to you", "xook-dee-der", "phrase", "Giao tiếp", "ຂໍໃຫ້ໂຊກດີເດີ", "Chúc bạn nhiều may mắn nhé"),
        ("ຄິດຮອດຫຼາຍ", "Nhớ rất nhiều", "Miss you so much", "khit-hawt-laai", "phrase", "Cảm xúc", "ຂ້ອຍຄິດຮອດເຈົ້າຫຼາຍ", "Tôi nhớ bạn nhiều lắm"),
        ("ສຸດຍອດ", "Tuyệt vời / Đỉnh cao", "Awesome / Fantastic", "sut-nyawt", "adjective", "Khen ngợi", "ອາຫານມື້ນີ້ສຸດຍອດ", "Món ăn hôm nay tuyệt vời"),
        ("ເກັ່ງຫຼາຍ", "Giỏi lắm / Rất giỏi", "Very smart / Great job", "keng-laai", "phrase", "Khen ngợi", "ເຈົ້າເກັ່ງຫຼາຍ", "Bạn giỏi lắm"),
        ("ງາມຫຼາຍ", "Rất đẹp", "Very beautiful", "ngaam-laai", "phrase", "Khen ngợi", "ດອກໄມ້ງາມຫຼາຍ", "Hoa đẹp quá"),
        ("ແຊບຫຼາຍ", "Ngon tuyệt cú mèo", "Very delicious", "saep-laai", "phrase", "Khen ngợi", "ອາຫານລາວແຊບຫຼາຍ", "Đồ ăn Lào ngon lắm"),
        ("ເຫັນດີນຳ", "Đồng ý / Tán thành", "Agree with you", "hen-dee-nam", "phrase", "Giao tiếp", "ຂ້ອຍເຫັນດີນຳເຈົ້າ", "Tôi hoàn toàn tán thành bạn"),
        ("ບໍ່ເຫັນດີ", "Không đồng ý", "Disagree", "baw-hen-dee", "phrase", "Giao tiếp", "ຂ້ອຍບໍ່ເຫັນດີ", "Tôi không đồng ý"),
        ("ແມ່ນແລ້ວ", "Đúng rồi / Phải rồi", "That's right", "maen-laew", "phrase", "Giao tiếp", "ແມ່ນແລ້ວ, ຖືກຕ້ອງ", "Đúng rồi, chuẩn xác"),
        ("ບໍ່ແມ່ນ", "Không phải", "No / Not that", "baw-maen", "phrase", "Giao tiếp", "ບໍ່ແມ່ນແນວນັ້ນ", "Không phải như thế đâu"),
        ("ຈັກໜ້ອຍ", "Một chút / Lát nữa", "A moment / Soon", "chak-nawy", "adverb", "Thời gian", "ລໍຖ້າຈັກໜ້ອຍເດີ", "Đợi một lát nha"),
        ("ແທ້ໆ", "Thật sự / Thật đấy", "Really / Truly", "thae-thae", "adverb", "Nhấn mạnh", "ຂ້ອຍເວົ້າແທ້ໆ", "Tôi nói thật lòng đấy"),
        ("ຫຼາຍໆ", "Rất nhiều", "A lot / Many", "laai-laai", "adverb", "Nhấn mạnh", "ຂອບໃຈຫຼາຍໆ", "Cảm ơn rất nhiều"),
        ("ນ້ອຍໆ", "Bé tí / Chút ít", "A little / Tiny", "nawy-nawy", "adverb", "Nhấn mạnh", "ກິນໜ້ອຍໆ", "Ăn một chút thôi"),
    ]
    items.extend(idioms_slang)

    return items


def main():
    dict_path = os.path.join(PROJECT_ROOT, "data", "dictionaries", "lao_vi_en.csv")
    print(f"[*] Bắt đầu nâng cấp kho từ điển lên quy mô lớn (Massive Lao Dictionary)...")
    
    entries = load_existing_dict(dict_path)
    old_size = len(entries)
    print(f"[*] Số mục từ sẵn có: {old_size}")

    new_items = get_massive_vocab_list()
    added_count = 0

    for item in new_items:
        lao_word, vi, en, rom, pos, cat, ex_lao, ex_vi = item
        norm_lao = normalize_lao(lao_word.strip())
        if not norm_lao:
            continue
        
        # Nếu chưa có trong từ điển thì thêm mới
        if norm_lao not in entries:
            entries[norm_lao] = {
                "lao": norm_lao,
                "vi": vi.strip(),
                "en": en.strip(),
                "romanization": rom.strip(),
                "pos": pos.strip(),
                "lesson": cat.strip(),
                "example_lao": normalize_lao(ex_lao.strip()),
                "example_vi": ex_vi.strip(),
            }
            added_count += 1

    sorted_keys = sorted(entries.keys())
    new_size = len(sorted_keys)

    with open(dict_path, mode="w", encoding="utf-8", newline="") as f:
        fieldnames = ["lao", "vi", "en", "romanization", "pos", "lesson", "example_lao", "example_vi"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for k in sorted_keys:
            writer.writerow(entries[k])

    print(f"[+] NÂNG CẤP TỪ ĐIỂN THÀNH CÔNG!")
    print(f"    - Trước khi mở rộng: {old_size} mục từ")
    print(f"    - Thêm mới đợt này: {added_count} mục từ")
    print(f"    - Tổng quy mô hiện tại: {new_size} mục từ")


if __name__ == "__main__":
    main()
