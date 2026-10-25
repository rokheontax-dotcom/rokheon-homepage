"""록헌 세무회계 홈페이지 생성 스크립트.

메뉴·푸터·연락처를 한 곳에서 관리하고, 모든 페이지 HTML을 만든다.
실행:  python build.py   (이 폴더에서)

- 홈/회사소개 본문: _원본/홈.html, _원본/회사소개.html
- 업무 분야 페이지: 아래 SERVICES 데이터에서 생성 → services/*.html
- 결과 HTML은 직접 고치지 말고 이 파일이나 _원본을 고친 뒤 다시 실행한다.
"""
from pathlib import Path
from html import escape
import hashlib

ROOT = Path(__file__).parent


def ver(rel):
    """파일 내용 해시 — CSS/JS가 바뀌면 주소가 달라져 휴대폰 캐시에 옛 파일이 남지 않는다."""
    return hashlib.md5((ROOT / rel).read_bytes()).hexdigest()[:8]

# ── 연락처 (확정되면 여기만 바꾸면 전 페이지 반영) ──
KAKAO = "https://pf.kakao.com/_EGkQG/chat"  # 누르면 바로 채팅창이 열리는 주소
TEL = "tel:0325454263"
TEL_TEXT = "032-545-4263"
MOBILE = "tel:01045234263"
MOBILE_TEXT = "010-4523-4263"
BLOG = "https://blog.naver.com/PostList.naver?blogId=rokheontax&amp;from=postList&amp;categoryNo=3"  # 블로그 세무칼럼 카테고리 (HTML 속성이라 &는 &amp;)
EMAIL = "gnstjd3636@rokheon.com"
ADDRESS = "인천광역시 서해구 가정로 451, 446호"
HOURS = "평일 09:00 ~ 18:00"
BIZ_NO = "453-07-02934"

