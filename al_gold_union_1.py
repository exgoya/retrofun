import csv
from sqlalchemy import create_engine, text, union, Identity,func,select,String,MetaData, ForeignKey
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker, WriteOnlyMapped, relationship

class Model(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })

engine = create_engine('goldilocks://test:test@127.0.0.1:30009', echo=True)
Session = sessionmaker(engine)

class Product(Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Identity(),primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    manufacturer: Mapped[str] = mapped_column(String(64), index=True)
    year: Mapped[int] = mapped_column(index=True)
    country: Mapped[Optional[str]] = mapped_column(String(32))
    cpu: Mapped[Optional[str]] = mapped_column(String(32))

    def __repr__(self):
        return f'Product({self.id}, "{self.name}")'

def dropCrt(engine):

    Model.metadata.drop_all(engine)  # warning: this deletes all data!
    Model.metadata.create_all(engine)

    with Session() as session:
        with session.begin():
            with open('products.csv') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['year'] = int(row['year'])
                    product = Product(**row)
                    session.add(product)


def main():
    #dropCrt(engine)

    with Session() as session:
        page_views = func.count(Product.id).label(None)

        q1 = (select(Product.name, page_views).group_by(Product.name))
        q2 = (select(Product.name, page_views).group_by(Product.name))
        q = union(q1,q2).order_by(page_views.desc(),Product.name)
        print(q)
        res = session.execute(q1).all()
        print(res)
        print(q)

if __name__ == '__main__':
    main()


