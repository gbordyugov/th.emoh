--
-- to make this automatically runnable, please adjust the path to the
-- csv files in the copy statements below
--

drop table if exists attributions;
drop table if exists user_pressed_registered_btn_events;
drop table if exists user_pressed_bank_connect_button;


create table attributions (
  id                int primary key,
  created_at        timestamp,
  user_email        varchar,
  anonymous_user_id int
);

create table user_pressed_registered_btn_events (
  id                int primary key,
  created_at        timestamp,
  user_email        varchar,
  anonymous_user_id int
);

create table user_pressed_bank_connect_button (
  id                int primary key,
  created_at        timestamp,
  bank_name         varchar,
  anonymous_user_id int
);

--
-- load test data
--

copy
  attributions
from
  '/Users/gri/src/home.ht/challenge/csv/attributions.csv'
with
  (format csv);

copy
  user_pressed_registered_btn_events
from
  '/Users/gri/src/home.ht/challenge/csv/button_events.csv'
with
  (format csv);

copy
  user_pressed_bank_connect_button
from
  '/Users/gri/src/home.ht/challenge/csv/bank_events.csv'
with
  (format csv);

--
-- now the actual code, I'm presenting here two solutions, one is a
-- bit more SQL-engine heavy by having a join, but more bullet-proof,
-- the second is lighter, but assumes things that have not been
-- explicitly stated in the assignment
--

--
-- this one is a more bullet-proof solution that checks that events
-- from button clicks and bank details entry tables are backed up by
-- existing users from the attributions table
--

select 
  'attribution' as event_name,
  count(distinct a.anonymous_user_id) as count_of_events
from
  attributions a

union all 

select 
  'user_register' as event_name,
  count(distinct bu.anonymous_user_id) as count_of_events
from
  attributions a
left join
  user_pressed_registered_btn_events bu
on a.anonymous_user_id = bu.anonymous_user_id

union all

select 
  'bank_connect' as event_name,
  count(distinct ba.anonymous_user_id) as count_of_events
from
  attributions a
left join
  user_pressed_bank_connect_button ba
on a.anonymous_user_id = ba.anonymous_user_id;

--
-- this is a more simply-minded solution that just counts the unique
-- user_ids in all three tables
-- 

select 
  'attribution' as event_name,
  count(distinct a.anonymous_user_id) as count_of_events
from
  attributions a

union all 

select 
  'user_register' as event_name,
  count(distinct bu.anonymous_user_id) as count_of_events
from
  user_pressed_registered_btn_events bu

union all

select 
  'bank_connect' as event_name,
  count(distinct ba.anonymous_user_id) as count_of_events
from
  user_pressed_bank_connect_button ba;