# ── 업무 분야 (메뉴 순서 = 이 목록 순서) ──
# 광고 문구 주의: 세무사법 시행령 제33조②에 따라 근거 없는 '무료·최저가', 처분 결과 예측, 환급액 수치 광고 금지
SERVICES = [
    {
        "slug": "bookkeeping", "name": "기장·신고 대리",
        "card": "신고만 맡기셔도, 장부까지 맡기셔도 됩니다. 개인·법인 상황에 맞게 진행합니다.",
        "lead": "신고만 맡기셔도, 장부까지 맡기셔도 됩니다.",
        # 세 가지 맡기는 방식 — 페이지 상단 카드 3장
        "parts": [
            {"name": "신고 대리", "tag": "필요한 신고만",
             "who": "장부는 직접 정리하시거나, 1년에 몇 번 있는 신고만 맡기고 싶은 개인사업자",
             "items": ["부가가치세 신고 (일반·간이과세자)", "사업장현황신고 (면세사업자)", "종합소득세 신고 대리"]},
            {"name": "개인사업자 기장", "tag": "매달 장부까지",
             "who": "매달 장부와 신고를 모두 맡기고 사업에만 집중하고 싶은 개인사업자",
             "items": ["매달 장부 작성 (복식부기)", "부가가치세·원천세 신고", "종합소득세 신고 (성실신고확인 포함)", "신고 전 예상 세액 안내"],
             "note": "종합소득세 신고 수수료(조정료)는 기장료와 별도입니다."},
            {"name": "법인사업자 기장", "tag": "결산·법인세까지",
             "who": "장부 작성부터 결산, 법인세 신고까지 맡겨야 하는 법인",
             "items": ["장부 작성과 결산", "법인세·부가가치세·원천세 신고", "대표자 급여·가지급금 점검", "중간예납 등 일정 안내"],
             "note": "법인세 신고 수수료(조정료)는 기장료와 별도입니다."},
        ],
        "for": [
            "매달 돌아오는 세금 신고 일정을 챙기기 버거운 사장님",
            "장부는 직접 정리하고 신고만 맡기고 싶은 분",
            "매출이 늘어 간편장부에서 복식부기로 바뀌는 분",
            "지금 세무대리인과 연락이 잘 닿지 않아 답답한 분",
        ],
        "check": [
            "매달 증빙 자료를 검토해 경비로 인정되는 것과 아닌 것을 구분합니다.",
            "부가가치세·원천세·종합소득세(법인세) 신고 일정을 미리 안내합니다.",
            "업종에 적용할 수 있는 공제·감면 요건을 하나씩 확인합니다.",
            "신고 전에 예상 세액을 알려드려 자금 계획을 세우실 수 있게 합니다.",
        ],
        "basis": "부가가치세법, 소득세법, 법인세법, 조세특례제한법, 국세기본법",
        "steps": [
            ("상담·자료 확인", "업종, 매출 규모, 현재 신고 상황을 확인하고 맞는 방식을 정합니다."),
            ("수임 계약", "계약 후 홈택스 수임 동의로 신고 자료를 연결합니다."),
            ("장부 작성·신고", "기장은 매달 장부를 쓰고, 신고 대리는 신고 시기에 맞춰 진행합니다."),
            ("결산·리포트", "손익과 예상 세액을 보고드리고 다음 신고를 준비합니다."),
        ],
        # 아래 rules·calendar는 (탭 이름, 항목들) 목록이면 탭으로 나뉜다.
        # 조문은 국가법령정보센터 원문으로 확인한 것만 쓴다 (2026-10-25 확인, 현행 기준)
        "rules": [
            ("개인사업자", [
                ("간편장부와 복식부기, 기준은 매출입니다",
                 "개업한 해에는 간편장부대상자입니다. 다음 해부터는 직전 연도 수입금액이 업종별 기준(도소매업 등 3억원, "
                 "제조·음식점업 등 1억5천만원, 부동산임대·서비스업 등 7,500만원) 이상이면 복식부기의무자가 됩니다. "
                 "의료업·수의업·약국과 변호사·세무사 등 전문직은 매출과 상관없이 복식부기의무자입니다.",
                 "소득세법 제160조, 같은 법 시행령 제208조 ⑤"),
                ("간편장부대상자도 복식부기로 쓰면 공제를 받습니다",
                 "간편장부대상자가 복식부기로 장부를 쓰고 신고하면 사업소득 산출세액의 20%를 100만원 한도로 공제받습니다. "
                 "다만 소득을 20% 이상 누락하거나 장부·증빙을 5년간 보관하지 않으면 공제하지 않습니다.",
                 "소득세법 제56조의2"),
                ("장부가 없으면 가산세가 붙습니다",
                 "장부를 쓰지 않으면 산출세액 중 기장하지 않은 소득 비율만큼에 20%를 곱한 가산세가 붙습니다. "
                 "개업한 해이거나 직전 연도 수입금액이 4,800만원 미만인 소규모사업자는 제외됩니다.",
                 "소득세법 제81조의5, 같은 법 시행령 제147조 ①·제132조 ④"),
                ("적자도 장부가 있어야 인정됩니다",
                 "장부로 계산한 결손금은 다른 소득에서 빼고, 남으면 15년 동안 이월해 공제합니다. "
                 "장부 없이 추계로 신고하면 이월결손금 공제를 받을 수 없습니다.",
                 "소득세법 제45조 ①·③·④"),
                ("복식부기의무자는 사업용계좌를 신고해야 합니다",
                 "복식부기의무자가 되면 그 과세기간 개시일부터 6개월 이내에 사업용계좌를 신고하고, 거래대금·인건비·임차료를 그 계좌로 주고받아야 합니다. "
                 "신고하지 않으면 창업중소기업 세액감면 등을 받을 수 없습니다.",
                 "소득세법 제160조의5, 조세특례제한법 제128조 ④"),
                ("면세사업자는 2월 10일까지 사업장현황신고를 합니다",
                 "부가가치세를 신고하지 않는 면세 개인사업자는 다음 해 2월 10일까지 수입금액 등 사업장 현황을 신고해야 합니다.",
                 "소득세법 제78조"),
            ]),
            ("법인사업자", [
                ("법인은 규모와 상관없이 복식부기입니다",
                 "법인은 매출 규모와 상관없이 복식부기로 장부를 쓰고, 장부와 관련된 중요한 증빙을 보관해야 합니다.",
                 "법인세법 제112조"),
                ("장부가 없으면 산출세액이 없어도 가산세가 붙습니다",
                 "장부를 쓰지 않으면 산출세액의 20%와 수입금액의 0.07% 중 큰 금액이 가산세로 붙고, 산출세액이 없어도 적용됩니다.",
                 "법인세법 제75조의3"),
                ("증빙은 적격증빙으로, 5년간 보관합니다",
                 "사업 관련 거래의 증빙은 신고기한이 지난 날부터 5년간 보관해야 합니다. 사업자에게 대가를 지급할 때는 "
                 "세금계산서·계산서·신용카드매출전표·현금영수증을 받아야 하고, 받지 않으면 가산세가 붙습니다.",
                 "법인세법 제116조, 제75조의5"),
                ("법인 부가가치세는 1년에 네 번 신고합니다",
                 "법인은 분기마다 예정신고와 확정신고를 합니다. 다만 직전 과세기간 공급가액이 1억5천만원 미만인 법인은 "
                 "예정신고 대신 세무서가 고지한 금액을 납부합니다.",
                 "부가가치세법 제48조·제49조, 같은 법 시행령 제90조 ④"),
            ]),
        ],
        "calendar": [
            ("개인사업자", [
                ("매월 10일", "원천세 신고·납부", "직원·프리랜서에게 지급한 급여·용역비가 있는 경우 (반기납부 승인 시 반기별)", "소득세법 제128조"),
                ("1월 25일", "부가가치세 확정신고", "일반과세자 2기분, 간이과세자 1년분", "부가가치세법 제49조, 제67조"),
                ("2월 10일", "사업장현황신고", "면세사업자", "소득세법 제78조"),
                ("3월 10일", "연말정산·지급명세서 제출", "직원·프리랜서가 있는 경우", "소득세법 제137조, 제164조"),
                ("4월 25일", "부가가치세 예정고지 납부", "일반과세자 (세무서 고지 금액)", "부가가치세법 제48조 ③"),
                ("5월 31일", "종합소득세 신고", "성실신고확인대상자는 6월 30일", "소득세법 제70조, 제70조의2"),
                ("7월 25일", "부가가치세 확정신고", "일반과세자 1기분", "부가가치세법 제49조"),
                ("10월 25일", "부가가치세 예정고지 납부", "일반과세자 (세무서 고지 금액)", "부가가치세법 제48조 ③"),
                ("11월 30일", "종합소득세 중간예납", "세무서 고지 금액 납부 (개업한 해는 제외)", "소득세법 제65조"),
            ]),
            ("법인사업자 (12월 결산)", [
                ("매월 10일", "원천세 신고·납부", "급여·용역비 등을 지급한 경우 (반기납부 승인 시 반기별)", "소득세법 제128조"),
                ("1월 25일", "부가가치세 2기 확정신고", "", "부가가치세법 제49조"),
                ("3월 10일", "연말정산·지급명세서 제출", "직원·프리랜서가 있는 경우", "소득세법 제137조, 제164조"),
                ("3월 31일", "법인세 신고", "성실신고확인 법인은 4월 30일", "법인세법 제60조"),
                ("4월 25일", "부가가치세 1기 예정신고", "직전 과세기간 공급가액 1억5천만원 미만 법인은 고지 금액 납부", "부가가치세법 제48조"),
                ("7월 25일", "부가가치세 1기 확정신고", "", "부가가치세법 제49조"),
                ("8월 31일", "법인세 중간예납", "설립 후 첫 사업연도는 제외", "법인세법 제63조"),
                ("10월 25일", "부가가치세 2기 예정신고", "직전 과세기간 공급가액 1억5천만원 미만 법인은 고지 금액 납부", "부가가치세법 제48조"),
            ]),
        ],
        "calendar_note": "기한이 토요일·일요일·공휴일이면 그다음 날까지입니다. (국세기본법 제5조)",
        "docs": [
            "사업자등록증, 대표자 신분증",
            "홈택스 수임 동의 (계약 후 안내드립니다)",
            "사업용 통장·카드 내역",
            "임대차계약서 (사업장을 임차한 경우)",
            "직원 인적사항과 급여 조건 (직원이 있는 경우)",
            "법인등기사항증명서·정관·주주명부 (법인인 경우)",
            "지난 신고서 (다른 세무대리인에게서 옮기시는 경우)",
        ],
        "faq": [
            ("신고 대리와 기장, 어떤 걸 맡겨야 할까요?",
             "매출 규모, 직원 유무, 장부를 직접 정리하실 수 있는지에 따라 달라집니다. "
             "복식부기의무자이거나 직원이 있다면 기장을 권해드리고, 그 외에는 상황을 듣고 함께 정합니다."),
            ("신고 대리로 시작했다가 기장으로 바꿀 수 있나요?",
             "네. 매출이 늘어 복식부기의무자가 되거나 직원을 채용하시면 기장으로 바꿔 이어서 진행합니다."),
            ("지금 세무대리인이 있는데, 중간에 옮길 수 있나요?",
             "네, 가능합니다. 새로 수임 동의를 하시면 되고, 이전 신고 내역과 장부를 넘겨받아 이어서 진행합니다."),
            ("영수증은 어떻게 전달하나요?",
             "카드·현금영수증·세금계산서처럼 홈택스에서 조회되는 자료는 저희가 직접 확인합니다. "
             "조회되지 않는 계약서나 간이영수증만 사진으로 보내주시면 됩니다."),
            ("기장료와 신고 수수료는 어떻게 정해지나요?",
             "업종, 매출 규모, 직원 수, 거래 건수에 따라 달라집니다. 현재 상황을 확인한 뒤 안내드립니다. "
             "기장을 맡기셔도 종합소득세·법인세 신고 수수료(조정료)는 별도입니다."),
        ],
    },
    {
        "slug": "startup", "name": "창업·법인 설립 지원",
        "card": "개인사업자와 법인 중 어느 쪽이 맞는지 비교하고, 설립 절차까지 함께 진행합니다.",
        "lead": "개인사업자로 시작할지, 법인으로 시작할지부터 함께 정합니다.",
        "for": [
            "창업을 준비 중인데 사업자 형태를 정하지 못한 분",
            "개인사업자에서 법인 전환을 고민하는 분",
            "공동 창업으로 지분 구조를 정해야 하는 분",
            "창업 관련 세액감면 대상인지 궁금한 분",
        ],
        "check": [
            "예상 매출과 이익을 기준으로 개인과 법인의 세부담을 비교합니다.",
            "업종·지역·대표자 나이 등 창업 세액감면 요건을 확인합니다.",
            "정관과 지분 구조가 이후 세금에 미치는 영향을 검토합니다.",
            "사업자등록과 법인 설립 절차를 안내하고 함께 진행합니다.",
        ],
        "basis": "조세특례제한법(창업중소기업 등에 대한 세액감면 등), 소득세법, 법인세법, 상법",
        "steps": [
            ("사업 구조 상담", "사업 내용, 예상 매출, 동업 여부를 확인합니다."),
            ("개인·법인 비교", "세부담과 감면 요건을 비교해 형태를 정합니다."),
            ("설립·등록 지원", "법인 설립과 사업자등록 절차를 진행합니다."),
            ("기장·신고 시작", "첫 신고부터 놓치는 부분이 없게 챙깁니다."),
        ],
    },
    {
        "slug": "tax-planning", "name": "절세 컨설팅",
        "card": "놓친 공제·감면이 없는지 점검하고, 근거가 있는 방법만 제안합니다.",
        "lead": "법이 허용하는 범위 안에서, 근거가 있는 방법만 제안합니다.",
        "for": [
            "소득이 늘어 세금 부담이 커진 사업자",
            "법인 대표의 급여·배당·퇴직금을 어떻게 받을지 고민하는 분",
            "법인에 쌓인 이익이나 가업 승계를 정리하고 싶은 분",
            "다른 곳에서 들은 절세 방법이 맞는지 확인하고 싶은 분",
        ],
        "check": [
            "지난 신고 내역을 바탕으로 놓친 공제·감면이 없는지 점검합니다.",
            "대표자 급여·배당·퇴직금 등 받는 방법별 세부담을 비교합니다.",
            "제안하는 방법마다 근거 법령과 국세청 해석 사례를 함께 드립니다.",
            "나중에 세무조사에서 문제될 수 있는 위험도 같이 설명드립니다.",
        ],
        "basis": "소득세법, 법인세법, 조세특례제한법, 국세청 예규·심판례",
        "steps": [
            ("현황 상담", "지금 고민과 목표를 듣습니다."),
            ("자료 분석", "신고 내역과 재무 자료를 검토합니다."),
            ("검토 보고서", "방법별 세부담과 근거를 정리해 드립니다."),
            ("실행·관리", "실행 과정과 이후 신고까지 함께합니다."),
        ],
    },
    {
        "slug": "capital-gains", "name": "양도소득세",
        "card": "부동산·주식을 팔기 전 비과세·감면 요건을 법령과 예규로 미리 확인합니다.",
        "lead": "팔기 전에 확인하면 선택지가 더 많습니다.",
        "for": [
            "집이나 땅을 팔 계획이 있는 분",
            "1세대 1주택 비과세에 해당하는지 확인이 필요한 분",
            "일시적 2주택·상속주택 등 주택 수 판단이 복잡한 분",
            "주식·분양권·입주권을 양도하시는 분",
        ],
        "check": [
            "비과세·감면 요건을 법령과 국세청 예규로 하나씩 확인합니다.",
            "취득가액과 필요경비로 인정받을 수 있는 서류를 정리합니다.",
            "양도 시기에 따라 달라지는 세액을 비교해 드립니다.",
            "신고 기한과 납부 방법을 안내하고 신고를 대행합니다.",
        ],
        "basis": "소득세법(양도소득), 소득세법 시행령, 조세특례제한법, 국세청 예규·심판례",
        "steps": [
            ("상담·서류 확인", "취득·보유 내역과 가족의 주택 보유 현황을 확인합니다."),
            ("요건 검토", "비과세·감면 요건을 확인하고 예상 세액을 계산합니다."),
            ("시기·방법 조언", "양도 시기와 방법에 따른 차이를 설명드립니다."),
            ("신고 대행", "기한 안에 신고와 납부를 마칩니다."),
        ],
    },
    {
        "slug": "inheritance-gift", "name": "상속·증여세",
        "card": "가족 상황에 맞는 공제와 평가 방법을 확인하고, 사전 준비부터 신고까지 함께합니다.",
        "lead": "미리 준비할수록 가족에게 맞는 선택지가 넓어집니다.",
        "for": [
            "부모님 재산의 상속을 앞두고 미리 준비하고 싶은 분",
            "자녀에게 재산 증여를 고민하는 분",
            "상속이 시작되어 신고를 준비해야 하는 분",
            "가족 간 부동산·자금 이동이 증여로 보일지 걱정되는 분",
        ],
        "check": [
            "상속·증여 공제 요건을 가족 상황에 맞춰 확인합니다.",
            "과거에 증여한 재산이 합산되는지 점검합니다.",
            "부동산 평가 방법에 따른 세액 차이를 비교합니다.",
            "분납·연부연납 등 납부 방법을 함께 검토합니다.",
        ],
        "basis": "상속세 및 증여세법, 같은 법 시행령, 국세청 예규·심판례",
        "steps": [
            ("가족·재산 상담", "가족 관계와 재산 현황을 정리합니다."),
            ("공제·평가 검토", "적용 가능한 공제와 평가 방법을 확인합니다."),
            ("계획 수립", "사전 증여 또는 상속 신고 계획을 세웁니다."),
            ("신고·사후 관리", "신고 후 세무서 확인 과정까지 대응합니다."),
        ],
    },
    {
        "slug": "tax-audit", "name": "세무조사 대응",
        "card": "조사 통지를 받으셨다면, 쟁점과 소명 자료부터 함께 정리합니다.",
        "lead": "조사 통지를 받으셨다면, 쟁점부터 정리합니다.",
        "for": [
            "세무조사 사전통지를 받은 분",
            "세무서로부터 소명 자료 제출 요구를 받은 분",
            "과세예고통지를 받아 대응을 검토 중인 분",
            "이미 고지된 세금에 이의가 있는 분",
        ],
        "check": [
            "조사 범위와 예상 쟁점을 먼저 파악합니다.",
            "소명 자료를 근거 법령에 맞춰 정리합니다.",
            "조사 과정에 함께하며 질의에 대응합니다.",
            "필요하면 과세전적부심사·이의신청 등 불복 절차를 검토합니다.",
        ],
        "basis": "국세기본법(세무조사·불복 절차), 각 세법, 국세청 예규·조세심판원 결정례",
        "steps": [
            ("통지 내용 확인", "조사 대상 세목과 기간을 확인합니다."),
            ("쟁점·자료 검토", "문제될 수 있는 부분과 소명 자료를 정리합니다."),
            ("조사 대응", "조사 과정에서 질의와 자료 제출에 대응합니다."),
            ("결과 검토", "결과를 검토하고 필요하면 불복 절차를 안내합니다."),
        ],
    },
]

