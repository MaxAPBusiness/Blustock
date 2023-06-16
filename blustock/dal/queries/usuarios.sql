SELECT p.nombre, p.usuario, c.descripcion, p.dni 
FROM personal p
JOIN clases c ON c.id = p.id_clase
WHERE p.usuario IS NOT NULL
AND (p.nombre LIKE ?
OR p.usuario LIKE ?
OR c.descripcion LIKE ?
OR p.dni LIKE ?);