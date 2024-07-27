import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from flask_socketio import emit

# Links para las materias
history_links = [
    "https://www.history.com/", "https://www.nationalgeographic.com/history",
    "https://www.bbc.co.uk/history", "https://www.historytoday.com/",
    "https://www.historyextra.com/", "https://www.ancient.eu/",
    "https://www.smithsonianmag.com/history", "https://www.britannica.com/topic/history",
    "https://www.biography.com/history", "https://www.historyhit.com/",
    "https://www.pbs.org/history", "https://www.archaeology.org/",
    "https://www.revolutionary-war.net/", "https://www.civilwar.org/",
    "https://www.historynet.com/", "https://www.timemaps.com/",
    "https://www.worldhistory.org/", "https://www.nationalarchives.gov.uk/education/",
    "https://www.livescience.com/history", "https://www.washingtonpost.com/history/",
    "https://www.historylearningsite.co.uk/", "https://www.historic-uk.com/",
    "https://www.historyworld.net/",
    "https://www.historyplace.com/", "https://www.historyofwar.org/",
    "https://www.localhistories.org/", "https://www.bbc.co.uk/timelines/z8br87h",
    "https://www.schoolhistory.co.uk/", "https://www.historycentral.com/",
    "https://www.historyforkids.net/", "https://www.ducksters.com/history/",
    "https://www.britishmuseum.org/learn/schools",
    "https://www.ushistory.org/", "https://www.historyonthenet.com/",
    "https://www.historyisfun.org/", "https://www.military.com/history",
    "https://www.battlefields.org/learn/articles/civil-war-history",
    "https://www.reenact.com/history/", "https://www.thelatinlibrary.com/",
    "https://www.famousbirthdays.com/history.html", "https://www.museumnext.com/article/top-20-museums-around-world/",
    "https://www.metmuseum.org/toah/chronology/", "https://www.british-history.ac.uk/",
    "https://www.history.ac.uk/", "https://www.londonmet.ac.uk/research/centres-groups-and-units/museum-of-london-archaeology/",
    "https://www.vam.ac.uk/info/learning", "https://www.nationalgallery.org.uk/learn",
    "https://www.theguardian.com/world/history"
]

math_links = [
    "https://www.khanacademy.org/math", "https://www.mathsisfun.com/",
    "https://www.purplemath.com/", "https://www.coolmath.com/",
    "https://www.math.com/", "https://www.mathplanet.com/",
    "https://www.wolframalpha.com/", "https://www.mathway.com/",
    "https://www.desmos.com/", "https://www.symbolab.com/",
    "https://www.cut-the-knot.org/", "https://www.artofproblemsolving.com/",
    "https://www.mathleague.com/", "https://www.mathcounts.org/",
    "https://www.merlot.org/merlot/materials.htm?category=2783", "https://www.onlinemathlearning.com/",
    "https://www.ixl.com/math/", "https://www.algebrahelp.com/",
    "https://www.geogebra.org/", "https://www.mathwarehouse.com/",
    "https://www.ck12.org/student/", "https://www.sosmath.com/",
    "https://www.coolmath4kids.com/", "https://www.thatquiz.org/",
    "https://www.mathopenref.com/", "https://www.math-aids.com/",
    "https://www.math-drills.com/", "https://www.mathgoodies.com/",
    "https://www.mathpickle.com/", "https://www.nctm.org/",
    "https://www.mathigon.org/", "https://www.weareteachers.com/math-websites/",
    "https://www.studypug.com/", "https://www.mathscareers.org.uk/",
    "https://www.mashupmath.com/", "https://www.math.toronto.edu/mathnet/",
    "https://www.splashlearn.com/math", "https://www.edutopia.org/math",
    "https://www.edhelper.com/math.htm", "https://www.kidsmathgamesonline.com/",
    "https://www.mathatube.com/", "https://www.homeworkspot.com/elementary/math/",
    "https://www.theteacherscorner.net/lesson-plans/math/", "https://www.ixl.com/",
    "https://www.mathplayground.com/", "https://www.xpmath.com/",
    "https://www.learnzillion.com/resources/72423-math-resources", "https://www.commoncoresheets.com/",
    "https://www.bbc.co.uk/bitesize/subjects/z826n39", "https://www.pbslearningmedia.org/subjects/mathematics/"
]

