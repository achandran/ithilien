-- Capture actual Python Tree-sitter roles in an isolated nvim.
-- KANSO_ROOT=/path/kanso TS_ROOT=/path/nvim-treesitter/runtime TS_SITE=/path/nvim/site
-- nvim --headless -u NONE -i NONE -l scripts/check_python_syntax.lua
vim.opt.rtp:prepend(assert(vim.env.KANSO_ROOT))
vim.opt.rtp:prepend(assert(vim.env.TS_ROOT))
vim.opt.rtp:prepend(assert(vim.env.TS_SITE))
vim.opt.rtp:prepend(vim.fn.getcwd())
require('ithilien').load('day')
vim.cmd('edit reports/python-review/sample.py')
vim.bo.filetype='python'
vim.cmd('syntax on')
vim.cmd('set syntax=python')
vim.treesitter.start(0,'python')
local parser=vim.treesitter.get_parser(0,'python')
local tree=parser:parse()[1]
assert(not tree:root():has_error(),'Python fixture must parse without errors')
local function resolve(name)
  while name~='' do
    if vim.fn.hlexists(name)==1 then
      local h=vim.api.nvim_get_hl(0,{name=name,link=false})
      if next(h) then return name,h end
    end
    name=name:match('^(.*)%.[^.]+$') or ''
  end
  return 'Normal',vim.api.nvim_get_hl(0,{name='Normal',link=false})
end
local rows={}
for row,line in ipairs(vim.api.nvim_buf_get_lines(0,0,-1,false)) do
  local cells={}
  for col=0,#line-1 do
    local captures=vim.treesitter.get_captures_at_pos(0,row-1,col)
    local chosen=nil
    for _,cap in ipairs(captures) do
      if cap.capture ~= "spell" and cap.capture ~= "nospell" and (not chosen or (tonumber(cap.metadata.priority) or 100)>=(tonumber(chosen.metadata.priority) or 100)) then chosen=cap end
    end
    local group,style=resolve(chosen and '@'..chosen.capture..'.python' or 'Normal')
    table.insert(cells,{text=line:sub(col+1,col+1),capture=chosen and chosen.capture or '',group=group,
                       style=style})
  end
  table.insert(rows,{text=line,cells=cells})
end
vim.fn.writefile({vim.json.encode({version=vim.version(),rows=rows})},'reports/python-review/neovim.json')
print(#rows..' Python lines parsed and captured')
vim.cmd('qa!')
