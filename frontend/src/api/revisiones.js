import client from "./client";

export async function getRevisionEstrategica(familiaId) {
  const { data } = await client.get(`/familias/${familiaId}/revision`);
  return data;
}

export async function updateRevisionEstrategica(familiaId, payload) {
  const { data } = await client.put(`/familias/${familiaId}/revision`, payload);
  return data;
}