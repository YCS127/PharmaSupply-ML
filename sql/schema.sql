-- Schema DDL pour PharmaSupply-ML (Staging / Raw Data)

DROP TABLE IF EXISTS raw_pharmaceutical_demand CASCADE;

CREATE TABLE raw_pharmaceutical_demand (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    target_demand INT NOT NULL,
    sales_volume INT NOT NULL,
    stock_on_hand INT NOT NULL,
    is_stockout INT NOT NULL DEFAULT 0,
    supplier_lead_time INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index pour optimiser les requêtes sur les séries temporelles et par produit
CREATE INDEX idx_pharma_date_product ON raw_pharmaceutical_demand (date, product_id);