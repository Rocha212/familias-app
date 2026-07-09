export default function Spinner({ size = 32 }) {
  return (
    <div
      className="animate-spin rounded-full border-4 border-surface-border border-t-navy"
      style={{ width: size, height: size }}
      role="status"
      aria-label="Cargando"
    />
  );
}
