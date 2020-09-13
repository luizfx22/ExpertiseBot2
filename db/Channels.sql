create table sec_channels
(
    id        bigint               not null,
    guild_id  bigint               not null,
    `name`      varchar(255)         not null,
    fl_backup tinyint(1) default 0 not null,
    fl_log    tinyint(1) default 0 null,
    fl_active tinyint(1) default 1 null,
    constraint sec_channels_id_uindex
        unique (id),
    constraint sec_channels_sec_guilds_id_fk
        foreign key (guild_id) references sec_guilds (id)
);

