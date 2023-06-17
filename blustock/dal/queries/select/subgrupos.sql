SELECT s.descripcion, g.descripcion
FROM subgrupos s
JOIN grupos g
ON s.id_grupo=g.id
WHERE s.id LIKE ?
OR s.descripcion LIKE ?
OR g.descripcion LIKE ?;