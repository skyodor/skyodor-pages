(() => {
  const nav = document.querySelector('.site-header nav');
  const scriptSrc = document.currentScript?.getAttribute('src') || 'navigation.js';
  const depth = (scriptSrc.match(/\.\.\//g) || []).length;
  const root = '../'.repeat(depth);
  const current = location.pathname.split('/').pop() || 'index.html';
  const href = file => `${root}${file}`;

  // Canonical product-image map. Paths come from the verified v21 product catalogue;
  // products without a verified source image intentionally remain without an image.
  const productImages = {
    'NO.C1':'assets/uploads/1/2/8/6/128601763/yutacar-jkmnm3cincw-unsplash.jpg',
    'NO.C2':'assets/uploads/1/2/8/6/128601763/1244221102.jpg',
    'NO.C3':'assets/uploads/1/2/8/6/128601763/2087698222.jpg',
    'NO.C4':'assets/uploads/1/2/8/6/128601763/mohammad-alizade-dunskupql7g-unsplash.jpg',
    'NO.C5':'assets/uploads/1/2/8/6/128601763/chermiti-mohamed-gjvokrp-6yk-unsplash.jpg',
    'NO.C6':'assets/uploads/1/2/8/6/128601763/adult-black-and-white-concentration-1061130.jpg',
    'NO.C7':'assets/uploads/1/2/8/6/128601763/city-buildings-near-body-of-water-1449455.jpg',
    'NO.C8':'assets/uploads/1/2/8/6/128601763/s-207052814.jpg',
    'NO.C9':'assets/uploads/1/2/8/6/128601763/architecture-buildings-city-cityscape-366283.jpg',
    'NO.L1':'assets/uploads/1/2/8/6/128601763/bride-couple-groom-70737.jpg',
    'NO.L2':'assets/uploads/1/2/8/6/128601763/jacob-rank-pgkyqck99cg-unsplash.jpg',
    'NO.L3':'assets/uploads/1/2/8/6/128601763/backlit-blur-couple-556667.jpg',
    'NO.L4':'assets/uploads/1/2/8/6/128601763/lua-valentia-buy0ng5-9ds-unsplash.jpg',
    'NO.L5':'assets/uploads/1/2/8/6/128601763/attachment-couple-dark-41068.jpg',
    'NO.L6':'assets/uploads/1/2/8/6/128601763/backlit-couple-dawn-1824684.jpg',
    'NO.P1':'assets/uploads/1/2/8/6/128601763/1961643371.jpg',
    'NO.P2':'assets/uploads/1/2/8/6/128601763/bibi-pace-lzbgmtwt5ey-unsplash.jpg',
    'NO.P3':'assets/uploads/1/2/8/6/128601763/annie-spratt-dktj6ttchmk-unsplash.jpg',
    'NO.P4':'assets/uploads/1/2/8/6/128601763/casey-horner-4rdca5hblcs-unsplash.jpg',
    'NO.P6':'assets/uploads/1/2/8/6/128601763/sergey-norkov-fd8lrufg0sm-unsplash.jpg',
    'NO.P7':'assets/uploads/1/2/8/6/128601763/s-202219571.jpg',
    'NO.P8':'assets/uploads/1/2/8/6/128601763/pexels-photo-1637114.jpeg',
    'NO.P9':'assets/uploads/1/2/8/6/128601763/s-205955079.jpg',
    'NO.S1':'assets/uploads/1/2/8/6/128601763/1450243138.jpg',
    'NO.S2':'assets/uploads/1/2/8/6/128601763/heng-films-mpdiphyqz4y-unsplash.jpg',
    'NO.S3':'assets/uploads/1/2/8/6/128601763/beautiful-cute-facial-expression-1170654.jpg',
    'NO.S5':'assets/uploads/1/2/8/6/128601763/pexels-photo-708440.jpeg',
    'NO.S6':'assets/uploads/1/2/8/6/128601763/a73edf35-bfa8-46e5-8efc-7edd40af8b38.jpg',
    'NO.S7':'assets/uploads/1/2/8/6/128601763/s-214745099.jpg',
    'NO.S8':'assets/uploads/1/2/8/6/128601763/d7d6b47b-d68a-421d-b1ae-87333cf24d18.jpg',
    'NO.N1':'assets/uploads/1/2/8/6/128601763/greg-rakozy-ompaz-dn-9i-unsplash.jpg',
    'NO.N2':'assets/uploads/1/2/8/6/128601763/498942889.jpg',
    'NO.N3':'assets/uploads/1/2/8/6/128601763/paul-green-fhogkxwqz0s-unsplash.jpg',
    'NO.N4':'assets/uploads/1/2/8/6/128601763/casey-horner-d4toocieyf4-unsplash.jpg',
    'NO.N5':'assets/uploads/1/2/8/6/128601763/s-200458293.jpg',
    'NO.N6':'assets/uploads/1/2/8/6/128601763/s-200458293.jpg'
  };

  const imageAlt = code => {
    const card = [...document.querySelectorAll('.catalog-card')].find(el => el.querySelector('.catalog-code')?.textContent.trim() === code);
    return card?.querySelector('h3')?.textContent.trim() || code;
  };

  const restoreProductImages = () => {
    document.querySelectorAll('.catalog-card').forEach(card => {
      const code = card.querySelector('.catalog-code')?.textContent.trim();
      const path = productImages[code];
      if (!path) return;
      const holder = card.querySelector('.catalog-image');
      if (!holder || holder.querySelector('img')) return;
      const placeholder = holder.querySelector('.product-placeholder');
      const img = document.createElement('img');
      img.src = href(path);
      img.alt = imageAlt(code);
      img.loading = 'lazy';
      img.decoding = 'async';
      img.className = 'catalog-product-image';
      if (placeholder) placeholder.replaceWith(img); else holder.prepend(img);
    });

    const detail = document.querySelector('.detail-image');
    const code = decodeURIComponent(location.hash.slice(1));
    const path = productImages[code];
    if (detail && path && !detail.querySelector('img')) {
      const img = document.createElement('img');
      img.src = href(path);
      img.alt = code;
      img.loading = 'eager';
      img.decoding = 'async';
      img.className = 'detail-product-image';
      const placeholder = detail.querySelector('.detail-placeholder');
      if (placeholder) placeholder.replaceWith(img); else detail.prepend(img);
    }
  };

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
  restoreProductImages();

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
