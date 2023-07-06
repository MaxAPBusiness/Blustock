SELECT u.nombre_apellido || ' ' || u.usuario, h.fecha_hora, g.descripcion,
t.descripcion, h.id_fila, h.datos_viejos, h.datos_nuevos
FROM historial h
JOIN personal u ON h.id_usuario=u.id
JOIN tipos_cambio t ON h.id_tipo=t.id
JOIN gestiones g ON h.id_gest=g.id
WHERE g.descripcion LIKE ?
ORDER BY h.fecha_hora DESC;