## input : 회사이름
## output : 신년사, 회사소개, 인재상
def get_company_info(company_name):
    import os
    from tavily import TavilyClient
    from datetime import date

    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    ## 신년사
    list1 = client.search(company_name+"의 "+str(date.today().year)+"년 신년사", search_depth="advanced")["results"]
    year_greeting = [s["content"] for s in list1 if company_name in s["content"]] 

    ## 회사소개
    list1 = client.search(company_name+"의 회사소개", search_depth="advanced")["results"]
    comp_intro = [s["content"] for s in list1 if company_name in s["content"]] 

    ## 신년사
    list1 = client.search(company_name+"의 인재상", search_depth="advanced")["results"]
    comp_membership = [s["content"] for s in list1 if company_name in s["content"]] 

    return year_greeting, comp_intro, comp_membership