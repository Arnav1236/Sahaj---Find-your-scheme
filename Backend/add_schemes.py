import csv
import io
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Setup Firebase Connection
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. Your Raw CSV Data
csv_data = """State,Category,Scheme Name (EN),Scheme Name (HI),Scheme Name (MR),Scheme Name (TA),Scheme Name (TE),Scheme Name (BN)
"Maharashtra","Women","Majhi Ladki Bahin Yojana","माझी लाडकी बहीण योजना","माझी लाडकी बहीण योजना","மாஜி லாட்கি பஹின் யோजனா","మాఝీ లాడ్కీ బహిన్ యోజన","মাঝি লাডকি বহিন যোজনা"
"Maharashtra","Health","Mahatma Phule Jan Arogya Yojana","महात्मा फुले जन आरोग्य योजना","महात्मा फुले जन आरोग्य योजना","மகாத்மா பூலே ஜன் ஆரோக்கிய யோஜனா","మహాత్మా ఫులే జన ఆరోగ్య యోజన","মহাত্মা ফুলে জন আরোগ্য যোজনা"
"Maharashtra","Business","CMEGP Maharashtra","मुख्यमंत्री रोजगार सृजन कार्यक्रम","मुख्यमंत्री रोजगार निर्मिती कार्यक्रम","முதலமைச்சர் வேலைவாய்ப்பு உருவாக்கம்","ముఖ్యమంత్రి ఉపాధి కల్పన","মুখ্যমন্ত্রী কর্মসংস্থান সৃষ্টি"
"Maharashtra","Student","Dr. Punjabrao Deshmukh Hostel","डॉ. पंजाबराव देशमुख वसतिगृह","डॉ. पंजाबराव देशमुख वसतिगृह","டாக்டர் பஞ்சாப்ராவ் தேஷ்முக் விடுதி","డాక్టర్ పంజాబ్‌రావ్ దేశ్‌ముఖ్ హాస్టల్","ডাঃ পাঞ্জাবরাও দেশমুখ হোস্টেল"
"Maharashtra","Student","Swadhar Yojana","स्वाधार योजना","स्वाधार योजना","சுவாதார் யோஜனா","స్వాధార్ యోజన","স্বাধার যোজনা"
"Maharashtra","Farmer","Magel Tyala Shet Tale","मागेल त्याला शेततळे","मागेल त्याला शेततळे","மாகேல் தியாலா ஷெட் தாலே","మాగేల్ త్యాలా షెట్ తలే","মাগেল ত্যালা শেত তালে"
"Maharashtra","Farmer","Nanaji Deshmukh Krishi Sanjivani","नानाजी देशमुख कृषि संजीवनी","नानाजी देशमुख कृषी संजीवनी","நாநாஜி தேஷ்முக் கிரிஷி சஞ்சீவனி","నానాజీ దేశ్‌ముఖ్ కృషి సంజీవని","নানাজি দেশমুখ কৃষি সঞ্জীবনী"
"Maharashtra","Women","Asmita Yojana","अस्मिता योजना","अस्मिता योजना","அஸ்மிதா யோஜனா","అస్మితా యోజన","অস্মিতা যোজনা"
"Maharashtra","Student","Savitribai Phule Scholarship","सावित्रीबाई फुले छात्रवृत्ति","सावित्रीबाई फुले शिष्यवृत्ती","சாவித்ரிபாய் புலே உதவித்தொகை","సావిత్రిబాయి ఫూలే స్కాలర్‌షిప్","সাবিত্রীবাঈ ফুলে স্কলারশিপ"
"Maharashtra","Social Security","Sanjay Gandhi Niradhar Anudan","संजय गांधी निराधार अनुदान","संजय गांधी निराधार अनुदान","சஞ்சய் காந்தி நிராதார் அனுதான்","సంజయ్ గాంధీ నిరాధార్ అనుదాన్","সঞ্জয় গান্ধী নিরাধার অনুদান"
"Maharashtra","Social Security","Shravanbal Seva Rajya Nivruttivetan","श्रवणबाल सेवा राज्य निवृत्तिवेतन","श्रवणबाळ सेवा राज्य निवृत्तीवेतन","ஷ்ரவன் பால் சேவா ஓய்வூதியம்","శ్రవణ్‌బాల్ సేవా నివృత్తి వేతనం","শ্রাবণবাল সেবা নিবৃত্তিবেতন"
"Maharashtra","Women","Navtejaswini Yojana","नवतेजस्विनी योजना","नवतेजस्विनी योजना","நவதேஜஸ்வினி யோஜனா","నవతేజస్విని యోజన","নবতেজস্বিনী যোজনা"
"Maharashtra","Farmer","Gopinath Munde Shetkari Suraksha","गोपीनाथ मुंडे शेतकरी सुरक्षा","गोपीनाथ मुंडे शेतकरी सुरक्षा","கோபிநாத் முண்டே விவசாய பாதுகாப்பு","గోపీనాథ్ ముండే షెట్కారీ సురక్ష","গোপীনাথ মুন্ডে শেতকারি সুরক্ষা"
"Maharashtra","Infrastructure","Jalyukt Shivar Abhiyan","जलयुक्त शिवार अभियान","जलयुक्त शिवार अभियान","ஜல்யுக்த் ஷிவார் அபியான்","జలయుక్త్ శివార్ అభియాన్","জলযুক্ত শিবার অভিযান"
"Maharashtra","Farmer","Mukhymantri Krishi Sanjivani","मुख्यमंत्री कृषि संजीवनी","मुख्यमंत्री कृषी संजीवनी","முதலமைச்சர் கிரிஷி சஞ்சீவனி","ముఖ్యమంత్రి కృషి సంజీవని","মুখ্যমন্ত্রী কৃষি সঞ্জীবনী"
"Maharashtra","Student","Rajarshi Shahu Shikshan Shulk","राजर्षि शाहू शिक्षण शुल्क","राजर्षी शाहू शिक्षण शुल्क","ராஜரிஷி ஷாகு கல்வி உதவித்தொகை","రాజర్షి షాహు శిక్షణ శుల్క","राजর্ষি শাহু শিক্ষণ শুল্ক"
"Maharashtra","Farmer","Sharad Pawar Gram Samridhi","शरद पवार ग्राम समृद्धि","शरद पवार ग्राम समृद्धी","சரத் பவார் கிராம சம்ரிதி","శరద్ పవార్ గ్రామ సమృద్ధి","শরদ पওয়ার গ্রাম সমৃদ্ধি"
"Maharashtra","Business","Pramod Mahajan Skill Development","प्रमोद महाजन कौशल विकास","प्रमोद महाजन कौशल्य विकास","பிரமோத் மகாஜன் திறன் மேம்பாடு","ప్రమోద్ మహాజన్ నైపుణ్యాభివృద్ధి","প্রমোদ মহাজন দক্ষতা উন্নয়ন"
"Maharashtra","Farmer","Bhausaheb Fundkar Horticulture","भाऊसाहेब फुंडकर फळबाग लागवड","भाऊसाहेब फुंडकर फळबाग लागवड","பௌசாஹேப் புண்ட்கர் தோட்டக்கலை","భౌసాహెబ్ ఫుండ్కర్ హార్టికల్చర్","ভাউসাহেব ফুন্ডকার উদ্যানপালন"
"Maharashtra","Women","Majhi Kanya Bhagyashree","माझी कन्या भाग्यश्री","माझी कन्या भाग्यश्री","மாஜி கன்யா பாக்யஸ்ரீ","మాఝీ కన్యా భాగ్యశ్రీ","মাঝি কন্যা ভাগ্যশ্রী"
"West Bengal","Women","Lakshmir Bhandar","लक्ष्मी भंडार","लक्ष्मी भंडार","லட்சுமி பண்டார்","లక్ష్మీర్ భండార్","লক্ষ্মীর ভাণ্ডার"
"West Bengal","Farmer","Krishak Bandhu","कृषक बंधु","कृषक बंधू","கிரிஷக் பந்து","కృషక్ బంధু","কৃষক বন্ধু"
"West Bengal","Student","Kanyashree Prakalpa","कन्याश्री प्रकल्प","कन्याश्री प्रकल्प","கன்யாஸ்ரீ பிரகல்பம்","కన్యాశ্রি ప్రకల్ప","কন্যাশ্রী প্রকল্প"
"West Bengal","Health","Swasthya Sathi","स्वास्थ्य साथी","स्वास्थ्य साथी","சுவஸ்தியா சாதி","స్వస్థ్య సాథి","স্বাস্থ্য সাথী"
"West Bengal","Student","Sabooj Sathi","सबूज साथी","सबूज साथी","சபூஜ் சாதி","సబూజ్ సాథి","সবুজ সাথী"
"West Bengal","Women","Rupashree Prakalpa","रूपश्री प्रकल्प","रूपश्री प्रकल्प","ரூபஸ்ரீ பிரகல்பம்","రూపశ్రీ ప్రకల్ప","রূপশ্রী প্রকল্প"
"West Bengal","Student","WB Student Credit Card","पश्चिम बंगाल छात्र क्रेडिट कार्ड","पश्चिम बंगाल विद्यार्थी क्रेडिट कार्ड","மேற்கு வங்க மாணவர் கிரெடிட் கார்டு","పశ్చిమ బెঙ্গాల్ స్టూడెంట్ క్రెడిট కార్ড","পশ্চিমবঙ্গ স্টুডেন্ট ক্রেডিট কার্ড"
"West Bengal","Youth","Yuvashree","युवाश्री","युवाश्री","யுவஸ்ரீ","యువశ్రీ","যুবশ্রী"
"West Bengal","Employment","Gatidhara","गतिधारा","गतिधारा","கதிதாரா","గతిధార","গতিধারা"
"West Bengal","Food Security","Khadya Sathi","खाद्य साथी","खाद्य साथी","காதிய சாதி","ఖాద్య సాথি","খাদ্য সাথী"
"West Bengal","Student","Sikshashree","शिक्षाश्री","शिक्षाश्री","சிக்ஷாஸ்ரீ","శిక్షాశ్రీ","শিক্ষাশ্রী"
"West Bengal","Social Security","Jai Bangla Pension","जय बांग्ला पेंशन","जय बांग्ला पेन्शन","ஜெய் பங்களா ஓய்வூதியம்","జై బంగ్లా పెన్షన్","জয় বাংলা পেনশন"
"West Bengal","Youth","Utkarsh Bangla","उत्कर्ष बांग्ला","उत्कर्ष बांग्ला","உத்கர்ஷ் பங்களா","ఉత్కర్ష బంగ్లా","উৎকর্ষ বাংলা"
"West Bengal","Women","Jagago Scheme","जगागो योजना","जगागो योजना","ஜாகாகோ திட்டம்","జగాగో పథకం","জাগো প্রকল্প"
"West Bengal","Farmer","Matir Srishti","मातिर सृष्टि","मातिर सृष्टी","மாதிர் சிருஷ்டி","మాటిర్ సృష్టి","মাটির সৃষ্টি"
"West Bengal","Student","Aikyashree","ऐक्यश्री","ऐक्यश्री","ஐக்யஸ்ரீ","ఐక్యశ్రీ","ঐক্যশ্রী"
"West Bengal","Housing","Geetanjali Housing","गीतांजलि आवास","गीतांजली आवास","கீதாஞ்சலி வீட்டு வசதி","గీతాంజలి హౌసింగ్","গীতাঞ্জলি আবাসন"
"West Bengal","Artisan","Lokprasar Prakalpa","लोकप्रसार प्रकल्प","लोकप्रसार प्रकल्प","லோக் பிரசாத் பிரகல்பம்","లోక్ ప్రసార్ ప్రకల్ప","লোকপ্রসার প্রকল্প"
"West Bengal","Women","Swayangsiddha","स्वयं सिद्धा","स्वयं सिद्धा","சுயம் சித்தா","స్వయం సిద్ధ","স্বয়ংসিদ্ধা"
"West Bengal","Farmer","Jal Dharo Jal Bharo","जल धरो जल भरो","जल धरो जल भरो","ஜல் தாரோ ஜல் பாரோ","జல் ధరో జల్ భరో","জল ধরো জল ভরো"
"Tamil Nadu","Women","Pudhumai Penn Scheme","पुधुमै पेन योजना","पुधुमै पेन योजना","புதுமைப் பெண் திட்டம்","పుదుమై పెన్ పథకం","পুধুমাই পেন প্রকল্প"
"Tamil Nadu","Student","CM Breakfast Scheme","मुख्यमंत्री नाश्ता योजना","मुख्यमंत्री नाश्ता योजना","முதலமைச்சர் காலை உணவுத் திட்டம்","ముఖ్యమంత్రి అల్పాహార పథకం","মুখ্যমন্ত্রী প্রাতঃরাশ প্রকল্প"
"Tamil Nadu","Women","Magalir Urimai Thogai","मगलिर उरिमई थोगाई","मगलिर उरिमई थोगाई","மகளிர் உரிமைத் தொகை","మగలిర్ ఉరిమై తొగై","মাগালির উরিমা ই থোগাই"
"Tamil Nadu","Youth","Naan Mudhalvan","नान मुधलवन","नान मुधलवन","நான் முதல்வன்","నాన్ ముదల్వన్","নান মুধলবন"
"Tamil Nadu","Health","CMCHIS Insurance","मुख्यमंत्री स्वास्थ्य बीमा","मुख्यमंत्री आरोग्य विमा","முதலமைச்சரின் விரிவான மருத்துவக் காப்பீட்டுத் திட்டம்","ముఖ్యమంత్రి సమగ్ర ఆరోగ్య బీమా","মুখ্যমন্ত্রী স্বাস্থ্য বিমা"
"Tamil Nadu","Student","Illam Thedi Kalvi","इल्लम थेडी कल्वि","इल्लम थेडी कल्वि","இல்லம் தேடிக் கல்வி","ఇల్లం థేడి కల్వి","ইল্লাম থেডি কালভি"
"Tamil Nadu","Health","Makkalai Thedi Maruthuvam","मक्कलई थेडी मरुथुवम","मक्कलई थेडी मरुथुवम","மக்களைத் தேடி மருத்துவம்","మక్కలై థేడి మరుతువం","মাক্কালাই থেডি মারুথুবাম"
"Tamil Nadu","Student","Moovalur Ramamirtham Assurance","मूवलूर रामामृतम आश्वासन","मूवलूर रामामृतम आश्वासन","மூவலூர் ராமாமிர்தம் உயர்கல்வி உறுதித் திட்டம்","మూవలూరు రామామృతం హామీ పథకం","মুভালুর রামামৃতম আশ্বাস"
"Tamil Nadu","Student","Tamil Pudhalvan Scheme","तमिल पुधलवन योजना","तमिळ पुधलवन योजना","தமிழ்ப் புதல்வன் திட்டம்","తమిళ పుదల్వన్ పథకం","তামিল পুধলবন প্রকল্প"
"Tamil Nadu","Youth","UYEGP Employment","युवा रोजगार कार्यक्रम","युवा रोजगार कार्यक्रम","வேலையற்ற இளைஞர்களுக்கான வேலைவாய்ப்பு உருவாக்கும் திட்டம்","నిరుద్యోగ యువత ఉపాధి కల్పన","বেকার যুবক কর্মসংস্থান"
"Tamil Nadu","Women","Marriage Assistance Scheme","विवाह सहायता योजना","विवाह सहायता योजना","திருமண உதவித் திட்டம்","వివాహ సహాయ పథకం","বিবাহ সহায়তা প্রকল্প"
"Tamil Nadu","Business","NEEDS Scheme","नीड्स योजना","नीड्स योजना","நீட்ஸ் திட்டம்","నీడ్స్ పథకం","নিডস প্রকল্প"
"Tamil Nadu","Farmer","Uzhavar Santhai","उझावर संथाई","उझावर संथाई","உழவர் சந்தை","ఉళవర్ సంత","উঝাভার সান্থাই"
"Tamil Nadu","Social Security","OAP Pension TN","वृद्धावस्था पेंशन","वृद्धापकाळ पेन्शन","முதியோர் ஓய்வூதியத் திட்டம்","వృద్ధాప్య పెన్షన్","বার্ধক্য পেনশন"
"Tamil Nadu","Energy","Solar Rooftop Incentive","सौर छत प्रोत्साहन","सौर छत प्रोत्साहन","சூரிய மேற்கூரை ஊக்கத் திட்டம்","సోలార్ రూఫ్‌టాప్ ప్రోత్సాహకం","সৌর ছাদ উৎসাহ"
"Uttar Pradesh","Women","Kanya Sumangala Yojana","कन्या सुमंगला योजना","कन्या सुमंगला योजना","கன்யா சுமங்கலா யோஜனா","కన్యా సుమంగళ యోజన","কন্যা সুমঙ্গলা যোজনা"
"Uttar Pradesh","Student","Abhyuday Yojana","अभ्युदय योजना","अभ्युदय योजना","அப்யுதய யோஜனா","అభ్యుదయ యోజన","অভ্যুদয় যোজনা"
"Uttar Pradesh","Farmer","Kisan Sarvahit Bima","किसान सर्वहित बीमा","शेतकरी सर्वहित विमा","கிசான் சர்வஹித் பீமா","కిసాన్ సర్వహిత్ బీమా","কিষাণ সর্বহিত বিমা"
"Uttar Pradesh","Women","Bhagya Laxmi Yojana","भाग्य लक्ष्मी योजना","भाग्य लक्ष्मी योजना","பாக்ய லட்சுமி யோஜனா","భాగ్య లక్ష్మి యోజన","ভাগ্য লক্ষ্মী যোজনা"
"Uttar Pradesh","Women","BC Sakthi Scheme","बीसी सखी योजना","बीसी सखी योजना","பிசி சக்தி திட்டம்","బీసీ சக்தி పథకం","বিসি শক্তি প্রকল্প"
"Uttar Pradesh","Business","Vishwakarma Shram Samman","विश्वकर्मा श्रम सम्मान","विश्वकर्मा श्रम सन्मान","விஸ்வகர்மா ஷ்ரம் சம்மான்","విశ్వకర్మ శ్రమ సమ్మాన్","বিশ্বকর্মা শ্রম সম্মান"
"Uttar Pradesh","Women","Pankh Yojana","पंख योजना","पंख योजना","பங்க் யோஜனா","పంఖ్ యోజన","পঙ্খ যোজনা"
"Uttar Pradesh","Student","UP Scholarship Scheme","यूपी छात्रवृत्ति","यूपी शिष्यवृत्ती","உபி உதவித்தொகை","యూపీ స్కాలర్‌షిప్ పథకం","ইউপি স্কলারশিপ"
"Uttar Pradesh","Student","Kanya Vidya Dhan","कन्या विद्या धन","कन्या विद्या धन","கன்யா வித்யா தன்","కన్యా విద్యా ధన్","কন্যা বিদ্যা ধন"
"Uttar Pradesh","Women","UP Shadi Anudan","शादी अनुदान योजना","लग्न अनुदान योजना","திருமண உதவித் திட்டம்","వివాహ సహాయ పథకం","বিবাহ অনুদান"
"Uttar Pradesh","Farmer","UP Free Boring Scheme","नि:शुल्क बोरिंग योजना","मोफत बोअरिंग योजना","இலவச போர்வெல் திட்டம்","ఉచిత బోరింగ్ పథకం","বিনামূল্যে বোরিং প্রকল্প"
"Uttar Pradesh","Social Security","UP Widow Pension","विधवा पेंशन","विधवा पेन्शन","விதவை ஓய்வூதியம்","విధవ పెన్షన్","বিধবা পেনশন"
"Uttar Pradesh","Farmer","UP Khet Talab Yojana","खेत तालाब योजना","शेत तलाव योजना","கேட் தலாப் யோஜனா","ఖేత్ తలాబ్ యోజన","ক্ষেত তালাব যোজনা"
"Uttar Pradesh","Healthcare","UP Jan Arogya Yojana","जन आरोग्य योजना","जन आरोग्य योजना","ஜன் ஆரோக்கிய யோஜனா","జన ఆరోగ్య యోజన","জন আরোগ্য যোজনা"
"Uttar Pradesh","Social Security","UP Divyang Pension","दिव्यांग पेंशन","दिव्यांग पेन्शन","மாற்றுத்திறனாளி ஓய்வூதியம்","దివ్యాంగుల పెన్షన్","প্রতিবন্ধী পেনশন"
"Telangana","Farmer","Rythu Bharosa","रैथु भरोसा","रैथु भरोसा","ரைத்து பரோசா","రైతు భరోసా","রাইথু ভরসা"
"Telangana","Women","Maha Lakshmi Scheme","महालक्ष्मी योजना","महालक्ष्मी योजना","மகாலட்சுமி திட்டம்","మహాలక్ష్మి పథకం","మহা লক্ষ্মী যোজনা"
"Telangana","Energy","Gruha Jyothi Telangana","गृह ज्योति","गृह ज्योती","கிருஹ ஜோதி","గృహ జ్యోతి","গৃহ জ্যোতি"
"Telangana","Health","Rajiv Arogyasri","राजीव आरोग्यश्री","राजीव आरोग्यश्री","ராஜீவ் ஆரோக்கியஸ்ரீ","రాజీవ్ ఆరోగ్యశ్రీ","রাজীব আরোগ্যশ্রী"
"Telangana","Social Security","Cheyutha Pension","चेयुथा पेंशन","चेयुथा पेन्शन","செய்யுதா ஓய்வூதியம்","చేయూత పెన్షన్","চেয়ুথা পেনশন"
"Telangana","Housing","Indiramma Indlu","इंदिरम्मा इंदलू","इंदिरम्मा इंदलू","இந்திரம்மா இண்ட்லு","ఇందిరమ్మ ఇండ్లు","ইন্দিরাম্মা ইন্দলু"
"Telangana","Women","Kalyana Lakshmi","कल्याण लक्ष्मी","कल्याण लक्ष्मी","கல்யாண லட்சுமி","కళ్యాణ లక్ష్మి","কল্যাণ লক্ষ্মী"
"Telangana","Business","Dalit Bandhu","दलित बंधु","दलित बंधू","தலித் பந்து","దళిత బంధు","দলিত বন্ধু"
"Telangana","Health","KCR Kit","केसीआर किट","केसीआर किट","கேசிஆர் கிட்","కేసీఆర్ కిట్","কেসিআর কিট"
"Telangana","Farmer","Rythu Bima","रैथु बीमा","रैथु विमा","ரைத்து பீமா","రైతు బీమా","রাইথু బిమా"
"Telangana","Education","Mana Ooru Mana Badi","मन ऊरु मन बड़ी","मन ऊरु मन बड़ी","மனா ஊரு மனா பாடி","మన ఊరు మన బడి","মানা ঊরু মানা বাড়ি"
"Telangana","Youth","Rajiv Yuva Vikasam","राजीव युवा विकासम","राजीव युवा विकासम","ராஜீவ் யுவ விகாசம்","రాజీవ్ యువ వికాసం","রাজীব যুব বিকাশম"
"Telangana","Women","Arogya Lakshmi","आरोग्य लक्ष्मी","आरोग्य लक्ष्मी","ஆரோக்கிய லட்சுமி","ఆరోగ్య లక్ష్మి","আরোগ্য লক্ষ্মী"
"Telangana","Social Security","Aasara Pension","आसरा पेंशन","आसरा पेन्शन","ஆசரா ஓய்வூதியம்","ఆసరా పెన్షన్","আাসরা পেনশন"
"Telangana","Farmer","Rythu Bandhu","रैथु बंधु","रैथु बंधू","ரைத்து பந்து","రైతు బంధు","রাইথু বন্ধু"
"Karnataka","Women","Gruha Lakshmi Karnataka","गृह लक्ष्मी","गृह लक्ष्मी","கிருஹ லட்சுமி","గృహ లక్ష్మి","গৃহ লক্ষ্মী"
"Karnataka","Energy","Gruha Jyothi Karnataka","गृह ज्योति","गृह ज्योती","கிருஹ ஜோதி","గృహ జ్యోతి","গৃহ জ্যোতি"
"Karnataka","Women","Shakti Scheme","शक्ति योजना","शक्ती योजना","சக்தி திட்டம்","శక్తి పథకం","শক্তি प्रकल्प"
"Karnataka","Food Security","Anna Bhagya","अन्न भाग्य","अन्न भाग्य","அன்ன பாக்யா","అన్న భాగ్య","অন্ন भाग्य"
"Karnataka","Youth","Yuva Nidhi","युवा निधि","युवा निधी","யுவ நிதி","యువ నిధి","যুব নিধি"
"Karnataka","Women","Bhagyalakshmi Scheme","भाग्यलक्ष्मी योजना","भाग्यलक्ष्मी योजना","பாக்யலட்சுமி திட்டம்","భాగ్యలక్ష్మి పథకం","ভাগ্যলক্ষ্মী যোজনা"
"Karnataka","Student","Vidyasiri Scholarship","विद्यासिरी","विद्यासिरी","வித்யாசிறி","విద్యాసిరి","বিদ্যাসিরি"
"Karnataka","Farmer","Ganga Kalyana","गंगा कल्याण","गंगा कल्याण","கங்கா கல்யாணா","గంగా కళ్యాణ","গঙ্গা কল্যাণ"
"Karnataka","Women","Udyogini Scheme","उद्योगिनी योजना","उद्योगिनी योजना","உத்யோகினி திட்டம்","ఉద్యోగిని పథకం","উদ্যোগিনী যোজনা"
"Karnataka","Farmer","Krushi Aranya Protsaha","कृषि अरण्य प्रोत्साहन","कृषी अरण्य प्रोत्साहन","கிருஷி அரண்ய புரோட்சாஹா","కృషి అరణ్య ప్రోత్సాహ","কৃষি অরণ্য উৎসাহ"
"Karnataka","Student","Arivu Education Loan","अरीवू शिक्षा ऋण","अरीवू शिक्षण कर्ज","அரிவு கல்வி கடன்","అరివు విద్యా రుణం","অরিভু শিক্ষা ঋণ"
"Karnataka","Student","Prabhuddha Overseas","प्रबुद्ध विदेशी छात्रवृत्ति","प्रबुद्ध विदेशी शिष्यवृत्ती","பிரபுத்தா வெளிநாட்டு உதவித்தொகை","ప్రబుద్ధ విదేశీ స్కాలర్‌షిప్","প্রবুদ্ধ বিদেশী স্কলারশিপ"
"Karnataka","Health","Gruha Arogya Yojana","गृह आरोग्य योजना","गृह आरोग्य योजना","கிருஹ ஆரோக்கிய யோஜனா","గృహ ఆరోగ్య పథకం","গৃহ আরোগ্য যোজনা"
"Karnataka","Business","Swavalambi Sarathi","स्वावलंबी सारथी","स्वावलंबी सारथी","சுவாலம்பி சாரதி","స్వావలంబి సారథి","স্বাবলম্বী সারথি"
"Karnataka","Youth","Vrutti Protsaha","वृत्ति प्रोत्साहन","वृत्ती प्रोत्साहन","விருத்தி புரோட்சாஹா","వృత్తి ప్రోత్సాహ","বৃত্তি উৎসাহ"
"Karnataka","Women","Shramashakthi Special","श्रमशक्ति विशेष","श्रमशक्ती विशेष","ஷ்ரமசக்தி சிறப்பு திட்டம்","శ్రమశక్తి ప్రత్యేక పథకం","শ্রমশক্তি विशेष"
"Maharashtra","Farmer","Balasaheb Thackeray Accident Insurance","बालासाहेब ठाकरे दुर्घटना बीमा","बाळासाहेब ठाकरे अपघात विमा","பாலசாகேப் தாக்கரே விபத்து காப்பீடு","బాలాసాహెబ్ థాకరే ప్రమాద బీమా","বালাসাহেব ঠাকরে দুর্ঘটনা বিমা"
"Maharashtra","Infrastructure","Mukhyamantri Gram Sadak","मुख्यमंत्री ग्राम सड़क","मुख्यमंत्री ग्राम सडक","முதலமைச்சர் கிராம சாலைத் திட்டம்","ముఖ్యమంత్రి గ్రామ సడక్","মুখ্যমন্ত্রী গ্রাম সড়ক"
"West Bengal","Student","Taruner Swapno","तरुणेर स्वप्नो","तरुणेর स्वप्नो","தருணேர் ஸ்வப்னோ","తరుణేర్ స్వప్నో","তরুণের স্বপ্ন"
"West Bengal","Health","Chokher Alo","चोखेर आलो","चोखेर आलो","சோகர் அலோ","చోఖేర్ ఆలో","চোখের আলো"
"Tamil Nadu","Social Security","Kalaignar Pension","कलैग्नार पेंशन","कलैग्नार पेन्शन","கலைஞர் ஓய்வூதியத் திட்டம்","కలైజ్ఞార్ పెన్షన్","কালাইগনার পেনশন"
"Uttar Pradesh","Student","UP Laptop Vitran","लैपटॉप वितरण योजना","लॅपटॉप वितरण योजना","மடிக்கணினி விநியோகத் திட்டம்","ల్యాప్‌టాప్ పంపిణీ పథకం","ল্যাপটপ বিতরণ প্রকল্প"
"Telangana","Farmer","Rythu Vedika","रैथु वेदिका","रैथु वेदिका","ரைத்து வேதிகா","రైతు వేదిక","রাইথু বেদিকা"
"Karnataka","Farmer","Raitha Vidya Nidhi","रैथु विद्या निधि","रैथु विद्या निधी","ரைத்தா வித்யா நிதி","రైతు విద్యా నిధి","রাইথা বিদ্যা నిధి"
"Maharashtra","Women","Punyashlok Ahilyadevi Holkar","पुण्यश्लोक अहिल्यादेवी होलकर","पुण्यश्लोक अहिल्यादेवी होळकर","புண்யஸ்லோக் அகில்யாதேவி ஹோல்கர்","పుణ్యశ్లోక్ అహిల్యాదేవి హోల్కర్","পুণ্যশ্লোক অহল্যাদেবী হোলকার"
"West Bengal","Farmer","Hasir Alo","हसीर आलो","हसीर आलो","ஹசீர் அலோ","హసీర్ ఆలో","হাসির আলো"
"Tamil Nadu","Infrastructure","Namakku Naame","नमक्कु नामे","नमक्कु नामे","நமக்கு நாமே திட்டம்","నమక్కు నామే పథకం","নামাক্কু নামে"
"Uttar Pradesh","Business","UP ODOP Scheme","एक जिला एक उत्पाद","एक जिल्हा एक उत्पादन","ஒரு மாவட்டம் ஒரு தயாரிப்பு","ఒక జిల్లా ఒక ఉత్పత్తి","এক জেলা এক পণ্য"
"""

