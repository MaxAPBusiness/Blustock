--Obtenemos id, categoría y clase.
SELECT cl.id, cat.descripcion, cl.descripcion
FROM clases cl
JOIN cats_clase cat ON cl.id_cat=cat.id
WHERE cl.descripcion NOT LIKE 'Egresado'
AND (cl.descripcion LIKE ?
OR cat.descripcion LIKE ?)
ORDER BY cl.descripcion asc;