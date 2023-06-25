SELECT p.id,p.dni, p.nombre_apellido, c.descripcion  
FROM personal p
JOIN clases c ON c.id = p.id_clase
WHERE p.nombre_apellido LIKE ?
OR c.descripcion LIKE ?
OR p.dni LIKE ?;