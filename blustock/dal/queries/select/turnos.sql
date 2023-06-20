SELECT t.id, p.nombre_apellido, t.fecha_ing, t.fecha_egr,(select p.nombre_apellido WHERE p.id=t.id_prof_ing), (select p.nombre_apellido WHERE p.id=t.id_prof_egr)
, u.descripcion
FROM turnos t
JOIN personal p ON t.id_panolero =p.id
JOIN ubicaciones u ON t.id_ubi=u.id


