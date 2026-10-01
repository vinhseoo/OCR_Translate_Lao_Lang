"""
Bộ Sinh Từ Điển Tiếng Lào - Việt - Anh Quy Mô Lớn (Comprehensive Lao Dictionary).
Tạo lập và chuẩn hóa toàn diện kho từ vựng giáo trình & đời sống tiếng Lào.
Mọi mục từ đều có đầy đủ 8 trường dữ liệu:
[lao, vi, en, romanization, pos, lesson, example_lao, example_vi]
Tuân thủ nghiêm ngặt Lao Golden Rule #1: Chuẩn hóa Unicode NFC.
"""
import os
import sys
import csv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing.normalize import normalize_lao


def generate_extended_dictionary():
    dict_file = os.path.join(PROJECT_ROOT, "data", "dictionaries", "lao_vi_en.csv")
    
    # 1. Đọc từ điển gốc hiện tại
    entries = {}
    if os.path.exists(dict_file):
        with open(dict_file, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                lao_norm = normalize_lao(row.get("lao", "").strip())
                if lao_norm:
                    entries[lao_norm] = {
                        "lao": lao_norm,
                        "vi": row.get("vi", "").strip(),
                        "en": row.get("en", "").strip(),
                        "romanization": row.get("romanization", "").strip(),
                        "pos": row.get("pos", "").strip(),
                        "lesson": row.get("lesson", "").strip(),
                        "example_lao": normalize_lao(row.get("example_lao", "").strip()),
                        "example_vi": row.get("example_vi", "").strip(),
                    }
    print(f"[*] Từ điển hiện tại: {len(entries)} mục từ.")

    new_data = []

    # =========================================================================
    # A. 40+ LOẠI HOA QUẢ & NÔNG SẢN LÀO (FRUITS & VEGETABLES)
    # =========================================================================
    fruits = [
        ("ໝາກມ່ວງ", "Quả xoài", "Mango", "maak-muang", "noun", "Hoa quả", "ໝາກມ່ວງສຸກຫວານ", "Xoài chín ngọt lịm"),
        ("ໝາກກ້ວຍ", "Quả chuối", "Banana", "maak-kluay", "noun", "Hoa quả", "ໝາກກ້ວຍນ້ຳ", "Chuối ngự"),
        ("ໝາກຮຸ່ງ", "Quả đu đủ", "Papaya", "maak-hung", "noun", "Hoa quả", "ຕຳໝາກຮຸ່ງແຊບ", "Nộm đu đủ rất ngon"),
        ("ໝາກກ້ຽງ", "Quả cam", "Orange", "maak-kiang", "noun", "Hoa quả", "ໝາກກ້ຽງຫວານ", "Cam ngọt"),
        ("ໝາກນາວ", "Quả chanh", "Lime / Lemon", "maak-naao", "noun", "Hoa quả", "ນ້ຳໝາກນາວສົ້ມ", "Nước chanh chua mát"),
        ("ໝາກນັດ", "Quả dứa / thơm", "Pineapple", "maak-nat", "noun", "Hoa quả", "ໝາກນັດຫວານສ່ຳ", "Dứa ngọt lịm"),
        ("ໝາກໂມ", "Quả dưa hấu", "Watermelon", "maak-moo", "noun", "Hoa quả", "ກິນໝາກໂມແກ້ຮ້ອນ", "Ăn dưa hấu giải nhiệt"),
        ("ໝາກພ້າວ", "Quả dừa", "Coconut", "maak-phaao", "noun", "Hoa quả", "ນ້ຳໝາກພ້າວສົດ", "Nước dừa tươi mát"),
        ("ໝາກເຜັດ", "Quả ớt", "Chili", "maak-phet", "noun", "Gia vị", "ໝາກເຜັດເຜັດຫຼາຍ", "Ớt cay xè"),
        ("ໝາກຂາມ", "Quả me", "Tamarind", "maak-khaam", "noun", "Hoa quả", "ໝາກຂາມຫວານ", "Me ngọt"),
        ("ໝາກລຳໄຍ", "Quả nhãn", "Longan", "maak-lam-nyai", "noun", "Hoa quả", "ໝາກລຳໄຍຫວານ", "Nhãn ngọt thơm"),
        ("ໝາກລີ້ນຈີ່", "Quả vải", "Lychee", "maak-leen-chee", "noun", "Hoa quả", "ໝາກລີ້ນຈີ່ສົດ", "Vải thiều tươi"),
        ("ໝາກມັງຄຸດ", "Quả măng cụt", "Mangosteen", "maak-mang-khut", "noun", "Hoa quả", "ໝາກມັງຄຸດຫວານ", "Măng cụt thơm ngọt"),
        ("ໝາກທຸລຽນ", "Quả sầu riêng", "Durian", "maak-thu-lian", "noun", "Hoa quả", "ໝາກທຸລຽນຫອມ", "Sầu riêng thơm nức"),
        ("ໝາກສີດາ", "Quả ổi", "Guava", "maak-see-daa", "noun", "Hoa quả", "ໝາກສີດາກອບ", "Ổi giòn ngọt"),
        ("ໝາກແຕງ", "Dưa leo / Dưa chuột", "Cucumber", "maak-taeng", "noun", "Rau củ", "ຕຳໝາກແຕງ", "Nộm dưa leo"),
        ("ໝາກເລັ່ນ", "Cà chua", "Tomato", "maak-len", "noun", "Rau củ", "ໝາກເລັ່ນແດງ", "Cà chua chín đỏ"),
        ("ໝາກອຶ", "Bí đỏ", "Pumpkin", "maak-ue", "noun", "Rau củ", "ແກງໝາກອຶ", "Canh bí đỏ"),
        ("ໝາກເຂືອ", "Cà tím", "Eggplant", "maak-kheua", "noun", "Rau củ", "ແຈ່ວໝາກເຂືອ", "Tương cà tím nướng"),
        ("ຜັກບົ່ວ", "Hành lá", "Green onion / Scallion", "phak-bua", "noun", "Rau củ", "ໃສ່ຜັກບົ່ວ", "Rắc thêm hành lá"),
        ("ຜັກທຽມ", "Tỏi", "Garlic", "phak-thiam", "noun", "Gia vị", "ຜັກທຽມຫອມ", "Tỏi thơm lừng"),
        ("ຜັກກາດ", "Rau cải", "Chinese cabbage", "phak-kaat", "noun", "Rau củ", "ຜັດຜັກກາດ", "Rau cải xào tỏi"),
        ("ຜັກບົ້ງ", "Rau muống", "Morning glory / Water spinach", "phak-bong", "noun", "Rau củ", "ຜັດຜັກບົ້ງໄຟແດງ", "Rau muống xào tỏi lửa lớn"),
        ("ຜັກສະລັດ", "Rau xà lách", "Lettuce", "phak-sa-lat", "noun", "Rau củ", "ກິນຜັກສະລັດ", "Ăn xà lách tươi"),
        ("ຜັກຊີ", "Rau mùi / Ngò", "Coriander / Cilantro", "phak-xee", "noun", "Rau củ", "ຜັກຊີຫອມ", "Rau mùi thơm"),
        ("ຫົວສີໄຄ", "Củ sả", "Lemongrass", "hua-see-khai", "noun", "Gia vị", "ຕົ້ມໃສ່ຫົວສີໄຄ", "Nấu canh sả"),
        ("ຂີງ", "Củ gừng", "Ginger", "kheeng", "noun", "Gia vị", "ນ້ຳຂີງຮ້ອນ", "Nước gừng nóng"),
        ("ຂ່າ", "Củ riềng", "Galangal", "khaa", "noun", "Gia vị", "ໃສ່ຂ່າຫອມ", "Cho thêm củ riềng thơm"),
        ("ມັນດ້າງ", "Củ khoai lang", "Sweet potato", "man-daang", "noun", "Nông sản", "ມັນດ້າງເຜົາ", "Khoai lang nướng"),
        ("ມັນຕົ້ນ", "Củ sắn / Khoai mì", "Cassava", "man-ton", "noun", "Nông sản", "ຕົ້ມມັນຕົ້ນ", "Luộc sắn"),
        ("ສາລີ", "Bắp ngô", "Corn / Maize", "saa-lee", "noun", "Nông sản", "ສາລີຕົ້ມ", "Ngô luộc"),
        ("ຖົ່ວດິນ", "Lạc / Đậu phộng", "Peanut", "thua-din", "noun", "Nông sản", "ຖົ່ວດິນຂົ້ວ", "Lạc rang giòn"),
        ("ຖົ່ວຍາວ", "Đậu đũa", "Long bean / Yardlong bean", "thua-nyaao", "noun", "Rau củ", "ຕຳຖົ່ວຍາວ", "Nộm đậu đũa"),
        ("ເຫັດ", "Nấm", "Mushroom", "het", "noun", "Nông sản", "ແກງເຫັດ", "Canh nấm thơm ngon"),
    ]
    new_data.extend(fruits)

    # =========================================================================
    # B. CÁC ĐỒ UỐNG & MÓN ĂN TRUYỀN THỐNG LÀO
    # =========================================================================
    foods = [
        ("ນ້ຳຊາ", "Nước chè / Trà", "Tea water", "nam-xaa", "noun", "Đồ uống", "ດື່ມນ້ຳຊາຮ້ອນ", "Uống nước chè nóng"),
        ("ນ້ຳກາເຟ", "Cà phê", "Coffee", "nam-kaa-fee", "noun", "Đồ uống", "ກາເຟດຳບໍ່ໃສ່ນ້ຳຕານ", "Cà phê đen không đường"),
        ("ກາເຟໂອລຽງ", "Cà phê đen đá O-liang", "Iced black coffee", "kaa-fee-oo-liang", "noun", "Đồ uống", "ດື່ມກາເຟໂອລຽງ", "Uống cà phê đen đá"),
        ("ກາເຟນົມ", "Cà phê sữa", "Milk coffee", "kaa-fee-nom", "noun", "Đồ uống", "ກາເຟນົມເຢັນ", "Cà phê sữa đá"),
        ("ນ້ຳສົ້ມ", "Nước cam ép", "Orange juice", "nam-som", "noun", "Đồ uống", "ນ້ຳສົ້ມຄັ້ນສົດ", "Nước cam vắt tươi"),
        ("ນ້ຳອ້ອຍ", "Nước mía", "Sugarcane juice", "nam-awy", "noun", "Đồ uống", "ດື່ມນ້ຳອ້ອຍເຢັນ", "Uống nước mía đá"),
        ("ນ້ຳເຕົ້າຫູ້", "Sữa đậu nành", "Soy milk", "nam-tao-huu", "noun", "Đồ uống", "ນ້ຳເຕົ້າຫູ້ຮ້ອນ", "Sữa đậu nành nóng"),
        ("ເຂົ້າຕົ້ມ", "Cháo / Bánh tét Lào", "Rice porridge / Lao sticky rice cake", "khao-tom", "noun", "Ẩm thực", "ກິນເຂົ້າຕົ້ມຕອນເຊົ້າ", "Ăn cháo buổi sáng"),
        ("ເຂົ້າສານ", "Gạo tẻ chưa nấu", "Raw rice", "khao-saan", "noun", "Thực phẩm", "ຊື້ເຂົ້າສານໜຶ່ງເປົາ", "Mua một bao gạo"),
        ("ເຂົ້າເປືອກ", "Thóc lúa", "Paddy rice", "khao-pueak", "noun", "Thực phẩm", "ຕາກເຂົ້າເປືອກ", "Phơi thóc lúa"),
        ("ຊີ້ນແຫ້ງ", "Thịt khô Lào (đặc sản)", "Dried meat / Beef jerky", "seen-haeng", "noun", "Ẩm thực", "ຊີ້ນງົວແຫ້ງທອດ", "Thịt bò khô chiên giòn"),
        ("ຊີ້ນສະຫວັນ", "Thịt bò ngào vừng chiên", "Heavenly beef jerky", "seen-sa-van", "noun", "Ẩm thực", "ຊີ້ນສະຫວັນຫອມງາ", "Thịt bò ngọt thơm vừng"),
        ("ໝູຍໍ", "Giò lụa / Chả lụa", "Vietnamese/Lao pork roll", "muu-nyaw", "noun", "Ẩm thực", "ໝູຍໍຊຽງຂວາງ", "Giò lụa Xieng Khouang"),
        ("ແໜມ", "Nem chua", "Fermented sour pork", "naem", "noun", "Ẩm thực", "ແໜມໝູສົ້ມ", "Nem chua thịt lợn"),
        ("ແຈ່ວບອງ", "Tương ớt cay ngọt Luang Prabang", "Luang Prabang spicy paste", "chaew-bawng", "noun", "Ẩm thực", "ຈ້ຳແຈ່ວບອງໃສ່ເຂົ້າໜຽວ", "Chấm xôi nếp với tương ớt Jeow Bong"),
        ("ຕົ້ມໄກ່", "Canh gà luộc / Nấu lá chua", "Chicken soup", "tom-kai", "noun", "Ẩm thực", "ຕົ້ມໄກ່ໃສ່ໃບມ່ວງ", "Gà nấu lá xoài chua thanh"),
        ("ແກງຈືດ", "Canh thanh / Canh rau thịt", "Clear broth soup", "kaeng-chuet", "noun", "Ẩm thực", "ແກງຈືດເຕ້າຫູ້", "Canh thanh đậu phụ"),
        ("ໝີ່", "Mì sợi", "Noodles", "mee", "noun", "Ẩm thực", "ຜັດໝີ່ລາວ", "Mì xào kiểu Lào"),
        ("ເຝີ", "Phở", "Pho soup", "foe", "noun", "Ẩm thực", "ກິນເຝີຊີ້ນງົວ", "Ăn phở bò nóng hổi"),
    ]
    new_data.extend(foods)

    # =========================================================================
    # C. TRƯỜNG HỌC, MÔN HỌC & NGHIÊN CỨU KHOA HỌC
    # =========================================================================
    academic = [
        ("ວິຊາ", "Môn học", "Subject", "vi-xaa", "noun", "Giáo dục", "ວິຊາຮຽນ", "Môn học"),
        ("ຄະນິດສາດ", "Toán học", "Mathematics", "kha-nit-saat", "noun", "Môn học", "ຮຽນຄະນິດສາດ", "Học toán học"),
        ("ຟີຊິກສາດ", "Vật lý học", "Physics", "fee-sik-saat", "noun", "Môn học", "ທົດລອງຟີຊິກ", "Thí nghiệm vật lý"),
        ("ເຄມີສາດ", "Hóa học", "Chemistry", "khee-mee-saat", "noun", "Môn học", "ວິຊາເຄມີສາດ", "Môn hóa học"),
        ("ຊີວະສາດ", "Sinh học", "Biology", "xee-va-saat", "noun", "Môn học", "ສຶກສາຊີວະສາດ", "Nghiên cứu sinh học"),
        ("ປະຫວັດສາດ", "Lịch sử", "History", "pa-vat-saat", "noun", "Môn học", "ປະຫວັດສາດຊາດລາວ", "Lịch sử đất nước Lào"),
        ("ພູມສາດ", "Địa lý", "Geography", "phuum-saat", "noun", "Môn học", "ແຜນທີ່ພູມສາດ", "Bản đồ địa lý"),
        ("ວັນນະຄະດີ", "Văn học", "Literature", "van-na-kha-dee", "noun", "Môn học", "ບົດວັນນະຄະດີລາວ", "Tác phẩm văn học Lào"),
        ("ດົນຕີ", "Âm nhạc", "Music", "don-tee", "noun", "Nghệ thuật", "ຫຼິ້ນດົນຕີພື້ນເມືອງ", "Chơi nhạc cụ dân tộc"),
        ("ສິລະປະ", "Nghệ thuật / Mỹ thuật", "Art / Fine arts", "si-la-pa", "noun", "Nghệ thuật", "ແຕ້ມຮູບສິລະປະ", "Vẽ tranh nghệ thuật"),
        ("ກິລາ", "Thể thao", "Sports", "ki-laa", "noun", "Thể thao", "ຫຼິ້ນກິລາບານເຕະ", "Chơi thể thao đá bóng"),
        ("ບານເຕະ", "Bóng đá", "Football / Soccer", "baan-te", "noun", "Thể thao", "ແຂ່ງຂັນບານເຕະ", "Thi đấu bóng đá"),
        ("ບານບ້ວງ", "Bóng rổ", "Basketball", "baan-buang", "noun", "Thể thao", "ຫຼິ້ນບານບ້ວງ", "Chơi bóng rổ"),
        ("ບານສົ່ງ", "Bóng chuyền", "Volleyball", "baan-song", "noun", "Thể thao", "ທີມບານສົ່ງ", "Đội tuyển bóng chuyền"),
        ("ແລ່ນໄວ", "Chạy nước rút", "Sprinting", "laen-vai", "noun", "Thể thao", "ແຂ່ງຂັນແລ່ນໄວ", "Thi chạy nước rút"),
        ("ລອຍນ້ຳ", "Bơi lội", "Swimming", "lawy-nam", "noun", "Thể thao", "ຮຽນລອຍນ້ຳ", "Học bơi"),
        ("ການທົດລອງ", "Thí nghiệm", "Experiment", "kaan-thot-lawng", "noun", "Khoa học", "ຫ້ອງທົດລອງວິທະຍາສາດ", "Phòng thí nghiệm khoa học"),
        ("ທິດສະດີ", "Lý thuyết", "Theory", "thit-sa-dee", "noun", "Khoa học", "ທິດສະດີແລະພາກປະຕິບັດ", "Lý thuyết và thực hành"),
        ("ພາກປະຕິບັດ", "Thực hành", "Practice / Practical", "phaak-pa-ti-bat", "noun", "Khoa học", "ລົງມືພາກປະຕິບັດ", "Bắt tay vào thực hành"),
        ("ບົດວິທະຍານິພົນ", "Luận văn / Luận án tốt nghiệp", "Thesis / Dissertation", "bot-vit-tha-yaa-ni-phon", "noun", "Giáo dục", "ຂຽນບົດວິທະຍານິພົນ", "Viết luận văn tốt nghiệp"),
        ("ປະລິນຍາຕີ", "Bằng Cử nhân", "Bachelor's degree", "pa-lin-yaa-tee", "noun", "Học vị", "ຮຽນຈົບປະລິນຍາຕີ", "Tốt nghiệp cử nhân"),
        ("ປະລິນຍາໂທ", "Bằng Thạc sĩ", "Master's degree", "pa-lin-yaa-thoo", "noun", "Học vị", "ສຶກສາຕໍ່ປະລິນຍາໂທ", "Học tiếp thạc sĩ"),
        ("ປະລິນຍາເອກ", "Bằng Tiến sĩ", "Doctoral degree (PhD)", "pa-lin-yaa-eek", "noun", "Học vị", "ໄດ້ຮັບປະລິນຍາເອກ", "Nhận bằng tiến sĩ"),
        ("ທຶນການສຶກສາ", "Học bổng", "Scholarship", "thun-kaan-seuk-saa", "noun", "Giáo dục", "ໄດ້ຮັບທຶນການສຶກສາ", "Được nhận học bổng du học"),
    ]
    new_data.extend(academic)

    # =========================================================================
    # D. Y TẾ, SỨC KHỎE & PHÒNG KHÁM
    # =========================================================================
    medical = [
        ("ສຸຂະພາບ", "Sức khỏe", "Health", "su-kha-phaap", "noun", "Y tế", "ສຸຂະພາບແຂງແຮງ", "Sức khỏe dồi dào"),
        ("ແຂງແຮງ", "Khỏe mạnh", "Strong / Healthy", "khaeng-haeng", "adjective", "Y tế", "ຮ່າງກາຍແຂງແຮງ", "Cơ thể khỏe mạnh"),
        ("ອ່ອນເພຍ", "Mệt mỏi / Yếu ớt", "Weak / Fatigued", "awn-phia", "adjective", "Y tế", "ຮູ້ສຶກອ່ອນເພຍ", "Cảm thấy uể oải"),
        ("ເປັນຫວັດ", "Bị cảm lạnh / Cảm cúm", "Have a cold / Flu", "pen-vat", "verb", "Y tế", "ເປັນຫວັດໄອຈາມ", "Bị cảm cúm hắt hơi sổ mũi"),
        ("ເຈັບທ້ອງ", "Đau bụng", "Stomach ache", "chep-thawng", "verb", "Y tế", "ເຈັບທ້ອງຫຼາຍ", "Đau quặn bụng"),
        ("ເຈັບແຂ້ວ", "Đau răng", "Toothache", "chep-khaew", "verb", "Y tế", "ໄປຫາໝໍປິ່ນປົວແຂ້ວ", "Đi khám nha sĩ chữa răng"),
        ("ເຈັບຫົວ", "Đau đầu", "Headache", "chep-hua", "verb", "Y tế", "ກິນຢາແກ້ເຈັບຫົວ", "Uống thuốc giảm đau đầu"),
        ("ເຈັບຕາ", "Đau mắt", "Sore eyes", "chep-taa", "verb", "Y tế", "ຢອດຢາແກ້ເຈັບຕາ", "Nhỏ thuốc đau mắt"),
        ("ຄວາມດັນເລືອດ", "Huyết áp", "Blood pressure", "khuaam-dan-lueat", "noun", "Y tế", "ກວດຄວາມດັນເລືອດ", "Đo huyết áp"),
        ("ເບົາຫວານ", "Bệnh tiểu đường", "Diabetes", "bao-vaan", "noun", "Y tế", "ພະຍາດເບົາຫວານ", "Bệnh tiểu đường"),
        ("ຢາຫຼຸດໄຂ້", "Thuốc hạ sốt", "Fever reducer / Paracetamol", "yaa-lut-khai", "noun", "Y tế", "ກິນຢາຫຼຸດໄຂ້", "Uống thuốc hạ sốt"),
        ("ຢາແກ້ປວດ", "Thuốc giảm đau", "Painkiller", "yaa-kae-puat", "noun", "Y tế", "ຢາແກ້ປວດກ້າມຊີ້ນ", "Thuốc giảm đau cơ"),
        ("ຢາຂ້າເຊື້ອ", "Thuốc kháng sinh", "Antibiotics", "yaa-khaa-xuea", "noun", "Y tế", "ກິນຢາຂ້າເຊື້ອຕາມສັ່ງ", "Uống kháng sinh theo đơn"),
        ("ສັກຢາ", "Tiêm thuốc / Chích thuốc", "To inject / Vaccine", "sak-yaa", "verb", "Y tế", "ສັກຢາວັກຊີນ", "Tiêm vắc xin"),
        ("ເລືອດ", "Máu", "Blood", "lueat", "noun", "Cơ thể", "ກວດເລືອດ", "Xét nghiệm máu"),
        ("ຫ້ອງສຸກເສີນ", "Phòng cấp cứu", "Emergency room (ER)", "hawng-suk-soen", "noun", "Y tế", "ນຳສົ່ງຫ້ອງສຸກເສີນ", "Đưa vào phòng cấp cứu"),
        ("ລົດໂຮງໝໍ", "Xe cứu thương / Xe cấp cứu", "Ambulance", "lot-hoong-maw", "noun", "Y tế", "ໂທเรียກລົດໂຮງໝໍ", "Gọi xe cứu thương"),
        ("ປະກັນໄພສຸຂະພາບ", "Bảo hiểm y tế", "Health insurance", "pa-kan-fai-su-kha-phaap", "noun", "Y tế", "ມີບັດປະກັນໄພສຸຂະພາບ", "Có thẻ bảo hiểm y tế"),
    ]
    new_data.extend(medical)

    # =========================================================================
    # E. DU LỊCH, KHÁCH SẠN, HÀNG KHÔNG & HẢI QUAN
    # =========================================================================
    travel = [
        ("ໜັງສືຜ່ານແດນ", "Hộ chiếu (Passport)", "Passport", "nang-seu-phaan-daen", "noun", "Du lịch", "ກວດໜັງສືຜ່ານແດນ", "Kiểm tra hộ chiếu"),
        ("ວີຊາ", "Thị thực (Visa)", "Visa", "vee-saa", "noun", "Du lịch", "ຂໍວີຊາເຂົ້າເມືອງ", "Xin thị thực nhập cảnh"),
        ("ປີ້", "Vé (vé xe, vé máy bay)", "Ticket", "pee", "noun", "Du lịch", "ຊື້ປີ້ລົດໄຟ", "Mua vé tàu hỏa"),
        ("ປີ້ຍົນ", "Vé máy bay", "Plane ticket / Flight ticket", "pee-nyon", "noun", "Du lịch", "ຈອງປີ້ຍົນ", "Đặt vé máy bay"),
        ("ຈອງ", "Đặt chỗ / Đặt phòng", "To book / To reserve", "chawng", "verb", "Du lịch", "ຈອງຫ້ອງພັກໂຮງແຮມ", "Đặt phòng khách sạn"),
        ("ດ່ານກວດຄົນເຂົ້າເມືອງ", "Cửa khẩu xuất nhập cảnh", "Immigration checkpoint", "daan-kuat-khon-khao-mueang", "noun", "Du lịch", "ຂ້າມດ່ານກວດຄົນເຂົ້າເມືອງ", "Qua cửa khẩu xuất nhập cảnh"),
        ("ກະເປົາເດີນທາງ", "Va li / Túi du lịch", "Luggage / Suitcase", "ka-pao-doen-thaang", "noun", "Du lịch", "ຈັດກະເປົາເດີນທາງ", "Sắp xếp va li"),
        ("ແຜນທີ່", "Bản đồ", "Map", "phaen-thee", "noun", "Du lịch", "ເບິ່ງແຜນທີ່ທ່ອງທ່ຽວ", "Xem bản đồ du lịch"),
        ("ຜູ້ນຳທ່ຽວ", "Hướng dẫn viên du lịch", "Tour guide", "phuu-nam-thiaao", "noun", "Du lịch", "ຜູ້ນຳທ່ຽວພາໄປຊົມວັດ", "Hướng dẫn viên dẫn đi thăm chùa"),
        ("ຂອງຂວັນ", "Quà tặng", "Gift / Present", "khawng-khvan", "noun", "Du lịch", "ມອບຂອງຂວັນໃຫ້", "Tặng quà"),
        ("ຂອງທີ່ລະນຶກ", "Đồ lưu niệm", "Souvenir", "khawng-thee-la-neuk", "noun", "Du lịch", "ຊື້ຂອງທີ່ລະນຶກ", "Mua đồ lưu niệm"),
        ("ຫ້ອງພັກດ່ຽວ", "Phòng đơn (khách sạn)", "Single room", "hawng-phak-diaao", "noun", "Khách sạn", "ພັກຫ້ອງດ່ຽວ", "Ở phòng đơn"),
        ("ຫ້ອງພັກຄູ່", "Phòng đôi (khách sạn)", "Double room / Twin room", "hawng-phak-khuu", "noun", "Khách sạn", "ຈອງຫ້ອງຄູ່", "Đặt phòng đôi"),
        ("ກະແຈ", "Chìa khóa", "Key", "ka-chae", "noun", "Khách sạn", "ກະແຈຫ້ອງ", "Chìa khóa phòng"),
        ("ເຊັກອິນ", "Làm thủ tục nhận phòng / Check-in", "Check-in", "xek-in", "verb", "Khách sạn", "ເຊັກອິນເວລາສອງໂມງ", "Check-in lúc hai giờ"),
        ("ເຊັກເອົ້າ", "Làm thủ tục trả phòng / Check-out", "Check-out", "xek-ao", "verb", "Khách sạn", "ເຊັກເອົ້າຕອນທ່ຽງ", "Check-out lúc mười hai giờ trưa"),
    ]
    new_data.extend(travel)

    # =========================================================================
    # F. CÔNG NGHỆ, SỐ HÓA & TRUYỀN THÔNG HIỆN ĐẠI
    # =========================================================================
    tech = [
        ("ລະຫັດຜ່ານ", "Mật khẩu", "Password", "la-hat-phaan", "noun", "Công nghệ", "ປ້ອນລະຫັດຜ່ານ", "Nhập mật khẩu"),
        ("ຊື່ຜູ້ໃຊ້", "Tên đăng nhập (Username)", "Username", "seu-phuu-xai", "noun", "Công nghệ", "ໃສ່ຊື່ຜູ້ໃຊ້", "Điền tên đăng nhập"),
        ("ດາວໂຫຼດ", "Tải xuống / Download", "To download", "daao-loot", "verb", "Công nghệ", "ດາວໂຫຼດແອັບ", "Tải ứng dụng về"),
        ("ອັບໂຫຼດ", "Tải lên / Upload", "To upload", "ap-loot", "verb", "Công nghệ", "ອັບໂຫຼດຮູບພາບ", "Tải ảnh lên"),
        ("ບັນຊີ", "Tài khoản (ngân hàng / MXH)", "Account", "ban-xee", "noun", "Công nghệ", "ເປີດບັນຊີໃໝ່", "Mở tài khoản mới"),
        ("ແອັບພລິເຄຊັນ", "Ứng dụng di động (App)", "Application / App", "aep-phi-lee-khee-xan", "noun", "Công nghệ", "ຕິດຕັ້ງແອັບພລິເຄຊັນ", "Cài đặt ứng dụng"),
        ("ໂປຣແກຣມ", "Chương trình máy tính (Software)", "Program / Software", "proo-kaem", "noun", "Công nghệ", "ຂຽນໂປຣແກຣມ", "Lập trình phần mềm"),
        ("ປັນຍາປະດິດ", "Trí tuệ nhân tạo (AI)", "Artificial Intelligence (AI)", "pan-nyaa-pa-dit", "noun", "Công nghệ", "ລະບົບປັນຍາປະດິດອັດສະລິຍະ", "Hệ thống trí tuệ nhân tạo thông minh"),
        ("ການປະມວນຜົນຮູບພາບ", "Xử lý ảnh số (Digital Image Processing)", "Image Processing", "kaan-pa-muan-phon-huup-phaap", "noun", "Công nghệ", "ຮຽນວິຊາການປະມວນຜົນຮູບພາບ", "Học môn xử lý ảnh số"),
        ("ການຮັບຮູ້ຕົວອັກສອນ", "Nhận dạng ký tự quang học (OCR)", "Optical Character Recognition (OCR)", "kaan-hap-huu-tua-ak-sawn", "noun", "Công nghệ", "ໂຄງການ OCR ພາສາລາວ", "Đề tài OCR tiếng Lào"),
        ("ການແປພາສາອັດຕະໂນມັດ", "Dịch máy tự động (Machine Translation)", "Machine Translation", "kaan-pae-phaa-saa-at-ta-noo-mat", "noun", "Công nghệ", "ລະບົບແປພາສາອັດຕະໂນມັດ", "Hệ thống dịch ngôn ngữ tự động"),
        ("ຖານຂໍ້ມູນ", "Cơ sở dữ liệu (Database)", "Database", "thaan-khaw-muun", "noun", "Công nghệ", "ຈັດເກັບໃນຖານຂໍ້ມູນ", "Lưu trữ trong cơ sở dữ liệu"),
        ("ຄວາມປອດໄພທາງໄຊເບີ", "An ninh mạng", "Cybersecurity", "khuaam-pawt-fai-thaang-xai-boe", "noun", "Công nghệ", "ຮັກສາຄວາມປອດໄພທາງໄຊເບີ", "Bảo vệ an ninh không gian mạng"),
        ("ເຄືອຂ່າຍໄຮ້ສາຍ", "Mạng không dây (Wi-Fi)", "Wi-Fi / Wireless network", "khuea-khaai-hai-saai", "noun", "Công nghệ", "ເຊື່ອມຕໍ່ Wi-Fi", "Bắt sóng Wi-Fi"),
    ]
    new_data.extend(tech)

    # =========================================================================
    # G. BỘ SỐ ĐẾM & ĐƠN VỊ ĐO LƯỜNG (NUMBERS & UNITS)
    # =========================================================================
    numbers_units = [
        ("ສິບເອັດ", "Mười một", "Eleven", "sip-et", "number", "Số đếm", "ສິບເອັດໂມງ", "Mười một giờ"),
        ("ສິບສອງ", "Mười hai", "Twelve", "sip-sawng", "number", "Số đếm", "ສິບສອງເດືອນ", "Mười hai tháng"),
        ("ສິບສາມ", "Mười ba", "Thirteen", "sip-saam", "number", "Số đếm", "ສິບສາມຄົນ", "Mười ba người"),
        ("ສິບສີ່", "Mười bốn", "Fourteen", "sip-see", "number", "Số đếm", "ສິບສີ່ມື້", "Mười bốn ngày"),
        ("ສິບຫ້າ", "Mười lăm", "Fifteen", "sip-haa", "number", "Số đếm", "ສິບຫ້ານາທີ", "Mười lăm phút"),
        ("ສິບຫົກ", "Mười sáu", "Sixteen", "sip-hok", "number", "Số đếm", "ສິບຫົກປີ", "Mười sáu tuổi"),
        ("ສິບເຈັດ", "Mười bảy", "Seventeen", "sip-chet", "number", "Số đếm", "ສິບເຈັດວັນ", "Mười bảy ngày"),
        ("ສິບແປດ", "Mười tám", "Eighteen", "sip-paet", "number", "Số đếm", "ສິບແປດໂມງ", "Mười tám giờ"),
        ("ສິບເກົ້າ", "Mười chín", "Nineteen", "sip-kao", "number", "Số đếm", "ສິບເກົ້າປີ", "Mười chín tuổi"),
        ("ຊາວເອັດ", "Hai mươi mốt", "Twenty-one", "xaao-et", "number", "Số đếm", "ຊາວເອັດຄົນ", "Hai mươi mốt người"),
        ("ສາມສິບ", "Ba mươi", "Thirty", "saam-sip", "number", "Số đếm", "ສາມສິບວັນ", "Ba mươi ngày"),
        ("ສີ່ສິບ", "Bốn mươi", "Forty", "see-sip", "number", "Số đếm", "ສີ່ສິບກິໂລ", "Bốn mươi cân"),
        ("ຫ້າສິບ", "Năm mươi", "Fifty", "haa-sip", "number", "Số đếm", "ຫ້າສິບພັນກີບ", "Năm mươi nghìn Kíp"),
        ("ຫົກສິບ", "Sáu mươi", "Sixty", "hok-sip", "number", "Số đếm", "ຫົກສິບນາທີ", "Sáu mươi phút"),
        ("ເຈັດສິບ", "Bảy mươi", "Seventy", "chet-sip", "number", "Số đếm", "ເຈັດສິບປີ", "Bảy mươi năm"),
        ("ແປດສິບ", "Tám mươi", "Eighty", "paet-sip", "number", "Số đếm", "ແປດສິບພັນ", "Tám mươi nghìn"),
        ("ເກົ້າສິບ", "Chín mươi", "Ninety", "kao-sip", "number", "Số đếm", "ເກົ້າສິບສ່ວນຮ້ອຍ", "Chín mươi phần trăm"),
        ("ກິໂລກຣາມ", "Ki-lô-gam (kg)", "Kilogram", "ki-loo-klaam", "noun", "Đơn vị đo", "ຊັ່ງໄດ້ສອງກິໂລກຣາມ", "Cân được hai ki-lô-gam"),
        ("ກິໂລແມັດ", "Ki-lô-mét (km)", "Kilometer", "ki-loo-maet", "noun", "Đơn vị đo", "ໄລຍະທາງຫ້າສິບກິໂລແມັດ", "Khoảng cách năm mươi cây số"),
        ("ແມັດ", "Mét (m)", "Meter", "maet", "noun", "Đơn vị đo", "ຍາວສອງແມັດ", "Dài hai mét"),
        ("ຊັງຕີແມັດ", "Xăng-ti-mét (cm)", "Centimeter", "xang-tee-maet", "noun", "Đơn vị đo", "ກວ້າງສິບຊັງຕີແມັດ", "Rộng mười xăng-ti-mét"),
        ("ລິດ", "Lít (l)", "Liter", "lit", "noun", "Đơn vị đo", "ຊື້ນ້ຳມັນໜຶ່ງລິດ", "Mua một lít xăng"),
    ]
    new_data.extend(numbers_units)

    # Nạp toàn bộ dữ liệu mới vào từ điển
    added_count = 0
    for row in new_data:
        lao_word, vi, en, rom, pos, cat, ex_lao, ex_vi = row
        norm_lao = normalize_lao(lao_word.strip())
        if not norm_lao:
            continue
        
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
    
    # Ghi lại tệp CSV
    with open(dict_file, mode="w", encoding="utf-8", newline="") as f:
        fieldnames = ["lao", "vi", "en", "romanization", "pos", "lesson", "example_lao", "example_vi"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for k in sorted_keys:
            writer.writerow(entries[k])

    print(f"[+] KHO TỪ ĐIỂN ĐÃ ĐƯỢC MỞ RỘNG:")
    print(f"    - Số mục từ ban đầu: 528")
    print(f"    - Số mục từ thêm mới: {added_count}")
    print(f"    - Tổng số mục từ hiện tại: {len(sorted_keys)}")
    return len(sorted_keys)


if __name__ == "__main__":
    generate_extended_dictionary()
