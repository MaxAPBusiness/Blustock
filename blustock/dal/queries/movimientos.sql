SELECT m.id_turno, s.descripcion, e.descripcion, p.nombre_apellido,
m.fecha_hora, m.cant, t.descripcion, m.motivo, u.descripcion
FROM movimientos m
JOIN stock s ON s.id=m.id_elem
JOIN estados e ON e.id =m.id_estado
JOIN personal p ON p.dni = m.id_persona
JOIN tipos_mov t ON t.id=m.id_tipo
JOIN ubicaciones u ON u.id=m.id_ubi
WHERE m.id_turno LIKE ?
OR s.descripcion LIKE ?
OR e.descripcion LIKE ?
OR p.nombre_apellido LIKE ?
OR m.fecha_hora LIKE ?
OR m.cant LIKE ?
OR t.descripcion LIKE ?
OR m.motivo LIKE ?
OR u.descripcion LIKE ?;