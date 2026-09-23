(() => {
  const nav = document.querySelector('.site-header nav');
  if (!nav) return;
  const current = location.pathname.split('/').pop() || 'index.html';
  nav.innerHTML = `
    <a href="index.html"${current === 'index.html' ? ' aria-current="page"' : ''}>首頁</a>
    <a href="about.html"${current === 'about.html' ? ' aria-current="page"' : ''}>品牌與工藝</a>
    <div class="nav-dropdown">
      <button type="button" class="nav-parent" aria-expanded="false">產品 <span>⌄</span></button>
      <div class="nav-menu">
        <a href="products.html">全部產品</a>
        <a href="product-30ml.html">生產線 · 30ml</a>
        <a href="product-50ml.html">生產線 · 50ml</a>
        <a href="category.html">沉香／大香</a>
        <a href="product-50mlx.html">50ml X</a>
      </div>
    </div>
    <a href="lifestyle.html"${current === 'lifestyle.html' ? ' aria-current="page"' : ''}>品香生活</a>
    <a href="purchase-process.html"${current === 'purchase-process.html' ? ' aria-current="page"' : ''}>購買流程</a>
  `;
  const parent = nav.querySelector('.nav-parent');
  const dropdown = nav.querySelector('.nav-dropdown');
  parent?.addEventListener('click', () => {
    const open = dropdown.classList.toggle('open');
    parent.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('click', e => {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove('open');
      parent?.setAttribute('aria-expanded', 'false');
    }
  });
})();
