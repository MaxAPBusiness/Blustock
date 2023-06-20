SELECT t.id, p.nombre_apellido, 
t.fecha_ing, 
t.fecha_egr,
(SELECT p.nombre_apellido WHERE p.id = t.id_prof_ing) prof_ing, 
(SELECT p.nombre_apellido WHERE p.id = t.id_prof_egr) prof_egr,
u.descripcion
FROM turnos t
JOIN personal p ON t.id_panolero =p.id
JOIN ubicaciones u ON t.id_ubi=u.id
WHERE t.id LIKE ?
OR p.nombre_apellido LIKE ?
OR t.fecha_ing LIKE ?
OR t.fecha_egr LIKE ?
OR prof_ing LIKE ?
OR prof_egr LIKE ?
OR u.descripcion LIKE ?


