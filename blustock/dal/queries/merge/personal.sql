--Obtenemos el nombre viejo, dni, nombre nuevo y clase nueva
SELECT p.nombre_apellido, p.dni, pn.nombre_apellido, cn.descripcion
FROM personal p
JOIN clases c ON p.id_clase = c.id
LEFT JOIN personal_nuevo pn ON p.dni = pn.dni
LEFT JOIN clases cn ON pn.id_curso = cn.id
JOIN cats_clase cat ON c.id_cat = cat.id
WHERE cat.descripcion LIKE 'Personal'
UNION
-- Obtenemos nombre viejo, dni nuevo, nombre nuevo y clase nueva.
SELECT p.nombre_apellido, pn.dni, pn.nombre_apellido, cn.descripcion
FROM personal_nuevo pn
JOIN clases cn ON pn.id_curso = pn.id
LEFT JOIN personal p
ON p.dni = pn.dni