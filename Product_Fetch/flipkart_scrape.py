import re
import requests
from bs4 import BeautifulSoup
from Product_Fetch.code_reuse import create_df_product, csv_file_handling

def flipkart_data(product_type,search_brand,search_product):
    start_url = "https://www.flipkart.com/search?q="
    query = search_brand+"+"+search_product
    url = start_url+query
    # print(url)

    req = requests.get(url)
    content= BeautifulSoup(req.content,'html.parser')

    data=content.find_all('div',{'class':'_4ddWXP'})
    links=[]
    product_name=[]
    start_url_product="https://www.flipkart.com"

    for items in data:
        rest_link=items.find('a')['href']
        name = items.find('a', attrs={'class':'s1Q9rs'})
        name_split=name.text.split()
        name_list = name_split[0:8][0:6]
        name_list_joint=' '.join(name_list)
        product_name.append(name_list_joint)
        links.append(start_url_product+rest_link)


    if(len(links) == 0):
        return False
    
    else:
        product_reviews_url=links[0]
        req2 = requests.get(product_reviews_url)
        content2 = BeautifulSoup(req2.content,'html.parser')
        product_links = []

        for t in content2.findAll('a', attrs={'href': re.compile("/product-reviews/")}):
            q=t.get('href')
            print(start_url+q)
            print(start_url+q)
            product_links.append(start_url_product+q)

        final_review_url=product_links[0]
        req3=requests.get(final_review_url)
        content3 = BeautifulSoup(req3.content, 'html.parser')
        review_list=[]

        for review in content3.find_all('div',{'class':'t-ZTKy'}):
            rev=review.get_text()
            rev_split=rev.split()
            rev_joint = " ".join(rev_split[:-1])
            rev_correct=rev_joint[:-4]
            review_list.append([product_type,search_product, rev_correct])

        df = create_df_product(review_list)
    
        csv_file = csv_file_handling(df, 'flipkart_data.csv', 'write')
        return True

# flipkart_data("printer","HP","Smart Tank")    

