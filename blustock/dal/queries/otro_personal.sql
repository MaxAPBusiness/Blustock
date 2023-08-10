--Obtenemos id, nombre, clase y dni de personal filtrado por personal
SELECT p.id, p.nombre_apellido, cl.descripcion, p.dni 
FROM personal p
JOIN clases cl ON cl.id = p.id_clase
JOIN cats_clase cat ON cl.id_cat = cat.id
WHERE cat.descripcion = 'Personal' 
AND (p.nombre_apellido LIKE ?
OR cl.descripcion LIKE ?
OR p.dni LIKE ?);