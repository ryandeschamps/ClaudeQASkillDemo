# Entities and Flows - E-commerce Website

## Document Information
- **Project**: Online Apparels Shopping Website
- **Version**: 1.0
- **Date**: November 14, 2025

---

## 1. Key Entities

### 1.1 User Entities

#### Visitor (Guest User)
**Description**: Unauthenticated users browsing the website

**Attributes**:
- Session ID
- IP Address
- Browser information
- Temporary cart data (if applicable)

**Capabilities**:
- Search products
- View product listings
- View product details
- Check shipping availability
- View ratings and reviews
- Share products on social media
- Contact support

**Limitations**:
- Cannot add items to wishlist
- Cannot complete checkout
- Cannot post ratings/reviews
- Cannot view order history

#### Buyer (Registered Customer)
**Description**: Authenticated users who can make purchases

**Attributes**:
- User ID
- First Name
- Last Name
- Email Address
- Contact Number
- Password (encrypted)
- Email Verification Status
- Account Status (Active/Inactive)
- Registration Date
- Social Login Provider (Facebook/Google, optional)

**Capabilities**:
- All Visitor capabilities
- Login/Logout
- Manage profile
- Manage addresses
- Add items to wishlist
- Add items to shopping cart
- Complete checkout and payment
- Place orders
- Track orders
- View order history
- Post ratings and reviews
- Reorder past items

#### Admin/Owner
**Description**: Business owner with full system access

**Attributes**:
- Admin ID
- Username
- Password (encrypted)
- Role
- Permissions
- Last Login

**Capabilities**:
- Manage customers (view, edit, activate, deactivate)
- Manage product catalog
- Manage categories and sub-categories
- Manage orders
- Update order status
- Manage shipments
- View payment information
- Approve/reject ratings and reviews
- View reports and statistics
- Manage CMS pages
- Manage sub-admin users and roles
- Send promotional emails
- View customer support requests

#### Sub-Admin User
**Description**: Admin team members with role-based access

**Attributes**:
- User ID
- Username
- Password (encrypted)
- Assigned Role
- Permissions
- Account Status
- Created Date

**Capabilities**:
- Role-based access to admin functions
- Limited by assigned permissions

---

### 1.2 Product Entities

#### Product
**Description**: Individual apparel items available for purchase

**Attributes**:
- Product ID
- SKU (Stock Keeping Unit)
- Product Name
- Description
- Keywords
- Category ID
- Sub-category ID
- Base Price (USD)
- Status (Active/Inactive)
- Created Date
- Modified Date

**Relationships**:
- Belongs to one Category
- Belongs to one Sub-category
- Has many Product Variations
- Has many Product Images
- Has many Ratings and Reviews

#### Product Category
**Description**: Top-level grouping of products

**Attributes**:
- Category ID
- Category Name
- Description
- Status (Active/Inactive)
- Display Order

**Examples**:
- Men's Apparel
- Women's Apparel
- Kids' Apparel
- Accessories

#### Product Sub-category
**Description**: Second-level grouping within categories

**Attributes**:
- Sub-category ID
- Parent Category ID
- Sub-category Name
- Description
- Status (Active/Inactive)
- Display Order

**Examples**:
- Shirts
- Jeans
- T-Shirts
- Dresses
- Jackets

#### Product Variation
**Description**: Different size/color combinations for products

**Attributes**:
- Variation ID
- Product ID
- Size
- Color
- Additional Price (if variation affects price)
- Stock Status
- SKU Variant

**Examples**:
- Size: S, M, L, XL, XXL
- Color: Red, Blue, Black, White, etc.

#### Product Image
**Description**: Visual representation of products

**Attributes**:
- Image ID
- Product ID
- Image URL
- Image Type (Thumbnail, Detail, Gallery)
- Display Order
- Alt Text

---

### 1.3 Transaction Entities

#### Shopping Cart
**Description**: Temporary collection of items buyer intends to purchase

