/*Obtenemos la herramienta, cantidad adeudada, persona que adeuda,
fecha y hora del registro de la deuda, id de movimiento, id de turno,
nombre y curso del pañolero a cargo del turno*/
SELECT h.descripcion || ' ' || u.descripcion, d.cant, pe.nombre_apellido || ' ' || cpe.descripcion,
m.fecha_hora, m.id, m.id_turno, pa.nombre_apellido || ' ' || cpa.descripcion
FROM deudas d
JOIN movimientos m ON d.id_mov=m.id
JOIN stock h ON m.id_elem = h.id
JOIN ubicaciones u ON u.id = h.id_ubi
JOIN personal pe ON m.id_persona=pe.id
JOIN clases cpe ON pe.id_clase=cpe.id
LEFT JOIN turnos t ON m.id_turno = t.id
LEFT JOIN personal pa ON t.id_panolero=pa.id
LEFT JOIN clases cpa ON pa.id_clase = cpa.id
WHERE m.id LIKE ?
AND (m.id_turno LIKE ? OR m.id_turno IS NULL)
AND (
    pa.nombre_apellido || ' ' || cpa.descripcion LIKE ?
    OR pa.nombre_apellido || ' ' || cpa.descripcion IS NULL
) AND (h.descripcion LIKE ?
OR d.cant LIKE ?
OR pe.nombre_apellido || ' ' || cpe.descripcion LIKE ?
OR m.fecha_hora LIKE ?
OR m.id LIKE ?
OR m.id_turno LIKE ?
OR pa.nombre_apellido || ' ' || cpa.descripcion LIKE ?);