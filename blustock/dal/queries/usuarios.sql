-- Obtenemos id, nombre, clase, dni, usuario y contraseña
SELECT p.id, p.nombre_apellido, c.descripcion, p.dni, p.usuario, p.contrasena
FROM personal p
JOIN clases c ON c.id = p.id_clase
JOIN cats_clase cat ON c.id_cat = cat.id
WHERE cat.descripcion = 'Usuario'
AND (p.nombre_apellido LIKE ?
OR p.usuario LIKE ?
OR c.descripcion LIKE ?
OR p.dni LIKE ?)
ORDER BY p.nombre_apellido;