HOW = [
    ("직접 상담", "대표 세무사가 처음부터 끝까지 직접 상담합니다. 담당자가 바뀌어 같은 설명을 반복하실 일이 없습니다."),
    ("근거로 답변", '"아마 될 거예요"라고 답하지 않습니다. 관련 법령과 국세청 예규를 찾아 근거와 함께 설명드립니다.'),
    ("확인한 것만", "바로 답하기 어려운 질문은 확인한 뒤 말씀드립니다. 확인하지 않은 내용은 말씀드리지 않습니다."),
]


# ── 홈 "이런 고민으로 찾아오십니다" (질문, 업무 slug) — 메신저 말풍선으로 하나씩 나타남 ──
# 고객 후기가 아니라 상담에서 자주 듣는 질문이다. 결과를 약속하는 문구는 넣지 않는다. 짧게 유지.
WORRIES = [
    ("법인으로 바꾸면 세금이 줄어드나요?", "startup"),
    ("매달 신고 챙기기가 버거워요", "bookkeeping"),
    ("집 팔기 전에 비과세인지 알고 싶어요", "capital-gains"),
    ("대표 퇴직금, 얼마까지 가능할까요?", "tax-planning"),
    ("자녀에게 증여, 지금 해도 될까요?", "inheritance-gift"),
    ("세무서에서 소명 요청이 왔어요", "tax-audit"),
]
WORRY_REPLY = "하나씩 확인하고, 근거와 함께 답해드릴게요."


