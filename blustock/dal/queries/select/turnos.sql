SELECT t.id, p.nombre_apellido, 
t.fecha_ing, 
t.fecha_egr,
pi.nombre_apellido, 
pe.nombre_apellido,
u.descripcion
FROM turnos t
JOIN personal p ON t.id_panolero =p.id
JOIN personal pi ON pi.id = t.id_prof_ing
LEFT JOIN personal pe ON pe.id=t.id_prof_egr
JOIN ubicaciones u ON t.id_ubi=u.id
WHERE t.id LIKE ?
OR p.nombre_apellido LIKE ?
OR t.fecha_ing LIKE ?
OR t.fecha_egr LIKE ?
OR u.descripcion LIKE ?
OR pi.nombre_apellido LIKE ?
OR pe.nombre_apellido LIKE ?


