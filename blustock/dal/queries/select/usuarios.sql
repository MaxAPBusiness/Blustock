SELECT p.dni, p.nombre_apellido, p.usuario, p.contrasena, c.descripcion,  
FROM personal p
JOIN clases c ON c.descripcion = p.id_clase
WHERE p.usuario IS NOT NULL
AND (p.nombre_apellido LIKE ?
OR p.usuario LIKE ?
OR c.descripcion LIKE ?
OR p.dni LIKE ?);