def worry_chat(r):
    out = [f'        <a class="msg" href="{r}services/{slug}.html" data-reveal style="--d:{i * 0.12:.2f}s">{escape(q)}</a>'
           for i, (q, slug) in enumerate(WORRIES)]
    out.append(f'        <p class="msg me" data-reveal style="--d:{len(WORRIES) * 0.12 + 0.1:.2f}s">'
               f'<img src="{r}이미지/심볼.png" alt="록헌">{escape(WORRY_REPLY)}</p>')
    return "\n".join(out)


def steps_html(items, cls="steps"):
    out = [f'      <div class="{cls}">']
    for i, (title, desc) in enumerate(items):
        out.append(f'        <div class="step" data-reveal style="--d:{i * 0.12:.2f}s"><div class="n">{i + 1:02d}</div>'
                   f'<b>{escape(title)}</b><p>{escape(desc)}</p></div>')
    out.append("      </div>")
    return "\n".join(out)


def info_html():
    return f"""          <dl class="info">
            <div><dt>대표번호</dt><dd><a href="{TEL}">{TEL_TEXT}</a></dd></div>
            <div><dt>휴대전화</dt><dd><a href="{MOBILE}">{MOBILE_TEXT}</a></dd></div>
            <div><dt>카카오톡</dt><dd><a href="{KAKAO}" target="_blank" rel="noopener">록헌 세무회계 채널</a></dd></div>
            <div><dt>이메일</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
            <div><dt>주소</dt><dd>{ADDRESS}</dd></div>
            <div><dt>상담 시간</dt><dd>{HOURS}</dd></div>
          </dl>"""


