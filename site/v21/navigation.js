(() => {
  const nav = document.querySelector('.site-header nav');
  const scriptSrc = document.currentScript?.getAttribute('src') || 'navigation.js';
  const depth = (scriptSrc.match(/\.\.\//g) || []).length;
  const root = '../'.repeat(depth);
  const current = location.pathname.split('/').pop() || 'index.html';
  const href = file => `${root}${file}`;

  // Canonical site branding: SKYODOR / 蝶漾香韻.
  const applyBrand = () => {
    document.querySelectorAll('.brand').forEach(el => {
      el.innerHTML = '<strong>SKYODOR /</strong><span> 蝶漾香韻</span>';
      el.setAttribute('aria-label', 'SKYODOR / 蝶漾香韻');
    });
    document.querySelectorAll('footer div').forEach(el => {
      const strong = el.querySelector('strong');
      const span = el.querySelector('span');
      if (strong && span && (strong.textContent.trim() === 'SKYODOR' || strong.textContent.trim() === 'ODOR')) {
        strong.textContent = 'SKYODOR /';
        span.textContent = ' 蝶漾香韻';
      }
    });
    document.querySelectorAll('.product-placeholder, .detail-placeholder').forEach(el => {
      if (/^(ODOR|SKYODOR)$/.test(el.textContent.trim())) el.textContent = 'SKYODOR';
    });
    if (document.title.includes('ODOR') || document.title.includes('｜蝶漾香韻')) {
      document.title = document.title.replaceAll('ODOR', 'SKYODOR').replaceAll('SKYODOR｜蝶漾香韻', 'SKYODOR / 蝶漾香韻');
    }
    document.querySelectorAll('meta[name="description"]').forEach(el => {
      el.content = el.content.replaceAll('ODOR', 'SKYODOR').replaceAll('SKYODOR 蝶漾香韻', 'SKYODOR / 蝶漾香韻');
    });
  };
  applyBrand();

  if (!nav) return;
  nav.innerHTML = `
    <a href="${href('index.html')}"${current === 'index.html' ? ' aria-current="page"' : ''}>首頁</a>
    <a href="${href('about.html')}"${current === 'about.html' ? ' aria-current="page"' : ''}>品牌與工藝</a>
    <div class="nav-dropdown">
      <button type="button" class="nav-parent" aria-expanded="false">產品 <span aria-hidden="true">⌄</span></button>
      <div class="nav-menu">
        <a href="${href('products.html')}">全部產品</a>
        <a href="${href('product-lines.html')}">產品線</a>
        <a href="${href('products/30ml.html')}">30ml</a>
        <a href="${href('products/50ml.html')}">50ml</a>
        <a href="${href('products/50ml-x.html')}">50ml X</a>
      </div>
    </div>
    <a href="${href('lifestyle.html')}"${current === 'lifestyle.html' ? ' aria-current="page"' : ''}>品香生活</a>
    <a href="${href('purchase-process.html')}"${current === 'purchase-process.html' ? ' aria-current="page"' : ''}>購買流程</a>
  `;

  const header = document.querySelector('.site-header');
  const mobileButton = header?.querySelector('.menu');
  const parent = nav.querySelector('.nav-parent');
  const dropdown = nav.querySelector('.nav-dropdown');

  mobileButton?.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    mobileButton.setAttribute('aria-expanded', String(open));
    mobileButton.setAttribute('aria-label', open ? '關閉選單' : '開啟選單');
  });

  parent?.addEventListener('click', () => {
    const open = dropdown.classList.toggle('open');
    parent.setAttribute('aria-expanded', String(open));
  });

  document.addEventListener('click', e => {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove('open');
      parent?.setAttribute('aria-expanded', 'false');
    }
    if (!header?.contains(e.target)) {
      nav.classList.remove('open');
      mobileButton?.setAttribute('aria-expanded', 'false');
      mobileButton?.setAttribute('aria-label', '開啟選單');
    }
  });
})();