# --- TRANSLATION DICTIONARIES ---
cat_translations = {
    "Women & Child": {"hi": "महिला और बाल", "mr": "महिला आणि बालक", "ta": "பெண்கள் மற்றும் குழந்தைகள்", "te": "మహిళలు & పిల్లలు", "bn": "নারী ও শিশু"},
    "Health and wellness": {"hi": "स्वास्थ्य और कल्याण", "mr": "आरोग्य आणि कल्याण", "ta": "சுகாதாரம்", "te": "ఆరోగ్యం", "bn": "স্বাস্থ্য ও সুস্থতা"},
    "Skill & employment": {"hi": "कौशल और रोजगार", "mr": "कौशल्य आणि रोजगार", "ta": "திறன் மற்றும் வேலைவாய்ப்பு", "te": "నైపుణ్యం & ఉపాధి", "bn": "দক্ষতা ও কর্মসংস্থান"},
    "Education": {"hi": "शिक्षा", "mr": "शिक्षण", "ta": "கல்வி", "te": "విద్య", "bn": "শিক্ষা"},
    "Agriculture": {"hi": "कृषि", "mr": "कृषी", "ta": "வேளாண்மை", "te": "వ్యవసాయం", "bn": "কৃষি"},
    "Social welfare & empowerment": {"hi": "समाज कल्याण", "mr": "समाज कल्याण", "ta": "சமூக நலன்", "te": "సామాజిక సంక్షేమం", "bn": "সমাজ কল্যাণ"},
    "Housing and shelter": {"hi": "आवास और आश्रय", "mr": "निवारा आणि घर", "ta": "வீட்டு வசதி", "te": "గృహ & ఆశ్రయం", "bn": "আবাসন ও আশ্রয়"}
}

