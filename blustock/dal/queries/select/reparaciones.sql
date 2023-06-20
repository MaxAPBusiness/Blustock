SELECT r.id, s.descripcion, r.cantidad, p.nombre_apellido, r.destino, r.fecha_envio, r.fecha_regreso 
FROM reparaciones r
JOIN stock s ON s.id = r.id_herramienta
JOIN personal p ON p.id = r.id_usuario
WHERE r.id LIKE ?
OR s.descripcion LIKE ?
OR r.cantidad LIKE ?
OR p.nombre_apellido LIKE ?
OR r.destino LIKE ?
OR r.fecha_envio LIKE ?
OR r.fecha_regreso LIKE ? 
