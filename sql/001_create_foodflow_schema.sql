/*
    westeros-foodflow
    Phase 3 - Stage 3A.2
    Relational SQL schema

    Purpose:
      Create the transactional source model used by FoodFlow.

    Design principles:
      - BIGINT IDENTITY for transactional/entity surrogate keys
      - restaurants.restaurant_id is a business key
      - menu_item_id is globally unique
      - Explicit PK/FK relationships
      - Business-rule CHECK constraints
      - updated_at indexes support future incremental extraction
      - No CDC at this stage
*/

SET NOCOUNT ON;
GO

/* ============================================================
   1. RESTAURANTS
   ============================================================ */

CREATE TABLE dbo.restaurants
(
    restaurant_id    VARCHAR(20)    NOT NULL,
    restaurant_name  VARCHAR(150)   NOT NULL,
    city             VARCHAR(100)   NOT NULL,
    state            VARCHAR(100)   NOT NULL,
    country          VARCHAR(100)   NOT NULL,
    address          VARCHAR(300)   NULL,
    cuisine          VARCHAR(100)   NOT NULL,
    opening_date     DATE           NOT NULL,
    phone            VARCHAR(20)    NULL,
    rating           DECIMAL(3,2)   NULL,
    created_at       DATETIME2(3)   NOT NULL,
    updated_at       DATETIME2(3)   NOT NULL,
    is_active        BIT            NOT NULL,

    CONSTRAINT PK_restaurants
        PRIMARY KEY (restaurant_id),

    CONSTRAINT CK_restaurants_rating
        CHECK (rating IS NULL OR (rating >= 1.00 AND rating <= 5.00))
);
GO

CREATE INDEX IX_restaurants_updated_at
    ON dbo.restaurants (updated_at);
GO


/* ============================================================
   2. CUSTOMERS
   ============================================================ */

CREATE TABLE dbo.customers
(
    customer_id    BIGINT         IDENTITY(1,1) NOT NULL,
    customer_name  VARCHAR(150)   NOT NULL,
    email          VARCHAR(255)   NOT NULL,
    phone          VARCHAR(20)    NULL,
    city           VARCHAR(100)   NULL,
    state          VARCHAR(100)   NULL,
    created_at     DATETIME2(3)   NOT NULL,
    updated_at     DATETIME2(3)   NOT NULL,
    is_active      BIT            NOT NULL,

    CONSTRAINT PK_customers
        PRIMARY KEY (customer_id),

    CONSTRAINT UQ_customers_email
        UNIQUE (email)
);
GO

CREATE INDEX IX_customers_updated_at
    ON dbo.customers (updated_at);
GO


/* ============================================================
   3. DELIVERY PARTNERS
   ============================================================ */

CREATE TABLE dbo.delivery_partners
(
    delivery_partner_id  BIGINT        IDENTITY(1,1) NOT NULL,
    partner_name         VARCHAR(150)  NOT NULL,
    phone                VARCHAR(20)   NULL,
    vehicle_type         VARCHAR(30)   NULL,
    city                 VARCHAR(100)  NOT NULL,
    status               VARCHAR(30)   NOT NULL,
    created_at           DATETIME2(3)  NOT NULL,
    updated_at           DATETIME2(3)  NOT NULL,

    CONSTRAINT PK_delivery_partners
        PRIMARY KEY (delivery_partner_id),

    CONSTRAINT CK_delivery_partners_status
        CHECK (status IN ('AVAILABLE', 'BUSY', 'OFFLINE'))
);
GO

CREATE INDEX IX_delivery_partners_updated_at
    ON dbo.delivery_partners (updated_at);
GO


/* ============================================================
   4. MENU ITEMS
   ============================================================ */