docs_translations = {
    "en": ["Aadhaar Card", "Resident Proof", "Bank Details"],
    "hi": ["आधार कार्ड", "निवास प्रमाण", "बैंक विवरण"],
    "mr": ["आधार कार्ड", "रहिवासी पुरावा", "बँक तपशील"],
    "ta": ["ஆதார் அட்டை", "இருப்பிடச் சான்று", "வங்கி விவரங்கள்"],
    "te": ["ఆధార్ కార్డ్", "నివాస రుజువు", "బ్యాంకు వివరాలు"],
    "bn": ["আধার কার্ড", "আবাসিক প্রমাণ", "ব্যাঙ্কের বিবরণ"]
}

benefit_translations = {
    "en": "Financial Assistance",
    "hi": "आर्थिक सहायता",
    "mr": "आर्थिक मदत",
    "ta": "நிதி உதவி",
    "te": "ఆర్థిక సహాయం",
    "bn": "আর্থিক সহায়তা"
}

mode_translations = {
    "en": "Online Portal",
    "hi": "ऑनलाइन पोर्टल",
    "mr": "ऑनलाइन पोर्टल",
    "ta": "ஆன்லைன் போர்டல்",
    "te": "ఆన్‌లైన్ పోర్టల్",
    "bn": "অনলাইন পোর্টাল"
}

