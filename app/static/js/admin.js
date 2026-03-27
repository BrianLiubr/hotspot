async function postAction(url) {
  const response = await fetch(url, { method: 'POST' });
  const data = await response.json();
  alert(data.message || '操作已触发');
}

document.getElementById('refresh-btn')?.addEventListener('click', () => {
  postAction('/api/admin/refresh');
});

document.getElementById('rerank-btn')?.addEventListener('click', () => {
  postAction('/api/admin/rerank');
});
