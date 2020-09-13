create table sec_messages
(
    id          int auto_increment
        primary key,
    guild_id    bigint                               not null,
    channel_id  bigint                               not null,
    author_name text                                 not null,
    author_id   bigint                               not null,
    content     longtext                             not null,
    media_url   text                                 not null,
    createdAt   datetime   default CURRENT_TIMESTAMP null,
    fl_pin      tinyint(1) default 0                 not null,
    constraint sec_messages_sec_channels_id_fk
        foreign key (channel_id) references sec_channels (id)
            on delete cascade,
    constraint sec_messages_sec_guilds_id_fk
        foreign key (guild_id) references sec_guilds (id)
            on delete cascade
);
