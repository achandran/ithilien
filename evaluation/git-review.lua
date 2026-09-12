return function(scene,state)
  local function git(...)
    local args={'git','-c','core.hooksPath=/dev/null','-c','user.name=Theme Test','-c','user.email=theme@example.invalid'}
    vim.list_extend(args,{...})
    local result=vim.fn.system(args)
    assert(vim.v.shell_error==0,result)
  end
  vim.env.GIT_AUTHOR_DATE='2026-01-01T00:00:00Z'
  vim.env.GIT_COMMITTER_DATE='2026-01-01T00:00:00Z'
  git('init','-q');vim.fn.writefile({'nvim/'},'.git/info/exclude');git('config','commit.gpgsign','false')
  local before={'LIMIT = 10','', 'def accept(value):','    return value >= LIMIT','','# Remove this obsolete note'}
  vim.fn.writefile(before,'review.py');git('add','review.py');git('commit','-qm','Baseline','--date=2026-01-01T00:00:00Z')
  local after={'LIMIT = 11','','def accept(value):','    return value > LIMIT','','# Validate incoming readings'}
  vim.fn.writefile(after,'review.py')
  vim.cmd('edit review.py');vim.bo.filetype='python';vim.cmd('syntax on')
  vim.o.number=true;vim.o.signcolumn='yes'
  if scene=='diffview' then
    vim.cmd('DiffviewOpen')
    assert(vim.wait(4000,function()
      local n=0;for _,w in ipairs(vim.api.nvim_list_wins()) do if vim.wo[w].diff then n=n+1 end end
      return n>=2
    end,20),'Diffview panes unavailable')
  elseif scene=='neogit' then
    git('add','review.py')
    vim.fn.writefile({'# Pending work'},'pending.py')
    require('neogit').open({kind='replace'})
    assert(vim.wait(4000,function() return vim.bo.filetype=='NeogitStatus' and table.concat(vim.api.nvim_buf_get_lines(0,0,-1,false),'\n'):find('review.py',1,true)~=nil end,20),'Neogit status unavailable')
  else
    require('gitsigns').attach()
    assert(vim.wait(4000,function() return #(require('gitsigns').get_hunks() or {})>0 end,20),'Gitsigns hunks unavailable')
    vim.api.nvim_win_set_cursor(0,{1,0})
    require('gitsigns').preview_hunk()
    assert(vim.wait(2000,function()
      for _,w in ipairs(vim.api.nvim_list_wins()) do if vim.api.nvim_win_get_config(w).relative~='' then return true end end
    end,20),'Hunk preview unavailable')
  end
  if state=='reload' then vim.cmd('colorscheme ithilien-dawn') end
  _G.ithilien_workflow_evidence=function()
    local windows={}
    for _,w in ipairs(vim.api.nvim_list_wins()) do
      windows[#windows+1]={filetype=vim.bo[vim.api.nvim_win_get_buf(w)].filetype,diff=vim.wo[w].diff,floating=vim.api.nvim_win_get_config(w).relative~=''}
    end
    return {windows=windows,messages=vim.fn.execute('messages')}
  end
end
