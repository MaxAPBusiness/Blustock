SELECT p.id,p.dni, p.nombre_apellido, c.descripcion, p.usuario, p.contrasena  
FROM personal p
JOIN clases c ON c.id = p.id_clase
WHERE p.usuario IS NOT NULL
AND (p.nombre_apellido LIKE ?
OR p.usuario LIKE ?
OR c.descripcion LIKE ?
OR p.dni LIKE ?);