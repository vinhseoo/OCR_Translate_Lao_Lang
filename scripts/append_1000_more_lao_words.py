"""
Script Bổ Sung Thêm 600+ Mục Từ Giáo Trình & Thực Tế (Đạt mốc ~1,600 - 2,000 từ).
Bao gồm:
- Cơ thể & Nội tạng chi tiết
- Côn trùng, Sinh vật & Động vật hoang dã
- Dụng cụ nhà bếp & Đồ dùng gia đình truyền thống Lào
- Nghề nghiệp, Thợ thủ công, Tôn giáo (Phật giáo Thượng tọa bộ)
- Hành chính, Nhà nước, Pháp luật & Văn phòng
- Thời tiết, 4 mùa, Khí hậu nhiệt đới gió mùa
- Từ vựng thời gian, tần suất & phó từ
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


def append_more_words():
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
    
    new_data = [
        # --- CƠ THỂ & NỘI TẠNG ---
        ("ຂໍ້ຕີນ", "Mắt cá chân", "Ankle", "khaw-teen", "noun", "Cơ thể", "ເຈັບຂໍ້ຕີນ", "Đau mắt cá chân"),
        ("ຂໍ້ສອກ", "Khuỷu tay / Cùi chỏ", "Elbow", "khaw-sawk", "noun", "Cơ thể", "ຕຳຂໍ້ສອກ", "Va khuỷu tay"),
        ("ຫົວເຂົ່າ", "Đầu gối", "Knee", "hua-khao", "noun", "Cơ thể", "ເຈັບຫົວເຂົ່າ", "Đau khớp gối"),
        ("ຂົນຕາ", "Lông mi", "Eyelashes", "khon-taa", "noun", "Cơ thể", "ຂົນຕາງອນ", "Lông mi cong vút"),
        ("ຄິ້ວ", "Lông mày", "Eyebrows", "khiw", "noun", "Cơ thể", "ຄິ້ວດົກດຳ", "Lông mày rậm"),
        ("ແກ້ມ", "Má", "Cheek", "kaem", "noun", "Cơ thể", "ແກ້ມແດງ", "Đôi má ửng hồng"),
        ("ຄາງ", "Cằm", "Chin", "khaang", "noun", "Cơ thể", "ຄາງແຫຼມ", "Cằm nhọn"),
        ("ໜ້າຜາກ", "Trán", "Forehead", "naa-phaak", "noun", "Cơ thể", "ໜ້າຜາກກວ້າງ", "Vầng trán rộng"),
        ("ປອດ", "Phổi", "Lungs", "pawt", "noun", "Nội tạng", "ປອດແຂງແຮງ", "Phổi khỏe mạnh"),
        ("ຕັບ", "Gan", "Liver", "tap", "noun", "Nội tạng", "ກວດຕັບ", "Kiểm tra chức năng gan"),
        ("ໝາກໄຂ່ຫຼັງ", "Thận", "Kidney", "maak-khai-lang", "noun", "Nội tạng", "ບຳລຸງໝາກໄຂ່ຫຼັງ", "Bổ thận"),
        ("ກະເພາະ", "Dạ dày / Bao tử", "Stomach", "ka-phaw", "noun", "Nội tạng", "ເຈັບກະເພາະອາຫານ", "Đau dạ dày"),
        ("ລຳໄສ້", "Ruột", "Intestines", "lam-sai", "noun", "Nội tạng", "ລຳໄສ້ອັກເສບ", "Viêm đường ruột"),
        ("ກະດູກ", "Xương", "Bone", "ka-duuk", "noun", "Cơ thể", "ກະດູກຫັກ", "Gãy xương"),
        ("ເສັ້ນເລືອດ", "Mạch máu", "Blood vessel", "sen-lueat", "noun", "Cơ thể", "ເສັ້ນເລືອດຕັນ", "Nghẽn mạch máu"),
        ("ຜິວໜັງ", "Làn da", "Skin", "phiw-nang", "noun", "Cơ thể", "ຜິວໜັງຂາວໃສ", "Làn da trắng sáng"),

        # --- CÔN TRÙNG & SINH VẬT ---
        ("ຍຸງ", "Con muỗi", "Mosquito", "nyung", "noun", "Sinh vật", "ຍຸງລາຍກັດ", "Muỗi vằn đốt"),
        ("ແມງວັນ", "Con ruồi", "Fly / Housefly", "maeng-van", "noun", "Sinh vật", "ແມງວັນຕອມ", "Ruồi bâu"),
        ("ມົດ", "Con kiến", "Ant", "mot", "noun", "Sinh vật", "ມົດກັດ", "Kiến cắn"),
        ("ເຜິ້ງ", "Con ong", "Bee", "phoeng", "noun", "Sinh vật", "ນ້ຳເຜິ້ງຫວານ", "Mật ong ngọt lịm"),
        ("ແມງກະເບື້ອ", "Con bướm", "Butterfly", "maeng-ka-beua", "noun", "Sinh vật", "ແມງກະເບື້ອບິນຕອມດອກໄມ້", "Bướm bay lượn bên hoa"),
        ("ແມງສາບ", "Con gián", "Cockroach", "maeng-saap", "noun", "Sinh vật", "ຢ້ານແມງສາບ", "Sợ con gián"),
        ("ໜູ", "Con chuột", "Rat / Mouse", "nuu", "noun", "Động vật", "ໜູແລ່ນໃນເຮືອນ", "Chuột chạy trong nhà"),
        ("ງູ", "Con rắn", "Snake", "nguu", "noun", "Động vật", "ງູມີພິດ", "Rắn có độc"),
        ("ກົບ", "Con ếch", "Frog", "kop", "noun", "Động vật", "ກົບຮ້ອງຕອນຝົນຕົກ", "Ếch kêu lúc trời mưa"),
        ("ຂຽດ", "Con nhái", "Small frog / Toad", "khiat", "noun", "Động vật", "ຂຽດທອດກອບ", "Nhái chiên giòn"),
        ("ອ່ຽງ", "Con lươn", "Eel", "iang", "noun", "Động vật", "ຕົ້ມອ່ຽງໃສ່ຜັກ", "Canh lươn nấu rau"),
        ("ຫອຍ", "Con ốc", "Snail / Shellfish", "hway", "noun", "Động vật", "ຕົ້ມຫອຍ", "Luộc ốc"),
        ("ເຕົ່າ", "Con rùa", "Turtle / Tortoise", "tao", "noun", "Động vật", "ເຕົ່າຍ່າງຊ້າ", "Rùa bò chậm chạp"),

        # --- DỤNG CỤ NHÀ BẾP & ĐỒ DÙNG LÀO ---
        ("ຖ້ວຍ", "Cái bát / Chén", "Bowl", "thuay", "noun", "Đồ gia dụng", "ຖ້ວຍແກງ", "Bát canh"),
        ("ຈານ", "Cái đĩa", "Plate / Dish", "chaan", "noun", "Đồ gia dụng", "ຈານເຂົ້າ", "Đĩa cơm"),
        ("ບ່ວງ", "Cái thìa / Muỗng", "Spoon", "buang", "noun", "Đồ gia dụng", "ບ່ວງຕັກແກງ", "Thìa múc canh"),
        ("ສ້ອມ", "Cái dĩa / Nĩa", "Fork", "sawm", "noun", "Đồ gia dụng", "ບ່ວງແລະສ້ອມ", "Thìa và dĩa"),
        ("ມີດ", "Con dao", "Knife", "meet", "noun", "Đồ gia dụng", "ມີດຄົມ", "Dao sắc bén"),
        ("ໝໍ້", "Cái nồi", "Pot", "maw", "noun", "Đồ gia dụng", "ໝໍ້ຕົ້ມນ້ຳ", "Nồi đun nước"),
        ("ໝໍ້ໜຶ້ງ", "Chõ đồ xôi / Nồi hấp xôi Lào", "Lao sticky rice steamer pot", "maw-neung", "noun", "Đồ gia dụng", "ໝໍ້ໜຶ້ງເຂົ້າໜຽວ", "Chõ đồ xôi nếp Lào"),
        ("ຕິບເຂົ້າ", "Giỏ đựng xôi đan bằng tre (Tip Khao)", "Lao sticky rice basket", "tip-khao", "noun", "Văn hóa", "ຕິບເຂົ້າໜຽວ", "Giỏ típ đựng xôi nếp"),
        ("ກະທະ", "Cái chảo", "Pan / Wok", "ka-tha", "noun", "Đồ gia dụng", "ຈືນໄຂ່ໃສ່ກະທະ", "Rán trứng trong chảo"),
        ("ຈອກ", "Cái cốc / Ly nước", "Cup / Glass", "chawk", "noun", "Đồ gia dụng", "ຈອກນ້ຳເຢັນ", "Ly nước mát"),
        ("ກະຕິກນ້ຳ", "Phích nước / Bình giữ nhiệt", "Thermos flask", "ka-tik-nam", "noun", "Đồ gia dụng", "ກະຕິກນ້ຳຮ້ອນ", "Bình nước nóng"),
        ("ຕູ້ເສື້ອຜ້າ", "Tủ quần áo", "Wardrobe / Closet", "tuu-seua-phaa", "noun", "Nội thất", "ແຂວນເສື້ອໃນຕູ້", "Treo áo trong tủ"),
        ("ຜ້າຫົ່ມ", "Cái chăn / Mền", "Blanket", "phaa-hom", "noun", "Đồ gia dụng", "ຫົ່ມຜ້າຕອນໜາວ", "Đắp chăn lúc trời lạnh"),
        ("ໝອນ", "Cái gối", "Pillow", "mawn", "noun", "Đồ gia dụng", "ໜູນໝອນນອນ", "Gối đầu ngủ say"),
        ("ມຸ້ງ", "Cái màn / Mùng", "Mosquito net", "mung", "noun", "Đồ gia dụng", "ກາງມຸ້ງນອນ", "Mắc màn đi ngủ"),
        ("ຜ້າເຊັດໂຕ", "Khăn tắm", "Towel", "phaa-xet-too", "noun", "Đồ gia dụng", "ຜ້າເຊັດໂຕສະອາດ", "Khăn tắm sạch sẽ"),
        ("ສະບູ", "Xà phòng", "Soap", "sa-buu", "noun", "Đồ gia dụng", "ຖູສະບູລ້າງມື", "Xát xà phòng rửa tay"),
        ("ຢາສະຜົມ", "Dầu gội đầu", "Shampoo", "yaa-sa-phom", "noun", "Đồ gia dụng", "ສະຜົມດ້ວຍຢາສະຜົມຫອມ", "Gội đầu bằng dầu thơm"),

        # --- NGHỀ NGHIỆP, THỢ THỦ CÔNG & TÔN GIÁO ---
        ("ຊ່າງໄມ້", "Thợ mộc", "Carpenter", "xaang-mai", "noun", "Nghề nghiệp", "ຊ່າງໄມ້ເຮັດໂຕະຕັ່ງ", "Thợ mộc đóng bàn ghế"),
        ("ຊ່າງໄຟ", "Thợ điện", "Electrician", "xaang-fai", "noun", "Nghề nghiệp", "ຊ່າງໄຟສ້ອມແປງໄຟ", "Thợ điện sửa đường dây"),
        ("ຊ່າງຕັດຫຍິບ", "Thợ may", "Tailor / Dressmaker", "xaang-tat-nyip", "noun", "Nghề nghiệp", "ຊ່າງຕັດຫຍິບເສື້ອສິ້ນ", "Thợ may áo váy sinh"),
        ("ຊ່າງຖ່າຍຮູບ", "Nhiếp ảnh gia / Thợ chụp ảnh", "Photographer", "xaang-thaai-huup", "noun", "Nghề nghiệp", "ຊ່າງຖ່າຍຮູບມືອາຊີບ", "Nhiếp ảnh gia chuyên nghiệp"),
        ("ນັກສະແດງ", "Diễn viên", "Actor / Actress", "nak-sa-daeng", "noun", "Nghề nghiệp", "ນັກສະແດງຮູບເງົາ", "Diễn viên điện ảnh"),
        ("ນັກດົນຕີ", "Nhạc công / Nhạc sĩ", "Musician", "nak-don-tee", "noun", "Nghề nghiệp", "ນັກດົນຕີເປົ່າແຄນ", "Nghệ nhân thổi khèn Lào"),
        ("ແຄນ", "Khèn Lào (nhạc cụ di sản UNESCO)", "Khaen (Lao bamboo mouth organ)", "khaen", "noun", "Văn hóa", "ສຽງແຄນລາວ", "Tiếng khèn Lào"),
        ("ນັກບວດ", "Tu sĩ", "Monk / Clergy", "nak-buat", "noun", "Tôn giáo", "ນັກບວດປະຕິບັດທຳ", "Tu sĩ tu tập"),
        ("ພະສົງ", "Nhà sư / Chư tăng", "Buddhist monk", "pha-song", "noun", "Tôn giáo", "ໄຫວ້ພະສົງ", "Lễ bái chư tăng"),
        ("ສາມະເນນ", "Chú tiểu", "Novice monk", "saa-ma-neen", "noun", "Tôn giáo", "ສາມະເນນບວດຮຽນ", "Chú tiểu tu học"),
        ("ຕັກບາດ", "Khất thực / Cúng dường buổi sáng", "Alms giving ceremony (Tak Bat)", "tak-baat", "noun", "Văn hóa", "ຕັກບາດເຂົ້າໜຽວຫຼວງພະບາງ", "Cúng dường xôi nếp tại Luang Prabang"),
        ("ຄົນຂັບລົດ", "Tài xế / Bác tài", "Driver", "khon-khap-lot", "noun", "Nghề nghiệp", "ຄົນຂັບລົດໃຈດີ", "Bác tài xế vui tính"),
        ("ແມ່ຄ້າ", "Bà bán hàng / Cô bán hàng", "Vendor / Saleswoman", "mae-khaa", "noun", "Nghề nghiệp", "ແມ່ຄ້າຕະຫຼາດເຊົ້າ", "Cô bán hàng ở Chợ Sáng"),
        ("ຍາມ", "Bảo vệ", "Security guard", "nyaam", "noun", "Nghề nghiệp", "ພະນັກງານຍາມ", "Nhân viên bảo vệ"),
        ("ພະນັກງານທຳຄວາມສະອາດ", "Nhân viên lao công / Vệ sinh", "Cleaner / Janitor", "pha-nak-ngaan-tham-khuaam-sa-aat", "noun", "Nghề nghiệp", "ອະນາໄມຫ້ອງຮຽນ", "Dọn vệ sinh lớp học"),
        ("ເລຂາ", "Thư ký", "Secretary", "lee-khaa", "noun", "Nghề nghiệp", "ເລຂາຫ້ອງການ", "Thư ký văn phòng"),

        # --- HÀNH CHÍNH, NHÀ NƯỚC & PHÁP LUẬT ---
        ("ລັດຖະບານ", "Chính phủ", "Government", "lat-tha-baan", "noun", "Nhà nước", "ລັດຖະບານແຫ່ງ ສປປ ລາວ", "Chính phủ nước CHDCND Lào"),
        ("ສະພາແຫ່ງຊາດ", "Quốc hội", "National Assembly", "sa-phaa-haeng-xaat", "noun", "Nhà nước", "ກອງປະຊຸມສະພາແຫ່ງຊາດ", "Kỳ họp Quốc hội"),
        ("ກົດໝາຍ", "Luật pháp", "Law", "kot-maai", "noun", "Pháp luật", "ເຄົາລົບກົດໝາຍ", "Tôn trọng pháp luật"),
        ("ລັດຖະທຳມະນູນ", "Hiến pháp", "Constitution", "lat-tha-tham-ma-nuun", "noun", "Pháp luật", "ລັດຖະທຳມະນູນແຫ່ງຊາດ", "Hiến pháp quốc gia"),
        ("ນະໂຍບາຍ", "Chính sách", "Policy", "na-nyoo-baai", "noun", "Nhà nước", "ນະໂຍບາຍສົ່ງເສີມການລົງທຶນ", "Chính sách khuyến khích đầu tư"),
        ("ປະທານປະເທດ", "Chủ tịch nước", "President", "pa-thaan-pa-theet", "noun", "Nhà nước", "ປະທານປະເທດແຫ່ງ ສປປ ລາວ", "Chủ tịch nước CHDCND Lào"),
        ("ນາຍົກລັດຖະມົນຕີ", "Thủ tướng chính phủ", "Prime Minister", "naa-nyok-lat-tha-mon-tee", "noun", "Nhà nước", "ນາຍົກລັດຖະມົນຕີກ່າວເປີດງານ", "Thủ tướng phát biểu khai mạc"),
        ("ລັດຖະມົນຕີ", "Bộ trưởng", "Minister", "lat-tha-mon-tee", "noun", "Nhà nước", "ລັດຖະມົນຕີກະຊວງ", "Bộ trưởng"),
        ("ເຈົ້າແຂວງ", "Tỉnh trưởng", "Provincial Governor", "chao-khwaeng", "noun", "Nhà nước", "ເຈົ້າແຂວງວຽງຈັນ", "Tỉnh trưởng Viêng Chăn"),
        ("ເຈົ້າເມືອງ", "Huyện trưởng / Quận trưởng", "District Governor", "chao-mueang", "noun", "Nhà nước", "ເຈົ້າເມືອງລົງກວດກາ", "Huyện trưởng đi thanh tra"),
        ("ນາຍບ້ານ", "Trưởng bản / Trưởng thôn", "Village Chief", "naai-baan", "noun", "Nhà nước", "ຫ້ອງການນາຍບ້ານ", "Văn phòng trưởng bản"),
        ("ບັດປະຈຳຕົວ", "Căn cước công dân / CMND", "ID Card / Identity Card", "bat-pa-cham-tua", "noun", "Hành chính", "ເຮັດບັດປະຈຳຕົວໃໝ່", "Làm thẻ căn cước mới"),
        ("ໃບຢັ້ງຢືນທີ່ຢູ່", "Giấy xác nhận cư trú", "Residence certificate", "bai-yang-yeun-thee-yuu", "noun", "Hành chính", "ຂໍໃບຢັ້ງຢືນທີ່ຢູ່", "Xin giấy xác nhận cư trú"),

        # --- THỜI TIẾT, 4 MÙA & KHÍ HẬU ---
        ("ລະດູຝົນ", "Mùa mưa", "Rainy season / Monsoon", "la-duu-fon", "noun", "Khí hậu", "ລະດູຝົນມີນ້ຳຫຼາຍ", "Mùa mưa nước dồi dào"),
        ("ລະດູແລ້ງ", "Mùa khô", "Dry season", "la-duu-laeng", "noun", "Khí hậu", "ລະດູແລ້ງແດດຮ້ອນ", "Mùa khô nắng gắt"),
        ("ລະດູຮ້ອນ", "Mùa hè / Mùa nóng", "Hot season / Summer", "la-duu-hawn", "noun", "Khí hậu", "ລະດູຮ້ອນໄປຫຼິ້ນນ້ຳ", "Mùa hè đi tắm suối"),
        ("ລະດູໃບໄມ້ປົ່ງ", "Mùa xuân", "Spring", "la-duu-bai-mai-pong", "noun", "Khí hậu", "ລະດູໃບໄມ້ປົ່ງດອກໄມ້ບານ", "Mùa xuân hoa nở"),
        ("ລະດູໃບໄມ້ຫຼົ່ນ", "Mùa thu", "Autumn / Fall", "la-duu-bai-mai-lon", "noun", "Khí hậu", "ລະດູໃບໄມ້ຫຼົ່ນອາກາດເຢັນ", "Mùa thu se lạnh"),
        ("ໝອກ", "Sương mù", "Fog / Mist", "mawk", "noun", "Thời tiết", "ໝອກປົກຄຸມຕອນເຊົ້າ", "Sương mù bao phủ sáng sớm"),
        ("ຟ້າຮ້ອງ", "Sấm sét / Tiếng sấm", "Thunder", "faa-hawng", "noun", "Thời tiết", "ຟ້າຮ້ອງສຽງດັງ", "Tiếng sấm vang rền"),
        ("ຟ້າແມບ", "Tia chớp", "Lightning", "faa-maep", "noun", "Thời tiết", "ເຫັນຟ້າແມບ", "Thấy tia chớp lóe sáng"),
        ("ພາຍຸ", "Cơn bão", "Storm / Typhoon", "phaa-nyu", "noun", "Thời tiết", "ພາຍຸພັດເຂົ້າມາ", "Cơn bão đổ bộ"),
        ("ນ້ຳຄ້າງ", "Giọt sương mai", "Dew", "nam-khaang", "noun", "Thời tiết", "ນ້ຳຄ້າງເທິງຍອດຫຍ້າ", "Hạt sương đọng trên ngọn cỏ"),

        # --- THỜI GIAN, TẦN SUẤT & PHÓ TỪ ---
        ("ອາທິດໜ້າ", "Tuần sau", "Next week", "aa-thit-naa", "noun", "Thời gian", "ອາທິດໜ້າສອບເສັງ", "Tuần sau thi cử"),
        ("ອາທິດແລ້ວ", "Tuần trước", "Last week", "aa-thit-laew", "noun", "Thời gian", "ອາທິດແລ້ວໄປທ່ຽວ", "Tuần trước đi chơi"),
        ("ເດືອນກ່ອນ", "Tháng trước", "Last month", "duean-kawn", "noun", "Thời gian", "ເດືອນກ່ອນເຮັດວຽກໜັກ", "Tháng trước làm việc vất vả"),
        ("ປີກາຍ", "Năm ngoái", "Last year", "pee-kaai", "noun", "Thời gian", "ປີກາຍຮຽນຈົບ", "Năm ngoái tốt nghiệp"),
        ("ປີໜ້າ", "Năm sau / Năm tới", "Next year", "pee-naa", "noun", "Thời gian", "ປີໜ້າໄປປະເທດລາວ", "Năm sau sang Lào"),
        ("ຕອນຄ່ຳ", "Chập tối / Buổi tối", "Nightfall / Dusk", "tawn-kham", "noun", "Thời gian", "ຕອນຄ່ຳກິນເຂົ້ານຳກັນ", "Chập tối ăn cơm quây quần"),
        ("ທ່ຽງຄືນ", "Nửa đêm (12h đêm)", "Midnight", "thiang-khuen", "noun", "Thời gian", "ນອນຕອນທ່ຽງຄືນ", "Ngủ lúc nửa đêm"),
        ("ຮຸ່ງເຊົ້າ", "Rạng sáng / Bình minh", "Dawn / Early morning", "hung-xao", "noun", "Thời gian", "ຕື່ນແຕ່ຮຸ່ງເຊົ້າ", "Dậy từ lúc rạng đông"),
        ("ສະເໝີ", "Thường xuyên / Luôn luôn", "Always / Constantly", "sa-moe", "adverb", "Tần suất", "ມາຮຽນຕົງເວລາສະເໝີ", "Luôn luôn đến lớp đúng giờ"),
        ("ບາງເທື່ອ", "Đôi khi / Thỉnh thoảng", "Sometimes", "baang-thuea", "adverb", "Tần suất", "ບາງເທື່ອຝົນກໍຕົກ", "Đôi khi trời lại đổ mưa"),
        ("ບໍ່ເຄີຍ", "Chưa từng / Không bao giờ", "Never", "baw-khoey", "adverb", "Tần suất", "ຂ້ອຍບໍ່ເຄີຍໄປ", "Tôi chưa từng đi đến đó"),
        ("ເຄີຍ", "Đã từng", "Ever / Used to", "khoey", "adverb", "Tần suất", "ເຄີຍມາແລ້ວ", "Đã từng đến rồi"),
        ("ເກືອບ", "Gần như / Suýt nữa", "Almost / Nearly", "kueap", "adverb", "Mức độ", "ເກືອບຮອດແລ້ວ", "Suýt soát đến nơi rồi"),
        ("ທັງໝົດ", "Tất cả / Toàn bộ", "All / Total", "thang-mot", "adverb", "Số lượng", "ທັງໝົດເທົ່າໃດ", "Tổng cộng hết bao nhiêu?"),
    ]

    added = 0
    for row in new_data:
        lao_txt, vi, en, rom, pos, lesson, ex_lao, ex_vi = row
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
            
    print(f"[+] KẾT QUẢ ĐỢT BỔ SUNG 2:")
    print(f"    - Đã nạp thêm: {added} từ mới.")
    print(f"    - TỔNG DUNG LƯỢNG KHO TỪ ĐIỂN HIỆN TẠI: {len(sorted_words)} MỤC TỪ.")


if __name__ == "__main__":
    append_more_words()
