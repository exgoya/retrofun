import jaydebeapi
conn = jaydebeapi.connect("sunje.goldilocks.jdbc.GoldilocksDriver",
                          "jdbc:goldilocks://127.0.0.1:30009/test",
                          ["test", "test"],
                          "/home2/goya/goldilocks_home/lib/goldilocks8.jar",)
curs = conn.cursor()
curs.execute('create table CUSTOMER'
             '("CUST_ID" INTEGER not null,'
             ' "NAME" VARCHAR(50) not null,'
             ' primary key ("CUST_ID"))'
            )
curs.execute("insert into CUSTOMER values (1, 'John')")
curs.execute("select * from CUSTOMER")
curs.fetchall()
curs.close()
conn.close()
