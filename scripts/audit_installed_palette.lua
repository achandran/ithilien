-- Run through audit_installed_palette.py; uses the actual user config without installing plugins.
vim.opt.rtp:prepend(assert(vim.env.ITHILIEN_LAZY_ROOT, 'Set ITHILIEN_LAZY_ROOT'))
local lazy=require('lazy');local setup=lazy.setup
lazy.setup=function(o)
 o.install={missing=false};o.checker={enabled=false};o.change_detection={enabled=false};o.readme={enabled=false}
 o.lockfile=vim.env.ITHILIEN_AUDIT_OUTPUT..'/lock.json';o.state=vim.env.ITHILIEN_AUDIT_OUTPUT..'/state.json';table.insert(o.spec,{ 'achandran/ithilien', dir=assert(vim.env.ITHILIEN_ROOT, 'Set ITHILIEN_ROOT') });return setup(o)
end
dofile(assert(vim.env.ITHILIEN_NVIM_INIT, 'Set ITHILIEN_NVIM_INIT'))
vim.schedule(function()
 local r={plugins={},snapshots={}}
 local s=vim.json.decode(table.concat(vim.fn.readfile(vim.env.ITHILIEN_ROOT..'/scripts/palette/ithilien.json'),'\n')).variants['ithilien-dawn']
 r.palette=s.colors;r.theme=vim.g.colors_name
 local allowed={};for _,v in pairs(s.colors) do allowed[tonumber(v:sub(2),16)]=true end
 local function snap(label)
  local bad={};local count=0
  for n,h in pairs(vim.api.nvim_get_hl(0,{})) do
   count=count+1
   for _,a in ipairs({'fg','bg','sp'}) do if h[a] and not allowed[h[a]] then bad[#bad+1]={group=n,attribute=a,color=string.format('#%06X',h[a])} end end
  end
  r.snapshots[#r.snapshots+1]={label=label,groups=count,off_palette=bad}
 end
 snap('startup')
 local skip={catppuccin=true,['tokyonight.nvim']=true,['dark-notify']=true}
 for n,p in pairs(require('lazy.core.config').plugins) do
  local status
  if skip[n] then status='excluded alternate theme or appearance watcher'
  elseif vim.fn.isdirectory(p.dir)==0 then status='missing'
  else local ok,e=pcall(lazy.load,{plugins={n}});status=ok and (p._.loaded and 'loaded' or 'not loaded') or tostring(e) end
  r.plugins[#r.plugins+1]={name=n,status=status}
 end
 vim.wait(100);snap('plugins loaded');vim.cmd('colorscheme ithilien-dawn');vim.wait(100);snap('theme reapplied')
 vim.fn.writefile({vim.json.encode(r)},vim.env.ITHILIEN_AUDIT_OUTPUT..'/result.json');local failed=false
 for _,stage in ipairs(r.snapshots) do if #stage.off_palette>0 then failed=true end end
 for _,plugin in ipairs(r.plugins) do if plugin.status~='loaded' and not plugin.status:match('^excluded') then failed=true end end
 vim.cmd(failed and 'cquit 1' or 'qa!')
end)
