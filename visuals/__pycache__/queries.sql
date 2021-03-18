/* Question 1 8*/
SELECT DISTINCT firstname, lastname, cid from coaches_season where cid in (select cid from coaches_season group by cid having count(distinct tid) < 2) order by lastname;

/*Question 2*/
Select Distinct P.firstname from player_rs P, teams T where  (P.tid=T.tid and T.location='Miami' and T.league='N') intersect
Select Distinct P1.firstname from player_rs P1, teams T1 where  (P1.tid=T1.tid and T1.location='New York' and T1.league='A');

/* Question 3 */
select C.firstname, C.lastname, C.tid, C.year from coaches_season C, player_rs P where (lower(C.cid)=lower(P.ilkid) or (lower(C.firstname)=lower(P.firstname) and lower(C.lastname)=lower(P.lastname))) and P.year=C.year and P.tid=C.tid;

/* Question 4 */
select Distinct T.name, P1.year, avg(P.h_feet*30.48 + P.h_inches*2.54) from teams T, player_rs P1, players P where P1.tid=T.tid and lower(P.ilkid)=lower(P1.ilkid) and P1.year=2002 group by T.name, P1.year order by avg(P.h_feet*30.48 + P.h_inches*2.54) desc;

/* Question 5 */
select c.firstname , c.lastname , c.cid from coaches_season c, player_rs pr
where c.year = 2000 and pr.year = 2000 and c.tid=pr.tid
group by pr.tid ,c.firstname , c.lastname, c.cid
order by count(pr.ilkid) DESC limit 1;

