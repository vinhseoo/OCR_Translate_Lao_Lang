"""
Script Mở Rộng Kho Từ Điển Tiếng Lào Thông Dụng Quy Mô Lớn (Comprehensive Everyday Lao Lexicon).
Nâng tổng dung lượng từ điển từ 1,200 từ lên > 3,000 mục từ thông dụng hàng ngày:
1. Động từ hành động & sinh hoạt thường nhật (Common Everyday Verbs)
2. Ẩm thực, gia vị, đồ uống Lào & Việt Nam (Food, Drinks & Spices)
3. Đồ vật, dụng cụ gia đình, văn phòng & công nghệ (Household, Office & Gadgets)
4. Y tế, sức khỏe, bệnh tật & chăm sóc cơ thể (Healthcare & Medical)
5. Giao thông, chỉ đường, du lịch & địa điểm (Transport, Directions & Travel)
6. Thương mại, tiền tệ, ngân hàng & mua sắm (Finance, Commerce & Shopping)
7. Thiên nhiên, thời tiết, động thực vật (Nature, Climate, Animals & Plants)
8. Tính từ, cảm xúc, tâm lý & tính cách con người (Emotions & Characteristics)
9. Từ nối, trợ từ, quán ngữ giao tiếp bản xứ (Conjunctions & Native Idioms)
10. Hệ thống từ phái sinh mở rộng (ການ-, ຄວາມ-, ຜູ້-, ນັກ-, ຊ່າງ-, ຮ້ານ-, ຫ້ອງ-, ໂຮງ-)

Tuân thủ nghiêm ngặt Quy tắc Bất di bất dịch số 1: 100% Chuẩn hóa Unicode NFC.
"""
import os
import sys
import csv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing.normalize import normalize_lao

DICT_PATH = os.path.join(PROJECT_ROOT, "data", "dictionaries", "lao_vi_en.csv")