def header(r, current):
    links = "\n".join(
        f'          <a href="{r}services/{s["slug"]}.html"{" class=\"on\"" if current == s["slug"] else ""}>{s["name"]} <span>→</span></a>'
        for s in SERVICES)
    svc_on = ' on' if current in [s["slug"] for s in SERVICES] else ''
    about_on = ' class="on"' if current == "about" else ''
    return f"""<header class="site">
  <div class="wrap nav">
    <a href="{r}index.html" class="logo"><img src="{r}이미지/로고_가로.png" alt="록헌 세무회계"></a>
    <button class="burger" aria-label="메뉴 열기" aria-expanded="false"><i></i></button>
    <nav class="menu">
      <a href="{r}about.html"{about_on}>회사소개</a>
      <div class="dd">
        <button class="dd-btn{svc_on}" aria-expanded="false">업무 분야<span class="chev"></span></button>
        <div class="dd-panel">
{links}
        </div>
      </div>
      <a href="{BLOG}" target="_blank" rel="noopener">세무칼럼<span class="ext">↗</span></a>
      <a href="{KAKAO}" target="_blank" rel="noopener" class="cta">카톡 상담하기</a>
    </nav>
  </div>
  <div class="progress"></div>
</header>"""


def footer(r):
    svc = "".join(f'<a href="{r}services/{s["slug"]}.html">{s["name"]}</a>' for s in SERVICES)
    return f"""<footer class="site">
  <div class="wrap">
    <div>
      <b>록헌 세무회계</b><br>
      대표 세무사 이훈성 · 사업자등록번호 {BIZ_NO}<br>
      {ADDRESS} · 대표번호 {TEL_TEXT} · 휴대전화 {MOBILE_TEXT} · {EMAIL}<br>
      © 2026 록헌 세무회계. All rights reserved.
    </div>
    <nav>
      <a href="{r}about.html">회사소개</a>{svc}<a href="{BLOG}" target="_blank" rel="noopener">세무칼럼</a>
    </nav>
  </div>
</footer>

<div class="mbar">
  <a href="{TEL}" class="tel">전화하기</a>
  <a href="{KAKAO}" target="_blank" rel="noopener" class="kakao">카톡 상담하기</a>
</div>"""


