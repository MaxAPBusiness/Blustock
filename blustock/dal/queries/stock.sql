SELECT s.id, s.descripcion, s.cant_condiciones, s.cant_reparacion,
s.cant_baja, s.cant_prest, (CASE 
WHEN s.cant_reparacion IS NULL THEN s.cant_condiciones + s.cant_prest
ELSE s.cant_condiciones + s.cant_reparacion + s.cant_baja + s.cant_prest END) total,
g.descripcion, sub.descripcion, u.descripcion
FROM stock s
JOIN subgrupos sub ON s.id_subgrupo = sub.id
JOIN grupos g ON sub.id_grupo=g.id
JOIN ubicaciones u ON s.id_ubi=u.id
WHERE u.descripcion LIKE ? 
AND (s.descripcion LIKE ?
OR s.cant_condiciones LIKE ?
OR s.cant_reparacion LIKE ?
OR s.cant_baja LIKE ?
OR g.descripcion LIKE ?
OR sub.descripcion LIKE ?
OR u.descripcion LIKE ?
OR s.cant_prest LIKE ?);