CREATE TABLE dbo.menu_items
(
    menu_item_id    BIGINT         IDENTITY(1,1) NOT NULL,
    restaurant_id   VARCHAR(20)    NOT NULL,
    item_name       VARCHAR(150)   NOT NULL,
    category        VARCHAR(100)   NULL,
    description     VARCHAR(500)   NULL,
    price           DECIMAL(10,2)  NOT NULL,
    is_available    BIT            NOT NULL,
    created_at      DATETIME2(3)   NOT NULL,
    updated_at      DATETIME2(3)   NOT NULL,

    CONSTRAINT PK_menu_items
        PRIMARY KEY (menu_item_id),

    CONSTRAINT FK_menu_items_restaurants
        FOREIGN KEY (restaurant_id)
        REFERENCES dbo.restaurants (restaurant_id),

    CONSTRAINT CK_menu_items_price
        CHECK (price > 0)
);
GO

CREATE INDEX IX_menu_items_restaurant_id
    ON dbo.menu_items (restaurant_id);
GO

CREATE INDEX IX_menu_items_updated_at
    ON dbo.menu_items (updated_at);
GO


/* ============================================================
   5. ORDERS
   ============================================================ */

CREATE TABLE dbo.orders
(
    order_id             BIGINT          IDENTITY(1,1) NOT NULL,
    customer_id          BIGINT          NOT NULL,
    restaurant_id        VARCHAR(20)     NOT NULL,
    delivery_partner_id  BIGINT          NULL,
    order_type            VARCHAR(20)     NOT NULL,
    order_status          VARCHAR(30)     NOT NULL,
    order_total          DECIMAL(12,2)   NOT NULL,
    delivery_fee         DECIMAL(10,2)   NOT NULL,
    tax_amount            DECIMAL(10,2)   NOT NULL,
    order_date            DATETIME2(3)   NOT NULL,
    created_at            DATETIME2(3)   NOT NULL,
    updated_at            DATETIME2(3)   NOT NULL,

    CONSTRAINT PK_orders
        PRIMARY KEY (order_id),

    CONSTRAINT FK_orders_customers
        FOREIGN KEY (customer_id)
        REFERENCES dbo.customers (customer_id),

    CONSTRAINT FK_orders_restaurants
        FOREIGN KEY (restaurant_id)
        REFERENCES dbo.restaurants (restaurant_id),

    CONSTRAINT FK_orders_delivery_partners
        FOREIGN KEY (delivery_partner_id)
        REFERENCES dbo.delivery_partners (delivery_partner_id),

    CONSTRAINT CK_orders_type
        CHECK (order_type IN ('DINE_IN', 'TAKE_AWAY', 'DELIVERY')),

    CONSTRAINT CK_orders_status
        CHECK
        (
            order_status IN
            (
                'PLACED',
                'CONFIRMED',
                'PREPARING',
                'READY_FOR_PICKUP',
                'PICKED_UP',
                'ON_THE_WAY',
                'DELIVERED',
                'CANCELLED_BY_CUSTOMER',
                'CANCELLED_PAYMENT_FAILURE'
            )
        ),

    CONSTRAINT CK_orders_order_total
        CHECK (order_total >= 0),

    CONSTRAINT CK_orders_delivery_fee
        CHECK (delivery_fee >= 0),

    CONSTRAINT CK_orders_tax_amount
        CHECK (tax_amount >= 0)
);
GO

CREATE INDEX IX_orders_customer_id
    ON dbo.orders (customer_id);
GO

CREATE INDEX IX_orders_restaurant_id
    ON dbo.orders (restaurant_id);
GO

CREATE INDEX IX_orders_delivery_partner_id
    ON dbo.orders (delivery_partner_id);
GO

CREATE INDEX IX_orders_order_date
    ON dbo.orders (order_date);
GO

CREATE INDEX IX_orders_updated_at
    ON dbo.orders (updated_at);
GO


/* ============================================================
   6. ORDER ITEMS
   ============================================================ */

