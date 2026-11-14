-- 1. List all competitions along with their category name
SELECT c.competition_name, cat.category_name 
FROM competitions c 
JOIN categories cat ON c.category_id = cat.category_id;

-- 2. Count the number of competitions in each category
SELECT cat.category_name, COUNT(c.competition_id) AS total_competitions 
FROM categories cat 
LEFT JOIN competitions c ON cat.category_id = c.category_id 
GROUP BY cat.category_name;

-- 3. Find all competitions of type 'doubles'
SELECT * FROM competitions WHERE type = 'doubles';

-- 4. List all venues along with their associated complex name
SELECT v.venue_name, c.complex_name 
FROM venues v 
JOIN complexes c ON v.complex_id = c.complex_id;

-- 5. Find competitors ranked in the top 5
SELECT comp.name, comp.country, r.rank, r.points 
FROM competitors comp 
JOIN competitor_rankings r ON comp.competitor_id = r.competitor_id 
WHERE r.rank <= 5;

-- 6. Get the total points of competitors from a specific country (e.g., Croatia)
SELECT comp.country, SUM(r.points) AS total_points 
FROM competitors comp 
JOIN competitor_rankings r ON comp.competitor_id = r.competitor_id 
WHERE comp.country = 'Croatia' 
GROUP BY comp.country;