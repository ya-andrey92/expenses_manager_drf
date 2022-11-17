-- Задание 1
SELECT nb.title,
       COUNT(*) AS count_n
FROM notebooks_brand nb
    JOIN notebooks_notebook nn ON nb.id = nn.brand_id
GROUP BY nb.title
ORDER BY count_n DESC;

-- Задание 2
SELECT CAST(nn.width as numeric) + (5 - CAST(nn.width as numeric) % 5) % 5 AS width_n,
       CAST(nn.depth as numeric) + (5 - CAST(nn.depth as numeric) % 5) % 5 AS depth_n,
       CAST(nn.height as numeric) + (5 - CAST(nn.height as numeric) % 5) % 5 AS height_n,
       COUNT(*) as count_n
FROM notebooks_notebook nn
GROUP BY width_n, depth_n, height_n
ORDER BY width_n, depth_n, height_n;