CREATE TABLE dbo.order_items
(
    order_item_id  BIGINT         IDENTITY(1,1) NOT NULL,
    order_id       BIGINT         NOT NULL,
    menu_item_id   BIGINT         NOT NULL,
    quantity       INT            NOT NULL,
    unit_price     DECIMAL(10,2)  NOT NULL,
    created_at     DATETIME2(3)   NOT NULL,
    updated_at     DATETIME2(3)   NOT NULL,

    CONSTRAINT PK_order_items
        PRIMARY KEY (order_item_id),

    CONSTRAINT FK_order_items_orders
        FOREIGN KEY (order_id)
        REFERENCES dbo.orders (order_id),

    CONSTRAINT FK_order_items_menu_items
        FOREIGN KEY (menu_item_id)
        REFERENCES dbo.menu_items (menu_item_id),

    CONSTRAINT CK_order_items_quantity
        CHECK (quantity > 0),

    CONSTRAINT CK_order_items_unit_price
        CHECK (unit_price > 0)
);
GO

CREATE INDEX IX_order_items_order_id
    ON dbo.order_items (order_id);
GO

CREATE INDEX IX_order_items_menu_item_id
    ON dbo.order_items (menu_item_id);
GO

CREATE INDEX IX_order_items_updated_at
    ON dbo.order_items (updated_at);
GO


/* ============================================================
   7. PAYMENTS
   ============================================================ */

CREATE TABLE dbo.payments
(
    payment_id             BIGINT         IDENTITY(1,1) NOT NULL,
    order_id               BIGINT         NOT NULL,
    payment_method         VARCHAR(30)    NOT NULL,
    payment_status         VARCHAR(30)    NOT NULL,
    amount                 DECIMAL(12,2)  NOT NULL,
    transaction_reference  VARCHAR(100)   NULL,
    created_at              DATETIME2(3)   NOT NULL,
    updated_at              DATETIME2(3)   NOT NULL,

    CONSTRAINT PK_payments
        PRIMARY KEY (payment_id),

    CONSTRAINT FK_payments_orders
        FOREIGN KEY (order_id)
        REFERENCES dbo.orders (order_id),

    CONSTRAINT CK_payments_method
        CHECK
        (
            payment_method IN
            (
                'UPI',
                'CARD',
                'NET_BANKING',
                'CASH',
                'WALLET'
            )
        ),

    CONSTRAINT CK_payments_status
        CHECK
        (
            payment_status IN
            (
                'PENDING',
                'AUTHORIZED',
                'SUCCESS',
                'FAILED',
                'REFUNDED'
            )
        ),

    CONSTRAINT CK_payments_amount
        CHECK (amount > 0)
);
GO

CREATE INDEX IX_payments_order_id
    ON dbo.payments (order_id);
GO

CREATE INDEX IX_payments_updated_at
    ON dbo.payments (updated_at);
GO


/* ============================================================
   8. ORDER STATUS HISTORY
   ============================================================ */

CREATE TABLE dbo.order_status_history
(
    status_history_id  BIGINT        IDENTITY(1,1) NOT NULL,
    order_id           BIGINT        NOT NULL,
    status             VARCHAR(30)   NOT NULL,
    status_timestamp   DATETIME2(3)  NOT NULL,
    changed_by         VARCHAR(50)   NULL,

    CONSTRAINT PK_order_status_history
        PRIMARY KEY (status_history_id),

    CONSTRAINT FK_order_status_history_orders
        FOREIGN KEY (order_id)
        REFERENCES dbo.orders (order_id),

    CONSTRAINT CK_order_status_history_status
        CHECK
        (
            status IN
            (
                'PLACED',
                'CONFIRMED',
                'PREPARING',
                'READY_FOR_PICKUP',
                'PICKED_UP',
                'ON_THE_WAY',
                'DELIVERED',
                'CANCELLED_BY_CUSTOMER',
                'CANCELLED_PAYMENT_FAILURE'
            )
        )
);
GO

CREATE INDEX IX_order_status_history_order_id
    ON dbo.order_status_history (order_id);
GO

CREATE INDEX IX_order_status_history_timestamp
    ON dbo.order_status_history (status_timestamp);
