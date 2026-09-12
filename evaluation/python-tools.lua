return function(scene,state)
  local errors={}
  vim.notify=function(msg,level) if level and level>=vim.log.levels.ERROR then errors[#errors+1]=tostring(msg) end end
  local python=assert(vim.env.ITHILIEN_TEST_PYTHON)
  local file=vim.fn.getcwd()..'/test_readings.py'
  vim.fn.writefile({'import pytest','','def test_pass():','    assert 6 * 7 == 42','','def test_fail():','    assert 6 * 7 == 43','','@pytest.mark.skip(reason="fixture")','def test_skip():','    assert False'},file)
  vim.fn.writefile({'[tool.pytest.ini_options]','addopts = "--color=no"'},'pyproject.toml')
  vim.cmd('edit '..file);vim.bo.filetype='python';vim.treesitter.start(0,'python')
  local source=vim.api.nvim_get_current_buf()
  local counts,stopped
  if scene:match('^neotest') then
    local nt=require('neotest')
    nt.setup({adapters={require('neotest-python')({python=python,runner='pytest'})},discovery={enabled=false},watch={enabled=false}})
    nt.run.run(file)
    assert(vim.wait(9000,function()
      for _,id in ipairs(nt.state.adapter_ids()) do
        counts=nt.state.status_counts(id)
        if counts and counts.passed==1 and counts.failed==1 and counts.skipped==1 then return true end
      end
    end,30),'pytest results unavailable: '..vim.inspect(counts)..table.concat(errors,';'))
    if scene=='neotest-summary' then nt.summary.open()
    else nt.output.open({position_id=file..'::test_fail',enter=true,short=true}) end
  else
    file=vim.fn.getcwd()..'/debug_readings.py'
    vim.fn.writefile({'def summarize():','    total = 42','    label = "sensor"','    print(total, label)','','summarize()'},file)
    vim.cmd('edit '..file);vim.bo.filetype='python';vim.treesitter.start(0,'python');source=vim.api.nvim_get_current_buf()
    local dap=require('dap');local ui=require('dapui')
    ui.setup({layouts={{elements={'scopes','breakpoints','stacks'},size=45,position='left'}}})
    dap.adapters.python={type='executable',command=python,args={'-m','debugpy.adapter'}}
    vim.api.nvim_win_set_cursor(0,{4,0});dap.toggle_breakpoint()
    dap.run({type='python',request='launch',name='Python fixture',program=file,pythonPath=python,console='internalConsole',justMyCode=true})
    assert(vim.wait(9000,function() local session=dap.session();return session and session.stopped_thread_id~=nil end,30),'debugpy breakpoint unavailable')
    stopped=true;ui.open()
  end
  if state=='reload' then vim.cmd('colorscheme ithilien-dawn') end
  _G.ithilien_workflow_evidence=function()
    local windows={}
    for _,w in ipairs(vim.api.nvim_list_wins()) do windows[#windows+1]={filetype=vim.bo[vim.api.nvim_win_get_buf(w)].filetype,text=table.concat(vim.api.nvim_buf_get_lines(vim.api.nvim_win_get_buf(w),0,-1,false),'\n')} end
    return {parser=vim.treesitter.highlighter.active[source]~=nil,counts=counts,stopped=stopped,windows=windows,errors=errors}
  end
end
