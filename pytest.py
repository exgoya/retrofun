import pygoldilocks
conn = pygoldilocks.connect( 'DSN=GOLDILOCKS;UID=test;PWD=test' )

curs = conn.cursor()
curs.execute('drop table customer')
curs.execute('create table CUSTOMER'
             '("CUST_ID" INTEGER not null,'
             ' "NAME" VARCHAR(50) not null,'
             ' primary key ("CUST_ID"))'
            )
curs.execute("insert into CUSTOMER values (1, 'John')")
curs.execute("select * from CUSTOMER")
r = curs.fetchall()
print(r)
curs.close()
conn.close()
