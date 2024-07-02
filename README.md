## DynamoDB single-table design

![Coverage Status](docs/images/coverage.svg)

* Steps for Modeling with DynamoDB
    * Create an entity-relationship diagram ("ERD")
    * Write out all of your access patterns
    * Model your primary key structure
    * Satisfy additional access patterns with secondary indexes

---

### I. Create entity-relationship Diagram

* Basic shopping application
* Entities
    * User
    * Category
    * Brand
    * Product
    * Order
    * OrderItem

  ```mermaid
  erDiagram
    USER {
        int id PK
        string name
        string email
        string password
        datetime created_at
        datetime updated_at
    }
    BRAND {
        int id PK
        string name
        datetime created_at
        datetime updated_at
    }
    CATEGORY {
        int id PK
        string name
        datetime created_at
        datetime updated_at
    }
    PRODUCT {
        int id PK
        string name
        float price
        int stock
        int category_id FK
        int brand_id FK
        datetime created_at
        datetime updated_at
    }
    ORDER {
        int id PK
        int user_id FK
        string status
        float total_price
        datetime created_at
        datetime updated_at
    }
    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        float price
    }

    USER ||--o{ ORDER: "places"
    CATEGORY ||--o{ PRODUCT: "contains"
    BRAND ||--o{ PRODUCT: "contains"
    PRODUCT ||--o{ ORDER_ITEM: "included in"
    ORDER ||--o{ ORDER_ITEM: "includes"
  ```

### II. Write out all access patterns

1. **Users**
    * List users
    * Get a user by id
    * Get a user by email

2. **Categories**
    * List categories
    * Get a category by id

3. **Brands**
    * List brands
    * Get a brand by id

4. **Products**
    * Get a product by id
    * List products by category
    * List products by brand
    * List products by category and brand

5. **Orders**
    * Get order by id
    * List user's orders
    * List orders by status

### III. Model your primary key structure

| Entity   | PK             | SK               |
|----------|----------------|------------------|
| Category | CAT            | CAT#<cat_id>     |
| Brand    | BRAND          | BRAND#<brand_id> |
| Product  | PROD           | PRO#<product_id> |
| User     | USER           | USER#<user_id>   |
| Order    | USER#<user_id> | ORDER#<order_id> |

### IV. Satisfy additional access patterns with secondary indexes

|         | Entity   | Access Pattern                        | Table/Index | Key Condition                                               | Notes                          |
|:--------|:---------|:--------------------------------------|:------------|-------------------------------------------------------------|:-------------------------------|
| &check; | User     | Get a user by id                      | Table       | PK="USER" AND SK="USER#001"                                 |                                |
| &check; | User     | Get a user by email                   | LSI         | PK="USER" AND SKU="EMAIL#test01@gmail.com"                  |                                |
| &check; | User     | List users                            | Table       | PK="USER"                                                   | order by created_at            |
| &check; | User     | List users filter by created_at       | Table       | PK="USER" AND SK > "USER#<ksuid_prefix_time>"               | order by created_at            |
| &check; | User     | List users filter by email-prefix     | GSI1        | GSI1PK="USER" AND GSI1SK.startswith("EMAIL#test")           | order by email                 |
| &check; | Category | Get a category by id                  | Table       | PK="CAT" AND SK="CAT#123"                                   |                                |
| &check; | Category | List categories                       | Table       | PK="CAT"                                                    | order by created_at            |
| &check; | Category | List categories filter by name-prefix | LSI         | PK="CAT" AND SKU.startswith("CAT#NAME#CatX")                | order by name                  |
| &check; | Brand    | Get a brand by id                     | Table       | PK="BRAND" AND SK="BRAND#456"                               |                                |
| &check; | Brand    | List brands                           | Table       | PK="BRAND"                                                  | order by created_at            |
| &check; | Brand    | List brands filter by name-prefix     | LSI         | PK="BRAND" AND SKU.startswith("BRAND#NAME#BrY")             | order by name                  |
| &check; | Product  | Get a product by id                   | Table       | PK="PROD" AND SK="PRO#222"                                  |                                |
| &check; | Product  | List products                         | Table       | PK="PROD"                                                   | order by created_at            |
| &check; | Product  | List products by brand                | GSI1        | GSI1PK="BRAND#123"                                          | order by created_at            |
| &check; | Product  | List products by brand + categogy     | GSI1        | GSI1PK="BRAND#123" AND GSI1SK.startswith("CAT#456")         | order by category's created_at |
| &check; | Product  | List products by category             | GSI2        | GSI2PK="CAT#123"                                            | order by created_at            |
| &check; | Product  | List products by categogy + brand     | GSI2        | GSI2PK="CAT#123" AND GSI2SK.startswith("BRAND#456")         | order by brand's created_at    |
| &check; | Order    | Get user's order by id                | Table       | PK="USER#001" AND SK="ORDER#333"                            |                                |
| &check; | Order    | List user's orders                    | Table       | PK="USER#001" AND SK.startswith("ORDER")                    | order by created_at            |
| &check; | Order    | List orders by status                 | GSI1        | GSI2PK="ORDER#STATUS#DELIVERED" AND GSI2SK>="AT#1719473962" | order by updated_at            |

#### Local secondary index

| Entity   | PK    | SKU               |
|----------|-------|-------------------|
| User     | USER  | EMAIL#<email>     |
| Brand    | BRAND | BRAND#NAME#<name> |
| Category | CAT   | CAT#NAME#<name>   |

#### Global secondary indexes

| Entity  | GSI1PK                      | GSI1PK                       |
|---------|-----------------------------|------------------------------|
| Order   | ORDER#STATUS#<order_status> | AT#<updated_at>              |
| Product | BRAND#<brand_id>            | CAT#<cat_id>#AT#<created_at> |

| Entity  | GSI2PK       | GSI2PK                           |
|---------|--------------|----------------------------------|
| Product | CAT#<cat_id> | BRAND#<brand_id>#AT#<created_at> |

* **Notes**:
    * Use [ksuid](https://github.com/saresend/KSUID) instead of uuid. It's very useful for sorting items by `created_at`
    * SK should be entity id
    * PK should be group of entity id(s)
    * When listing entities
        * Group them by **Partition Key** and prefix of **Sort Key**
        * Order them by **Sort Key** using `scan_index_forward`:
            * `true` for ascending order
            * `false` for descending order
