SELECT cl.id, cl.descripcion, cat.descripcion
FROM clases cl
JOIN cats_clase cat ON cl.id_cat=cat.id
WHERE cl.descripcion LIKE ?
OR cat.descripcion LIKE ?;