SELECT t.id, p.nombre_apellido, t.fecha, t.hora_ing, t.hora_egr, (
    p.nombre_apellido WHERE p.id=t.prof_ing
) prof_ing, (
    p.nombre_apellido WHERE p.id=t.prof_egr
) prof_egr, u.descripcion
FROM turnos t
JOIN personal p ON t.id_panolero =p.id
JOIN ubicaciones u ON t.id_ubi=u.id


