-- Skyodor content database schema
-- Source of truth remains content-database.json until every record is verified.
-- Unknown source values must remain NULL.

CREATE TABLE sites (
  id TEXT PRIMARY KEY,
  brand_name TEXT NOT NULL,
  brand_name_latin TEXT,
  domain TEXT NOT NULL,
  locale TEXT NOT NULL,
  currency CHAR(3) NOT NULL,
  verification_status TEXT NOT NULL,
  publication_status TEXT NOT NULL,
  updated_at DATE NOT NULL
);

CREATE TABLE pages (
  id TEXT PRIMARY KEY,
  site_id TEXT NOT NULL REFERENCES sites(id),
  slug TEXT NOT NULL UNIQUE,
  source_path TEXT NOT NULL,
  page_type TEXT NOT NULL,
  title TEXT,
  body_text TEXT,
  meta_title TEXT,
  meta_description TEXT,
  verification_status TEXT NOT NULL,
  publication_status TEXT NOT NULL,
  updated_at DATE NOT NULL
);

CREATE TABLE products (
  id TEXT PRIMARY KEY,
  code TEXT UNIQUE,
  name TEXT NOT NULL,
  size TEXT,
  price_twd INTEGER,
  description TEXT,
  image_asset_id TEXT,
  source_page_id TEXT REFERENCES pages(id),
  verification_status TEXT NOT NULL,
  publication_status TEXT NOT NULL,
  updated_at DATE NOT NULL
);

CREATE TABLE offerings (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  price_twd INTEGER,
  price_options_json TEXT,
  source_page_id TEXT REFERENCES pages(id),
  verification_status TEXT NOT NULL,
  publication_status TEXT NOT NULL,
  updated_at DATE NOT NULL
);

CREATE TABLE brand_content (
  id TEXT PRIMARY KEY,
  content_key TEXT NOT NULL UNIQUE,
  value TEXT,
  source_page_id TEXT REFERENCES pages(id),
  verification_status TEXT NOT NULL,
  publication_status TEXT NOT NULL,
  updated_at DATE NOT NULL
);

CREATE TABLE assets (
  id TEXT PRIMARY KEY,
  source_path TEXT NOT NULL,
  filename TEXT NOT NULL,
  mime_type TEXT,
  byte_size INTEGER,
  width_px INTEGER,
  height_px INTEGER,
  sha256 TEXT,
  verified_present BOOLEAN NOT NULL DEFAULT FALSE,
  verification_status TEXT NOT NULL,
  updated_at DATE NOT NULL
);

CREATE TABLE page_links (
  source_page_id TEXT NOT NULL REFERENCES pages(id),
  target_url TEXT NOT NULL,
  link_type TEXT NOT NULL,
  verification_status TEXT NOT NULL,
  PRIMARY KEY (source_page_id, target_url)
);

CREATE TABLE product_assets (
  product_id TEXT NOT NULL REFERENCES products(id),
  asset_id TEXT NOT NULL REFERENCES assets(id),
  sort_order INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (product_id, asset_id)
);

CREATE TABLE quality_checks (
  id TEXT PRIMARY KEY,
  check_name TEXT NOT NULL,
  status TEXT NOT NULL,
  details TEXT,
  checked_at TIMESTAMP NOT NULL
);

-- Recommended indexes
CREATE INDEX idx_products_code ON products(code);
CREATE INDEX idx_products_publication_status ON products(publication_status);
CREATE INDEX idx_pages_publication_status ON pages(publication_status);
CREATE INDEX idx_assets_verification_status ON assets(verification_status);
