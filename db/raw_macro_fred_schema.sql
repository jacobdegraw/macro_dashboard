drop table if exists observations_current;
drop table if exists observations_history;
drop table if exists series_current;
drop table if exists series_history;
drop table if exists series_releases_current;
drop table if exists series_releases_history;
drop table if exists releases_current;
drop table if exists releases_history;
drop table if exists release_dates_current;
drop table if exists release_dates_history;
drop table if exists tracked_series;


create table observations_current(
	series_id varchar(16) not null,
	date date not null,
	value double precision,
	realtime_start date not null,
	realtime_end date not null,
	ingested_at timestamp not null,
	primary key (series_id, date)
);

create table observations_history(
	series_id varchar(16) not null,
	date date not null,
	value double precision,
	realtime_start date not null,
	realtime_end date not null,
	ingested_at timestamp not null,
	primary key (series_id, date, realtime_start)
);

create table series_current(
	series_id varchar(16) not null primary key,	
	title varchar(32) not null,
	observation_start date not null,
	observation_end date not null,
	frequency varchar(32) not null,
	frequency_short varchar(4) not null,
	units varchar(32) not null,
	units_short varchar(4) not null,
	seasonal_adjustment varchar(16) not null,
	seasonal_adjustment_short varchar(4) not null,
	last_updated timestamp not null,
	popularity integer not null,
	notes varchar(256) not null,
	realtime_start date not null,
	realtime_end date not null,
	ingested_at timestamp not null
);

create table series_history(
	series_id varchar(16) not null,	
	title varchar(32) not null,
	observation_start date not null,
	observation_end date not null,
	frequency varchar(32) not null,
	frequency_short varchar(4) not null,
	units varchar(32) not null,
	units_short varchar(4) not null,
	seasonal_adjustment varchar(16) not null,
	seasonal_adjustment_short varchar(4) not null,
	last_updated timestamp not null,
	popularity integer not null,
	notes varchar(256) not null,
	realtime_start date not null,
	realtime_end date not null,
	ingested_at timestamp not null,
	primary key (series_id, realtime_start)
);

create table series_releases_current(
	series_id varchar(16) not null,
	release_id int not null,
	release_name varchar(32) not null,
	realtime_start date not null,
	realtime_end date not null,
	ingested_at timestamp not null,
	primary key (series_id, release_id)
);

create table series_releases_history(
	series_id varchar(16) not null,
	release_id int not null,
	release_name varchar(128) not null,
	realtime_start date not null,
	realtime_end date not null,
	ingested_at timestamp not null,
	primary key (series_id, release_id, realtime_start)
);

create table releases_current(
	release_id int	not null,
	name varchar(128) not null,
	press_release bool not null,
	link varchar(32),
	note varchar(256),
	realtime_start date not null,
	realtime_end date not null,
	ingested_at timestamp not null,
	primary key (release_id)
);

create table releases_history(
	release_id int	not null,
	name varchar(128) not null,
	press_release bool not null,
	link varchar(32),
	note varchar(256),
	realtime_start date not null,
	realtime_end date not null,
	ingested_at timestamp not null,
	primary key (release_id, realtime_start)
);

create table release_dates_current(
	release_id int not null primary key,
	release_name varchar(128) not null,
	release_date date not null,
	realtime_start date not null,
	realtime_end date not null,
	ingested_at timestamp not null
);

create table release_dates_history(
	release_id int not null,
	release_name varchar(128) not null,
	release_date date not null,
	realtime_start date not null,
	realtime_end date not null,
	ingested_at timestamp not null,
	primary key (release_id, realtime_start)
);

create table tracked_series(
	series_id varchar(16) primary key
);



