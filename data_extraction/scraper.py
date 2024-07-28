import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Links para las materias
history_links = [
    "https://www.history.com/",
    "https://www.historytoday.com/",
    "https://www.historyextra.com/",
    "https://www.historynet.com/",
    "https://www.historylearningsite.co.uk/"
]

math_links = [
    "https://www.khanacademy.org/math",
    "https://www.mathsisfun.com/",
    "https://www.coolmath.com/",
    "https://www.math.com/",
    "https://www.mathplanet.com/"
]

english_links = [
    "https://www.englishclub.com/",
    "https://learnenglish.britishcouncil.org/",
    "https://www.englishpage.com/",
    "https://www.talkenglish.com/",
    "https://www.eslfast.com/"
]

def extract_educational_content(url):
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

def get_all_content():
    all_content = {"historia": [], "matematica": [], "ingles": []}

    print("Scraping contenido de historia...")
    for url in tqdm(history_links, desc="Historia", unit="url"):
        all_content['historia'].extend(extract_educational_content(url))

    print("Scraping contenido de matemática...")
    for url in tqdm(math_links, desc="Matemática", unit="url"):
        all_content['matematica'].extend(extract_educational_content(url))

    print("Scraping contenido de inglés...")
    for url in tqdm(english_links, desc="Inglés", unit="url"):
        all_content['ingles'].extend(extract_educational_content(url))

    return all_content
