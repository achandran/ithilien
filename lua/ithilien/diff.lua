-- Window-local diff presentation; restored when diff mode ends.
local M = {}
local saved = {}
local original_diffopt, applied_diffopt
local function refresh_tab(tab)
  local wins = vim.api.nvim_tabpage_list_wins(tab)
  local ft
  for _, w in ipairs(wins) do
    if vim.wo[w].diff then
      local value = vim.bo[vim.api.nvim_win_get_buf(w)].filetype
      if value ~= '' then ft = value; break end
    end
  end
  for _, w in ipairs(wins) do
    if vim.wo[w].diff and vim.g.colors_name == 'ithilien-dawn' then
      if not saved[w] then saved[w] = {fillchars=vim.wo[w].fillchars, winbar=vim.wo[w].winbar,winhighlight=vim.wo[w].winhighlight} end
      vim.api.nvim_win_call(w, function()
        vim.opt_local.fillchars:append({diff='·'})
        if vim.g.colors_name == 'ithilien-dawn' then
          local mappings = vim.wo.winhighlight:gsub('DiffDelete:[^,]+,?', ''):gsub(',$','')
          vim.wo.winhighlight = (mappings ~= '' and mappings .. ',' or '') .. 'DiffDelete:IthilienDiffFiller'
        end
        local b = vim.api.nvim_get_current_buf()
        if vim.bo[b].filetype == '' and ft then vim.bo[b].filetype = ft end
        local name = vim.api.nvim_buf_get_name(b)
        local revision = name:match('^fugitive://') or name:match('^gitsigns://')
        local label = vim.b[b].ithilien_diff_label
          or (revision and 'REVISION' or (vim.bo[b].buftype == '' and 'FILE' or 'BUFFER'))
        vim.wo.winbar = ' ' .. label:gsub('%%','%%%%') .. ' · %f %m'
      end)
    elseif saved[w] then
      vim.wo[w].fillchars = saved[w].fillchars
      vim.wo[w].winbar = saved[w].winbar
      vim.wo[w].winhighlight = saved[w].winhighlight
      saved[w] = nil
    end
  end
  for w in pairs(saved) do if not vim.api.nvim_win_is_valid(w) then saved[w]=nil end end
end
function M.refresh()
  local active = vim.g.colors_name == 'ithilien-dawn' or vim.g.colors_name == 'ithilien-dusk'
  if active and not original_diffopt and vim.fn.has('nvim-0.12') == 1 then
    original_diffopt = vim.o.diffopt
    vim.opt.diffopt:remove({'inline:simple','inline:word'})
    vim.opt.diffopt:append('inline:char')
    applied_diffopt = vim.o.diffopt
  elseif not active and original_diffopt then
    -- Respect an intervening user or plugin edit.
    if vim.o.diffopt == applied_diffopt then vim.o.diffopt = original_diffopt end
    original_diffopt, applied_diffopt = nil, nil
  end
  for _, tab in ipairs(vim.api.nvim_list_tabpages()) do refresh_tab(tab) end
end
function M.setup()
  local group = vim.api.nvim_create_augroup('IthilienDiff', {clear=true})
  vim.api.nvim_create_autocmd({'BufWinEnter','WinEnter','FileType','ColorScheme'}, {
    group=group, callback=function() vim.schedule(M.refresh) end,
  })
  vim.api.nvim_create_autocmd('OptionSet', {group=group, pattern='diff', callback=function() vim.schedule(M.refresh) end})
  M.refresh()
end
return M