**Attributes**:
- Cart ID
- User ID (Buyer)
- Created Date
- Modified Date
- Status (Active, Converted to Order, Abandoned)

**Relationships**:
- Belongs to one Buyer
- Contains many Cart Items

#### Cart Item
**Description**: Individual product in shopping cart

**Attributes**:
- Cart Item ID
- Cart ID
- Product ID
- Variation ID
- Quantity
- Unit Price
- Sub-total
- Added Date

#### Wishlist
**Description**: Collection of products buyer wants to save for later

**Attributes**:
- Wishlist ID
- User ID (Buyer)
- Created Date

**Relationships**:
- Belongs to one Buyer
- Contains many Wishlist Items

#### Wishlist Item
**Description**: Individual product in wishlist

**Attributes**:
- Wishlist Item ID
- Wishlist ID
- Product ID
- Added Date

#### Order
**Description**: Completed purchase transaction

**Attributes**:
- Order ID
- User ID (Buyer)
- Order Date
- Order Status (Open, Confirmed, In Process, Shipped, Delivered)
- Billing Address ID
- Shipping Address ID
- Subtotal
- Shipping Cost
- Tax Amount
- Total Amount
- Payment Status
- Payment Method
- Payment Transaction ID

**Relationships**:
- Belongs to one Buyer
- Contains many Order Items
- Has one Shipment
- Has one Payment

#### Order Item
**Description**: Individual product in an order

**Attributes**:
- Order Item ID
- Order ID
- Product ID
- Variation ID
- Quantity
- Unit Price
- Subtotal

#### Payment
**Description**: Financial transaction for order

**Attributes**:
- Payment ID
- Order ID
- Payment Method (Credit Card, Debit Card, Net Banking)
- Payment Gateway (Stripe)
- Transaction ID
- Payment Status (Pending, Completed, Failed, Refunded)
- Payment Date
- Amount
- Currency (USD)

#### Shipment
**Description**: Delivery information for order

**Attributes**:
- Shipment ID
- Order ID
- Shipping Carrier
- Tracking ID
- Shipment Status
- Shipping Address
- Delivery Location
- Shipping Cost
- Shipment Date
- Estimated Delivery Date
- Actual Delivery Date

---

### 1.4 Content Entities

#### Address
**Description**: Billing or shipping address for buyers

**Attributes**:
- Address ID
- User ID (Buyer)
- Address Type (Billing, Shipping)
- First Name
- Last Name
- Address Line 1
- Address Line 2
- City
- State
- ZIP/PIN Code
- Country (US only)
- Phone Number
- Is Default Address

#### Rating & Review
**Description**: Customer feedback on products

**Attributes**:
- Review ID
- Product ID
- User ID (Buyer)
- Order ID (must have purchased)
- Rating (scale TBD)
- Review Title
- Review Text
- Review Date
- Approval Status (Pending, Approved, Rejected)
- Approved By (Admin ID)
- Approved Date

#### CMS Page
**Description**: Static content pages

**Attributes**:
- Page ID
- Page Title
- Page Slug
- Page Content
- Status (Active/Inactive)
- Last Modified Date
- Modified By (Admin ID)

**Examples**:
- About Us
- Contact Us
- Privacy Policy
- Terms and Conditions

#### Support Request
**Description**: Customer inquiry or complaint

**Attributes**:
- Request ID
- User ID (if logged in)
- Name
- Email
- Contact Number
- Message
- Request Date
- Status (Open, In Progress, Resolved, Closed)
- Assigned To (Admin ID)

---

### 1.5 Administrative Entities

#### Role
**Description**: Permission group for admin users

**Attributes**:
- Role ID
- Role Name
- Description
- Permissions (JSON or linked table)
- Status (Active/Inactive)

**Examples**:
- Super Admin
- Product Manager
- Order Manager
- Customer Service Rep

#### Email Template
**Description**: Marketing and notification email content

**Attributes**:
- Template ID
- Template Name
- Subject
- Body Content
- Template Type (Marketing, Notification)
- Status (Active/Inactive)
- Created Date
- Modified Date

