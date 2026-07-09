import client from "./client";

export async function listFamilias(params) {
  const { data } = await client.get("/familias", { params });
  return data;
}

export async function getFamilia(id) {
  const { data } = await client.get(`/familias/${id}`);
  return data;
}

export async function createFamilia(payload) {
  const { data } = await client.post("/familias", payload);
  return data;
}

export async function updateFamilia(id, payload) {
  const { data } = await client.put(`/familias/${id}`, payload);
  return data;
}

export async function deleteFamilia(id) {
  await client.delete(`/familias/${id}`);
}

export async function duplicateFamilia(id) {
  const { data } = await client.post(`/familias/${id}/duplicar`);
  return data;
}

export async function downloadFamiliaPdf(id, nombreArchivo) {
  const response = await client.get(`/familias/${id}/pdf`, { responseType: "blob" });
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", nombreArchivo || `ficha_${id}.pdf`);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}
