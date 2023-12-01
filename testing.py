import spacy
from spacy.tokens import Token
from spacy.lang.ar import Arabic


Token.set_extension("gap", default="")


def arb_gap(token):
    tlen = len(token.text)
    if tlen < 2 or token.pos_ == 'PROPN':
        return 0  #skip this token
    return (tlen//2) + (tlen%2)

def chn_gap(token):
    tlen = len(token.text)
    if tlen < 2 or token.pos_ == 'PROPN':
        return 0  #skip this token
    return (tlen//2) + (tlen%2)

def eng_gap(token):
    tlen = len(token.text)
    if  tlen < 2 or token.pos_ == 'PROPN':
        return 0  #skip this token
    return (tlen//2) + (tlen%2)

def kor_gap(token):
    """ gaping is based on finding suffixes in each word then determining the 
        breakpoint based on ignoring the suffix portion."""
    tlen = len(token.text)
    if tlen < 2 or token.pos_ == 'PROPN':
        return 0  #skip this token
    # Get lexical info
    t = token.tag_
    p = token.pos_
    l = token.lemma_
    print(f'{token.text:{12}} {l:<{12}} {t:{12}} {p:{12}}')

    suffix_idx = l.find('+') # locate the suffix boundary from lemmatizer

    if suffix_idx:
        rlen = len(l[:suffix_idx])
        particle = token.text[suffix_idx:] #Todo: return this to caller to treat particle as next word
        return (rlen//2) + (rlen%2)
    return (tlen//2) + (tlen%2)

def por_gap(token):
    tlen = len(token.text)
    if tlen < 3 or token.pos_ == 'PROPN':
        return 0
    return (tlen//2) + (tlen%2)

def per_gap(token):
    pass

def rus_gap(token):
    tlen = len(token.text)
    if token.pos_ == 'PROPN':
        return 0  #skip this token
    return (tlen//2) + (tlen%2)

def get_start_index(doc):
    st = [i for i in doc.sents][1]
    return st[0].i

def strip_puncuation(doc):
    tokens = []
    for token in doc:
        if not token.is_punct:
            tokens.append(token)
    return tokens

def doc_data_dump(doc):
    print(f'{"I":{3}} {"TOKEN":{4}} {"LEMMA":{4}} {"TAG":{4}} {"POS":{4}}')
    for token in doc:
        print(f'{token.i:{3}} {token.text:{4}} {token.lemma_:{4}} {token.tag_:{4}} {token.pos_:{4}} {len(token.text):{4}}')

def doc_print_ctest(doc):
    s = ''
    for token in doc:
        if token._.gap:
            s = s + token._.gap + token.whitespace_
        else:
            s = s + token.text + token.whitespace_
    return s   

def base_test(doc, gap):
    start = get_start_index(doc)
    tokens = strip_puncuation(doc[start:])
    for pos, token in enumerate(tokens):
        if pos % 2:
            cut = gap(token)
            if cut:
                token._.gap = token.text[:cut] + '*' + token.text[cut:] + '*'


if __name__ == '__main__':

    # nlp = spacy.load("ko_core_news_lg")
    # doc = nlp("엄마는 학교 영어 선생님이다. 그리고 아버지는 일해요 은행에서.") # Mother is a school English teacher. and father works at a bank.
    
    # nlp = spacy.load("ko_core_news_lg")
    # doc = nlp("백화점에서") # At the department store.

    # nlp = spacy.load("ko_core_news_lg")
    # doc = nlp("의료 보험 혜택 개선을 위한 노력이 본격화되고 있습니다. 정부는 최근 의료 서비스에 대한 보다 포괄적이고 접근 가능한 보험 혜택을 제공하기 위해 새로운 정책을 발표했습니다. 새로운 제도는 보다 많은 국민들이 안정적이고 효과적인 의료 서비스를 받을 수 있도록 설계되었습니다.") 
    
    # nlp = spacy.load("ko_core_news_lg")
    # doc = nlp("기후 변화는 점점 더 중요한 문제로 부각되고 있습니다. 지구 온난화로 인한 극단적인 날씨 변화와 환경 파괴는 우리의 삶에 직접적인 영향을 미치고 있습니다. 정부와 시민들은 온실가스 감소와 재생에너지 사용을 통해 해결책을 모색하고 있습니다. 뿐만 아니라 우리 각자가 에너지 소비를 줄이고 재활용을 증가시키는 등의 작은 노력을 통해 이 문제에 대처할 수 있습니다. 모두가 협력하여 지구 환경을 보호하는 데 기여하면서 미래 세대를 위해 더 지속 가능한 미래를 구축하는 것이 중요합니다.") 

    # nlp = spacy.load("pt_core_news_lg")
    # doc = nlp("Esforços significativos estão sendo direcionados para a melhoria dos benefícios de seguros de saúde no país. Recentemente, o governo anunciou novas políticas com o objetivo de proporcionar benefícios de seguro de saúde mais abrangentes e acessíveis para os cidadãos. Essa mudança visa garantir que mais pessoas tenham acesso a serviços de saúde estáveis e eficazes.")

    # nlp = spacy.blank('ar')
    # nlp.add_pipe('sentencizer')
    # doc = nlp("وفي البلدان الناطقة باللغة العربية، تتألق كرة القدم بمكانة خاصة وشعبية لا مثيل لها. تعتبر هذه اللعبة الرياضية لغة مشتركة تربط بين الناس، بغض النظر عن ثقافاتهم. يعكس هذا الاهتمام الواسع جدًا بالرياضات الشعبية قدرة الكرة الطائرة على تجاوز الحدود وتوحيد المجتمعات. ويشهد المشهد الرياضي في هذه الدول حماسا مستمرا وولاء جماهيريا، حيث يعتبر اللاعبون والفرق أبطالا يلهمون الأجيال الشابة، كما تعتبر المباريات مناسبات اجتماعية تحيي الروح الوطنية وتعزز التكافل الاجتماعي. في كل شارع وحي، تجتمع العائلات والأصدقاء لمشاهدة هذه المباريات التي لديها القدرة على خلق تجارب لا تنسى وترسيخ كرة القدم كلغة مشتركة في قلوب الناس.")
    
    # nlp = spacy.load("ru_core_news_lg")
    # doc = nlp("В России футбол продолжает удерживать титул самого популярного и любимого видa спорта. Миллионы российских болельщиков ежедневно следят за матчами как в национальных, так и в мировых лигах. Футбольные стадионы наполняются атмосферой страсти и восторга, когда команды сражаются за победу. Премьер-лига России привлекает внимание своей конкурентоспособностью и выдающимися моментами на поле. Сборная России также поддерживает фанатская страсть, особенно во время международных турниров. Футбол стал неотъемлемой частью культуры страны, объединяя людей разных возрастов и социальных групп в общей любви к этому великому спорту.")

    # nlp = spacy.load("zh_core_web_lg")
    # doc = nlp("在中国，篮球非常受欢迎，是最受小学生们喜爱的运动之一。许多小朋友都喜欢观看国内和国际的篮球比赛，看他们的英雄在球场上比赛。学校和社区也经常组织篮球活动，让小朋友们可以一起打篮球，学到更多的篮球技巧。有一些很厉害的篮球明星，像姚明和周琦，他们的故事也让小朋友们更喜欢篮球。所以，篮球已经成为中国小学生们生活中很重要的一部分，大家都热爱这个有趣的运动！")

    nlp = spacy.load("en_core_web_sm")
    doc = nlp("Climate change is a big problem. The Earth is getting warmer. This is bad for people, animals, and nature. Too much pollution is causing this. We must do something. Use less energy, plant more trees. Governments should help. Everyone can make a difference. Let's work together to stop climate change and save our planet.")

    base_test(doc, eng_gap)
    print('\n', doc, '\n\n')
    print(doc_print_ctest(doc))