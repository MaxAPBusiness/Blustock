SELECT ti.descripcion, s.descripcion, e.descripcion, m.cant, p.nombre_apellido,
m.fecha_hora, m.motivo, m.id_turno, u.descripcion
FROM movimientos m
JOIN stock s ON s.id=m.id_elem
JOIN estados e ON e.id =m.id_estado
JOIN personal p ON p.dni = m.id_persona
JOIN tipos_mov ti ON ti.id=m.id_tipo
JOIN turnos tu ON tu.id=m.id_turno
JOIN ubicaiones u ON u.id=t.id_ubi
WHERE m.id_turno LIKE ?
OR s.descripcion LIKE ?
OR e.descripcion LIKE ?
OR p.nombre_apellido LIKE ?
OR m.fecha_hora LIKE ?
OR m.cant LIKE ?
OR ti.descripcion LIKE ?
OR m.motivo LIKE ?
OR u.descripcion LIKE ?;