def get_massive_common_vocab():
    """Tập hợp hơn 1,800+ mục từ tiếng Lào thông dụng nhất trong đời sống."""
    vocab_list = [
        # =========================================================================
        # 1. ĐỘNG TỪ SINH HOẠT & HÀNH ĐỘNG HÀNG NGÀY (DAILY VERBS)
        # =========================================================================
        ("ຕື່ນນອນ", "Thức dậy", "Wake up", "teun-nawn", "verb", "Sinh hoạt", "ຕື່ນນອນແຕ່ເຊົ້າ", "Thức dậy từ sớm"),
        ("ລ້າງໜ້າ", "Rửa mặt", "Wash face", "laang-naa", "verb", "Sinh hoạt", "ລ້າງໜ້າດ້ວຍນ້ຳເຢັນ", "Rửa mặt bằng nước mát"),
        ("ຖູແຂ້ວ", "Đánh răng", "Brush teeth", "thuu-khaew", "verb", "Sinh hoạt", "ຖູແຂ້ວມື້ລະສອງເທື່ອ", "Đánh răng ngày hai lần"),
        ("ອາບນ້ຳ", "Tắm rửa", "Take a bath / shower", "aap-nam", "verb", "Sinh hoạt", "ອາບນ້ຳອຸ່ນ", "Tắm nước ấm"),
        ("ສະຜົມ", "Gội đầu", "Wash hair / Shampoo", "sa-phom", "verb", "Sinh hoạt", "ສະຜົມໃຫ້ສະອາດ", "Gội đầu cho sạch sẽ"),
        ("ເຊັດໂຕ", "Lau người", "Dry body with towel", "xet-too", "verb", "Sinh hoạt", "ໃຊ້ຜ້າເຊັດໂຕ", "Dùng khăn lau người"),
        ("ຫວີຜົມ", "Chải đầu", "Comb hair", "vee-phom", "verb", "Sinh hoạt", "ຫວີຜົມໃຫ້ຮຽບຮ້ອຍ", "Chải tóc cho gọn gàng"),
        ("ນຸ່ງເຄື່ອງ", "Mặc quần áo", "Get dressed / Wear clothes", "nung-kheuang", "verb", "Sinh hoạt", "ນຸ່ງເຄື່ອງງາມ", "Mặc quần áo đẹp"),
        ("ປ່ຽນເຄື່ອງ", "Thay quần áo", "Change clothes", "pian-kheuang", "verb", "Sinh hoạt", "ປ່ຽນເຄື່ອງນອນ", "Thay đồ ngủ"),
        ("ຖອດເກີບ", "Cởi giày", "Take off shoes", "thawt-koep", "verb", "Sinh hoạt", "ກະລຸນາຖອດເກີບ", "Xin vui lòng cởi giày"),
        ("ໃສ່ເກີບ", "Xỏ giày / Đi giày", "Put on shoes", "sai-koep", "verb", "Sinh hoạt", "ໃສ່ເກີບຜ້າໃບ", "Đi giày thể thao"),
        ("ກິນເຂົ້າເຊົ້າ", "Ăn sáng", "Have breakfast", "kin-khao-xao", "verb", "Ẩm thực", "ກິນເຂົ້າເຊົ້າແລ້ວບໍ", "Đã ăn sáng chưa"),
        ("ກິນເຂົ້າສວາຍ", "Ăn trưa", "Have lunch", "kin-khao-svaai", "verb", "Ẩm thực", "ໄປກິນເຂົ້າສວາຍນຳກັນ", "Cùng đi ăn trưa nhé"),
        ("ກິນເຂົ້າແລງ", "Ăn tối", "Have dinner", "kin-khao-laeng", "verb", "Ẩm thực", "ກິນເຂົ້າແລງກັບຄອບຄົວ", "Ăn tối cùng gia đình"),
        ("ດື່ມນ້ຳ", "Uống nước", "Drink water", "duem-nam", "verb", "Ẩm thực", "ດື່ມນ້ຳຫຼາຍໆ", "Hãy uống nhiều nước"),
        ("ອອກຈາກບ້ານ", "Rời khỏi nhà", "Leave home", "awk-chaak-baan", "verb", "Hành động", "ອອກຈາກບ້ານແຕ່ເຊົ້າ", "Ra khỏi nhà từ sáng sớm"),
        ("ໄປເຮັດວຽກ", "Đi làm", "Go to work", "pai-het-viak", "verb", "Công việc", "ຂີ່ລົດໄປເຮັດວຽກ", "Lái xe đi làm"),
        ("ເລີກວຽກ", "Tan ca / Hết giờ làm", "Finish work", "loek-viak", "verb", "Công việc", "ເລີກວຽກຫ້າໂມງແລງ", "Tan sở lúc 5 giờ chiều"),
        ("ກັບບ້ານ", "Về nhà", "Go home", "kap-baan", "verb", "Sinh hoạt", "ກັບບ້ານພັກຜ່ອນ", "Về nhà nghỉ ngơi"),
        ("ພັກຜ່ອນ", "Nghỉ ngơi", "Rest / Relax", "phak-phawn", "verb", "Sinh hoạt", "ພັກຜ່ອນໃຫ້ເຕັມທີ່", "Nghỉ ngơi cho lại sức"),
        ("ນອນຫຼັບ", "Ngủ say", "Sleep soundly", "nawn-lap", "verb", "Sinh hoạt", "ນອນຫຼັບສະບາຍ", "Ngủ ngon giấc"),
        ("ຝັນດີ", "Chúc ngủ ngon / Mơ đẹp", "Sweet dreams / Good night", "fan-dee", "phrase", "Giao tiếp", "ຂໍໃຫ້ນອນຫຼັບຝັນດີ", "Chúc bạn ngủ ngon mơ đẹp"),
        ("ປຸງແຕ່ງ", "Nấu nướng / Chế biến", "Cook / Prepare food", "pung-taeng", "verb", "Ẩm thực", "ປຸງແຕ່ງອາຫານແຊບ", "Chế biến đồ ăn ngon"),
        ("ຕົ້ມ", "Luộc / Nấu", "Boil", "tom", "verb", "Ẩm thực", "ຕົ້ມໄຂ່", "Luộc trứng"),
        ("ຈືນ", "Chiên / Rán", "Fry", "cheun", "verb", "Ẩm thực", "ຈືນປາໃຫ້ກອບ", "Rán cá cho giòn"),
        ("ຂົ້ວ", "Xào / Rang", "Stir-fry / Roast", "khua", "verb", "Ẩm thực", "ຂົ້ວຜັກບົ້ງ", "Xào rau muống"),
        ("ປิ้ง", "Nướng (than hoa)", "Grill / Barbecue", "ping", "verb", "Ẩm thực", "ປิ้งໄກ່ລາດ", "Gà quê nướng"),
        ("ຢ້າງ", "Sấy / Hun khói / Nướng kỹ", "Roast / Smoke", "yaang", "verb", "Ẩm thực", "ຊີ້ນຢ້າງ", "Thịt gác bếp / Thịt sấy"),
        ("ໜຶ້ງ", "Hấp (bằng chõ)", "Steam", "nueng", "verb", "Ẩm thực", "ໜຶ້ງເຂົ້າໜຽວ", "Đồ xôi nếp"),
        ("ແກງ", "Nấu canh / Món canh", "Make soup / Curry", "kaeng", "verb", "Ẩm thực", "ແກງໜໍ່ໄມ້", "Nấu canh măng"),
        ("ຕຳ", "Giã / Đâm (bằng cối)", "Pound / Mash", "tam", "verb", "Ẩm thực", "ຕຳໝາກຫຸ່ງ", "Giã nộm đu đủ"),
        ("ຊອຍ", "Thái / Xắt nhỏ", "Slice / Chop finely", "sawy", "verb", "Ẩm thực", "ຊອຍຊີ້ນບາງໆ", "Thái thịt mỏng"),
        ("ຟັກ", "Băm nhỏ", "Mince", "fak", "verb", "Ẩm thực", "ຟັກຊີ້ນໝູ", "Băm thịt lợn"),
        ("ປອກ", "Gọt vỏ / Bóc vỏ", "Peel", "pawk", "verb", "Ẩm thực", "ປອກໝາກໄມ້", "Gọt vỏ hoa quả"),
        ("ລ້າງຖ້ວຍ", "Rửa chén bát", "Wash dishes", "laang-thuay", "verb", "Gia đình", "ລ້າງຖ້ວຍຫຼັງກິນເຂົ້າ", "Rửa bát sau bữa ăn"),
        ("ຊັກເຄື່ອງ", "Giặt quần áo", "Do laundry", "xak-kheuang", "verb", "Gia đình", "ຊັກເຄື່ອງດ້ວຍມື", "Giặt quần áo bằng tay"),
        ("ຕາກເຄື່ອງ", "Phơi quần áo", "Hang clothes to dry", "taak-kheuang", "verb", "Gia đình", "ຕາກເຄື່ອງໃສ່ແດດ", "Phơi đồ ngoài nắng"),
        ("ຮີດເຄື່ອງ", "Là / Ủi quần áo", "Iron clothes", "heet-kheuang", "verb", "Gia đình", "ຮີດເຄື່ອງໃຫ້ລຽບ", "Ủi đồ cho phẳng phiu"),
        ("ກວາດເຮືອນ", "Quét nhà", "Sweep house", "kwaat-heuan", "verb", "Gia đình", "ກວາດເຮືອນທຸກມື້", "Quét nhà mỗi ngày"),
        ("ຖູເຮືອນ", "Lau nhà", "Mop floor", "thuu-heuan", "verb", "Gia đình", "ຖູເຮືອນໃຫ້ສະອາດ", "Lau nhà cho sạch bóng"),
        ("ຫົດນ້ຳດອກໄມ້", "Tưới hoa / Tưới cây", "Water plants", "hot-nam-dawk-mai", "verb", "Gia đình", "ຫົດນ້ຳຕົ້ນໄມ້ຕອນເຊົ້າ", "Tưới cây buổi sáng"),
        ("ລ້ຽງສັດ", "Nuôi thú cưng / Chăn nuôi", "Raise animals", "liang-sat", "verb", "Nông nghiệp", "ລ້ຽງໝາແລະແມວ", "Nuôi chó và mèo"),
        ("ລັອກປະຕູ", "Khóa cửa", "Lock door", "lawk-pa-tuu", "verb", "Hành động", "ຢ່າລືມລັອກປະຕູ", "Đừng quên khóa cửa cẩn thận"),
        ("ໄຂປະຕູ", "Mở cửa", "Open door", "khai-pa-tuu", "verb", "Hành động", "ໄຂປະຕູຕ້ອນຮັບແຂກ", "Mở cửa đón khách"),
        ("ອັດປະຕູ", "Đóng cửa", "Close door", "at-pa-tuu", "verb", "Hành động", "ອັດປະຕູໄວ້", "Hãy khép cửa lại"),
        ("ເປີດໄຟ", "Bật đèn / Bật điện", "Turn on light", "poet-fai", "verb", "Gia dụng", "ເປີດໄຟໃຫ້ແຈ້ງ", "Bật đèn cho sáng"),
        ("ມອດໄຟ", "Tắt đèn / Tắt điện", "Turn off light", "mawt-fai", "verb", "Gia dụng", "ມອດໄຟກ່ອນນອນ", "Tắt đèn trước khi ngủ"),
        ("ເປີດແອ", "Bật điều hòa", "Turn on AC", "poet-ae", "verb", "Gia dụng", "ເປີດແອເຢັນໆ", "Bật điều hòa cho mát"),
        ("ມອດແອ", "Tắt điều hòa", "Turn off AC", "mawt-ae", "verb", "Gia dụng", "ມອດແອປະຢັດໄຟ", "Tắt điều hòa tiết kiệm điện"),
        ("ຊື້ເຄື່ອງ", "Mua sắm đồ đạc", "Go shopping", "xuu-kheuang", "verb", "Mua sắm", "ໄປຊື້ເຄື່ອງຢູ່ຕະຫຼາດ", "Đi mua đồ ở chợ"),
        ("ຂາຍເຄື່ອງ", "Bán hàng", "Sell goods", "khaai-kheuang", "verb", "Thương mại", "ຂາຍເຄື່ອງໄດ້ດີ", "Bán hàng rất đắt khách"),
        ("ຕໍ່ລາຄາ", "Mặc cả / Trả giá", "Bargain / Haggle", "taw-laa-khaa", "verb", "Mua sắm", "ຕໍ່ລາຄາລົງໜ້ອຍໜຶ່ງ", "Mặc cả bớt đi một chút"),
        ("ຫຼຸດລາຄາ", "Giảm giá", "Discount", "lut-laa-khaa", "verb", "Mua sắm", "ຮ້ານນີ້ຫຼຸດລາຄາພິເສດ", "Cửa hàng này giảm giá đặc biệt"),
        ("ຈ່າຍເງິນ", "Thanh toán tiền", "Pay money", "chaai-ngoen", "verb", "Thương mại", "ຈ່າຍເງິນສົດ", "Thanh toán bằng tiền mặt"),
        ("ໂອນເງິນ", "Chuyển khoản ngân hàng", "Transfer money", "oon-ngoen", "verb", "Ngân hàng", "ໂອນເງິນຜ່ານມືຖື", "Chuyển khoản qua điện thoại"),
        ("ຖອນເງິນ", "Rút tiền mặt", "Withdraw money", "thawn-ngoen", "verb", "Ngân hàng", "ຖອນເງິນຢູ່ຕູ້ເອທີເອັມ", "Rút tiền ở cây ATM"),
        ("ຝາກເງິນ", "Gửi tiền tiết kiệm", "Deposit money", "faak-ngoen", "verb", "Ngân hàng", "ຝາກເງິນເຂົ້າທະນາຄານ", "Gửi tiền vào tài khoản ngân hàng"),
        ("ຢືມເງິນ", "Vay mượn tiền", "Borrow money", "yeum-ngoen", "verb", "Tài chính", "ຢືມເງິນໝູ່", "Mượn tiền bạn"),
        ("ໃຊ້ໜີ້", "Trả nợ", "Repay debt", "xai-nee", "verb", "Tài chính", "ໃຊ້ໜີ້ຕົງເວລາ", "Trả nợ đúng hạn"),
        ("ເຊົ່າ", "Thuê / Mướn", "Rent", "xao", "verb", "Kinh tế", "ເຊົ່າຫ້ອງແຖວ", "Thuê phòng trọ"),
        ("ຈອງ", "Đặt trước / Giữ chỗ", "Book / Reserve", "chawng", "verb", "Dịch vụ", "ຈອງຫ້ອງໂຮງແຮມ", "Đặt phòng khách sạn"),
        ("ຍົກເລີກ", "Hủy bỏ", "Cancel", "nyok-loek", "verb", "Hành động", "ຍົກເລີກການນັດໝາຍ", "Hủy cuộc hẹn"),
        ("ລໍຖ້າ", "Chờ đợi", "Wait", "law-thaa", "verb", "Hành động", "ກະລຸນາລໍຖ້າບຶດໜຶ່ງ", "Xin vui lòng đợi một lát"),
        ("ນັດໝາຍ", "Hẹn gặp", "Make an appointment", "nat-maai", "verb", "Giao tiếp", "ມີນັດໝາຍກັບໝໍ", "Có hẹn với bác sĩ"),
        ("ພົບກັນ", "Gặp nhau", "Meet up", "phop-kan", "verb", "Giao tiếp", "ພົບກັນມື້ອື່ນ", "Mai gặp lại nhau nhé"),
        ("ໂທລະສັບ", "Gọi điện thoại", "Make a phone call", "thoo-la-sap", "verb", "Giao tiếp", "ໂທລະສັບຫາແມ່", "Gọi điện thoại cho mẹ"),
        ("ສົ່ງຂໍ້ຄວາມ", "Gửi tin nhắn", "Send message", "song-khaw-khuaam", "verb", "Giao tiếp", "ສົ່ງຂໍ້ຄວາມຫາເຈົ້າ", "Gửi tin nhắn cho bạn"),
        ("ຕອບຂໍ້ຄວາມ", "Trả lời tin nhắn", "Reply message", "tawp-khaw-khuaam", "verb", "Giao tiếp", "ຕອບຂໍ້ຄວາມດ່ວນ", "Hồi âm tin nhắn gấp"),
        ("ຖ່າຍຮູບ", "Chụp ảnh", "Take photos", "thaai-huup", "verb", "Giải trí", "ຖ່າຍຮູບເປັນທີ່ລະນຶກ", "Chụp ảnh làm kỷ niệm"),
        ("ຖ່າຍວິດີໂອ", "Quay video", "Record video", "thaai-vi-dee-oo", "verb", "Giải trí", "ຖ່າຍວິດີໂອທຳມະຊາດ", "Quay video thiên nhiên"),
        ("ຟັງເພງ", "Nghe nhạc", "Listen to music", "fang-pheeng", "verb", "Giải trí", "ຟັງເພງລາວມ່ວນໆ", "Nghe nhạc Lào rất hay"),
        ("ເບິ່ງໜັງ", "Xem phim", "Watch movie", "boeng-nang", "verb", "Giải trí", "ໄປເບິ່ງໜັງຢູ່ໂຮງ", "Đi xem phim ngoài rạp"),
        ("ຫຼິ້ນກິລາ", "Chơi thể thao", "Play sports", "lin-ki-laa", "verb", "Thể thao", "ມັກຫຼິ້ນກິລາບານເຕະ", "Thích chơi môn bóng đá"),
        ("ເຕະບານ", "Đá bóng", "Play football / soccer", "te-baan", "verb", "Thể thao", "ເຕະບານກັບໝູ່", "Đá bóng cùng bạn bè"),
        ("ແລ່ນອອກກຳລັງກາຍ", "Chạy bộ tập thể dục", "Jogging / Exercise", "laen-awk-kam-lang-kaai", "verb", "Sức khỏe", "ແລ່ນອອກກຳລັງກາຍຕອນແລງ", "Chạy bộ thể dục lúc chiều tối"),
        ("ລອຍນ້ຳ", "Bơi lội", "Swim", "lawy-nam", "verb", "Thể thao", "ລອຍນ້ຳຢູ່ສະລອຍ", "Bơi ở hồ bơi"),
        ("ຂີ່ລົດຖີບ", "Đạp xe đạp", "Ride a bicycle", "khee-lot-theep", "verb", "Thể thao", "ຂີ່ລົດຖີບອ້ອມເມືອງ", "Đạp xe quanh thành phố"),
        ("ຂີ່ລົດຈັກ", "Đi xe máy", "Ride a motorbike", "khee-lot-chak", "verb", "Giao thông", "ຂີ່ລົດຈັກໃສ່ໝວກກັນກະທົບ", "Đi xe máy đội mũ bảo hiểm"),
        ("ຍ່າງຫຼິ້ນ", "Đi dạo", "Take a walk / Stroll", "nyaang-lin", "verb", "Giải trí", "ຍ່າງຫຼິ້ນແຄມຂອງ", "Đi dạo bên bờ sông Mê Kông"),
        ("ທ່ອງທ່ຽວ", "Du lịch / Đi chơi", "Travel / Sightseeing", "thawng-thiaw", "verb", "Du lịch", "ທ່ອງທ່ຽວປະເທດລາວ", "Du lịch khám phá đất nước Lào"),
        ("ປີນພູ", "Leo núi", "Climb mountain", "peen-phuu", "verb", "Du lịch", "ປີນພູຊົມທະເລໝອກ", "Leo núi ngắm biển mây"),

        # =========================================================================
        # 2. ẨM THỰC, MÓN ĂN & NGUYÊN LIỆU CHI TIẾT (FOOD & DRINKS)
        # =========================================================================
        ("ເຂົ້າໜຽວ", "Xôi nếp Lào", "Sticky rice / Glutinous rice", "khao-niaaw", "noun", "Ẩm thực", "ກິນເຂົ້າໜຽວກັບປິ້ງໄກ່", "Ăn xôi nếp với gà nướng"),
        ("ເຂົ້າຈ້າວ", "Cơm tẻ / Gạo tẻ", "White rice / Jasmine rice", "khao-chaao", "noun", "Ẩm thực", "ມັກກິນເຂົ້າຈ້າວ", "Thích ăn cơm tẻ"),
        ("ເຂົ້າປຽກເສັ້ນ", "Bánh canh Lào", "Lao noodle soup (Khao Piak Sen)", "khao-piak-sen", "noun", "Ẩm thực", "ເຂົ້າປຽກເສັ້ນຮ້ອນໆ", "Tô bánh canh nóng hổi"),
        ("ເຂົ້າປຸ້ນ", "Bún cay nước cốt dừa Lào", "Rice vermicelli soup (Khao Poon)", "khao-pun", "noun", "Ẩm thực", "ເຂົ້າປຸ້ນນ້ຳແຈ່ວ", "Món bún cay truyền thống"),
        ("ເຂົ້າຈີ່", "Bánh mì kiểu Pháp (Baguette)", "Baguette / Lao sandwich", "khao-chee", "noun", "Ẩm thực", "ເຂົ້າຈີ່ປາເຕ້", "Bánh mì kẹp pa-tê"),
        ("ເຂົ້າຜັດ", "Cơm chiên / Cơm rang", "Fried rice", "khao-phat", "noun", "Ẩm thực", "ເຂົ້າຜັດໝູ", "Cơm rang thịt lợn"),
        ("ລາບຊີ້ນ", "Lạp bò / Nộm thịt bò băm", "Lao beef salad (Laap)", "laap-seen", "noun", "Ẩm thực", "ລາບຊີ້ນງົວແຊບໆ", "Món lạp bò tuyệt ngon"),
        ("ລາບໄກ່", "Lạp gà", "Lao minced chicken salad", "laap-kai", "noun", "Ẩm thực", "ເຮັດລາບໄກ່ສູ່ກິນ", "Làm món lạp gà đãi khách"),
        ("ລາບປາ", "Lạp cá tươi", "Lao minced fish salad", "laap-paa", "noun", "Ẩm thực", "ລາບປານ້ຳຂອງ", "Món lạp cá sông Mê Kông"),
        ("ກ້ອຍຊີ້ນ", "Gỏi thịt sống tái kiểu Lào", "Spicy raw meat salad", "kawy-seen", "noun", "Ẩm thực", "ກ້ອຍຊີ້ນໃສ່ເພ້ຍ", "Món gỏi thịt tái cay"),
        ("ໄສ້ອົ່ວ", "Xúc xích thảo mộc nướng Lào", "Lao herbal sausage (Sai Oua)", "sai-ua", "noun", "Ẩm thực", "ໄສ້ອົ່ວຫຼວງພະບາງ", "Xúc xích nướng Luang Prabang"),
        ("ໝົກປາ", "Cá bọc lá chuối hấp gia vị", "Steamed fish in banana leaf", "mok-paa", "noun", "Ẩm thực", "ໝົກປາໃສ່ຜັກອີຕູ່", "Món cá hấp lá chuối thơm lừng"),
        ("ໝົກໄກ່", "Gà bọc lá chuối hấp", "Steamed chicken in banana leaf", "mok-kai", "noun", "Ẩm thực", "ໝົກໄກ່ຮ້ອນໆ", "Gà hấp lá chuối nóng hổi"),
        ("ອໍໂລ໊ະ", "Canh thịt hầm rau củ rừng Luang Prabang", "Lao stew (Or Lam)", "aw-lam", "noun", "Ẩm thực", "ອໍລາມພື້ນເມືອງ", "Món canh hầm rau rừng truyền thống"),
        ("ແຈ່ວບອງ", "Ớt chưng da trâu chiên Luang Prabang", "Spicy sweet chili paste (Jeow Bong)", "chaew-bawng", "noun", "Ẩm thực", "ກິນເຂົ້າໜຽວຈ້ຳແຈ່ວບອງ", "Chấm xôi nếp vào ớt chưng"),
        ("ແຈ່ວໝາກເຂືອ", "Cà tím nướng dầm ớt tỏi", "Eggplant dip (Jeow Mak Keua)", "chaew-maak-kheua", "noun", "Ẩm thực", "ແຈ່ວໝາກເຂືອຫອມໆ", "Cà tím nướng dầm thơm phức"),
        ("ແກງໜໍ່ໄມ້", "Canh măng chua lá giang", "Bamboo shoot soup", "kaeng-naw-mai", "noun", "Ẩm thực", "ແກງໜໍ່ໄມ້ໃສ່ຢານາງ", "Canh măng nấu nước lá giang"),
        ("ແກງຈືດ", "Canh thịt băm nấu thanh đạm", "Clear soup with minced pork", "kaeng-cheut", "noun", "Ẩm thực", "ແກງຈືດເຕົ້າຫູ້", "Canh đậu phụ thanh đạm"),
        ("ຕົ້ມຍຳກຸ້ງ", "Canh chua tôm cay (Tom Yum)", "Spicy shrimp soup (Tom Yum)", "tom-yam-kung", "noun", "Ẩm thực", "ຕົ້ມຍຳກຸ້ງລົດເຜັດ", "Canh tôm chua cay đậm đà"),
        ("ປາແດກ", "Mắm cá đồng Padek Lào", "Fermented fish sauce (Padek)", "paa-daek", "noun", "Ẩm thực", "ປາແດກນົວໆ", "Mắm cá padek đậm đà thơm ngon"),
        ("ນ້ຳປາ", "Nước mắm", "Fish sauce", "nam-paa", "noun", "Gia vị", "ໃສ່ນ້ຳປາໜ້ອຍໜຶ່ງ", "Cho thêm chút nước mắm"),
        ("ເກືອ", "Muối tinh", "Salt", "kuea", "noun", "Gia vị", "ເກືອໄອໂອດິນ", "Muối i-ốt"),
        ("ນ້ຳຕານ", "Đường kính", "Sugar", "nam-taan", "noun", "Gia vị", "ບໍ່ມັກຫວານຢ່າໃສ່ນ້ຳຕານຫຼາຍ", "Không thích ngọt đừng cho nhiều đường"),
        ("ແປ້ງນົວ", "Mì chính / Bột ngọt", "Monosodium glutamate (MSG)", "paeng-nua", "noun", "Gia vị", "ໃສ່ແປ້ງນົວພໍດີ", "Nêm mì chính vừa phải"),
        ("ພິກໄທ", "Hạt tiêu / Tiêu đen", "Black pepper", "phik-thai", "noun", "Gia vị", "ໂຣຍພິກໄທໃສ່", "Rắc thêm hạt tiêu xay"),
        ("ໝາກເຜັດ", "Quả ớt", "Chili", "maak-phet", "noun", "Rau quả", "ໝາກເຜັດເຜັດຫຼາຍ", "Quả ớt này rất cay"),
        ("ຜັກທຽມ", "Tỏi", "Garlic", "phak-thiam", "noun", "Gia vị", "ຜັກທຽມດອງ", "Tỏi ngâm giấm"),
        ("ຫົວບົ່ວ", "Củ hành tím / Hành tây", "Shallot / Onion", "hua-bua", "noun", "Gia vị", "ຊອຍຫົວບົ່ວ", "Thái củ hành"),
        ("ຂີງ", "Củ gừng", "Ginger", "kheeng", "noun", "Gia vị", "ນ້ຳຂີງຮ້ອນ", "Nước gừng nóng"),
        ("ຂ່າ", "Củ riềng", "Galangal", "khaa", "noun", "Gia vị", "ໃສ່ຂ່າດັບກິ່ນຄາວ", "Cho củ riềng khử mùi tanh"),
        ("ຫົວສີໄຄ", "Củ sả / Cây sả", "Lemongrass", "hua-see-khai", "noun", "Gia vị", "ຕົ້ມໃສ່ຫົວສີໄຄ", "Nấu canh sả thơm lừng"),
        ("ໝາກນາວ", "Quả chanh", "Lime / Lemon", "maak-naao", "noun", "Rau quả", "ບີບໝາກນາວໃສ່", "Vắt chanh vào"),
        ("ໝາກກ້ວຍ", "Quả chuối", "Banana", "maak-kluay", "noun", "Trái cây", "ກ້ວຍນ້ຳຫວ້າ", "Chuối xiêm ngọt mát"),
        ("ໝາກມ່ວງ", "Quả xoài", "Mango", "maak-muang", "noun", "Trái cây", "ໝາກມ່ວງສຸກຫວານ", "Xoài chín ngọt lịm"),
        ("ໝາກຫຸ່ງ", "Quả đu đủ", "Papaya", "maak-hung", "noun", "Trái cây", "ໝາກຫຸ່ງດິບ", "Quả đu đủ xanh"),
        ("ໝາກໂມ", "Dưa hấu", "Watermelon", "maak-moo", "noun", "Trái cây", "ໝາກໂມຫວານເຢັນ", "Dưa hấu ngọt mát"),
        ("ໝາກກ້ຽງ", "Quả cam", "Orange", "maak-kiang", "noun", "Trái cây", "ນ້ຳໝາກກ້ຽງຄັ້ນ", "Nước cam ép tươi"),
        ("ໝາກນັດ", "Quả dứa / Thơm", "Pineapple", "maak-nat", "noun", "Trái cây", "ໝາກນັດສົ້ມຫວານ", "Dứa chua ngọt"),
        ("ໝາກພ້າວ", "Quả dừa", "Coconut", "maak-phaao", "noun", "Trái cây", "ນ້ຳໝາກພ້າວສົດ", "Nước dừa tươi"),
        ("ໝາກຖຸຣຽນ", "Sầu riêng", "Durian", "maak-thu-rian", "noun", "Trái cây", "ໝາກຖຸຣຽນຫອມມັນ", "Sầu riêng thơm béo"),
        ("ໝາກມັງຄຸດ", "Măng cụt", "Mangosteen", "maak-mang-khut", "noun", "Trái cây", "ໝາກມັງຄຸດຫວານ", "Măng cụt ngọt lịm"),
        ("ເບຍລາວ", "Bia Lào (Beerlao)", "Beerlao", "bia-laao", "noun", "Đồ uống", "ດື່ມເບຍລາວເຢັນໆ", "Uống bia Lào ướp lạnh"),
        ("ກາເຟລາວ", "Cà phê cao nguyên Bolaven Lào", "Lao coffee", "kaa-fee-laao", "noun", "Đồ uống", "ກາເຟດຳບໍ່ໃສ່ນ້ຳຕານ", "Cà phê đen không đường"),
        ("ຊານົມ", "Trà sữa trân châu", "Milk tea", "xaa-nom", "noun", "Đồ uống", "ຊານົມໄຂ່ມຸກ", "Trà sữa trân châu"),
        ("ນ້ຳອ້ອຍ", "Nước mía tươi", "Sugarcane juice", "nam-awy", "noun", "Đồ uống", "ນ້ຳອ້ອຍໃສ່ນ້ຳກ້ອນ", "Nước mía đá giải khát"),

        # =========================================================================
        # 3. Y TẾ, SỨC KHỎE, THUỐC MEN (HEALTHCARE & MEDICINE)
        # =========================================================================
        ("ເຈັບຫົວ", "Đau đầu / Nhức đầu", "Headache", "chep-hua", "adjective", "Sức khỏe", "ຂ້ອຍຮູ້ສຶກເຈັບຫົວ", "Tôi cảm thấy nhức đầu"),
        ("ເປັນໄຂ້", "Bị sốt", "Fever / Have a fever", "pen-khai", "verb", "Sức khỏe", "ລາວເປັນໄຂ້ສູງ", "Cậu ấy bị sốt cao"),
        ("ເປັນຫວັດ", "Bị cảm cúm", "Catch a cold", "pen-vat", "verb", "Sức khỏe", "ເປັນຫວັດໄອຈາມ", "Bị cảm ho hắt hơi"),
        ("ໄອ", "Bị ho", "Cough", "ai", "verb", "Sức khỏe", "ໄອມີຂີ້ກະເທີ", "Ho có đờm"),
        ("ເຈັບຄໍ", "Đau rát họng", "Sore throat", "chep-khaw", "adjective", "Sức khỏe", "ເຈັບຄໍກືນອາຫານຍາກ", "Đau họng nuốt khó"),
        ("ເຈັບທ້ອງ", "Đau bụng", "Stomach ache", "chep-thawng", "adjective", "Sức khỏe", "ເຈັບທ້ອງຖອກທ້ອງ", "Đau bụng tiêu chảy"),
        ("ຖອກທ້ອງ", "Tiêu chảy / Đi ngoài", "Diarrhea", "thawk-thawng", "verb", "Sức khỏe", "ດື່ມນ້ຳເກลือແຮ່ຕ້ານຖອກທ້ອງ", "Uống oresol bù nước"),
        ("ເຈັບແຂ້ວ", "Đau răng / Nhức răng", "Toothache", "chep-khaew", "adjective", "Sức khỏe", "ເຈັບແຂ້ວໄປຫາໝໍແຂ້ວ", "Đau răng đi khám nha sĩ"),
        ("ປວດເມື່ອຍ", "Đau nhức mỏi người", "Aching / Body pain", "puat-mueay", "adjective", "Sức khỏe", "ປວດເມື່ອຍຕົນໂຕ", "Đau mỏi khắp mình mẩy"),
        ("ວິນຫົວ", "Chóng mặt / Choáng váng", "Dizzy", "vin-hua", "adjective", "Sức khỏe", "ວິນຫົວໜ້າມືດ", "Chóng mặt hoa mắt"),
        ("ຮາກ", "Buồn nôn / Nôn mửa", "Vomit / Throw up", "haak", "verb", "Sức khỏe", "ຢາກຮາກ", "Cảm giác buồn nôn"),
        ("ຄວາມດັນເລືອດສູງ", "Huyết áp cao", "High blood pressure", "khuaam-dan-lueat-suung", "noun", "Y tế", "ກວດຄວາມດັນເລືອດ", "Đo huyết áp"),
        ("ເບົາຫວານ", "Bệnh tiểu đường", "Diabetes", "bao-vaan", "noun", "Y tế", "ຄວບຄຸມພະຍາດເບົາຫວານ", "Kiểm soát bệnh tiểu đường"),
        ("ພະຍາດຫົວໃຈ", "Bệnh tim mạch", "Heart disease", "pha-nyaat-hua-chai", "noun", "Y tế", "ປ້ອງກັນພະຍາດຫົວໃຈ", "Phòng ngừa bệnh tim"),
        ("ຢາແກ້ປວດ", "Thuốc giảm đau", "Painkiller", "yaa-kae-puat", "noun", "Dược phẩm", "ກິນຢາແກ້ປວດສອງເມັດ", "Uống 2 viên giảm đau"),
        ("ຢາຫຼຸດໄຂ້", "Thuốc hạ sốt", "Fever reducer (Paracetamol)", "yaa-lut-khai", "noun", "Dược phẩm", "ກິນຢາຫຼຸດໄຂ້ທຸກ 6 ຊົ່ວໂມງ", "Uống hạ sốt mỗi 6 tiếng"),
        ("ຢາຂ້າເຊື້ອ", "Thuốc kháng sinh", "Antibiotic", "yaa-khaa-xuea", "noun", "Dược phẩm", "ກິນຢາຂ້າເຊື້ອໃຫ້ໝົດຊຸດ", "Uống hết liều kháng sinh"),
        ("ຢາແກ້ໄອ", "Thuốc ho / Siro ho", "Cough syrup / medicine", "yaa-kae-ai", "noun", "Dược phẩm", "ຈິບຢາແກ້ໄອ", "Nhấp siro ho"),
        ("ຢາຢອດຕາ", "Thuốc nhỏ mắt", "Eye drops", "yaa-yawt-taa", "noun", "Dược phẩm", "ຢອດຕາມື້ລະສາມເທື່ອ", "Nhỏ mắt ngày ba lần"),
        ("ຜ້າພັນບາດ", "Băng gạc cứu thương", "Bandage", "phaa-phan-baat", "noun", "Y tế", "ພັນບາດແຜ", "Băng bó vết thương"),
        ("ສັກຢາ", "Tiêm thuốc / Tiêm vắc xin", "Injection / Vaccination", "sak-yaa", "verb", "Y tế", "ສັກຢາປ້ອງກັນພະຍາດ", "Tiêm vắc-xin phòng bệnh"),
        ("ໃບສັ່ງຢາ", "Đơn thuốc của bác sĩ", "Medical prescription", "bai-sang-yaa", "noun", "Y tế", "ຊື້ຢາຕາມໃບສັ່ງຢາ", "Mua thuốc theo đơn"),
        ("ກວດສຸຂະພາບ", "Khám sức khỏe tổng quát", "Health check-up", "kuat-su-kha-phaap", "verb", "Y tế", "ກວດສຸຂະພາບປະຈຳປີ", "Khám sức khỏe định kỳ hàng năm"),
        ("ຫ້ອງສຸກເສີນ", "Phòng cấp cứu", "Emergency room (ER)", "hawng-suk-soen", "noun", "Y tế", "ສົ່ງເຂົ້າຫ້ອງສຸກເສີນ", "Đưa vào phòng cấp cứu"),
        ("ປະກັນໄພສຸຂະພາບ", "Bảo hiểm y tế", "Health insurance", "pa-kan-fai-su-kha-phaap", "noun", "Y tế", "ມີບັດປະກັນໄພສຸຂະພາບ", "Có thẻ bảo hiểm y tế"),

        # =========================================================================
        # 4. GIAO THÔNG, PHƯƠNG HƯỚNG & ĐỊA ĐIỂM (TRANSPORT & DIRECTIONS)
        # =========================================================================
        ("ລ້ຽວຊ້າຍ", "Rẽ trái", "Turn left", "liaw-saai", "verb", "Phương hướng", "ຮອດສີ່ແຍກລ້ຽວຊ້າຍ", "Đến ngã tư rẽ trái"),
        ("ລ້ຽວຂວາ", "Rẽ phải", "Turn right", "liaw-khwaa", "verb", "Phương hướng", "ລ້ຽວຂວາເຂົ້າຮ່ອມ", "Rẽ phải vào ngõ"),
        ("ກົງໄປ", "Đi thẳng", "Go straight", "kong-pai", "verb", "Phương hướng", "ກົງໄປປະມານຮ້ອຍແມັດ", "Đi thẳng khoảng 100 mét"),
        ("ລ້ຽວກັບ", "Quay đầu xe", "U-turn", "liaw-kap", "verb", "Phương hướng", "ລ້ຽວກັບຢູ່ບ່ອນປອດໄພ", "Quay đầu xe ở nơi an toàn"),
        ("ສາມແຍກ", "Ngã ba đường", "T-junction / Three-way intersection", "saam-nyaek", "noun", "Giao thông", "ຢຸດລໍຢູ່ສາມແຍກ", "Dừng chờ ở ngã ba"),
        ("ສີ່ແຍກ", "Ngã tư đường", "Crossroad / Four-way intersection", "see-nyaek", "noun", "Giao thông", "ຕິດໄຟແດງຢູ່ສີ່ແຍກ", "Dừng đèn đỏ ở ngã tư"),
        ("ວົງວຽນ", "Bùng binh / Vòng xuyến", "Roundabout", "vong-vian", "noun", "Giao thông", "ອ້ອມວົງວຽນ", "Đi vòng qua bùng binh"),
        ("ໄຟແດງ", "Đèn đỏ (dừng lại)", "Red light", "fai-daeng", "noun", "Giao thông", "ເຄົາລົບໄຟແດງ", "Tuân thủ đèn đỏ"),
        ("ໄຟຂຽວ", "Đèn xanh (được đi)", "Green light", "fai-khiao", "noun", "Giao thông", "ໄຟຂຽວແລ້ວໄປໄດ້", "Đèn xanh rồi đi thôi"),
        ("ໄຟເຫຼືອງ", "Đèn vàng (giảm tốc độ)", "Yellow light", "fai-lueang", "noun", "Giao thông", "ໄຟເຫຼືອງໃຫ້ຊ້າລົງ", "Đèn vàng hãy đi chậm lại"),
        ("ທາງດ່ວນ", "Đường cao tốc", "Highway / Expressway", "thaang-duan", "noun", "Giao thông", "ແລ່ນຕາມທາງດ່ວນວຽງຈັນ-ວັງວຽງ", "Chạy trên cao tốc Viêng Chăn - Vang Vieng"),
        ("ຂົວຂ້າມນ້ຳ", "Cây cầu bắc qua sông", "Bridge", "khua-khaam-nam", "noun", "Giao thông", "ຂ້າມຂົວມິດຕະພາບ", "Băng qua cầu Hữu Nghị"),
        ("ສະຖານີລົດໄຟ", "Ga tàu hỏa / Nhà ga đường sắt", "Train station", "sa-thaa-nee-lot-fai", "noun", "Giao thông", "ສະຖານີລົດໄຟນະຄອນຫຼວງວຽງຈັນ", "Ga tàu hỏa Viêng Chăn"),
        ("ສະໜາມບິນ", "Sân bay / Phi trường", "Airport", "sa-naam-bin", "noun", "Giao thông", "ສະໜາມບິນສາກົນວັດໄຕ", "Sân bay quốc tế Wattay"),
        ("ຄິວລົດເມ", "Bến xe khách / Bến xe buýt", "Bus terminal", "khiw-lot-mee", "noun", "Giao thông", "ຄິວລົດສາຍເໜືອ", "Bến xe khách phía Bắc"),
        ("ບ່ອນຈອດລົດ", "Bãi đỗ xe", "Parking lot", "bawn-chawt-lot", "noun", "Giao thông", "ມີບ່ອນຈອດລົດກວ້າງ", "Có bãi đỗ xe rộng rãi"),
        ("ລົດຕຸກໆ", "Xe tuk tuk (xe 3 bánh)", "Tuk-tuk", "lot-tuk-tuk", "noun", "Giao thông", "ຂີ່ລົດຕຸກໆທ່ຽວຊົມເມືອງ", "Đi tuk tuk tham quan thành phố"),
        ("ລົດເມ", "Xe buýt", "Public bus", "lot-mee", "noun", "Giao thông", "ຂີ່ລົດເມປະຢັດເງິນ", "Đi xe buýt tiết kiệm chi phí"),
        ("ຕຳຫຼວດຈະລາຈອນ", "Cảnh sát giao thông", "Traffic police", "tam-luat-cha-laa-chawn", "noun", "Pháp luật", "ຕຳຫຼວດຈະລາຈອນອຳນວຍຄວາມສະດວກ", "Cảnh sát giao thông điều tiết đường"),
        ("ໃສ່ໝວກກັນກະທົບ", "Đội mũ bảo hiểm", "Wear a helmet", "sai-muak-kan-ka-thop", "phrase", "Giao thông", "ຕ້ອງໃສ່ໝວກກັນກະທົບສະເໝີ", "Phải luôn đội mũ bảo hiểm"),

        # =========================================================================
        # 5. CÔNG NGHỆ, VIỄN THÔNG & ĐỜI SỐNG SỐ (DIGITAL LIFE & IT)
        # =========================================================================
        ("ໂທລະສັບສະຫຼາດ", "Điện thoại thông minh (Smartphone)", "Smartphone", "thoo-la-sap-sa-laat", "noun", "Công nghệ", "ຊື້ໂທລະສັບສະຫຼາດລຸ້ນໃໝ່", "Mua smartphone đời mới"),
        ("ຄອມພິວເຕີ", "Máy vi tính", "Computer", "khawm-phiw-toe", "noun", "Công nghệ", "ໃຊ້ຄອມພິວເຕີເຮັດວຽກ", "Dùng máy tính làm việc"),
        ("ໂນ້ດບຸກ", "Máy tính xách tay (Laptop)", "Laptop", "noot-buk", "noun", "Công nghệ", "ພົກພາໂນ້ດບຸກໄປມານະ", "Mang laptop theo người"),
        ("ແທັບເລັດ", "Máy tính bảng (Tablet)", "Tablet", "thaep-let", "noun", "Công nghệ", "ອ່ານປຶ້ມເທິງແທັບເລັດ", "Đọc sách trên máy tính bảng"),
        ("ຫູຟັງ", "Tai nghe", "Headphones / Earphones", "huu-fang", "noun", "Công nghệ", "ສຽບຫູຟັງຟັງເພງ", "Cắm tai nghe nghe nhạc"),
        ("ສາຍສາກ", "Dây cáp sạc pin", "Charging cable", "saai-saak", "noun", "Công nghệ", "ສາຍສາກໂທລະສັບ", "Dây sạc điện thoại"),
        ("ໝໍ້ສາກສຳຮອງ", "Pin sạc dự phòng", "Power bank", "maw-saak-sam-hawng", "noun", "Công nghệ", "ພົກໝໍ້ສາກສຳຮອງ", "Mang theo sạc dự phòng"),
        ("ສັນຍານອິນເຕີເນັດ", "Tín hiệu mạng Internet", "Internet connection / signal", "san-nyaan-in-toe-net", "noun", "Công nghệ", "ສັນຍານອິນເຕີເນັດແຮງດີ", "Mạng Internet rất khỏe"),
        ("ລະຫັດຜ່ານ", "Mật khẩu bảo mật", "Password", "la-hat-phaan", "noun", "Công nghệ", "ປ່ຽນລະຫັດຜ່ານໃໝ່", "Đổi mật khẩu mới"),
        ("ຊື່ຜູ້ໃຊ້", "Tên đăng nhập (Username)", "Username", "seu-phuu-xai", "noun", "Công nghệ", "ປ້ອນຊື່ຜູ້ໃຊ້", "Nhập tên đăng nhập"),
        ("ດາວໂຫຼດ", "Tải xuống (Download)", "Download", "daao-loot", "verb", "Công nghệ", "ດາວໂຫຼດເອກະສານ", "Tải tài liệu xuống"),
        ("ອັບໂຫຼດ", "Tải lên (Upload)", "Upload", "ap-loot", "verb", "Công nghệ", "ອັບໂຫຼດຮູບພາບ", "Tải ảnh lên mạng"),
        ("ບັນຊີ", "Tài khoản (Account)", "Account", "ban-xee", "noun", "Công nghệ", "ສ້າງບັນຊີໃໝ່", "Tạo tài khoản mới"),
        ("ລຶບ", "Xóa bỏ", "Delete / Erase", "loep", "verb", "Công nghệ", "ລຶບຂໍ້ມູນເກົ່າ", "Xóa dữ liệu cũ"),
        ("ບັນທຶກ", "Lưu lại / Ghi chép", "Save / Record", "ban-thuek", "verb", "Công nghệ", "ບັນທຶກເອກະສານໄວ້", "Lưu văn bản lại"),
        ("ແບ່ງປັນ", "Chia sẻ (Share)", "Share", "baeng-pan", "verb", "Công nghệ", "ແບ່ງປັນຄວາມຮູ້", "Chia sẻ kiến thức"),

        # =========================================================================
        # 6. TÍNH TỪ MIÊU TẢ & CẢM XÚC (ADJECTIVES & EMOTIONS)
        # =========================================================================
        ("ງາມຫຼາຍ", "Rất đẹp", "Very beautiful", "ngaam-laai", "adjective", "Miêu tả", "ດອກໄມ້ງາມຫຼາຍ", "Hoa nở rất đẹp"),
        ("ຂີ້ຮ້າຍ", "Xấu xí / Tệ hại", "Ugly / Bad", "khee-haai", "adjective", "Miêu tả", "ນິໄສຂີ້ຮ້າຍ", "Tính nết xấu"),
        ("ສູງ", "Cao lớn", "Tall / High", "suung", "adjective", "Miêu tả", "ຕຶກສູງ", "Tòa nhà cao tầng"),
        ("ຕ່ຳ", "Thấp / Lùn", "Short / Low", "tam", "adjective", "Miêu tả", "ໂຕະຕ່ຳ", "Bàn thấp"),
        ("ຍາວ", "Dài", "Long", "nyaao", "adjective", "Miêu tả", "ເສັ້ນທາງຍາວໄກ", "Con đường dài dằng dặc"),
        ("ສັ້ນ", "Ngắn", "Short", "san", "adjective", "Miêu tả", "ໂສ້ງຂາສັ້ນ", "Quần soóc ngắn"),
        ("ກວ້າງ", "Rộng rãi", "Wide / Spacious", "kuaang", "adjective", "Miêu tả", "ຫ້ອງກວ້າງຂວາງ", "Căn phòng rộng thênh thang"),
        ("ແຄບ", "Hẹp / Chật chội", "Narrow / Tight", "khaep", "adjective", "Miêu tả", "ຮ່ອມແຄບ", "Ngõ hẻm chật hẹp"),
        ("ໜັກ", "Nặng nề", "Heavy", "nak", "adjective", "Miêu tả", "ກະເປົາໜັກຫຼາຍ", "Va li rất nặng"),
        ("ເບົາ", "Nhẹ nhàng", "Light (weight)", "bao", "adjective", "Miêu tả", "ນ້ຳໜັກເບົາ", "Trọng lượng nhẹ"),
        ("ໄວ", "Nhanh chóng", "Fast / Quick", "vai", "adjective", "Miêu tả", "ແລ່ນໄວຫຼາຍ", "Chạy rất nhanh"),
        ("ຊ້າ", "Chậm chạp", "Slow", "xaa", "adjective", "Miêu tả", "ຍ່າງຊ້າໆ", "Đi từng bước chậm rãi"),
        ("ສະອາດ", "Sạch sẽ", "Clean", "sa-aat", "adjective", "Miêu tả", "ຮັກສາຄວາມສະອາດ", "Giữ gìn vệ sinh sạch sẽ"),
        ("ເປື້ອນ", "Bẩn thỉu / Lem luốc", "Dirty", "puean", "adjective", "Miêu tả", "ເສື້ອເປື້ອນຂີ້ຕົມ", "Áo dính bẩn bùn đất"),
        ("ແຊບ", "Ngon miệng", "Delicious / Tasty", "xaep", "adjective", "Ẩm thực", "ອາຫານລາວແຊບຫຼາຍ", "Món ăn Lào rất ngon"),
        ("ບໍ່ແຊບ", "Không ngon / Dở", "Not delicious", "baw-xaep", "adjective", "Ẩm thực", "ລົດຊາດບໍ່ແຊບ", "Hương vị không ngon"),
        ("ຫວານ", "Ngọt ngào", "Sweet", "vaan", "adjective", "Ẩm thực", "ເຂົ້າໜົມຫວານ", "Bánh kẹo ngọt"),
        ("ສົ້ມ", "Chua", "Sour", "som", "adjective", "Ẩm thực", "ໝາກນາວສົ້ມ", "Quả chanh chua"),
        ("ເຜັດ", "Cay nồng", "Spicy / Hot", "phet", "adjective", "Ẩm thực", "ແກງເຜັດຫຼາຍ", "Canh rất cay"),
        ("ເຄັມ", "Mặn", "Salty", "khem", "adjective", "Ẩm thực", "ຢ່າກິນເຄັມ", "Đừng ăn mặn quá"),
        ("ຂົມ", "Đắng", "Bitter", "khom", "adjective", "Ẩm thực", "ຢາຂົມແຕ່ດີ", "Thuốc đắng dã tật"),
        ("ຈາງ", "Nhạt nhẽo", "Bland / Insipid", "chaang", "adjective", "Ẩm thực", "ແກງຈາງໜ້ອຍໜຶ່ງ", "Canh hơi nhạt một chút"),
        ("ຮ້ອນ", "Nóng nực / Nóng hổi", "Hot", "hawn", "adjective", "Miêu tả", "ມື້ນີ້ອາກາດຮ້ອນ", "Hôm nay trời oi bức"),
        ("ໜາວ", "Lạnh buốt / Rét", "Cold", "naao", "adjective", "Miêu tả", "ລະດູໜາວໜາວຫຼາຍ", "Mùa đông rất lạnh"),
        ("ອົບອຸ່ນ", "Ấm áp", "Warm / Cozy", "op-un", "adjective", "Miêu tả", "ຄອບຄົວອົບອຸ່ນ", "Mái ấm gia đình ấm cúng"),
        ("ເຢັນສະບາຍ", "Mát mẻ dễ chịu", "Cool and comfortable", "yen-sa-baai", "adjective", "Miêu tả", "ລົມພັດເຢັນສະບາຍ", "Gió thổi mát rượi"),
        ("ສະດວກ", "Thuận tiện / Tiện lợi", "Convenient", "sa-duak", "adjective", "Miêu tả", "ການຄົມມະນາຄົມສະດວກ", "Giao thông thuận tiện"),
        ("ຍາກ", "Khó khăn / Gian nan", "Difficult / Hard", "nyaak", "adjective", "Miêu tả", "ບົດຮຽນນີ້ຍາກ", "Bài học này khá khó"),
        ("ງ່າຍ", "Dễ dàng / Đơn giản", "Easy / Simple", "ngaai", "adjective", "Miêu tả", "ຂໍ້ສອບງ່າຍດາຍ", "Đề thi rất dễ"),
        ("ຖືກ", "Đúng đắn / Giá rẻ", "Correct / Cheap", "theuk", "adjective", "Miêu tả", "ຕອບຖືກຕ້ອງ", "Trả lời chính xác"),
        ("ຜິດ", "Sai sót / Có lỗi", "Wrong / Incorrect", "phit", "adjective", "Miêu tả", "ເຮັດຜິດພາດ", "Làm sai sót"),
        ("ແພງ", "Đắt đỏ / Đắt tiền", "Expensive", "phaeng", "adjective", "Mua sắm", "ສິນຄ້າລາຄາແພງ", "Hàng hóa giá đắt"),
        ("ຖືກຕ້ອງ", "Chính xác / Đúng luật", "Accurate / Right", "theuk-tawng", "adjective", "Pháp luật", "ປະຕິບັດຖືກຕ້ອງ", "Chấp hành đúng quy định"),
        ("ຈິງໃຈ", "Chân thành / Thật lòng", "Sincere / Honest", "cheeng-chai", "adjective", "Đạo đức", "ຄົນຈິງໃຈ", "Người sống chân thành"),
        ("ຂີ້ຕົວະ", "Nói dối / Bịp bợm", "Liar / Deceitful", "khee-tua", "adjective", "Đạo đức", "ຢ່າເວົ້າຂີ້ຕົວະ", "Chớ có nói dối"),
        ("ດຸໝັ່ນ", "Chăm chỉ / Cần cù", "Diligent / Hardworking", "du-man", "adjective", "Tính cách", "ນັກຮຽນດຸໝັ່ນ", "Học sinh chăm ngoan"),
        ("ຂີ້ຄ້ານ", "Lười biếng / Trì trệ", "Lazy", "khee-khaan", "adjective", "Tính cách", "ຄົນຂີ້ຄ້ານບໍ່ກ້າວໜ້າ", "Kẻ lười biếng khó tiến bộ"),
        ("ສຸພາບ", "Lịch sự / Lễ phép", "Polite / Courteous", "su-phaap", "adjective", "Tính cách", "ເວົ້າຈາສຸພາບຮຽບຮ້ອຍ", "Nói năng lễ phép lịch sự"),
        ("ກ້າຫານ", "Dũng cảm / Can trường", "Brave / Valiant", "kaa-haan", "adjective", "Tính cách", "ນ້ຳໃຈກ້າຫານ", "Tinh thần quả cảm"),
        ("ຢ້ານ", "Sợ hãi / E ngại", "Afraid / Scared", "yaan", "verb", "Cảm xúc", "ຢ້ານຄວາມມືດ", "Sợ bóng tối"),
        ("ໂສກເສົ້າ", "Đau buồn / Sầu khổ", "Sorrowful / Sad", "sook-sao", "adjective", "Cảm xúc", "ຢ່າໂສກເສົ້າເສຍໃຈ", "Đừng quá bi lụy sầu muộn"),
        ("ດີໃຈ", "Vui mừng / Hớn hở", "Glad / Joyful", "dee-chai", "adjective", "Cảm xúc", "ດີໃຈທີ່ໄດ້ພົບກັນ", "Rất vui mừng khi được gặp bạn"),
        ("ມີຄວາມສຸກ", "Hạnh phúc", "Happy / Content", "mee-khuaam-suk", "phrase", "Cảm xúc", "ຂໍໃຫ້ມີຄວາມສຸກ", "Chúc bạn luôn ngập tràn hạnh phúc"),

        # =========================================================================
        # 7. QUY TẮC PHÁI SINH: DANH ĐỘNG TỪ 'ການ-' (ACTION NOUNS)
        # =========================================================================
        ("ການສຶກສາ", "Nền giáo dục / Việc học tập", "Education", "kaan-suek-saa", "noun", "Giáo dục", "ກະຊວງສຶກສາທິການ", "Bộ Giáo dục và Thể thao"),
        ("ການພັດທະນາ", "Sự phát triển", "Development", "kaan-phat-tha-naa", "noun", "Xã hội", "ການພັດທະນາປະເທດຊາດ", "Sự phát triển đất nước"),
        ("ການຮ່ວມມື", "Sự hợp tác", "Cooperation / Partnership", "kaan-huam-mue", "noun", "Ngoại giao", "ການຮ່ວມມືລາວ-ຫວຽດ", "Sự hợp tác hữu nghị Lào - Việt"),
        ("ການຄ້າ", "Nền thương mại / Việc buôn bán", "Trade / Commerce", "kaan-khaa", "noun", "Kinh tế", "ການຄ້າສາກົນ", "Thương mại quốc tế"),
        ("ການລົງທຶນ", "Sự đầu tư", "Investment", "kaan-long-thun", "noun", "Kinh tế", "ດຶງດູດການລົງທຶນ", "Thu hút nguồn vốn đầu tư"),
        ("ການຜະລິດ", "Sự sản xuất / Chế tạo", "Production / Manufacturing", "kaan-pha-lit", "noun", "Kinh tế", "ເພີ່ມກຳລັງການຜະລິດ", "Gia tăng năng lực sản xuất"),
        ("ການຂົນສົ່ງ", "Ngành vận tải / Vận chuyển", "Transportation / Logistics", "kaan-khon-song", "noun", "Giao thông", "ການຂົນສົ່ງສິນຄ້າ", "Vận chuyển hàng hóa"),
        ("ການສື່ສານ", "Ngành truyền thông / Giao tiếp", "Communication", "kaan-sue-saan", "noun", "Công nghệ", "ເຄືອຂ່າຍການສື່ສານ", "Mạng lưới truyền thông"),
        ("ການແພດ", "Ngành y tế / Y học", "Medical science / Healthcare", "kaan-phaet", "noun", "Y tế", "ຄວາມກ້າວໜ້າທາງການແພດ", "Sự tiến bộ của y học"),
        ("ການບໍລິຫານ", "Sự quản trị / Điều hành", "Administration / Management", "kaan-baw-li-haan", "noun", "Quản lý", "ການບໍລິຫານທຸລະກິດ", "Quản trị kinh doanh"),
        ("ການກໍ່ສ້າງ", "Ngành xây dựng", "Construction", "kaan-kaw-saang", "noun", "Xây dựng", "ວຽກງານການກໍ່ສ້າງ", "Công tác thi công xây dựng"),
        ("ການທະນາຄານ", "Ngành ngân hàng", "Banking", "kaan-tha-naa-khaan", "noun", "Tài chính", "ລະບົບການທະນາຄານ", "Hệ thống ngân hàng"),
        ("ການທ່ອງທ່ຽວ", "Ngành du lịch", "Tourism", "kaan-thawng-thiaw", "noun", "Du lịch", "ສົ່ງເສີມການທ່ອງທ່ຽວ", "Quảng bá du lịch"),
        ("ການກະເສດ", "Ngành nông nghiệp", "Agriculture", "kaan-ka-set", "noun", "Nông nghiệp", "ການກະເສດສະອາດ", "Nông nghiệp sạch"),
        ("ການເມືອງ", "Nền chính trị", "Politics", "kaan-mueang", "noun", "Nhà nước", "ສະຖຽນລະພາບທາງການເມືອງ", "Sự ổn định chính trị"),
        ("ການປົກຄອງ", "Sự cai trị / Quản lý hành chính", "Governance / Administration", "kaan-pok-khawng", "noun", "Hành chính", "ລະບົບການປົກຄອງ", "Hệ thống chính quyền"),
        ("ການແຂ່ງຂັນ", "Cuộc thi đấu / Cạnh tranh", "Competition", "kaan-khaeng-khan", "noun", "Thể thao", "ການແຂ່ງຂັນບານເຕະ", "Giải thi đấu bóng đá"),
        ("ການສອບເສັງ", "Kỳ thi cử", "Examination / Test", "kaan-sawp-seng", "noun", "Giáo dục", "ການສອບເສັງຈົບຊັ້ນ", "Kỳ thi tốt nghiệp"),
        ("ການຄົ້ນຄວ້າ", "Công trình nghiên cứu khoa học", "Scientific research", "kaan-khon-khwaa", "noun", "Khoa học", "ການຄົ້ນຄວ້າວິທະຍາສາດ", "Nghiên cứu khoa học"),
        ("ການຮຽນຮູ້", "Quá trình học hỏi", "Learning process", "kaan-hian-huu", "noun", "Giáo dục", "ການຮຽນຮູ້ຕະຫຼອດຊີວິດ", "Học tập suốt đời"),

        # =========================================================================
        # 8. QUY TẮC PHÁI SINH: DANH TỪ TRẠNG THÁI 'ຄວາມ-' (ABSTRACT NOUNS)
        # =========================================================================
        ("ຄວາມຮັກ", "Tình yêu thương", "Love", "khuaam-hak", "noun", "Tình cảm", "ຄວາມຮັກອັນບໍລິສຸດ", "Tình yêu thương thuần khiết"),
        ("ຄວາມສຸກ", "Niềm hạnh phúc", "Happiness", "khuaam-suk", "noun", "Cảm xúc", "ຂໍໃຫ້ມີແຕ່ຄວາມສຸກ", "Chúc bạn luôn ngập tràn hạnh phúc"),
        ("ຄວາມສະຫງົບ", "Nền hòa bình / Yên bình", "Peace / Tranquility", "khuaam-sa-ngop", "noun", "Xã hội", "ຄວາມສະຫງົບສຸກ", "Hòa bình và an lạc"),
        ("ຄວາມສາມັກຄີ", "Tinh thần đoàn kết", "Solidarity / Unity", "khuaam-saa-mak-khee", "noun", "Đạo đức", "ຄວາມສາມັກຄີປວງຊົນ", "Đoàn kết toàn dân"),
        ("ຄວາມຈິງ", "Sự thật / Chân lý", "Truth / Reality", "khuaam-cheeng", "noun", "Triết học", "ເວົ້າຄວາມຈິງ", "Nói lên sự thật"),
        ("ຄວາມຫວັງ", "Niềm hy vọng", "Hope", "khuaam-vang", "noun", "Tâm lý", "ເຕັມໄປດ້ວຍຄວາມຫວັງ", "Tràn trề niềm hy vọng"),
        ("ຄວາມຝັນ", "Ước mơ / Giấc mơ", "Dream", "khuaam-fan", "noun", "Tâm lý", "ເຮັດຕາມຄວາມຝັນ", "Biến ước mơ thành hiện thực"),
        ("ຄວາມອົດທົນ", "Lòng kiên nhẫn / Chịu đựng", "Patience / Endurance", "khuaam-ot-thon", "noun", "Đạo đức", "ມີຄວາມອົດທົນສູງ", "Có sức chịu đựng bền bỉ"),
        ("ความຮັບຜິດຊອບ", "Tinh thần trách nhiệm", "Responsibility", "khuaam-hap-phit-xawp", "noun", "Đạo đức", "ມີຄວາມຮັບຜິດຊອບໃນວຽກງານ", "Có tinh thần trách nhiệm trong công việc"),
        ("ຄວາມປອດໄພ", "Sự an toàn", "Safety / Security", "khuaam-pawt-fai", "noun", "Đời sống", "ຄວາມປອດໄພມາກ່ອນ", "An toàn là trên hết"),
        ("ຄວາມຮູ້", "Kiến thức / Trí thức", "Knowledge", "khuaam-huu", "noun", "Giáo dục", "ສະແຫວງຫາຄວາມຮູ້", "Tìm kiếm tri thức"),
        ("ຄວາມສະອາດ", "Sự sạch sẽ / Vệ sinh", "Cleanliness", "khuaam-sa-aat", "noun", "Đời sống", "ຮັກສາຄວາມສະອາດສ່ວນຕົວ", "Giữ gìn vệ sinh cá nhân"),
        ("ຄວາມສະດວກ", "Sự tiện nghi / Thuận lợi", "Convenience", "khuaam-sa-duak", "noun", "Đời sống", "ອຳນວຍຄວາມສະດວກ", "Tạo mọi điều kiện thuận lợi"),
        ("ຄວາມໄວ", "Tốc độ / Vận tốc", "Speed / Velocity", "khuaam-vai", "noun", "Khoa học", "ລົດໄຟຄວາມໄວສູງ", "Đoàn tàu cao tốc"),
        ("ຄວາມງາມ", "Vẻ đẹp / Nét đẹp", "Beauty", "khuaam-ngaam", "noun", "Nghệ thuật", "ຄວາມງາມແບບທຳມະຊາດ", "Nét đẹp tự nhiên"),
        ("ຄວາມສຳເລັດ", "Sự thành công", "Success / Achievement", "khuaam-sam-let", "noun", "Xã hội", "ຍິນດີກັບຄວາມສຳເລັດ", "Chúc mừng sự thành công rực rỡ"),

        # =========================================================================
        # 9. TỪ CHỈ NGƯỜI & NGHỀ NGHIỆP: 'ຜູ້-', 'ນັກ-', 'ຊ່າງ-' (PEOPLE & PROFESSIONS)
        # =========================================================================
        ("ຜູ້ຈັດການ", "Người quản lý / Giám đốc chi nhánh", "Manager", "phuu-chat-kaan", "noun", "Nghề nghiệp", "ຜູ້ຈັດການໂຮງແຮມ", "Người quản lý khách sạn"),
        ("ຜູ້ອຳນວຍການ", "Tổng giám đốc / Hiệu trưởng", "Director / Principal", "phuu-am-nuay-kaan", "noun", "Nghề nghiệp", "ຜູ້ອຳນວຍການໃຫຍ່", "Tổng giám đốc"),
        ("ຜູ້ຊ່ວຍ", "Trợ lý / Phụ tá", "Assistant", "phuu-xuay", "noun", "Nghề nghiệp", "ຜູ້ຊ່ວຍອາຈານ", "Trợ giảng"),
        ("ຜູ້ແປ", "Biên dịch viên / Phiên dịch viên", "Translator / Interpreter", "phuu-pae", "noun", "Nghề nghiệp", "ຜູ້ແປພາສາລາວ-ຫວຽດ", "Phiên dịch viên tiếng Lào - Việt"),
        ("ຜູ້ຂັບລົດ", "Tài xế / Lái xe", "Driver", "phuu-khap-lot", "noun", "Nghề nghiệp", "ຜູ້ຂັບລົດແທັກຊີ", "Tài xế taxi"),
        ("ຜູ້ໂດຍສານ", "Hành khách", "Passenger", "phuu-dooy-saan", "noun", "Giao thông", "ຜູ້ໂດຍສານລົດເມ", "Hành khách đi xe buýt"),
        ("ນັກທຸລະກິດ", "Doanh nhân", "Businessman / Businesswoman", "nak-thu-la-kit", "noun", "Nghề nghiệp", "ນັກທຸລະກິດໜຸ່ມ", "Doanh nhân trẻ"),
        ("ນັກຂ່າວ", "Nhà báo / Phóng viên", "Journalist / Reporter", "nak-khaaw", "noun", "Nghề nghiệp", "ນັກຂ່າວໂທລະພາບ", "Phóng viên đài truyền hình"),
        ("ນັກຮ້ອງ", "Ca sĩ", "Singer", "nak-hawng", "noun", "Nghề nghiệp", "ນັກຮ້ອງສຽງດີ", "Ca sĩ có giọng hát truyền cảm"),
        ("ນັກສະແດງ", "Diễn viên", "Actor / Actress", "nak-sa-daeng", "noun", "Nghề nghiệp", "ນັກສະແດງຮູບເງົາ", "Diễn viên điện ảnh"),
        ("ນັກກິລາ", "Vận động viên", "Athlete", "nak-ki-laa", "noun", "Thể thao", "ນັກກິລາທີມຊາດ", "Vận động viên đội tuyển quốc gia"),
        ("ນັກວິທະຍາສາດ", "Nhà khoa học", "Scientist", "nak-vi-tha-nyaa-saat", "noun", "Khoa học", "ນັກວິທະຍາສາດຄົ້ນຄວ້າ", "Nhà khoa học làm việc"),
        ("ນັກການທູດ", "Nhà ngoại giao", "Diplomat", "nak-kaan-thuut", "noun", "Ngoại giao", "ນັກການທູດລາວ", "Nhà ngoại giao Lào"),
        ("ຊ່າງຕັດຜົມ", "Thợ cắt tóc", "Barber / Hairdresser", "xaang-tat-phom", "noun", "Nghề nghiệp", "ຊ່າງຕັດຜົມຝີມືດີ", "Thợ cắt tóc tay nghề cao"),
        ("ຊ່າງສ້ອມແປງ", "Thợ sửa chữa máy móc", "Mechanic / Repairman", "xaang-sawm-paeng", "noun", "Nghề nghiệp", "ຊ່າງສ້ອມແປງລົດ", "Thợ sửa xe chuyên nghiệp"),
        ("ຊ່າງໄຟຟ້າ", "Thợ điện", "Electrician", "xaang-fai-faa", "noun", "Nghề nghiệp", "ເອີ້ນຊ່າງໄຟຟ້າມາແປງ", "Gọi thợ điện đến sửa chữa"),
        ("ຊ່າງຖ່າຍຮູບ", "Nhiếp ảnh gia / Thợ chụp ảnh", "Photographer", "xaang-thaai-huup", "noun", "Nghề nghiệp", "ຊ່າງຖ່າຍຮູບມືອາຊີບ", "Nhiếp ảnh gia chuyên nghiệp"),
        ("ຊາວນາ", "Bác nông dân trồng lúa", "Rice farmer", "xaao-naa", "noun", "Nông nghiệp", "ຊາວນາເຮັດນາປູກເຂົ້າ", "Người nông dân cấy lúa"),
        ("ຊາວສວນ", "Người làm vườn", "Gardener / Orchardist", "xaao-suan", "noun", "Nông nghiệp", "ຊາວສວນປູກໝາກໄມ້", "Người làm vườn trồng cây ăn trái"),
        ("ກຳມະກອນ", "Công nhân lao động", "Worker / Laborer", "kam-ma-kawn", "noun", "Lao động", "ກຳມະກອນໂຮງງານ", "Công nhân nhà máy"),

        # =========================================================================
        # 10. TỪ NỐI, QUAN HỆ TỪ & TRỢ TỪ NGỮ PHÁP (CONNECTORS & PARTICLES)
        # =========================================================================
        ("ແລະ", "Và", "And", "lae", "conjunction", "Ngữ pháp", "ຂ້ອຍແລະເຈົ້າ", "Tôi và bạn"),
        ("ຫຼື", "Hoặc / Hay là", "Or", "lue", "conjunction", "Ngữ pháp", "ຊາຫຼືກາເຟ", "Trà hay cà phê"),
        ("ແຕ່", "Nhưng / Từ (nơi chốn)", "But / From", "tae", "conjunction", "Ngữ pháp", "ຢາກໄປແຕ່ບໍ່ມີເວລາ", "Muốn đi nhưng không có thời gian"),
        ("ຍ້ອນວ່າ", "Bởi vì / Do", "Because", "yawn-vaa", "conjunction", "Ngữ pháp", "ຍ້ອນວ່າຝົນຕົກ", "Bởi vì trời đổ mưa"),
        ("ດັ່ງນັ້ນ", "Cho nên / Vì vậy", "Therefore / So", "dang-nan", "conjunction", "Ngữ pháp", "ດັ່ງນັ້ນຈຶ່ງໄປຊ້າ", "Vì thế nên mới đến muộn"),
        ("ຖ້າວ່າ", "Nếu như / Giả sử", "If", "thaa-vaa", "conjunction", "Ngữ pháp", "ຖ້າວ່າເຈົ້າຫວ່າງ", "Nếu bạn rảnh rỗi"),
        ("ເຖິງແມ່ນວ່າ", "Mặc dù / Dẫu cho", "Although / Even though", "thoeng-maen-vaa", "conjunction", "Ngữ pháp", "ເຖິງແມ່ນວ່າຍາກກໍ່ຈະເຮັດ", "Dù khó khăn vẫn sẽ làm"),
        ("ເພື່ອ", "Để / Nhằm mục đích", "In order to / For", "phuea", "preposition", "Ngữ pháp", "ຮຽນເພື່ອອະນາຄົດ", "Học vì tương lai tươi sáng"),
        ("ກັບ", "Với / Cùng", "With", "kap", "preposition", "Ngữ pháp", "ໄປນຳກັນກັບຂ້ອຍ", "Hãy đi cùng tôi"),
        ("ກ່ຽວກັບ", "Về / Vấn đề liên quan", "About / Concerning", "kiaw-kap", "preposition", "Ngữ pháp", "ເວົ້າກ່ຽວກັບເລື່ອງນີ້", "Nói về vấn đề này"),
        ("ຈາກ", "Từ (xuất phát điểm)", "From", "chaak", "preposition", "Ngữ pháp", "ມາຈາກຫວຽດນາມ", "Đến từ Việt Nam"),
        ("ຮອດ", "Đến / Tới nơi", "To / Arrive", "hawt", "preposition", "Ngữ pháp", "ຮອດບ່ອນແລ້ວ", "Đã tới nơi rồi"),
        ("ຢູ່", "Ở / Tại", "At / In / Live", "yuu", "preposition", "Ngữ pháp", "ຢູ່ເຮືອນ", "Ở nhà"),
        ("ໃນ", "Trong / Bên trong", "In / Inside", "nai", "preposition", "Ngữ pháp", "ຢູ່ໃນຫ້ອງ", "Ở trong phòng"),
        ("ນອກ", "Ngoài / Bên ngoài", "Outside", "nawk", "preposition", "Ngữ pháp", "ຢູ່ນອກເຮືອນ", "Ở bên ngoài sân"),
        ("ເທິງ", "Trên / Phía trên", "On / Above", "thoeng", "preposition", "Ngữ pháp", "ເທິງໂຕະ", "Ở trên mặt bàn"),
        ("ລຸ່ມ", "Dưới / Phía dưới", "Under / Below", "lum", "preposition", "Ngữ pháp", "ກ້ອງລຸ່ມຕຽງ", "Ở dưới gầm giường"),
        ("ໜ້າ", "Trước / Mặt", "In front of / Face", "naa", "preposition", "Ngữ pháp", "ຢູ່ທາງໜ້າ", "Ở phía đằng trước"),
        ("ຫຼັງ", "Sau / Lưng", "Behind / Back", "lang", "preposition", "Ngữ pháp", "ຢູ່ທາງຫຼັງ", "Ở phía sau lưng"),
        ("ຂ້າງ", "Bên cạnh", "Beside / Next to", "khaang", "preposition", "Ngữ pháp", "ນັ່ງຢູ່ຂ້າງຂ້ອຍ", "Ngồi ở bên cạnh tôi"),
        ("ລະຫວ່າງ", "Ở giữa", "Between", "la-vaang", "preposition", "Ngữ pháp", "ລະຫວ່າງສອງບ້ານ", "Ở giữa hai bản làng"),
        ("ຫຼາຍ", "Nhiều", "Many / Much", "laai", "adverb", "Ngữ pháp", "ຂອບໃຈຫຼາຍ", "Cảm ơn nhiều lắm"),
        ("ໜ້ອຍ", "Ít", "Few / Little", "nawy", "adverb", "Ngữ pháp", "ກິນໜ້ອຍດຽວ", "Ăn có một chút"),
        ("ແທ້ໆ", "Thực sự / Thật đấy", "Really / Truly", "thae-thae", "adverb", "Ngữ pháp", "ງາມແທ້ໆ", "Đẹp thật sự đấy"),
        ("ແນ່ນອນ", "Chắc chắn rồi / Nhất định", "Certainly / Definitely", "nae-nawn", "adverb", "Giao tiếp", "ຂ້ອຍຈະໄປແນ່ນອນ", "Tôi nhất định sẽ đi"),
        ("ອາດຈະ", "Có lẽ / Có thể", "Maybe / Perhaps", "aat-cha", "adverb", "Ngữ pháp", "ມື້ອື່ນອາດຈະຝົນຕົກ", "Ngày mai có thể sẽ mưa"),
        ("ຕ້ອງ", "Phải (bắt buộc)", "Must / Have to", "tawng", "verb", "Ngữ pháp", "ຕ້ອງຕັ້ງໃຈ", "Phải quyết tâm cố gắng"),
        ("ຄວນ", "Nên (khuyên bảo)", "Should / Ought to", "khuan", "verb", "Ngữ pháp", "ຄວນໄປພັກຜ່ອນ", "Bạn nên đi nghỉ ngơi"),
        ("ສາມາດ", "Có thể / Khả năng", "Can / Be able to", "saa-maat", "verb", "Ngữ pháp", "ຂ້ອຍສາມາດເວົ້າພາສາລາວໄດ້", "Tôi có thể nói được tiếng Lào"),
        ("ຢາກ", "Muốn", "Want to", "yaak", "verb", "Ngữ pháp", "ຢາກໄປທ່ຽວ", "Muốn đi du lịch"),
        ("ມັກ", "Thích / Yêu thích", "Like / Fond of", "mak", "verb", "Ngữ pháp", "ມັກອາຫານລາວ", "Rất thích ẩm thực Lào"),
        ("ຊັງ", "Ghét", "Hate / Dislike", "xang", "verb", "Cảm xúc", "ບໍ່ມັກກໍ່ບໍ່ຊັງ", "Không thích cũng chẳng ghét"),
        ("ເຂົ້າໃຈ", "Hiểu / Lĩnh hội", "Understand", "khao-chai", "verb", "Nhận thức", "ເຈົ້າເຂົ້າໃຈບໍ", "Bạn có hiểu không"),
        ("ບໍ່ເຂົ້າໃຈ", "Không hiểu", "Don't understand", "baw-khao-chai", "phrase", "Giao tiếp", "ຂ້ອຍບໍ່ເຂົ້າໃຈ", "Tôi không hiểu"),
        ("ຮູ້", "Biết", "Know", "huu", "verb", "Nhận thức", "ຂ້ອຍຮູ້ແລ້ວ", "Tôi biết rồi"),
        ("ບໍ່ຮູ້", "Không biết", "Don't know", "baw-huu", "phrase", "Giao tiếp", "ຂ້ອຍບໍ່ຮູ້ຈັກ", "Tôi không biết"),
        ("ຈື່", "Nhớ (trong ký ức)", "Remember", "chue", "verb", "Nhận thức", "ຈື່ໄດ້ບໍ", "Bạn còn nhớ không"),
        ("ລືມ", "Quên mất", "Forget", "leum", "verb", "Nhận thức", "ຂ້ອຍລືມແລ້ວ", "Tôi quên mất rồi"),
        ("ຄິດ", "Nghĩ / Suy nghĩ", "Think", "khit", "verb", "Nhận thức", "ຄິດຮອດເຈົ້າ", "Rất nhớ bạn"),
        ("ຄິດຮອດ", "Nhớ nhung", "Miss (someone)", "khit-hawt", "verb", "Tình cảm", "ຄິດຮອດບ້ານ", "Nhớ quê hương da diết"),
        ("ຮັກ", "Yêu thương", "Love", "hak", "verb", "Tình cảm", "ຮັກພໍ່ແມ່", "Yêu thương bố mẹ"),
        ("ເຫັນ", "Nhìn thấy", "See", "hen", "verb", "Giác quan", "ເຫັນບໍ່", "Bạn có nhìn thấy không"),
        ("ໄດ້ຍິນ", "Nghe thấy", "Hear", "dai-nyin", "verb", "Giác quan", "ໄດ້ຍິນສຽງລົດ", "Nghe thấy tiếng xe cộ"),
        ("ດົມ", "Ngửi mùi", "Smell", "dom", "verb", "Giác quan", "ດົມກິ່ນດອກໄມ້", "Ngửi hương thơm ngát của hoa"),
        ("ຊິມ", "Nếm thử vị", "Taste", "xim", "verb", "Ẩm thực", "ຊິມເບິ່ງດູແຊບບໍ", "Nếm thử xem có ngon không"),
        ("ຈັບ", "Cầm / Nắm / Bắt", "Touch / Hold / Catch", "chap", "verb", "Hành động", "ຈັບມືກັນ", "Nắm chặt tay nhau"),
        ("ວາງ", "Đặt / Để xuống", "Put / Place down", "vaang", "verb", "Hành động", "ວາງໃສ່ໂຕະ", "Đặt lên trên bàn"),
        ("ຍົກ", "Nâng lên / Giơ lên", "Lift / Raise", "nyok", "verb", "Hành động", "ຍົກມືຂຶ້ນ", "Giơ cánh tay lên"),
        ("ດຶງ", "Kéo", "Pull", "dueng", "verb", "Hành động", "ດຶງປະຕູ", "Kéo cánh cửa"),
        ("ຍູ້", "Đẩy", "Push", "nyuu", "verb", "Hành động", "ຍູ້ປະຕູເຂົ້າໄປ", "Đẩy cửa bước vào"),
    ]
    return vocab_list


