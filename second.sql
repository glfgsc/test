select count(1) cnt
from (select user_id
from event_log
where year(event_timestamp)=2020 and month(event_timestamp)=9
group by user_id
having count(*) >= 1000 and count(*) < 2000) a