from datetime import datetime
from sqlalchemy import select, func, union , or_,text
from db import Session
from models import BlogArticle, BlogView, Product

session = Session()

page_views = func.count(BlogView.id).label('count_1')

q1 = (select(Product.name, page_views)
    .join(BlogArticle.product, isouter=True)
    .join(BlogArticle.views)
    .where(BlogView.timestamp.between(
        datetime(2022, 11, 1), datetime(2022, 12, 1)))
    .group_by(Product.name))

q2 = (select(Product.name, page_views)
    .join(Product.blog_articles, isouter=True)
    .join(BlogArticle.views, isouter=True)
    .where(or_(
        BlogView.timestamp == None,
        BlogView.timestamp.between(
            datetime(2022, 11, 1), datetime(2022, 12, 1))))
    .group_by(Product.name)
    .having( page_views== 0))

#q = union(q1, q2).order_by(text('count_1 DESC'), Product.name)
q = union(q1, q2).order_by(func.count(BlogView.id), Product.name)
print(page_views)
#q = union(q1, q2).order_by(page_views.desc(), Product.name)
print(q)
print(session.execute(q).all())
