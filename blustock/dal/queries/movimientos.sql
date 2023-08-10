--Obtenemos id, tipo de movimiento, elemento, estado del elemento,
--cantidad, motivo, persona que hico el movimiento, fecha y hora,
--turno, ubicación, nombre del pañolero y nombre del profesor que
--autorizó el ingreso del turno.
SELECT m.id, ti.descripcion, s.descripcion, e.descripcion, m.cant,
m.descripcion, p.nombre_apellido || ' ' || c.descripcion, m.fecha_hora,
m.id_turno, u.descripcion, pa.nombre_apellido || ' ' || ca.descripcion,
pr.nombre_apellido
FROM movimientos m
JOIN stock s ON s.id=m.id_elem
JOIN estados e ON e.id =m.id_estado
JOIN personal p ON p.id = m.id_persona
JOIN clases c ON p.id_clase = c.id
JOIN tipos_mov ti ON ti.id=m.id_tipo
LEFT JOIN turnos tu ON tu.id=m.id_turno
LEFT JOIN ubicaciones u ON u.id=tu.id_ubi
LEFT JOIN personal pa ON tu.id_panolero = pa.id
LEFT JOIN clases ca ON pa.id_clase=ca.id
LEFT JOIN personal pr ON tu.id_prof_ing = pr.id
WHERE m.id LIKE ?
AND m.id_turno LIKE ?
AND s.descripcion LIKE ?
AND p.nombre_apellido || ' ' || c.descripcion LIKE ?
AND pa.nombre_apellido || ' ' || ca.descripcion LIKE ?
AND (m.id_turno LIKE ?
OR s.descripcion LIKE ?
OR e.descripcion LIKE ?
OR p.nombre_apellido LIKE ?
OR m.fecha_hora LIKE ?
OR m.cant LIKE ?
OR ti.descripcion LIKE ?
OR u.descripcion LIKE ?
OR m.id LIKE ?
OR pa.nombre_apellido LIKE ?
OR pr.nombre_apellido LIKE ?
OR m.descripcion LIKE ?);