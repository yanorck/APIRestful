import requests
from bs4 import BeautifulSoup

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    anime_list = []
    
    # Encontre todas as linhas da tabela
    rows = soup.find_all('tr', class_='ranking-list')
    
    for row in rows:
        # Obtenha o rank
        rank_elem = row.find('span', class_=['lightLink', 'top-anime-rank-text', 'rank1', 'rank2', 'rank3', 'rank4', 'rank5', 'rank6', 'rank7'])
        rank = rank_elem.text.strip() if rank_elem else "Rank not found"
        
        # Obtenha o título
        title_elem = row.find('h3', class_='fl-l fs14 fw-b anime_ranking_h3')
        title = title_elem.text.strip() if title_elem else "Title not found"
        
        # Obtenha o link
        link_elem = title_elem.find('a') if title_elem else None
        link = link_elem['href'] if link_elem else "Link not found"
        
        # Obtenha a imagem
        img_elem = row.find('img')
        img_url = img_elem['data-src'] if img_elem else "Image not found"

        # Obtenha a div com a classe 'information di-ib mt4'
        info_div = row.find('div', class_='information di-ib mt4')
        
        if info_div:
            # Divida o texto usando os <br> para encontrar os dados desejados
            br_elements = info_div.find_all('br')
            data_lancamento = br_elements[0].next_sibling.strip() if len(br_elements) > 0 else "Data de lançamento não encontrada"
            membros = br_elements[1].next_sibling.strip() if len(br_elements) > 1 else "Membros não encontrados"
        else:
            data_lancamento = "Data de lançamento não encontrada"
            membros = "Membros não encontrados"

        # Adicione as informações ao anime_list
        anime_list.append({
            'rank': rank,
            'title': title,
            'link': link,
            'image_url': img_url,
            'data_lancamento': data_lancamento,
            'membros': membros.replace(" members", "")
        })
    
    return anime_list
