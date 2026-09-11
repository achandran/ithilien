-- Window-local diff presentation; restored when diff mode ends.
local M = {}
local saved = {}
-- Infer direction only for a two-pane Gitsigns index/worktree pair of one file.
local function roles(wins)
  local diffwins, result = {}, {}
  for _,w in ipairs(wins) do if vim.wo[w].diff then table.insert(diffwins,w) end end
  if #diffwins ~= 2 then return result end
  for _,w in ipairs(diffwins) do
    local b=vim.api.nvim_win_get_buf(w)
    local role=vim.b[b].ithilien_diff_role
    if role=='old' or role=='new' then result[w]=role end
  end
  if result[diffwins[1]] and result[diffwins[2]] and result[diffwins[1]]~=result[diffwins[2]] then return result end
  result={}
  for _,w in ipairs(diffwins) do
    local name=vim.api.nvim_buf_get_name(vim.api.nvim_win_get_buf(w))
    local root,file=name:match('^gitsigns://(.-)/%.git//:0:(.+)$')
    if root then
      local other=diffwins[1]==w and diffwins[2] or diffwins[1]
      local b=vim.api.nvim_win_get_buf(other)
      if vim.bo[b].buftype=='' and vim.api.nvim_buf_get_name(b)==root..'/'..file then
        result[w]='old'; result[other]='new'
      end
    end
  end
  return result
end
function M.refresh()
  local wins = vim.api.nvim_tabpage_list_wins(0)
  local direction = roles(wins)
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
        local mappings = {}
        for entry in saved[w].winhighlight:gmatch('[^,]+') do
          local key=entry:match('^([^:]+):')
          if key~='DiffDelete' and (not direction[w] or (key~='DiffText' and key~='DiffTextAdd')) then table.insert(mappings,entry) end
        end
        table.insert(mappings,'DiffDelete:IthilienDiffFiller')
        if direction[w] then
          local target=direction[w]=='old' and 'GitSignsDeleteInline' or 'GitSignsAddInline'
          table.insert(mappings,'DiffText:'..target)
          table.insert(mappings,'DiffTextAdd:'..target)
        end
        vim.wo.winhighlight=table.concat(mappings,',')
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
function M.setup()
  -- Preserve unrelated options while requesting character-sized inline edits.
  if vim.fn.has('nvim-0.12') == 1 then
    vim.opt.diffopt:remove({'inline:simple','inline:word'})
    vim.opt.diffopt:append('inline:char')
  end
  local group = vim.api.nvim_create_augroup('IthilienDiff', {clear=true})
  vim.api.nvim_create_autocmd({'BufWinEnter','WinEnter','FileType'}, {group=group, callback=function() vim.schedule(M.refresh) end})
  vim.api.nvim_create_autocmd('OptionSet', {group=group, pattern='diff', callback=function() vim.schedule(M.refresh) end})
end
return M
