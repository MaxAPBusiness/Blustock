SELECT s.id, s.descripcion, g.descripcion
FROM subgrupos s
JOIN grupos g
ON s.id_grupo=g.id
WHERE s.id LIKE ?
OR c.descripcion LIKE ?
OR p.dni LIKE ?;