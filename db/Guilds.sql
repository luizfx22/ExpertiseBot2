create table sec_guilds
(
    id   bigint       not null,
    `name` varchar(255) not null,
    constraint sec_guilds_id_uindex
        unique (id)
);

alter table sec_guilds
    add primary key (id);
