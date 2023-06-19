SELECT p.id, p.nombre_apellido, c.descripcion, p.dni 
FROM personal p
JOIN clases c ON c.descripcion = p.id_clase
WHERE c.descripcion NOT IN ( 'profesor', 'egresado'
) AND (p.nombre_apellido LIKE ?
OR c.descripcion LIKE ?
OR p.dni LIKE ?);