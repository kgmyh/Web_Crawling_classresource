# 설치

`pip install -r requirements.txt`

# Table

```sql
drop table if exists news_list;

create table news_list (
    id int primary key auto_increment,
    title varchar(200) not null,
    link varchar(200) not null,
    created_at timestamp default current_timestamp
);
```