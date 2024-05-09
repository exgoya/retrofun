from sqlalchemy import create_engine, text
engine = create_engine('goldilocks://test:test@127.0.0.1:30009', echo=False)

curs = engine.connect()
curs.execute(text('drop table customer'))
curs.execute(text("""create table CUSTOMER 
             ("CUST_ID" INTEGER not null, 
             "NAME" VARCHAR(50) not null,
              primary key ("CUST_ID"))"""
            ))
curs.execute(text("insert into CUSTOMER values (1, 'John')"))
res = curs.execute(text("select * from CUSTOMER"))
r = res.fetchall()

print(r)
res.close()
curs.close()