def page(r, current, title, desc, body):
    full_title = "록헌 세무회계" if title is None else f"{title} | 록헌 세무회계"
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{escape(desc)}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{escape(desc)}">
<link rel="icon" href="{r}이미지/심볼.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}css/style.css?v={ver('css/style.css')}">
<script>document.documentElement.classList.add('js');</script>
</head>
<body>

<!-- 이 파일은 build.py가 만든 결과물입니다. 직접 고치지 말고 build.py 또는 _원본을 고친 뒤 다시 실행하세요. -->
{header(r, current)}

<main>
{body}
</main>

{footer(r)}

<script src="{r}js/main.js?v={ver('js/main.js')}"></script>
</body>
</html>
"""


def fill(text, r):
    return (text.replace("{R}", r).replace("{KAKAO}", KAKAO).replace("{TEL_TEXT}", TEL_TEXT)
            .replace("{TEL}", TEL).replace("{INFO}", info_html()).replace("{HOW_STEPS}", steps_html(HOW)))


def service_cards(r):
    out = []
    for i, s in enumerate(SERVICES):
        out.append(f'        <a class="card" href="{r}services/{s["slug"]}.html" data-reveal style="--d:{i * 0.08:.2f}s">'
                   f'<div class="num">{i + 1:02d}</div><h4>{s["name"]}</h4><p>{escape(s["card"])}</p>'
                   f'<span class="go">자세히 보기 <span class="arr">→</span></span></a>')
    return "\n".join(out)


def parts_section(s):
    """맡기는 방식 카드 (parts). 데이터가 없으면 빈 문자열."""
    if not s.get("parts"):
        return ""
    cards = []
    for i, p in enumerate(s["parts"]):
        items = "".join(f"<li>{escape(t)}</li>" for t in p["items"])
        note = f'<p class="part-note">{escape(p["note"])}</p>' if p.get("note") else ""
        cards.append(f'        <div class="part" data-reveal style="--d:{i * 0.1:.2f}s"><span class="tag">{escape(p["tag"])}</span>'
                     f'<h3>{escape(p["name"])}</h3><p class="who">{escape(p["who"])}</p><ul>{items}</ul>{note}</div>')
    cards = "\n".join(cards)
    return f"""  <section class="sec bg-white">
    <div class="wrap">
      <div class="sec-head" data-reveal><small>HOW TO START</small><h2>상황에 맞게 맡기세요</h2></div>
      <div class="parts">
{cards}
      </div>
    </div>
  </section>