gov_translations = {
    "en": "Official scheme provided by the government of",
    "hi": "सरकार द्वारा प्रदान की गई आधिकारिक योजना -",
    "mr": "सरकारने प्रदान केलेली अधिकृत योजना -",
    "ta": "அரசால் வழங்கப்படும் அதிகாரப்பூர்வ திட்டம் -",
    "te": "ప్రభుత్వం అందించే అధికారిక పథకం -",
    "bn": "সরকার কর্তৃক প্রদত্ত অফিসিয়াল প্রকল্প -"
}

def map_category(raw_cat):
    cat = raw_cat.strip()
    if cat in ["Women"]: return "Women & Child"
    if cat in ["Health", "Healthcare"]: return "Health and wellness"
    if cat in ["Business", "Youth", "Employment", "Artisan"]: return "Skill & employment"
    if cat in ["Student", "Education"]: return "Education"
    if cat in ["Farmer"]: return "Agriculture"
    if cat in ["Social Security"]: return "Social welfare & empowerment"
    if cat in ["Infrastructure", "Housing", "Energy"]: return "Housing and shelter"
    if cat in ["Food Security"]: return "Health and wellness"
    return "Social welfare & empowerment"

def get_icon_for_category(category):
    icons = {
        "Agriculture": "<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='var(--blue)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 2v20'></path><path d='M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6'></path></svg>",
        "Health and wellness": "<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='var(--blue)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M22 12h-4l-3 9L9 3l-3 9H2'></path></svg>",
        "Education": "<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='var(--blue)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M4 19.5A2.5 2.5 0 0 1 6.5 17H20'></path><path d='M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z'></path></svg>",
        "Women & Child": "<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='var(--blue)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'></path><circle cx='12' cy='7' r='4'></circle></svg>",
        "Skill & employment": "<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='var(--blue)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect x='2' y='7' width='20' height='14' rx='2' ry='2'></rect><path d='M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16'></path></svg>",
        "Housing and shelter": "<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='var(--blue)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'></path><polyline points='9 22 9 12 15 12 15 22'></polyline></svg>",
        "Social welfare & empowerment": "<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='var(--blue)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'></circle><circle cx='12' cy='12' r='6'></circle><circle cx='12' cy='12' r='2'></circle></svg>"
    }
    return icons.get(category, icons["Social welfare & empowerment"])

