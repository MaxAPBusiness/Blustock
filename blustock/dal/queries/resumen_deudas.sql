SELECT p.nombre_apellido || ' ' || c.descripcion, s.descripcion, m.cant,
m.id, pa.nombre_apellido || ' ' || ca.descripcion, u.descripcion, m.id_turno,
m.fecha_hora
FROM movimientos m
JOIN deudas d ON m.id=d.id_mov
JOIN stock s ON s.id=m.id_elem
JOIN personal p ON p.id = m.id_persona
JOIN clases c ON p.id_clase = c.id
JOIN turnos tu ON tu.id=m.id_turno
JOIN ubicaciones u ON u.id=tu.id_ubi
JOIN personal pa ON tu.id_panolero = pa.id
JOIN clases ca ON pa.id_clase=ca.id;