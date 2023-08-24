--Obtenemos el id, nombre, descripción y dni, filtrando por alumno.
SELECT p.id, p.nombre_apellido, cl.descripcion, p.dni 
FROM personal p
JOIN clases cl ON cl.id = p.id_clase
JOIN cats_clase cat ON cl.id_cat = cat.id
WHERE cat.descripcion = 'Alumno'
AND (p.nombre_apellido LIKE ?
OR p.id like ?
OR cl.descripcion LIKE ?
OR p.dni LIKE ?)
ORDER BY p.nombre_apellido;