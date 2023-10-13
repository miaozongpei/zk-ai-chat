from xinghuo_embedding import XhEmbeddings
import config

emb = XhEmbeddings(appid=config.embedding_xh_appid,
                       api_key=config.embedding_xh_api_key,
                       api_secret=config.embedding_xh_api_secret,
                       embedding_url=config.embedding_xh_embedding_url
                       )
vector = emb.embed_query('这个问题的向量是什么？')

print(vector)