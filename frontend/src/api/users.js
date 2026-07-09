import client from "./client";

export async function listUsuarios() {
  const { data } = await client.get("/usuarios");
  return data;
}

export async function createUsuario(payload) {
  const { data } = await client.post("/usuarios", payload);
  return data;
}

export async function updateUsuario(id, payload) {
  const { data } = await client.put(`/usuarios/${id}`, payload);
  return data;
}
