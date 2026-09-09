-- Exercise Neovim's real character-level diff engine, not hand-assigned spans.
-- KANSO_ROOT=/path/to/kanso.nvim nvim --headless -u NONE -i NONE -l scripts/check_day_diff.lua
vim.opt.rtp:prepend(assert(vim.env.KANSO_ROOT, 'Set KANSO_ROOT'))
vim.opt.rtp:prepend(vim.fn.getcwd())
require('ithilien').load('day')
vim.opt.diffopt = 'internal,filler,closeoff,inline:char'
local cases = {
  {name='digit replacement', before='limit = 2', after='limit = 3', old={9}, new={9}},
  {name='inserted equals sign', before='ready = value', after='ready == value', old={}, new={7}},
  {name='separated changed digits', before='limits = { min = 2, max = 4 }', after='limits = { min = 3, max = 5 }', old={18,27}, new={18,27}},
  {name='removed space', before='return  value', after='return value', old={8}, new={}},
  {name='trailing space', before='return value', after='return value ', old={}, new={13}},
  {name='operator replacement', before='ready && valid', after='ready || valid', old={7,8}, new={7,8}},
}
local result = {version=vim.version(), diffopt=vim.o.diffopt, cases={}}
for _,case in ipairs(cases) do
  vim.cmd('only!')
  local old=vim.api.nvim_create_buf(false,true)
  vim.api.nvim_win_set_buf(0,old)
  vim.api.nvim_buf_set_lines(old,0,-1,false,{case.before})
  vim.cmd('diffthis')
  local left=vim.api.nvim_get_current_win()
  vim.cmd('vnew')
  vim.api.nvim_buf_set_lines(0,0,-1,false,{case.after})
  vim.cmd('diffthis')
  local right=vim.api.nvim_get_current_win()
  vim.cmd('diffupdate')
  local captured={name=case.name,before=case.before,after=case.after}
  for _,side in ipairs({{'before',left,case.before,case.old},{'after',right,case.after,case.new}}) do
    vim.api.nvim_set_current_win(side[2])
    local cells={}
    for col=1,#side[3] do
      local id=vim.fn.diff_hlID(1,col)
      local name=vim.fn.synIDattr(id,'name')
      if name=='DiffText' or name=='DiffTextAdd' then
        local hl=vim.api.nvim_get_hl(0,{name=name,link=false})
        assert(hl.fg==0 and hl.underline, 'Inline diff must be black and underlined')
        table.insert(cells,{column=col,text=side[3]:sub(col,col),group=name})
      end
    end
    local columns=vim.tbl_map(function(cell) return cell.column end,cells)
    assert(vim.deep_equal(columns,side[4]), case.name..' '..side[1]..': incorrect changed columns')
    captured[side[1]..'Cells']=cells
  end
  table.insert(result.cases,captured)
  vim.cmd('diffoff!')
end
vim.fn.writefile({vim.json.encode(result)},'reports/day-refinement/native-diffs.json')
print(#cases..' native character-diff cases passed; exact changed cells black and underlined')
vim.cmd('qa!')
