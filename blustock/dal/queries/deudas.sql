SELECT h.descripcion, d.cant, pe.nombre_apellido || ' ' || cpe.descripcion,
m.fecha_hora, m.id, m.id_turno, pa.nombre_apellido || ' ' || cpa.descripcion
FROM deudas d
JOIN movimientos m ON d.id_mov=m.id
JOIN stock h ON m.id_elem = h.id
JOIN personal pe ON m.id_persona=pe.id
JOIN clases cpe ON pe.id_clase=cpe.id
JOIN turnos t ON m.id_turno = t.id
JOIN personal pa ON t.id_panolero=pa.id
JOIN clases cpa ON pa.id_clase = cpa.id
WHERE m.id LIKE ?
AND m.id_turno LIKE ?
AND pa.nombre_apellido || ' ' || cpa.descripcion LIKE ?
AND (h.descripcion LIKE ?
OR d.cant LIKE ?
OR pe.nombre_apellido || ' ' || cpe.descripcion LIKE ?
OR m.fecha_hora LIKE ?
OR m.id LIKE ?
OR m.id_turno LIKE ?
OR pa.nombre_apellido || ' ' || cpa.descripcion LIKE ?);