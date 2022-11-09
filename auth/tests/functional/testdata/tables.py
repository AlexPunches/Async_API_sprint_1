"""DDL всех таблиц нужных для тестов."""

from functional.settings import test_settings

create_user = """create table if not exists {users_tablename}
(
    id            uuid         not null,
    email         varchar      not null,
    login         varchar,
    active        boolean      not null,
    password      varchar      not null,
    primary key (id),
    unique (login),
    unique (email)
);
""".format(users_tablename=test_settings.users_tablename)

create_roles = """create table if not exists {roles_tablename}
(
    id          serial,
    name        varchar(80),
    description varchar(255),
    primary key (id),
    unique (name)
);
""".format(roles_tablename=test_settings.roles_tablename)

create_roles_users = """create table if not exists {roles_users_tablename}
(
    user_id uuid,
    role_id integer,
    foreign key (user_id) references users,
    foreign key (role_id) references roles
);
""".format(roles_users_tablename=test_settings.roles_users_tablename)

drop_user = 'drop table if exists {users_tablename};'.format(
    users_tablename=test_settings.users_tablename,
)
drop_roles = 'drop table if exists  {roles_tablename};'.format(
    roles_tablename=test_settings.roles_tablename,
)
drop_roles_users = 'drop table if exists  {roles_users_tablename};'.format(
    roles_users_tablename=test_settings.roles_users_tablename,
)