def get_arrays_for_category(category):
    arrays = {
        "gender": ["male", "female", "other"],
        "age": ["below18", "18-40", "40-60", "60+"],
        "income": ["below1L", "1-3L", "3-8L", "above8L"],
        "occupation": ["farmer", "student", "labor", "business", "govt"],
        "location": ["rural", "semi", "urban"]
    }
    if category == "Women & Child": arrays["gender"] = ["female"]
    elif category == "Education": 
        arrays["age"] = ["below18", "18-40"]
        arrays["occupation"] = ["student"]
    elif category == "Agriculture":
        arrays["occupation"] = ["farmer"]
        arrays["location"] = ["rural", "semi"]
    elif category == "Skill & employment":
        arrays["age"] = ["18-40", "40-60"]
        arrays["occupation"] = ["student", "labor", "business"]
    elif category == "Housing and shelter":
        arrays["income"] = ["below1L", "1-3L"]
    return arrays
def upload_data():
    collection_name = "SchemeMultilingual" 
    print(f"Starting bulk upload to '{collection_name}'...")
    
    reader = csv.DictReader(io.StringIO(csv_data.strip()))
    
    # --- SMART LINK DICTIONARY ---
    # Add any exact links you know here. 
    known_links = {
        "Majhi Ladki Bahin Yojana": "https://ladkibahin.maharashtra.gov.in/",
        "Mahatma Phule Jan Arogya Yojana": "https://www.jeevandayee.gov.in/",
        "Lakshmir Bhandar": "https://socialsecurity.wb.gov.in/",
        "Krishak Bandhu": "https://krishakbandhu.net/",
        "Kanyashree Prakalpa": "https://www.wbkanyashree.gov.in/",
        "Pudhumai Penn Scheme": "https://www.pudhumaipenn.tn.gov.in/",
        "Kanya Sumangala Yojana": "https://mksy.up.gov.in/",
        "Gruha Lakshmi Karnataka": "https://sevasindhugs.karnataka.gov.in/"
    }
    
    count = 0
    for row in reader:
        state = row['State']
        raw_cat = row['Category']
        name_en = row['Scheme Name (EN)']
        
        app_category = map_category(raw_cat)
        icon = get_icon_for_category(app_category)
        arrays = get_arrays_for_category(app_category)
        
        cat_hi = cat_translations[app_category]["hi"]
        cat_mr = cat_translations[app_category]["mr"]
        cat_ta = cat_translations[app_category]["ta"]
        cat_te = cat_translations[app_category]["te"]
        cat_bn = cat_translations[app_category]["bn"]

        # --- THE FIX: DYNAMIC LINK GENERATOR ---
        # If the exact link is in our dictionary, use it.
        # Otherwise, generate a direct Google Search for the official portal!
        search_query = f"{name_en.replace(' ', '+')}+{state.replace(' ', '+')}+official+website+apply"
        smart_link = known_links.get(name_en, f"https://www.google.com/search?q={search_query}")
        
        scheme_doc = {
            "category": app_category,
            "icon": icon,
            "link": smart_link,  # <--- UPDATED FIELD
            
            "gender": arrays["gender"],
            "age": arrays["age"],
            "income": arrays["income"],
            "occupation": arrays["occupation"],
            "location": arrays["location"],
            
            "name_en": name_en,
            "name_hi": row['Scheme Name (HI)'],
            "name_mr": row['Scheme Name (MR)'],
            "name_ta": row['Scheme Name (TA)'],
            "name_te": row['Scheme Name (TE)'],
            "name_bn": row['Scheme Name (BN)'],
            
            "desc_en": f"{gov_translations['en']} {state}. Category: {app_category}.",
            "desc_hi": f"{state} {gov_translations['hi']} {cat_hi}।",
            "desc_mr": f"{state} {gov_translations['mr']} {cat_mr}.",
            "desc_ta": f"{state} {gov_translations['ta']} {cat_ta}.",
            "desc_te": f"{state} {gov_translations['te']} {cat_te}.",
            "desc_bn": f"{state} {gov_translations['bn']} {cat_bn}।",
            
            "ministry_en": f"State Govt of {state}",
            "ministry_hi": f"{state} राज्य सरकार",
            "ministry_mr": f"{state} राज्य सरकार",
            "ministry_ta": f"{state} மாநில அரசு",
            "ministry_te": f"{state} రాష్ట్ర ప్రభుత్వం",
            "ministry_bn": f"{state} রাজ্য সরকার",
            
            "documents_en": docs_translations["en"],
            "documents_hi": docs_translations["hi"],
            "documents_mr": docs_translations["mr"],
            "documents_ta": docs_translations["ta"],
            "documents_te": docs_translations["te"],
            "documents_bn": docs_translations["bn"],

            "benefit_en": benefit_translations["en"],
            "benefit_hi": benefit_translations["hi"],
            "benefit_mr": benefit_translations["mr"],
            "benefit_ta": benefit_translations["ta"],
            "benefit_te": benefit_translations["te"],
            "benefit_bn": benefit_translations["bn"],

            "mode_en": mode_translations["en"],
            "mode_hi": mode_translations["hi"],
            "mode_mr": mode_translations["mr"],
            "mode_ta": mode_translations["ta"],
            "mode_te": mode_translations["te"],
            "mode_bn": mode_translations["bn"],
            
            "states_en": state,
            "states_hi": state,
            "states_mr": state,
            "states_ta": state,
            "states_te": state,
            "states_bn": state,
            
            "eligibility_summary_en": f"Residents of {state} qualifying under the {app_category} sector.",
            "eligibility_summary_hi": f"{state} के निवासी जो {cat_hi} क्षेत्र के अंतर्गत आते हैं।",
            "eligibility_summary_mr": f"{state} चे रहिवासी जे {cat_mr} क्षेत्रांतर्गत येतात.",
            "eligibility_summary_ta": f"{cat_ta} துறையின் கீழ் தகுதி பெறும் {state} குடியிருப்பாளர்கள்.",
            "eligibility_summary_te": f"{cat_te} రంగం కింద అర్హత పొందిన {state} నివాసితులు.",
            "eligibility_summary_bn": f"{state} এর বাসিন্দা যারা {cat_bn} খাতের অধীনে যোগ্য।",

            "beneficiary_en": f"Eligible {app_category} Beneficiaries",
            "beneficiary_hi": f"पात्र {cat_hi} लाभार्थी",
            "beneficiary_mr": f"पात्र {cat_mr} लाभार्थी",
            "beneficiary_ta": f"தகுதியான {cat_ta} பயனாளிகள்",
            "beneficiary_te": f"అర్హులైన {cat_te} లబ్ధిదారులు",
            "beneficiary_bn": f"যোগ্য {cat_bn} সুবিধাভোগী"
        }
        
        doc_id = name_en.lower().replace(" ", "-").replace("/", "-").replace("(", "").replace(")", "")
        
        db.collection(collection_name).document(doc_id).set(scheme_doc)
        print(f"Uploaded: {name_en} | Link: {smart_link}")
        count += 1

    print(f"\n Successfully auto-formatted and overwritten {count} schemes to Firestore!")

if __name__ == "__main__":
    upload_data()