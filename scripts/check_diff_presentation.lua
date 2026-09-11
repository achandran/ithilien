vim.opt.rtp:prepend(vim.env.KANSO_ROOT)
vim.opt.rtp:prepend(vim.fn.getcwd())
require('ithilien').load('dawn')
require('ithilien.diff').setup()
vim.cmd('filetype on')
vim.cmd('syntax on')
local path=vim.fn.getcwd()..'/comparison/scenarios/ghosttyconfig/working.conf'
local old=vim.fn.readfile('comparison/scenarios/ghosttyconfig/index.conf')
vim.api.nvim_buf_set_lines(0,0,-1,false,old)
vim.b.ithilien_diff_label='INDEX'
vim.b.ithilien_diff_role='old'
vim.cmd('diffthis')
local left=vim.api.nvim_get_current_win()
vim.cmd('vsplit '..vim.fn.fnameescape(path))
local right=vim.api.nvim_get_current_win()
vim.bo.filetype='conf'
vim.b.ithilien_diff_label='WORKING COPY'
vim.b.ithilien_diff_role='new'
vim.cmd('diffthis')
vim.cmd('diffupdate')
require('ithilien.diff').refresh()
assert(vim.bo[vim.api.nvim_win_get_buf(left)].filetype=='conf')
assert(vim.wo[left].winhighlight:find('DiffText:GitSignsDeleteInline',1,true))
assert(vim.wo[right].winhighlight:find('DiffTextAdd:GitSignsAddInline',1,true))
-- Exercise automatic Gitsigns provenance, then verify unknown pairs stay neutral.
local lb=vim.api.nvim_win_get_buf(left)
local rb=vim.api.nvim_win_get_buf(right)
vim.b[lb].ithilien_diff_role=nil; vim.b[rb].ithilien_diff_role=nil
vim.api.nvim_buf_set_name(lb,'gitsigns://'..vim.fn.getcwd()..'/.git//:0:comparison/scenarios/ghosttyconfig/working.conf')
require('ithilien.diff').refresh()
assert(vim.wo[left].winhighlight:find('DiffText:GitSignsDeleteInline',1,true))
assert(vim.wo[right].winhighlight:find('DiffText:GitSignsAddInline',1,true))
vim.api.nvim_buf_set_name(lb,'unrelated-revision')
require('ithilien.diff').refresh()
assert(not vim.wo[left].winhighlight:find('DiffText:',1,true))
assert(not vim.wo[right].winhighlight:find('DiffText:',1,true))
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