"""


def tabbed(key, data, render):
    """data가 (탭 이름, 항목들) 목록이면 탭으로, 그냥 항목 목록이면 탭 없이 render(items)."""
    if not (isinstance(data[0], tuple) and len(data[0]) == 2 and isinstance(data[0][1], list)):
        return render(data)
    btns = "".join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-tab="{key}-{i}">{escape(name)}</button>'
                   for i, (name, _) in enumerate(data))
    panels = "\n".join(f'      <div class="tab-panel{" on" if i == 0 else ""}" id="{key}-{i}" role="tabpanel">\n{render(items)}\n      </div>'
                       for i, (_, items) in enumerate(data))
    return f'      <div class="tabs" role="tablist" data-reveal>{btns}</div>\n{panels}'


def extra_sections(s):
    """업무 페이지 선택 섹션 (rules·calendar·docs·faq). 데이터가 없으면 빈 문자열."""
    out = []
    if s.get("rules"):
        def rules(items):
            cards = "\n".join(
                f'        <div class="rule" data-reveal style="--d:{i % 2 * 0.1:.2f}s"><h4>{escape(t)}</h4><p>{escape(b)}</p>'
                f'<small>{escape(law)}</small></div>'
                for i, (t, b, law) in enumerate(items))
            return f'      <div class="rules">\n{cards}\n      </div>'
        out.append(f"""  <section class="sec bg-white">
    <div class="wrap">
      <div class="sec-head" data-reveal><small>KEY RULES</small><h2>꼭 알아두실 규정</h2></div>
{tabbed("rules", s["rules"], rules)}
    </div>
  </section>
""")
    if s.get("calendar"):
        def cal(items):
            rows = "\n".join(
                f'        <div class="cal-row"><b>{escape(when)}</b><div><strong>{escape(what)}</strong>'
                + (f'<span>{escape(who)}</span>' if who else "") + f'</div><small>{escape(law)}</small></div>'
                for when, what, who, law in items)
            return f'      <div class="cal" data-reveal>\n{rows}\n      </div>'
        note = f'\n      <p class="cal-note" data-reveal>{escape(s["calendar_note"])}</p>' if s.get("calendar_note") else ""
        out.append(f"""  <section class="sec bg-cream">
    <div class="wrap">
      <div class="sec-head" data-reveal><small>TAX CALENDAR</small><h2>1년 세금 일정, 미리 챙겨드립니다</h2></div>
{tabbed("cal", s["calendar"], cal)}{note}
    </div>
  </section>
""")
    if s.get("docs") or s.get("faq"):
        li = "\n".join(f'            <li data-reveal style="--d:{i * 0.06:.2f}s"><i>{i + 1:02d}</i>{escape(t)}</li>'
                       for i, t in enumerate(s.get("docs", [])))
        qa = "\n".join(f'          <details class="qa" data-reveal><summary>{escape(q)}</summary><p>{escape(a)}</p></details>'
                       for q, a in s.get("faq", []))
        docs = f"""      <div>
        <div class="sec-head" data-reveal><small>DOCUMENTS</small><h2>준비 자료</h2></div>
        <ul class="checklist">
{li}
        </ul>
      </div>
