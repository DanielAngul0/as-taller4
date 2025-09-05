// Inicialización de la base de datos reservas_db en MongoDB

db = db.getSiblingDB("reservas_db");

// Crear colección de reservas con datos de ejemplo
db.createCollection("reservas");
db.reservas.insertMany([
  {
    usuario_id: 1,
    vuelo_id: 101,
    estado: "pendiente",
    fecha_reserva: new Date(),
    historial: [
      { accion: "creada", fecha: new Date() }
    ]
  },
  {
    usuario_id: 2,
    vuelo_id: 102,
    estado: "pagado",
    fecha_reserva: new Date(),
    historial: [
      { accion: "creada", fecha: new Date() },
      { accion: "pagada", fecha: new Date() }
    ]
  }
]);

// Crear colección de preferencias_usuario con datos de ejemplo
db.createCollection("preferencias_usuario");
db.preferencias_usuario.insertMany([
  {
    usuario_id: 1,
    preferencias: {
      comida: "vegetariana",
      equipaje_extra: true,
      asiento: "ventana"
    }
  },
  {
    usuario_id: 2,
    preferencias: {
      comida: "normal",
      equipaje_extra: false,
      asiento: "pasillo"
    }
  }
]);
