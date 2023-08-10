--Obtenemos id, subgrupo y grupo.
SELECT s.id, s.descripcion, g.descripcion
FROM subgrupos s
JOIN grupos g
ON s.id_grupo=g.id
WHERE s.descripcion LIKE ?
OR g.descripcion LIKE ?;