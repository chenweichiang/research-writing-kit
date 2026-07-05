-- lt_strip_noprose.lua — pandoc filter for lt_check.sh
-- Drops "non-prose" nodes so LanguageTool doesn't false-flag grammar in
-- code / math / citation keys. Discards: code blocks & inline code, math,
-- citation keys, raw (HTML/TeX).
function CodeBlock(_) return {} end
function Code(_) return {} end
function Math(_) return {} end
function RawBlock(_) return {} end
function RawInline(_) return {} end
function Cite(_) return {} end
