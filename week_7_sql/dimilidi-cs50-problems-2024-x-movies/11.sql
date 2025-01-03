SELECT m.title
FROM movies m
JOIN stars s ON m.id = s.movie_id
JOIN ratings r ON s.movie_id = r.movie_id
JOIN people p ON s.person_id = p.id
WHERE p.name LIKE 'Chadwick Boseman'
ORDER BY r.rating DESC
LIMIT 5;
