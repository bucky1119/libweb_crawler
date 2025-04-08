def get_website_configs():
    # 可以从 JSON、YAML 或数据库加载网站配置，这里举例返回一个列表
    return [
        # {
        #     "name": "网站1",
        #     "crawler_class": __import__("crawlers.website1_crawler", fromlist=["Website1Crawler"]).Website1Crawler,
        #     "url": "https://example1.com",
        #     # 其他必要的配置参数
        # },
        # {
        #     "name": "网站2",
        #     "crawler_class": __import__("crawlers.website2_crawler", fromlist=["Website2Crawler"]).Website2Crawler,
        #     "url": "https://example2.com",
        # },
        {
            "name": "网站3", # 具有攻击嫌疑，易被禁止访问
            "crawler_class": __import__("crawlers.website3_crawler", fromlist=["Website3Crawler"]).Website3Crawler,
            "url": "https://www.agriculture.gov.au/about/news/all?f%5B0%5D=topic%3A310",
        },
        {
            "name": "网站4",
            "crawler_class": __import__("crawlers.website4_crawler", fromlist=["Website4Crawler"]).Website4Crawler,
            "url": "https://www.uq.edu.au/news/",
        },
        {
            "name": "网站5",
            "crawler_class": __import__("crawlers.website5_crawler", fromlist=["Website5Crawler"]).Website5Crawler,
            "url": "https://researchimpact.uwa.edu.au/research-impact-stories/",
        },
        {
            "name": "网站6",
            "crawler_class": __import__("crawlers.website6_crawler", fromlist=["Website6Crawler"]).Website6Crawler,
            "url": "https://www.sydney.edu.au/news-opinion/news/science-and-technology.html",
        },
        # {
        #     "name": "网站7", 页面丢失
        #     "crawler_class": __import__("crawlers.website7_crawler", fromlist=["Website7Crawler"]).Website7Crawler,
        #     "url": "",
        # },
        {
            "name": "网站8",
            "crawler_class": __import__("crawlers.website8_crawler", fromlist=["Website8Crawler"]).Website8Crawler,
            "url": "https://news.ku.dk/all_news/",
        },
        {
            "name": "网站16",
            "crawler_class": __import__("crawlers.website16_crawler", fromlist=["Website16Crawler"]).Website16Crawler,
            "url": "https://www.pasteur.fr/en/actualites-jdr",
        },
        {
            "name": "网站17",
            "crawler_class": __import__("crawlers.website17_crawler", fromlist=["Website17Crawler"]).Website17Crawler,
            "url": "https://www.inrae.fr/en/news?inrae_prod%5BsortBy%5D=inrae_prod_created_date_desc&inrae_prod%5BrefinementList%5D%5Bfield_thematic_name%5D%5B0%5D=Food%2C%20Global%20Health",
        },
        {
            "name": "网站18",
            "crawler_class": __import__("crawlers.website18_crawler", fromlist=["Website18Crawler"]).Website18Crawler,
            "url": "https://www.mafra.go.kr/english/756/subview.do",
        },
        {
            "name": "网站19",
            "crawler_class": __import__("crawlers.website19_crawler", fromlist=["Website19Crawler"]).Website19Crawler,
            "url": "https://www.government.nl/ministries/ministry-of-economic-affairs-and-climate-policy/news?keyword=&start-date=&end-date=&element=Ministry+of+Economic+Affairs+and+Climate+Policy",
        },
        # {
        #     "name": "网站20",
        #     "crawler_class": __import__("crawlers.website20_crawler", fromlist=["Website20Crawler"]).Website20Crawler,
        #     "url": "https://www.government.nl/ministries/ministry-of-economic-affairs-and-climate-policy/documents?keyword=&start-date=&end-date=&issue=All+topics&element=Ministry+of+Economic+Affairs+and+Climate+Policy&type=All+documents",
        # },
        # {
        #     "name": "网站21",
        #     "crawler_class": __import__("crawlers.website21_crawler", fromlist=["Website21Crawler"]).Website21Crawler,
        #     "url": "https://www.government.nl/ministries/ministry-of-economic-affairs-and-climate-policy/news?keyword=&start-date=&end-date=&element=Ministry+of+Agriculture%2C+Nature+and+Food+Quality",
        # },
        # {
        #     "name": "网站22",
        #     "crawler_class": __import__("crawlers.website22_crawler", fromlist=["Website22Crawler"]).Website22Crawler,
        #     "url": "https://www.government.nl/ministries/ministry-of-agriculture-nature-and-food-quality/news",
        # },
        # {
        #     "name": "网站23",
        #     "crawler_class": __import__("crawlers.website23_crawler", fromlist=["Website23Crawler"]).Website23Crawler,
        #     "url": "https://www.wur.nl/en/research-results/research-institutes/food-safety-research/news-and-calendar.htm",
        # },
        # {
        #     "name": "网站24",
        #     "crawler_class": __import__("crawlers.website24_crawler", fromlist=["Website24Crawler"]).Website24Crawler,
        #     "url": "https://www.uu.nl/en/research/dynamics-of-youth",
        # },
        # {
        #     "name": "网站25",
        #     "crawler_class": __import__("crawlers.website25_crawler", fromlist=["Website25Crawler"]).Website25Crawler,
        #     "url": "https://www.government.nl/topics/agriculture/news",
        # },
        # {
        #     "name": "网站26",
        #     "crawler_class": __import__("crawlers.website26_crawler", fromlist=["Website26Crawler"]).Website26Crawler,
        #     "url": "https://www.ubc.ca/news/",
        # },
        # {
        #     "name": "网站27",
        #     "crawler_class": __import__("crawlers.website27_crawler", fromlist=["Website27Crawler"]).Website27Crawler,
        #     "url": "https://www.uoguelph.ca/research/discover-our-research/research-news",
        # },
        # {
        #     "name": "网站28",
        #     "crawler_class": __import__("crawlers.website28_crawler", fromlist=["Website28Crawler"]).Website28Crawler,
        #     "url": "https://uwaterloo.ca/news/",
        # },
        # {
        #     "name": "网站29",
        #     "crawler_class": __import__("crawlers.website29_crawler", fromlist=["Website29Crawler"]).Website29Crawler,
        #     "url": "https://agriculture.canada.ca/en/news/news-releases-and-statements",
        # },
        # {
        #     "name": "网站30",
        #     "crawler_class": __import__("crawlers.website30_crawler", fromlist=["Website30Crawler"]).Website30Crawler,
        #     "url": "https://agriculture.canada.ca/en/science/story-agricultural-science/scientific-achievements-agriculture",
        # },
        {
            "name": "网站61",
            "crawler_class": __import__("crawlers.website61_crawler", fromlist=["Website61Crawler"]).Website61Crawler,
            "url": "https://foodtank.com/news/category/food-tank/",
        },
        # {
        #     "name": "网站83",
        #     "crawler_class": __import__("crawlers.website83_crawler", fromlist=["Website83Crawler"]).Website83Crawler,
        #     "url": "https://www.nature.com/natsustain/reviews-and-analysis",
        # },
        # {
        #     "name": "网站84",
        #     "crawler_class": __import__("crawlers.website84_crawler", fromlist=["Website84Crawler"]).Website84Crawler,
        #     "url": "https://www.nature.com/natsustain/news-and-comment",
        # },
        # {
        #     "name": "网站85",
        #     "crawler_class": __import__("crawlers.website85_crawler", fromlist=["Website85Crawler"]).Website85Crawler,
        #     "url": "https://www.nature.com/srep/research-articles",
        # },
        # {
        #     "name": "网站86",
        #     "crawler_class": __import__("crawlers.website86_crawler", fromlist=["Website86Crawler"]).Website86Crawler,
        #     "url": "https://www.nature.com/srep/news-and-comment",
        # },
        # {
        #     "name": "网站87",
        #     "crawler_class": __import__("crawlers.website87_crawler", fromlist=["Website87Crawler"]).Website87Crawler,
        #     "url": "https://impact.ed.ac.uk/category/research/future-health-and-care/",
        # },
        # {
        #     "name": "网站88",
        #     "crawler_class": __import__("crawlers.website88_crawler", fromlist=["Website88Crawler"]).Website88Crawler,
        #     "url": "https://www.cam.ac.uk/research?ucam-ref=home-menu",
        # },
        # {
        #     "name": "网站89",
        #     "crawler_class": __import__("crawlers.website89_crawler", fromlist=["Website89Crawler"]).Website89Crawler,
        #     "url": "https://www.chathamhouse.org/search/content_format/Article/topic/agriculture-and-food-316",
        # },
        # {
        #     "name": "网站90",
        #     "crawler_class": __import__("crawlers.website90_crawler", fromlist=["Website90Crawler"]).Website90Crawler,
        #     "url": "https://www.gov.uk/search/news-and-communications?organisations[]=department-for-science-innovation-and-technology&parent=department-for-science-innovation-and-technology",
        # },
        # {
        #     "name": "网站91",
        #     "crawler_class": __import__("crawlers.website91_crawler", fromlist=["Website91Crawler"]).Website91Crawler,
        #     "url": "https://www.gov.uk/search/policy-papers-and-consultations?organisations[]=department-for-science-innovation-and-technology&parent=department-for-science-innovation-and-technology",
        # },
        # {
        #     "name": "网站92",
        #     "crawler_class": __import__("crawlers.website92_crawler", fromlist=["Website92Crawler"]).Website92Crawler,
        #     "url": "https://www.ukri.org/news/",
        # },
        # {
        #     "name": "网站93",
        #     "crawler_class": __import__("crawlers.website93_crawler", fromlist=["Website93Crawler"]).Website93Crawler,
        #     "url": "https://www.gov.uk/search/news-and-communications?organisations[]=department-for-environment-food-rural-affairs&parent=department-for-environment-food-rural-affairs",
        # },
        # {
        #     "name": "网站94",
        #     "crawler_class": __import__("crawlers.website94_crawler", fromlist=["Website94Crawler"]).Website94Crawler,
        #     "url": "https://www.gov.uk/search/policy-papers-and-consultations?organisations[]=department-for-environment-food-rural-affairs&parent=department-for-environment-food-rural-affairs",
        # },
        # {
        #     "name": "网站95",
        #     "crawler_class": __import__("crawlers.website95_crawler", fromlist=["Website95Crawler"]).Website95Crawler,
        #     "url": "https://www.food.gov.uk/search?keywords=&filter_type%5BNews%5D=News",
        # },
        # {
        #     "name": "网站96",
        #     "crawler_class": __import__("crawlers.website96_crawler", fromlist=["Website96Crawler"]).Website96Crawler,
        #     "url": "https://www.sanger.ac.uk/news/#",
        # },
        # {
        #     "name": "网站97",
        #     "crawler_class": __import__("crawlers.website97_crawler", fromlist=["Website97Crawler"]).Website97Crawler,
        #     "url": "https://www.nsfc.gov.cn/publish/portal0/tab609/",
        # },
        # {
        #     "name": "网站98",
        #     "crawler_class": __import__("crawlers.website98_crawler", fromlist=["Website98Crawler"]).Website98Crawler,
        #     "url": "https://www.most.gov.cn/szyw",
        # },
        # {
        #     "name": "网站99",
        #     "crawler_class": __import__("crawlers.website99_crawler", fromlist=["Website99Crawler"]).Website99Crawler,
        #     "url": "https://www.cas.cn/syky/",
        # },
        # {
        #     "name": "网站100",
        #     "crawler_class": __import__("crawlers.website100_crawler", fromlist=["Website100Crawler"]).Website100Crawler,
        #     "url": "http://news.cau.edu.cn/kxyj/index.htm",
        # },
        # {
        #     "name": "网站101",
        #     "crawler_class": __import__("crawlers.website101_crawler", fromlist=["Website101Crawler"]).Website101Crawler,
        #     "url": "https://www.caas.cn/xwzx/zjgd/index.htm",
        # },
        # {
        #     "name": "网站102",
        #     "crawler_class": __import__("crawlers.website102_crawler", fromlist=["Website102Crawler"]).Website102Crawler,
        #     "url": "http://www.moa.gov.cn/xw",
        # },
        # {
        #     "name": "网站103",
        #     "crawler_class": __import__("crawlers.website103_crawler", fromlist=["Website103Crawler"]).Website103Crawler,
        #     "url": "http://zdscxx.moa.gov.cn:8080/nyb/pc/messageList.jsp",
        # },
        # 依次添加50个网站的配置
    ]
