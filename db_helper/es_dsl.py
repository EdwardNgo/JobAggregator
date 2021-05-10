from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search,Q
from elasticsearch_dsl.query import MultiMatch, Match

es = Elasticsearch([{'host': 'localhost', 'port':9200}])
query = input("Your query: ")
#Search binh thuong
# res_3 = es.search(index="raw_article_2", q=query, size=100, from_=1)
# res_4 =  es.search(index="raw_article_2", q=query, size=100, filter_path = ['hits.hits._id','hits.hits.body','hits.hits._source.body'])
# print(res_4)
#Search voi dsl
search = Search(using = es,index = "raw_article_2")
# s = Search(using = es,index = "raw_article").query("match",body = query)
s = search.query("match",body = query).execute()
#multi search
multi_match = MultiMatch(query = query,fields = ['title','body','descri ption'])
q = Q("multi_match",query = query, fields = ['title','body','description'])
s_2 = search.query(multi_match).execute()
s_3 = search.query(q).execute()
print(s_3.to_dict())