#### Report
**Description**: Business intelligence data

**Attributes**:
- Report ID
- Report Type (Products, Revenue, Orders, Customers)
- Date Range
- Generated Date
- Generated By (Admin ID)
- Export Format (PDF, Excel)

---

## 2. Primary User Flows

### 2.1 Buyer Registration Flow

```
START
  → Buyer visits website
  → Clicks "Register" button
  → Fills registration form:
      - First Name
      - Last Name
      - Email
      - Contact Number
      - Password
      - Confirm Password
      - Accept Terms & Conditions
  → Submits form
  → System validates input
  → System creates user account (status: unverified)
  → System sends verification email with link
  → Buyer receives email
  → Buyer clicks verification link
  → System verifies email
  → System updates account status to "verified"
  → Buyer can now login
END
```

**Alternative Flow - Social Login**:
```
START
  → Buyer visits website
  → Clicks "Login with Facebook" or "Login with Google"
  → System redirects to social provider
  → Buyer authorizes access
  → System receives user data from provider
  → System creates/updates user account
  → System logs buyer in
  → Buyer is redirected to homepage
END
```

---

### 2.2 Product Search & Discovery Flow

```
START
  → Buyer visits website
  → OPTION 1: Browse by Category
      → Clicks on category (e.g., "Men's Apparel")
      → Clicks on sub-category (e.g., "Shirts")
      → Views product listing
  → OPTION 2: Search by Keyword
      → Enters keyword in search box (e.g., "blue jeans")
      → Clicks search button
      → Views product listing
  → Applies filters (price, size, color, etc.) [optional]
  → Applies sorting (price low-high, popularity, etc.) [optional]
  → Views filtered/sorted product listing
  → Clicks on product title/image
  → Views product detail page
END
```

---

### 2.3 Product Detail & Add to Cart Flow

```
START (on Product Detail Page)
  → Buyer views product details:
      - Images
      - Description
      - Price
      - Available sizes and colors
      - Ratings and reviews
  → Buyer checks shipping availability by entering PIN code [optional]
  → Buyer selects size and color variations
  → Buyer clicks "Add to Cart"
  → IF Buyer is not logged in:
      → System prompts login/registration
      → Buyer logs in or registers
  → System adds item to shopping cart
  → System displays confirmation message
  → Buyer can:
      - Continue shopping
      - View cart
      - Proceed to checkout
END
```

**Alternative Flow - Add to Wishlist**:
```
START (on Product Detail Page)
  → Buyer clicks "Add to Wishlist"
  → IF Buyer is not logged in:
      → System prompts login/registration
      → Buyer logs in or registers
  → System adds item to wishlist
  → System displays confirmation message
END
```

---

### 2.4 Checkout & Payment Flow

```
START
  → Buyer views shopping cart
  → Buyer reviews cart items:
      - Product details
      - Quantities
      - Prices
      - Subtotal
  → Buyer clicks "Proceed to Checkout"
  → IF Buyer is not logged in:
      → System prompts login/registration
      → Buyer logs in or registers
  → System displays checkout page
  → Buyer enters/selects billing address
  → Buyer enters/selects shipping address
  → Buyer reviews order summary:
      - Item total
      - Subtotal
      - Shipping cost
      - Tax
      - Order total
  → Buyer selects payment method:
      - Credit Card
      - Debit Card
      - Net Banking
  → Buyer enters payment details
  → Buyer clicks "Place Order"
  → System processes payment via Stripe gateway
  → IF Payment Successful:
      → System creates order record
      → System updates order status to "Open"
      → System sends order confirmation email
      → System displays order confirmation page with order number
      → Buyer can track order
  → IF Payment Failed:
      → System displays error message
      → Buyer can retry payment or cancel
END
```

---

### 2.5 Order Tracking Flow

