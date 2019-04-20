USE sakila;

#1a
SELECT first_name, last_name FROM actor;
#1b-I'm not altering the table, just going to display
SELECT CONCAT(first_name,' ',last_name) as Actor_Name FROM actor;
SELECT Upper(Actor_Name);

#2a
SELECT actor_id, first_name, last_name FROM actor
WHERE first_name = 'Joe';
#2b
SELECT * FROM actor
WHERE last_name like '%GEN%';
#2c
SELECT * FROM actor
WHERE last_name like '%LI%'
order by last_name, first_name;
#2d
SELECT country_id, country FROM country
WHERE country in ('Afghanistan', 'Bangladesh', 'China');

#3a
ALTER TABLE actor
ADD COLUMN description BLOB;
#3b
ALTER TABLE actor
DROP COLUMN description;

#4a
SELECT last_name, count(last_name) FROM actor
GROUP BY last_name;
#4b
SELECT last_name, count(last_name) as 'Number of Names' FROM actor
GROUP BY last_name
Having count(last_name) >=2;
#4c
UPDATE actor
SET first_name='HARPO'
WHERE first_name='GROUCHO' and last_name='WILLIAMS';
#4d
UPDATE actor
SET first_name='GROUCHO'
WHERE first_name='HARPO';

#5a
SHOW CREATE TABLE address;

#6a
SELECT staff.first_name, staff.last_name, address.address
FROM staff
JOIN address
ON staff.address_id=address.address_id;
#6b
SELECT staff.first_name, staff.last_name, sum(payment.amount) as 'August Payment'
FROM staff
JOIN payment
ON staff.staff_id=payment.staff_id
Where (payment.payment_date between '2005-08-01 00:00:00' and '2005-08-31 23:59:59')
Group by payment.staff_id;
#6c
select film.title as 'Title', count(film_actor.actor_id) as 'Number of Actors'
from film
join film_actor
on film.film_id=film_actor.film_id
group by film_actor.film_id;
#6d
select count(inventory_id) as 'Copies of Hunchback Impossible'
from inventory
where film_id = (select film_id from film where title = 'Hunchback Impossible');
#6e
select customer.first_name, customer.last_name, sum(payment.amount) as 'Sum of Amount'
from payment
join customer
on customer.customer_id=payment.customer_id
group by customer.customer_id
order by customer.last_name;

#7a
select film.title as 'Title with K and Q in English' from film
where (title like 'K%'or title like 'Q%')
and language_id = (select language_id from language where name='English');

#7b
select first_name, last_name 
from actor
where actor_id in (select actor_id 
					from film_actor 
					where film_id in (select film_id 
										from film
                                        where title = 'Alone Trip'));
#7c
select customer.first_name, customer.last_name, customer.email, country.country
from customer
join address
	on customer.address_id=address.address_id
join city
	on address.city_id=city.city_id
join country
	on city.country_id=country.country_id
where country.country='Canada';
#7d
select * from film
where film_id in (select film_id from film_category
					where category_id in (select category_id from category
											where name='family'));                                        
#7e
select film.title, count(rental.inventory_id) as 'Number of Rental'
from rental
left join inventory
	on rental.inventory_id = inventory.inventory_id
left join film
	on inventory.film_id = film.film_id
group by film.film_id
order by count(rental.inventory_id) desc;
#7f
select store.store_id,sum(payment.amount) as 'Store Business'
from payment
left join customer
	on payment.customer_id = customer.customer_id
left join store
	on customer.store_id = store.store_id
group by store.store_id;
#7g
select store.store_id, city.city, country.country
from store
join address on store.address_id=address.address_id
join city on address.city_id=city.city_id
join country on city.country_id=country.country_id;
#7h
select category.name as 'Genre', sum(payment.amount) as 'Gross'
from payment 
join rental on payment.rental_id=rental.rental_id
join inventory on rental.inventory_id=inventory.inventory_id
join film_category on inventory.film_id=film_category.film_id
join category on film_category.category_id=category.category_id
group by category.category_id
order by sum(rental.rental_id) desc limit 5;

#8a
create view Top_5_Genres as
select category.name as 'Genre', sum(payment.amount) as 'Gross'
from payment 
join rental on payment.rental_id=rental.rental_id
join inventory on rental.inventory_id=inventory.inventory_id
join film_category on inventory.film_id=film_category.film_id
join category on film_category.category_id=category.category_id
group by category.category_id
order by sum(rental.rental_id) desc limit 5;
#8b
select * from Top_5_Genres;
#8c
DROP VIEW Top_5_Genres;                                           