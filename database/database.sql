create database url_shortner;

use url_shortner;

create table dmforlink(
    id int AUTO_INCREMENT primary key,
    original text NOT NULL,
    pipiurl varchar(10) NOT NULL unique,
    dob timestamp default current_timestamp
);