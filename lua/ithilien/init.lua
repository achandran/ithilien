local M = {}

M.config = {
  bold = true,
  italics = true,
}

function M.setup(opts)
  M.config = vim.tbl_deep_extend("force", M.config, opts or {})
end

function M.load(variant)
  if variant ~= nil and variant ~= "dawn" and variant ~= "day" and variant ~= "light" then
    error("Unknown Ithilien variant: " .. tostring(variant))
  end
  require("ithilien.dawn").load(M.config)
  require("ithilien.diff").setup()
end

return M
