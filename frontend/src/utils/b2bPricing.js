export const normalizeB2BTiers = (tiers = []) => {
  return (Array.isArray(tiers) ? tiers : [])
    .filter(t => t && Number(t.cantidad_minima) > 0)
    .map(t => ({
      cantidad_minima: Number(t.cantidad_minima),
      descuento_porcentaje: Math.max(0, Math.min(90, Number(t.descuento_porcentaje || 0)))
    }))
    .sort((a, b) => a.cantidad_minima - b.cantidad_minima)
}

export const getTierForQty = (tiers, qty) => {
  const normalized = normalizeB2BTiers(tiers)
  const cantidad = Number(qty || 0)
  let selected = null
  normalized.forEach((tier) => {
    if (cantidad >= tier.cantidad_minima) {
      selected = tier
    }
  })
  return selected
}

export const getUnitPriceForQty = (basePrice, qty, tiers) => {
  const base = Number(basePrice || 0)
  const tier = getTierForQty(tiers, qty)
  if (!tier) return base
  const pct = tier.descuento_porcentaje || 0
  return base * (1 - pct / 100)
}
