vim.opt.rtp:prepend(vim.env.KANSO_ROOT)
vim.opt.rtp:prepend(vim.fn.getcwd())
require('ithilien').load('dawn')
require('ithilien.diff').setup()
vim.cmd('filetype on')
vim.cmd('syntax on')
local path=vim.fn.getcwd()..'/evaluation/fixtures/ithilien/ghosttyconfig.after.conf'
local old=vim.fn.readfile('evaluation/fixtures/ithilien/ghosttyconfig.before.conf')
vim.api.nvim_buf_set_lines(0,0,-1,false,old)
vim.b.ithilien_diff_label='INDEX'
vim.cmd('diffthis')
local left=vim.api.nvim_get_current_win()
vim.cmd('vsplit '..vim.fn.fnameescape(path))
local right=vim.api.nvim_get_current_win()
vim.bo.filetype='conf'
vim.b.ithilien_diff_label='WORKING COPY'
vim.cmd('diffthis')
vim.cmd('diffupdate')
require('ithilien.diff').refresh()
assert(vim.bo[vim.api.nvim_win_get_buf(left)].filetype=='conf')
local found=false
vim.api.nvim_set_current_win(left)
for n,line in ipairs(old) do
 if line=='font-style-bold-italic = false' then
  local col=assert(line:find('l',line:find('false'),true))
  local group=vim.fn.synIDattr(vim.fn.diff_hlID(n,col),'name')
  assert(group=='DiffText' or group=='DiffTextAdd',group)
  found=true
 end
end
assert(found)
for _,w in ipairs({left,right}) do
 assert(vim.wo[w].fillchars:find('diff:·',1,true))
 assert(vim.wo[w].winhighlight:find('DiffDelete:IthilienDiffFiller',1,true))
end
vim.cmd('diffoff!')
require('ithilien.diff').refresh()
for _,w in ipairs({left,right}) do assert(vim.wo[w].winbar=='');assert(vim.wo[w].winhighlight=='') end
print('Exact index/worktree diff passed: missing l emphasized, matching conf syntax, labeled panes, subdued filler, settings restored')
vim.cmd('qa!')