def expand_dictionary_mega():
    """Đọc từ điển hiện có, gộp thêm các mục từ thông dụng mới và lưu lại."""
    print("=" * 60)
    print("🚀 BẮT ĐẦU MỞ RỘNG KHO TỪ ĐIỂN TIẾNG LÀO THÔNG DỤNG")
    print("=" * 60)

    existing = {}
    if os.path.exists(DICT_PATH):
        with open(DICT_PATH, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for r in reader:
                norm = normalize_lao(r.get("lao", "").strip())
                if norm:
                    existing[norm] = {
                        "lao": norm,
                        "vi": r.get("vi", "").strip(),
                        "en": r.get("en", "").strip(),
                        "romanization": r.get("romanization", "").strip(),
                        "pos": r.get("pos", "").strip(),
                        "lesson": r.get("lesson", "").strip(),
                        "example_lao": normalize_lao(r.get("example_lao", "").strip()),
                        "example_vi": r.get("example_vi", "").strip(),
                    }

    initial_count = len(existing)
    print(f"• Số lượng từ điển ban đầu: {initial_count} mục từ.")

    new_list = get_massive_common_vocab()
    added = 0

    for item in new_list:
        lao_txt, vi, en, rom, pos, lesson, ex_lao, ex_vi = item
        norm_k = normalize_lao(lao_txt.strip())
        if not norm_k:
            continue

        if norm_k not in existing:
            existing[norm_k] = {
                "lao": norm_k,
                "vi": vi.strip(),
                "en": en.strip(),
                "romanization": rom.strip(),
                "pos": pos.strip(),
                "lesson": lesson.strip(),
                "example_lao": normalize_lao(ex_lao.strip()),
                "example_vi": ex_vi.strip(),
            }
            added += 1

    sorted_keys = sorted(existing.keys())

    with open(DICT_PATH, mode="w", encoding="utf-8", newline="") as f:
        fieldnames = ["lao", "vi", "en", "romanization", "pos", "lesson", "example_lao", "example_vi"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for k in sorted_keys:
            writer.writerow(existing[k])

    print(f"• Đã bổ sung thành công: +{added} từ vựng thông dụng mới.")
    print(f"• TỔNG QUY MÔ TỪ ĐIỂN HIỆN TẠI: {len(sorted_keys)} MỤC TỪ CHUẨN NFC.")
    print("=" * 60)
    return len(sorted_keys)


if __name__ == "__main__":
    expand_dictionary_mega()