""" if s.get("docs") else ""
        faq = f"""      <div>
        <div class="sec-head" data-reveal><small>FAQ</small><h2>자주 묻는 질문</h2></div>
        <div class="faq">
{qa}
        </div>
      </div>
""" if s.get("faq") else ""
        out.append(f"""  <section class="sec">
    <div class="wrap split">
{docs}{faq}    </div>
  </section>
""")
    return "\n".join(out)


def service_body(s):
    r = "../"
    li = lambda items: "\n".join(f'            <li data-reveal style="--d:{i * 0.08:.2f}s"><i>{i + 1:02d}</i>{escape(t)}</li>'
                                 for i, t in enumerate(items))
    others = "".join(f'<a href="{x["slug"]}.html">{x["name"]}</a>' for x in SERVICES if x is not s)
    return f"""  <div class="page-hero">
    <div class="wrap">
      <p class="crumb fade-in"><a href="{r}index.html">홈</a> / <a href="{r}index.html#services">업무 분야</a> / {s["name"]}</p>
      <h1><span class="line"><span style="--d:.1s">{s["name"]}</span></span></h1>
      <p class="lead fade-in" style="--d:.4s">{escape(s["lead"])}</p>
      <div class="btns fade-in" style="--d:.6s">
        <a href="{KAKAO}" target="_blank" rel="noopener" class="btn btn-dark">카톡으로 상담하기 <span class="arr">→</span></a>
      </div>
    </div>
    <div class="deco" aria-hidden="true"></div>
  </div>

{parts_section(s)}
  <section class="sec">
    <div class="wrap split">
      <div>
        <div class="sec-head" data-reveal><small>FOR YOU</small><h2>이런 분께 필요합니다</h2></div>
        <ul class="checklist">
{li(s["for"])}
        </ul>
      </div>
      <div>
        <div class="sec-head" data-reveal><small>WHAT WE CHECK</small><h2>록헌이 확인하는 것</h2></div>
        <ul class="checklist">
{li(s["check"])}
        </ul>
        <p class="basis" data-reveal><b>검토 근거</b> · {escape(s["basis"])}</p>
      </div>
    </div>
  </section>

{extra_sections(s)}
  <section class="sec bg-white">
    <div class="wrap">
      <div class="sec-head" data-reveal><small>PROCESS</small><h2>진행 순서</h2></div>
{steps_html(s["steps"], "steps four")}
    </div>
  </section>

  <section class="sec" style="padding-top:0;padding-bottom:96px;background:var(--white)">
    <div class="wrap">
      <div class="sec-head" data-reveal style="margin-bottom:24px"><small>OTHER SERVICES</small></div>
      <div class="others" data-reveal>{others}</div>
    </div>
  </section>

  <div class="cta-band">
    <div class="wrap">
      <div data-reveal>
        <h2>{s["name"]}, 상황부터 알려주세요.</h2>
        <p>확인 후 근거와 함께 답변드립니다.</p>
      </div>
      <div class="btns" data-reveal style="--d:.1s">
        <a href="{KAKAO}" target="_blank" rel="noopener" class="btn btn-kakao">카톡 상담하기 <span class="arr">→</span></a>
        <a href="{TEL}" class="btn btn-cream-line">전화 {TEL_TEXT}</a>
      </div>
    </div>
  </div>"""


def main():
    src = ROOT / "_원본"
    home = fill((src / "홈.html").read_text(encoding="utf-8"), "").replace("{SERVICE_CARDS}", service_cards("")).replace("{WORRY_CHAT}", worry_chat(""))
    (ROOT / "index.html").write_text(page("", "home", None,
        "법대 출신 세무사가 처음부터 끝까지 직접 상담합니다. 법령과 예규를 근거로 답하는 록헌 세무회계.", home), encoding="utf-8")

    about = fill((src / "회사소개.html").read_text(encoding="utf-8"), "")
    (ROOT / "about.html").write_text(page("", "about", "회사소개",
        "록헌 세무회계 대표 세무사 이훈성 소개, 일하는 방식, 오시는 길.", about), encoding="utf-8")

    (ROOT / "services").mkdir(exist_ok=True)
    for s in SERVICES:
        (ROOT / "services" / f'{s["slug"]}.html').write_text(
            page("../", s["slug"], s["name"], f'{s["name"]} — {s["lead"]} 록헌 세무회계.', service_body(s)), encoding="utf-8")
    print("생성 완료:", 2 + len(SERVICES), "페이지")


if __name__ == "__main__":
    main()
