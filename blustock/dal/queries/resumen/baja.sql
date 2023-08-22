--Esta es la consulta de elementos dados de baja de la pantalla resumen.
--Obtenemos persona, herramienta, cantidad, motivo de baja, id,
--pañolero, ubicación, id del turno y fecha y hora del movimiento.
SELECT p.nombre_apellido || ' ' || c.descripcion, s.descripcion, m.cant,
m.descripcion, m.id, pa.nombre_apellido || ' ' || ca.descripcion,
u.descripcion, m.id_turno, m.fecha_hora
FROM movimientos m
JOIN stock s ON s.id=m.id_elem
JOIN estados e ON m.id_estado=e.id
JOIN personal p ON p.id = m.id_persona
JOIN clases c ON p.id_clase = c.id
LEFT JOIN turnos tu ON tu.id=m.id_turno
JOIN ubicaciones u ON u.id=s.id_ubi
LEFT JOIN personal pa ON tu.id_panolero = pa.id
LEFT JOIN clases ca ON pa.id_clase=ca.id
WHERE e.descripcion='De Baja';
