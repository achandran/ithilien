-- Real plugin renderers, isolated deterministic Python content.
return function(scene, state)
  vim.cmd('enew!')
  -- Keep picker inputs separate from XDG caches and plugin logs.
  local project=vim.fn.getcwd()..'/project'
  vim.fn.mkdir(project,'p')
  local fixture=project..'/palette_workflow.py'
  local lines={
    'from dataclasses import dataclass', 'from typing import Iterable', '',
    '@dataclass', 'class Reading:', '    value: float', 'LIMIT = 10',
    'async def summarize(readings: Iterable[Reading]) -> str:',
    '    """Summarize sensor readings."""',
    '    values = [item.value for item in readings if item.value >= 0]',
    '    total = sum(values)', '    return f"total={total:.2f}"', '',
    'result: int = "invalid"', '# TODO: validate the sensor input',
    'summarize([])',
  }
  vim.fn.writefile(lines,fixture)
  vim.cmd.edit(vim.fn.fnameescape(fixture))
  vim.bo.filetype='python'
  vim.treesitter.start(0,'python')
  vim.opt.number=true
  vim.opt.relativenumber=false
  vim.opt.laststatus=3
  vim.opt.showtabline=2
  local buf=vim.api.nvim_get_current_buf()
  local ns=vim.api.nvim_create_namespace('ithilien-workflow')
  vim.diagnostic.set(ns,buf,{{lnum=13,col=0,end_col=6,severity=1,message='Incompatible assignment: str to int',source='deterministic fixture'}})
  if state=='reload' then vim.cmd('colorscheme ithilien-dawn') end
  local lsp_evidence=nil
  if scene=='python-lsp' then
    vim.diagnostic.reset(ns,buf)
    local command=vim.env.ITHILIEN_LSP_COMMAND
    assert(command and vim.fn.executable(command)==1,'Set ITHILIEN_LSP_COMMAND to basedpyright-langserver')
    local id=vim.lsp.start({name='workflow-basedpyright',cmd={command,'--stdio'},root_dir=vim.fn.getcwd(),
      capabilities={workspace={didChangeWatchedFiles={dynamicRegistration=false}}},
      settings={basedpyright={analysis={typeCheckingMode='standard',diagnosticMode='openFilesOnly'}}}})
    local client=assert(vim.lsp.get_client_by_id(id))
    assert(vim.wait(5000,function() return client.initialized end,20),'LSP initialization timeout')
    local response=client:request_sync('textDocument/semanticTokens/full',{textDocument={uri=vim.uri_from_bufnr(buf)}},5000,buf)
    assert(response and response.result and #response.result.data>0,'No Python semantic tokens')
    vim.lsp.semantic_tokens.start(buf,id)
    assert(vim.wait(5000,function() return #vim.diagnostic.get(buf)>0 end,20),'No live Python diagnostics')
    lsp_evidence={server=client.name,semantic_tokens=#response.result.data/5}
  elseif scene=='python-diff' then
    vim.cmd('diffthis')
    vim.cmd('vnew')
    local before=vim.deepcopy(lines)
    before[7]='LIMIT = 11'
    before[10]=before[10]:gsub('>=','>')
    before[12]='    return str(total)'
    vim.api.nvim_buf_set_lines(0,0,-1,false,before)
    vim.bo.filetype='python';vim.treesitter.start(0,'python');vim.cmd('diffthis');vim.cmd('diffupdate')
  elseif scene=='python-search' then
    vim.fn.setreg('/', 'values');vim.o.hlsearch=true;vim.cmd('normal! gg')
  elseif scene=='python-visual' then
    vim.api.nvim_win_set_cursor(0,{10,0});vim.cmd('normal! Vj')
  elseif scene=='python-diagnostic' then
    vim.api.nvim_win_set_cursor(0,{14,0});vim.defer_fn(function() vim.diagnostic.open_float({scope='line',focus=false}) end,150)
  elseif scene=='neo-tree' then
    require('neo-tree.command').execute({action='show',source='filesystem',dir=project,position='right'})
  elseif scene=='trouble' then
    require('trouble').open({mode='diagnostics',focus=false})
  elseif scene=='which-key' then
    local prefix=(vim.g.mapleader or ' ')..'z'
    vim.keymap.set('n',prefix..'t',function() end,{desc='Inspect Python'})
    vim.defer_fn(function() require('which-key').show({keys=prefix,global=true}) end,150)
  elseif scene=='grug-far' then
    require('grug-far').open({prefills={search='values',paths=fixture}})
  elseif scene=='fzf-lua' then
    require('fzf-lua').files({cwd=project,winopts={preview={hidden='hidden'}}})
  elseif scene=='dashboard' then
    Snacks.dashboard.open()
  elseif scene=='blink' then
    vim.api.nvim_buf_set_lines(buf,-1,-1,false,{'summ'})
    vim.api.nvim_win_set_cursor(0,{vim.api.nvim_buf_line_count(buf),4});vim.cmd('startinsert!')
    vim.defer_fn(function() require('blink.cmp').show({providers={'buffer'}}) end,150)
  end
  _G.ithilien_workflow_evidence=function()
    local history={}
    if package.loaded['noice.message.manager'] then
      for _,msg in ipairs(require('noice.message.manager').get(nil,{history=true})) do history[#history+1]=msg:content() end
    end
    local windows={}
    for _,w in ipairs(vim.api.nvim_list_wins()) do
      local wb=vim.api.nvim_win_get_buf(w)
      local first=vim.api.nvim_win_call(w,function() return vim.fn.line('w0') end)
      local last=vim.api.nvim_win_call(w,function() return vim.fn.line('w$') end)
      windows[#windows+1]={text=table.concat(vim.api.nvim_buf_get_lines(wb,first-1,last,false),'\n'),filetype=vim.bo[wb].filetype,blend=vim.wo[w].winblend,floating=vim.api.nvim_win_get_config(w).relative~=''}
    end
    local plugins={}
    for name,p in pairs(require('lazy.core.config').plugins) do
      if p._.loaded then plugins[#plugins+1]=name end
    end
    return {bufferline_parents=require('bufferline.config').get().highlights.buffer_visible,history=history,lsp=lsp_evidence,parser=vim.treesitter.highlighter.active[buf]~=nil,windows=windows,plugins=plugins,
      messages=_G.ithilien_messages,mode=vim.fn.mode(),blink_visible=package.loaded['blink.cmp'] and require('blink.cmp').is_visible() or false}
  end
end
