 <!-- Colecciones dinámicas en Mongo -->

# Colecciones MongoDB - Reservas Service

## reservas
{
  "_id": ObjectId,
  "usuario_id": int,
  "vuelo_id": int,
  "estado": "pendiente | pagado | check-in | cancelado",
  "fecha_reserva": ISODate,
  "historial": [
    { "accion": "creada", "fecha": ISODate },
    { "accion": "pagada", "fecha": ISODate }
  ]
}

## preferencias_usuario
{
  "_id": ObjectId,
  "usuario_id": int,
  "preferencias": {
    "comida": "vegetariana",
    "equipaje_extra": true,
    "asiento": "ventana"
  }
}