```
START
  → Buyer logs into account
  → Buyer navigates to "My Orders"
  → System displays list of orders with statuses:
      - Open
      - Confirmed
      - In Process
      - Shipped
      - Delivered
  → Buyer clicks on specific order
  → System displays order details:
      - Order number
      - Order date
      - Items ordered
      - Quantities
      - Prices
      - Shipping address
      - Current status
      - Tracking information (if shipped)
  → IF order is shipped:
      → Buyer views tracking ID and carrier information
      → Buyer can check shipment status
  → Buyer receives email notifications for status changes
END
```

---

### 2.6 Post Ratings & Review Flow

```
START
  → Buyer logs into account
  → Buyer navigates to "My Orders"
  → Buyer views past order details
  → Buyer clicks "Write Review" for purchased product
  → System verifies buyer purchased this product
  → System displays rating & review form
  → Buyer enters:
      - Rating (stars)
      - Review title
      - Review text
  → Buyer submits review
  → System saves review with "Pending" approval status
  → System notifies admin of new review
  → Admin reviews and approves/rejects
  → IF Approved:
      → Review appears on product detail page
  → IF Rejected:
      → Review is not displayed
END
```

---

### 2.7 Admin - Product Management Flow

```
START
  → Admin logs into admin panel
  → Admin navigates to "Product Management"
  → Admin clicks "Add New Product"
  → Admin enters product details:
      - Product name
      - SKU
      - Description
      - Category and sub-category
      - Base price
      - Keywords
      - Images (upload multiple)
      - Variations (sizes and colors)
  → Admin sets product status (Active/Inactive)
  → Admin clicks "Save Product"
  → System validates input
  → System saves product to catalog
  → Product becomes available on frontend (if Active)
END
```

**Alternative Flow - Edit Product**:
```
START
  → Admin navigates to "Product Management"
  → Admin searches/filters for product
  → Admin clicks "Edit" on product
  → Admin modifies product details
  → Admin clicks "Save Changes"
  → System updates product
  → Changes reflect on frontend
END
```

---

### 2.8 Admin - Order Fulfillment Flow

```
START
  → Buyer places order (see Flow 2.4)
  → System creates order with status "Open"
  → Admin receives order notification
  → Admin logs into admin panel
  → Admin navigates to "Order Management"
  → Admin views order list, filters by status
  → Admin clicks on "Open" order
  → Admin reviews order details
  → Admin updates status to "Confirmed"
  → System sends confirmation email to buyer
  → Admin prepares items for shipping
  → Admin updates status to "In Process"
  → Admin packages items
  → Admin arranges shipment with carrier
  → Admin enters shipment details:
      - Shipping carrier
      - Tracking ID
      - Estimated delivery date
  → Admin updates status to "Shipped"
  → System sends shipping notification email to buyer
  → Carrier delivers order
  → Admin updates status to "Delivered"
  → System sends delivery confirmation email to buyer
END
```

---

### 2.9 Admin - Customer Management Flow

```
START
  → Admin logs into admin panel
  → Admin navigates to "Customer Management"
  → Admin views list of registered buyers
  → Admin can filter by:
      - Active/Inactive status
      - Registration date
      - Order history
  → Admin clicks on specific buyer
  → Admin views buyer details:
      - Profile information
      - Addresses
      - Order history
      - Wishlist items
      - Cart items
  → Admin can:
      - Edit buyer information
      - Activate/Deactivate account
      - View buyer's complete activity
END
```

---

### 2.10 Admin - Reports & Analytics Flow

```
START
  → Admin logs into admin panel
  → Admin navigates to "Reports & Statistics"
  → Admin selects report type:
      - Products Uploaded
      - Revenue/Sales
  → Admin specifies date range:
      - Today
      - Current week
      - Specific date range
      - Month
      - Year
  → Admin clicks "Generate Report"
  → System compiles data
  → System displays report
  → Admin reviews statistics
  → Admin exports report:
      - PDF format
      - Excel format
  → System generates downloadable file
  → Admin downloads report
END
```

---

## 3. System Flows

