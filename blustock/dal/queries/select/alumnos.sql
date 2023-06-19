SELECT p.id, p.nombre_apellido, c.descripcion, p.dni 
FROM personal p
JOIN clases c ON c.id = p.id_clase
WHERE c.descripcion IN (
    '1A', '1B', '1C', '2A', '2B', '2C', '3A', '3B', '3C', '4A', '4B', '4C',
    '5A', '5B', '6A', '6B', '6C', '7A', '7B', '7C', 'Egresado'
) AND (p.nombre_apellido LIKE ?
OR c.descripcion LIKE ?
OR p.dni LIKE ?);