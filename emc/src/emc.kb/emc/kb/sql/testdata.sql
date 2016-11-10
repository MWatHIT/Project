-- Create some test data in the parameters database
-- Note that since the UI logic only shows things in the near future,
-- you may need to run this every few days :)

use parameters;



insert into model (xhdm, xhmc) 
values 
       -- model 
       ('C1', '电信手机'),
       ('C2', '联通手机'),
       ('C3', '移动手机');
       
insert into branch (modelId, fxtdm,fxtmc,fxtlb) 
values 
       -- branch 
       (1, 'c11','发射器','fashe'),
       (1, 'c12','发射天线','fashe'),
       (1, 'c13','发射机','fashe'),
       (2, 'c21','接收器','jieshou'),
       (2, 'c22','接收天线','jieshou'),
       (2, 'c23','接收机','jieshou');