### 3.1 Email Notification Flow

```
TRIGGER: Order Status Change
  → System detects status change
  → System retrieves buyer email
  → System selects appropriate email template
  → System populates template with order details
  → System sends email via email service
  → Buyer receives notification
END
```

**Email Triggers**:
- Registration email verification
- Order confirmation
- Order status updates (Confirmed, Shipped, Delivered)
- Password reset
- Support request acknowledgment

---

### 3.2 Payment Processing Flow

```
START
  → Buyer enters payment details on checkout page
  → System validates input format
  → System initiates Stripe payment gateway
  → System sends encrypted payment data to Stripe
  → Stripe processes payment
  → Stripe returns response:
      - Success: Transaction ID, confirmation
      - Failure: Error code, message
  → IF Success:
      → System creates order
      → System updates payment status to "Completed"
      → System triggers order confirmation flow
  → IF Failure:
      → System displays error to buyer
      → System logs failure
      → Buyer can retry or use different payment method
END
```

---

### 3.3 Session Management Flow

```
LOGIN:
  → Buyer enters credentials
  → System validates credentials
  → System creates session
  → System stores session ID in cookie
  → Buyer is authenticated for session duration

ACTIVITY:
  → Buyer performs actions (browse, add to cart, etc.)
  → System validates session on each request
  → Session remains active

LOGOUT:
  → Buyer clicks logout
  → System destroys session
  → System clears session cookie
  → Buyer is redirected to homepage
END
```

---

## 4. Data Relationships

### 4.1 Entity Relationship Diagram (Textual)

```
USER (Buyer)
  ├── has many ADDRESSES
  ├── has one SHOPPING CART
  │   └── contains many CART ITEMS
  │       └── references PRODUCT + VARIATION
  ├── has one WISHLIST
  │   └── contains many WISHLIST ITEMS
  │       └── references PRODUCT
  ├── has many ORDERS
  │   ├── contains many ORDER ITEMS
  │   │   └── references PRODUCT + VARIATION
  │   ├── has one PAYMENT
  │   └── has one SHIPMENT
  └── has many RATINGS & REVIEWS
      └── references PRODUCT + ORDER

PRODUCT
  ├── belongs to CATEGORY
  ├── belongs to SUB-CATEGORY
  ├── has many PRODUCT VARIATIONS
  ├── has many PRODUCT IMAGES
  └── has many RATINGS & REVIEWS

ADMIN USER
  ├── has assigned ROLE
  │   └── has many PERMISSIONS
  └── performs ADMIN ACTIONS (logged)

ORDER
  ├── placed by USER (Buyer)
  ├── has BILLING ADDRESS
  ├── has SHIPPING ADDRESS
  ├── has many ORDER ITEMS
  ├── has one PAYMENT
  └── has one SHIPMENT
```

---

## 5. State Transitions

### 5.1 Order Status State Machine

```
Open → Confirmed → In Process → Shipped → Delivered

Transitions:
- Open: Initial state when order is placed and payment confirmed
- Open → Confirmed: Admin reviews and confirms order
- Confirmed → In Process: Admin begins preparing order for shipment
- In Process → Shipped: Admin ships order and enters tracking details
- Shipped → Delivered: Carrier delivers order, admin confirms delivery
```

### 5.2 User Account Status State Machine

```
Unverified → Verified → Active ⇄ Inactive

Transitions:
- Unverified: Initial state after registration
- Unverified → Verified: User clicks email verification link
- Verified → Active: User completes first login (default active)
- Active ⇄ Inactive: Admin can activate/deactivate accounts
```

### 5.3 Review Approval Status State Machine

```
Pending → Approved (displayed)
        ↘ Rejected (not displayed)

Transitions:
- Pending: Initial state when buyer submits review
- Pending → Approved: Admin approves review, visible on product page
- Pending → Rejected: Admin rejects review, not visible
```

---

*This document provides a comprehensive view of all system entities and their interactions, forming the foundation for test scenario development.*
