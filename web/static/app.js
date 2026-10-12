/* 操作系统与 AI 操作系统智能体团队 - 前端交互 */
"use strict";

document.querySelectorAll('.tab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('view-' + btn.dataset.view).classList.add('active');
  });
});

async function api(path, body) {
  const opt = { headers: { 'Content-Type': 'application/json' } };
  if (body !== undefined) opt.method = 'POST', opt.body = JSON.stringify(body);
  const resp = await fetch(path, opt);
  if (!resp.ok) throw new Error('HTTP ' + resp.status);
  return resp.json();
}
function show(el, data) {
  el.classList.remove('hidden');
  el.textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
}

/* 内核工程 */
async function kArch() {
  const r = await api('/api/tasks', { goal: '设计自主操作系统内核架构', params: { action: 'arch', arch: document.getElementById('kernelArch').value } });
  show(document.getElementById('kResult'), r.results[0].result);
}
async function kSched() {
  const r = await api('/api/tasks', { goal: '内核调度策略设计', params: { action: 'scheduler' } });
  show(document.getElementById('kResult'), r.results[0].result);
}
async function kMem() {
  const r = await api('/api/tasks', { goal: '内存管理设计', params: { action: 'memory' } });
  show(document.getElementById('kResult'), r.results[0].result);
}
async function kFs() {
  const r = await api('/api/tasks', { goal: '文件系统设计', params: { action: 'fs', fs_name: 'CNFS' } });
  show(document.getElementById('kResult'), r.results[0].result);
}
async function kDrv() {
  const r = await api('/api/tasks', { goal: '驱动框架设计', params: { action: 'driver' } });
  show(document.getElementById('kResult'), r.results[0].result);
}

/* 构建裁剪 */
async function bProfile() {
  const r = await api('/api/tasks', { goal: '系统构建与裁剪', params: { action: 'profile', profile: document.getElementById('buildProfile').value } });
  show(document.getElementById('bResult'), r.results[0].result);
}
async function bKconfig() {
  const r = await api('/api/tasks', { goal: '内核配置建议', params: { action: 'kernelconfig' } });
  show(document.getElementById('bResult'), r.results[0].result);
}

/* AI OS */
async function aFw() {
  const r = await api('/api/tasks', { goal: 'AI 操作系统系统级智能体框架', params: { action: 'agent_framework' } });
  show(document.getElementById('aResult'), r.results[0].result);
}
async function aInter() {
  const r = await api('/api/tasks', { goal: 'AI 原生交互设计', params: { action: 'interaction' } });
  show(document.getElementById('aResult'), r.results[0].result);
}
async function aSched() {
  const r = await api('/api/tasks', { goal: 'AI 智能资源调度', params: { action: 'scheduler' } });
  show(document.getElementById('aResult'), r.results[0].result);
}

/* 反捆绑 */
async function fStore() {
  const r = await api('/api/tasks', { goal: '去中心化应用商店设计', params: { action: 'store' } });
  show(document.getElementById('fResult'), r.results[0].result);
}
async function fPre() {
  const r = await api('/api/tasks', { goal: '反强制预装治理', params: { action: 'preinstall' } });
  show(document.getElementById('fResult'), r.results[0].result);
}
async function fCombo() {
  const r = await api('/api/tasks', { goal: '软硬件自由组合', params: { action: 'combo', os_name: 'CNOS' } });
  show(document.getElementById('fResult'), r.results[0].result);
}

/* 流水线 */
async function plRun() {
  const r = await api('/api/tasks', { goal: document.getElementById('plGoal').value || '设计自主 OS 内核、构建裁剪并规划 AI 系统与反捆绑策略', params: {} });
  show(document.getElementById('plResult'), r);
}

/* 系统 */
async function loadSystem() {
  try {
    const h = await api('/api/health');
    document.getElementById('sysHealth').textContent = JSON.stringify(h, null, 2);
    const a = await api('/api/agents');
    document.getElementById('sysCards').innerHTML = a.agents.map(x => `<div class="card"><b>${x.name}</b><div class="hint">${x.description}</div></div>`).join('');
  } catch (e) { document.getElementById('sysHealth').textContent = '错误: ' + e.message; }
}
loadSystem();
