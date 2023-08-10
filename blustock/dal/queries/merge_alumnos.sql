--Obtenemos el nombre viejo, dni, nombre nuevo y clase nueva
SELECT a.nombre_apellido, a.dni, an.nombre_apellido, cn.descripcion
FROM personal a
JOIN clases c ON a.id_clase = c.id
LEFT JOIN alumnos_nuevos an ON a.dni = an.dni
LEFT JOIN clases cn ON an.id_curso = cn.id
JOIN cats_clase cat ON c.id_cat = cat.id
WHERE cat.descripcion LIKE 'Alumno'
UNION
-- Obtenemos nombre viejo, dni nuevo, nombre nuevo y clase nueva.
SELECT a.nombre_apellido, an.dni, an.nombre_apellido, cn.descripcion
FROM alumnos_nuevos an
JOIN clases cn ON an.id_curso = cn.id
LEFT JOIN personal a
ON a.dni = an.dni