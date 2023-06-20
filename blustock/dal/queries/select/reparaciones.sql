SELECT r.id, s.descripcion, cantidad, p.nombre_apellido, destino, fecha_envio,fecha_regreso 
FROM reparaciones r
JOIN stock s ON s.id = r.id_herramienta
join personal p ON p.id = r.id_usuario
