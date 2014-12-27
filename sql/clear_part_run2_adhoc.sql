select * from runner_race order by id
select count(*) from runner_run where race_id = 1

select * 
from runner_run r
join runner_runplace rp on (r.id=rp.run_id)
where r.race_id = 1
order by run_seq, lane

/*
delete from runner_runplace where run_id in (
    select id from runner_run where race_id=1)
    
delete from runner_run where race_id=1
*/



select count(*), rank from runner_person group by rank

/* Promote Persons from prior year */
update runner_person set rank='None', stamp=current_timestamp where rank='WEBELOS II'
update runner_person set rank='WEBELOS II', stamp=current_timestamp where rank='WEBELOS I'
update runner_person set rank='WEBELOS I', stamp=current_timestamp where rank='Bear'
update runner_person set rank='Bear', stamp=current_timestamp where rank='Wolf'
update runner_person set rank='Wolf', stamp=current_timestamp where rank='Tiger'