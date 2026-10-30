-- Raccourcis de liens vers le dépôt GitHub. Le chemin part de la racine du dépôt.
--   {{< colab seances/04_be-vie/notebooks/premiers-pas-python.ipynb >}}   « Ouvrir dans Colab »
--   {{< github seances/03_be-non-vie/corriges/td-3-5_chain-ladder.py >}}  « Voir sur GitHub »
-- Le dépôt et la branche viennent de `depot` et `branche` dans _quarto.yml.

local function cible(args, meta)
  local depot = pandoc.utils.stringify(meta.depot or "")
  local branche = pandoc.utils.stringify(meta.branche or "main")
  return depot, branche, pandoc.utils.stringify(args[1] or "")
end

local function lien(texte, url)
  return pandoc.Link({ pandoc.Str(texte) }, url, "", pandoc.Attr("", {}, { { "target", "_blank" } }))
end

return {
  ["colab"] = function(args, kwargs, meta)
    local depot, branche, chemin = cible(args, meta)
    return lien("Ouvrir dans Colab",
      "https://colab.research.google.com/github/" .. depot .. "/blob/" .. branche .. "/" .. chemin)
  end,
  ["github"] = function(args, kwargs, meta)
    local depot, branche, chemin = cible(args, meta)
    return lien("Voir sur GitHub", "https://github.com/" .. depot .. "/blob/" .. branche .. "/" .. chemin)
  end,
}
