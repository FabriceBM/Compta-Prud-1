-- Corrigés : un bloc  ::: {.corrige} … :::  n'est publié que si la page déclare `corriges: true`
-- dans son en-tête. Sinon il est remplacé par une mention « publié après la séance » et rien de ce
-- qu'il met en lien (PDF, notebook, script) n'est copié dans le site.
-- Version enseignant, tous corrigés visibles : CORRIGES=tous quarto render  (make site-enseignant).

local publier = false

local function lire_meta(meta)
  publier = meta.corriges == true or os.getenv("CORRIGES") == "tous"
end

local function bloc(div)
  if not div.classes:includes("corrige") then
    return nil
  end
  if publier then
    return div.content
  end
  return pandoc.Div(
    pandoc.Para({ pandoc.Emph({ pandoc.Str("Corrigé publié après la séance.") }) }),
    pandoc.Attr("", { "corrige-masque" })
  )
end

return { { Meta = lire_meta }, { Div = bloc } }
