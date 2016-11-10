/* This file contains table definitions for the emc.kb.
 */

create database if not exists parameters;
use parameters;

-- Model型号信息(型号代码，型号名称)
create table if not exists model (
    modelId integer unsigned not null auto_increment primary key,
    xhdm char(8) not null unique key,
    xhmc varchar(32) not null,
    index model_xhdm(xhdm)
) engine=InnoDB DEFAULT CHARSET=utf8;

-- Branch分系统信息 （型号代码，分系统代码，分系统名称，分系统类别）
create table if not exists branch (
    branchId integer unsigned not null auto_increment primary key,
    modelId integer unsigned not null,
    fxtdm char(16)  not null,
    fxtmc varchar(64)  not null,
    fxtlb char(16) not null,
    index branch_fxtdm(fxtdm),
    foreign key(modelId)
        references model(modelId)
            on update restrict
            on delete restrict
) engine=InnoDB DEFAULT CHARSET=utf8;
