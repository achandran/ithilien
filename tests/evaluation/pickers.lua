return function(scene,state)
  local errors={};vim.notify=function(m,l) if l and l>=vim.log.levels.ERROR then errors[#errors+1]=tostring(m) end end
  for _,name in ipairs({'reading.py','reading_test.py','other.py'}) do vim.fn.writefile({'def reading():','    return 42'},name) end
  vim.cmd('edit reading.py');vim.bo.filetype='python';vim.cmd('syntax on')
  if scene=='telescope' then
    require('telescope').setup({defaults={layout_config={width=0.95,height=0.85,preview_cutoff=0}}})
    require('telescope.builtin').find_files({cwd=vim.fn.getcwd(),default_text='reading'})
  elseif scene=='snacks' then
    Snacks.picker.files({cwd=vim.fn.getcwd(),pattern='reading',layout={preset='default',preview=true,layout={backdrop=false}}})
  else
    vim.cmd('runtime after/plugin/cmp_buffer.lua')
    local cmp=require('cmp')
    cmp.setup({sources={{name='buffer'}},completion={autocomplete=false},window={completion=cmp.config.window.bordered()}})
    vim.api.nvim_buf_set_lines(0,0,-1,false,{'reading reading_value reading_total','','read'})
    vim.api.nvim_win_set_cursor(0,{3,4});vim.cmd('startinsert!')
    vim.defer_fn(function() cmp.complete();vim.defer_fn(function() cmp.select_next_item() end,100) end,100)
  end
  if state=='reload' then vim.defer_fn(function() vim.cmd('colorscheme ithilien-dawn') end,400) end
  _G.ithilien_workflow_evidence=function()
    local windows={};for _,w in ipairs(vim.api.nvim_list_wins()) do
      local b=vim.api.nvim_win_get_buf(w);local preview=false
      if scene=='telescope' then local picker=require('telescope.actions.state').get_current_picker((function() for _,b in ipairs(vim.api.nvim_list_bufs()) do if vim.bo[b].filetype=='TelescopePrompt' then return b end end end)());preview=picker and picker.previewer and picker.previewer.state and picker.previewer.state.bufnr==b or false end
      windows[#windows+1]={preview=preview,filetype=vim.bo[b].filetype,text=table.concat(vim.api.nvim_buf_get_lines(b,0,-1,false),'\n')}
    end
    return {windows=windows,errors=errors,visible=scene=='cmp' and require('cmp').visible() or false}
  end
end
