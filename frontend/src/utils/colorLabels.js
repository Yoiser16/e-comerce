export const COLOR_LABELS = {
  negro_natural: 'Negro Natural',
  negro_azabache: 'Negro Azabache',
  castano_oscuro: 'Castaño Oscuro',
  castano_medio: 'Castaño Medio',
  castano_claro: 'Castaño Claro',
  castano_chocolate: 'Castaño Chocolate',
  rubio_oscuro: 'Rubio Oscuro',
  rubio_medio: 'Rubio Medio',
  rubio_claro: 'Rubio Claro',
  rubio_platino: 'Rubio Platino',
  rubio_cenizo: 'Rubio Cenizo',
  rubio_miel: 'Rubio Miel',
  pelirrojo: 'Pelirrojo',
  cobrizo: 'Cobrizo',
  borgona: 'Borgoña',
  rosa: 'Rosa',
  azul: 'Azul',
  morado: 'Morado',
  verde: 'Verde',
  gris: 'Gris',
  ombre: 'Ombré',
  balayage: 'Balayage',
  highlights: 'Highlights'
}

export const formatColorLabel = (color) => COLOR_LABELS[color] || color || ''
