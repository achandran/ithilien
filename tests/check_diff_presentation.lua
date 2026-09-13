vim.opt.rtp:prepend(vim.env.KANSO_ROOT)
vim.opt.rtp:prepend(vim.fn.getcwd())
local initial_diffopt=vim.o.diffopt
assert(not package.loaded['ithilien.diff'], 'Diff setup ran before colorscheme selection')
vim.cmd.colorscheme('ithilien-dawn')
local autocmd_count=#vim.api.nvim_get_autocmds({group='IthilienDiff'})
vim.cmd('filetype on')
vim.cmd('syntax on')
local path=vim.fn.getcwd()..'/tests/fixtures/diff-presentation/ghosttyconfig.after.conf'
local old=vim.fn.readfile('tests/fixtures/diff-presentation/ghosttyconfig.before.conf')
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
-- Repeated selection must not duplicate handlers or overwrite original options.
vim.cmd('diffthis')
vim.cmd.colorscheme('ithilien-dawn')
vim.cmd.colorscheme('ithilien-dawn')
assert(#vim.api.nvim_get_autocmds({group='IthilienDiff'})==autocmd_count)
assert(vim.wo[left].winbar~='')
-- Restore windows even when their tab is not current.
vim.cmd('tabnew')
vim.cmd.colorscheme('default')
assert(vim.wait(1000,function() return vim.wo[left].winbar=='' end,10))
assert(vim.wo[left].winbar=='' and vim.wo[left].winhighlight=='')
vim.cmd.colorscheme('ithilien-dawn')
assert(vim.wo[left].winbar~='')
vim.cmd.colorscheme('default')
assert(vim.wait(1000,function() return vim.wo[left].winbar=='' end,10))
assert(vim.wo[left].winhighlight=='')
assert(vim.o.diffopt==initial_diffopt, 'Original diffopt was not restored')
vim.cmd.colorscheme('ithilien-dawn')
vim.opt.diffopt:append('iwhite')
local user_diffopt=vim.o.diffopt
vim.cmd.colorscheme('default')
assert(vim.wait(1000,function() return vim.wo[left].winbar=='' end,10))
assert(vim.o.diffopt==user_diffopt, 'User diffopt change was overwritten')
print('Exact index/worktree diff passed: missing l emphasized, matching conf syntax, labeled panes, subdued filler, settings restored')
vim.cmd('qa!')