GO


/* ============================================================
   9. RESTAURANT REVIEWS
   ============================================================ */

CREATE TABLE dbo.restaurant_reviews
(
    review_id       BIGINT         IDENTITY(1,1) NOT NULL,
    order_id        BIGINT         NOT NULL,
    customer_id     BIGINT         NOT NULL,
    restaurant_id   VARCHAR(20)    NOT NULL,
    rating          DECIMAL(2,1)   NOT NULL,
    review_text     VARCHAR(1000)  NULL,
    created_at      DATETIME2(3)   NOT NULL,
    updated_at      DATETIME2(3)   NOT NULL,

    CONSTRAINT PK_restaurant_reviews
        PRIMARY KEY (review_id),

    CONSTRAINT FK_restaurant_reviews_orders
        FOREIGN KEY (order_id)
        REFERENCES dbo.orders (order_id),

    CONSTRAINT FK_restaurant_reviews_customers
        FOREIGN KEY (customer_id)
        REFERENCES dbo.customers (customer_id),

    CONSTRAINT FK_restaurant_reviews_restaurants
        FOREIGN KEY (restaurant_id)
        REFERENCES dbo.restaurants (restaurant_id),

    CONSTRAINT CK_restaurant_reviews_rating
        CHECK (rating >= 1.0 AND rating <= 5.0)
);
GO

CREATE INDEX IX_restaurant_reviews_order_id
    ON dbo.restaurant_reviews (order_id);
GO

CREATE INDEX IX_restaurant_reviews_customer_id
    ON dbo.restaurant_reviews (customer_id);
GO

CREATE INDEX IX_restaurant_reviews_restaurant_id
    ON dbo.restaurant_reviews (restaurant_id);
GO

CREATE INDEX IX_restaurant_reviews_updated_at
    ON dbo.restaurant_reviews (updated_at);
GO


/* ============================================================
   10. DELIVERY PARTNER REVIEWS
   ============================================================ */

CREATE TABLE dbo.delivery_partner_reviews
(
    review_id             BIGINT         IDENTITY(1,1) NOT NULL,
    order_id              BIGINT         NOT NULL,
    customer_id           BIGINT         NOT NULL,
    delivery_partner_id   BIGINT         NOT NULL,
    rating                DECIMAL(2,1)   NOT NULL,
    review_text           VARCHAR(1000)  NULL,
    created_at            DATETIME2(3)   NOT NULL,
    updated_at            DATETIME2(3)   NOT NULL,

    CONSTRAINT PK_delivery_partner_reviews
        PRIMARY KEY (review_id),

    CONSTRAINT FK_delivery_partner_reviews_orders
        FOREIGN KEY (order_id)
        REFERENCES dbo.orders (order_id),

    CONSTRAINT FK_delivery_partner_reviews_customers
        FOREIGN KEY (customer_id)
        REFERENCES dbo.customers (customer_id),

    CONSTRAINT FK_delivery_partner_reviews_delivery_partners
        FOREIGN KEY (delivery_partner_id)
        REFERENCES dbo.delivery_partners (delivery_partner_id),

    CONSTRAINT CK_delivery_partner_reviews_rating
        CHECK (rating >= 1.0 AND rating <= 5.0)
);
GO

CREATE INDEX IX_delivery_partner_reviews_order_id
    ON dbo.delivery_partner_reviews (order_id);
GO

CREATE INDEX IX_delivery_partner_reviews_customer_id
    ON dbo.delivery_partner_reviews (customer_id);
GO

CREATE INDEX IX_delivery_partner_reviews_partner_id
    ON dbo.delivery_partner_reviews (delivery_partner_id);
GO

CREATE INDEX IX_delivery_partner_reviews_updated_at
    ON dbo.delivery_partner_reviews (updated_at);
GO


/* ============================================================
   SCHEMA CREATION COMPLETE
   ============================================================ */

PRINT 'westeros-foodflow Phase 3 relational schema created successfully.';
GO