english_links = [
    "https://www.englishclub.com/", "https://learnenglish.britishcouncil.org/",
    "https://www.usingenglish.com/", "https://www.englishpage.com/",
    "https://www.talkenglish.com/", "https://www.ef.com/wwen/english-resources/",
    "https://www.fluentu.com/blog/english/", "https://www.busuu.com/en/english",
    "https://www.eslcafe.com/", "https://www.englishgrammar.org/",
    "https://www.grammarly.com/blog/", "https://www.ted.com/playlists/171/the_most_popular_talks_of_all",
    "https://www.bbc.co.uk/learningenglish", "https://www.english.com/",
    "https://www.language.com/learn-english/", "https://www.cambridgeenglish.org/",
    "https://www.duolingo.com/course/en/es/Learn-English", "https://www.memrise.com/courses/english/",
    "https://www.rosettastone.com/learn-english/", "https://www.engvid.com/",
    "https://www.espressoenglish.net/", "https://www.perfect-english-grammar.com/",
    "https://www.englishleap.com/", "https://www.languagesonline.org.uk/",
    "https://www.ecenglish.com/en/learn-english", "https://www.ted-ed.com/",
    "https://www.storynory.com/", "https://www.manythings.org/",
    "https://www.eslfast.com/", "https://www.breakingnewsenglish.com/",
    "https://www.talkenglish.com/speaking/listbasics.aspx", "https://www.english-at-home.com/",
    "https://www.learnenglishfeelgood.com/", "https://www.learnenglish.de/",
    "https://www.englishcentral.com/", "https://www.languageguide.org/english/",
    "https://www.speaklanguages.com/english/", "https://www.open.edu/openlearn/languages/english-language",
    "https://www.learn-english-today.com/", "https://www.englishbaby.com/",
    "https://www.examenglish.com/", "https://www.englishleap.com/",
    "https://www.studying-in-uk.org/", "https://www.vocabulary.com/",
    "https://www.merriam-webster.com/", "https://www.lexico.com/",
    "https://www.thesaurus.com/", "https://www.dictionary.com/",
    "https://www.wordreference.com/", "https://www.collinsdictionary.com/dictionary/english"
]
def extract_educational_content(url, socketio, category, total_urls):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        content = []
        for item in soup.find_all('div', class_='educational-content'):
            content.append(item.text)
        return content
    except requests.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return []

def get_all_content(socketio):
    all_content = {"historia": [], "matematica": [], "ingles": []}

    print("Scraping contenido de historia...")
    for i, url in tqdm(enumerate(history_links), desc="Historia", unit="url", total=len(history_links)):
        all_content['historia'].extend(extract_educational_content(url, socketio, 'historia', len(history_links)))
        socketio.emit('progress', {'category': 'historia', 'progress': int((i + 1) / len(history_links) * 100)})

    print("Scraping contenido de matemática...")
    for i, url in tqdm(enumerate(math_links), desc="Matemática", unit="url", total=len(math_links)):
        all_content['matematica'].extend(extract_educational_content(url, socketio, 'matematica', len(math_links)))
        socketio.emit('progress', {'category': 'matematica', 'progress': int((i + 1) / len(math_links) * 100)})

    print("Scraping contenido de inglés...")
    for i, url in tqdm(enumerate(english_links), desc="Inglés", unit="url", total=len(english_links)):
        all_content['ingles'].extend(extract_educational_content(url, socketio, 'ingles', len(english_links)))
        socketio.emit('progress', {'category': 'ingles', 'progress': int((i + 1) / len(english_links) * 100)})

    return all_content