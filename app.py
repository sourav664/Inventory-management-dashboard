import streamlit as st
import pandas as pd
from db_functions import (
    connect_to_db,
    get_basic_info,
    get_additonal_tables,
    get_suppliers,
    get_categories,
    add_new_manual_id,
    get_all_products,
    get_product_history,
    place_reorder,
    get_pending_reorders,
    mark_reorder_as_completed,
)

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide"
)

# ---------------------------------------------------
# Database Connection
# ---------------------------------------------------
db = connect_to_db()
cursor = db.cursor(dictionary=True)

# ---------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------
st.sidebar.title("📦 Inventory Dashboard")
option = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "⚙️ Operations"]
)

st.title("Inventory & Supply Chain Management System")

# ===================================================
# DASHBOARD SECTION
# ===================================================
if option == "📊 Dashboard":

    st.subheader("📈 Key Metrics")

    basic_info = get_basic_info(cursor)

    cols = st.columns(3)
    keys = list(basic_info.keys())

    for i in range(3):
        cols[i].metric(keys[i], basic_info[keys[i]])

    cols2 = st.columns(3)
    for i in range(3, 6):
        cols2[i-3].metric(keys[i], basic_info[keys[i]])

    st.markdown("---")

    st.subheader("📋 Detailed Information")

    additional_tables = get_additonal_tables(cursor)

    for label, table_data in additional_tables.items():
        with st.expander(label, expanded=False):
            st.dataframe(pd.DataFrame(table_data), use_container_width=True)


# ===================================================
# OPERATIONS SECTION
# ===================================================
elif option == "⚙️ Operations":

    st.subheader("Operational Tasks")

    selected_task = st.selectbox(
        "Choose Task",
        ["Add New Product", "Product History", "Place Reorder", "Receive Reorder"]
    )

    # ------------------------------------------------
    # ADD NEW PRODUCT
    # ------------------------------------------------
    if selected_task == "Add New Product":

        st.markdown("### ➕ Add New Product")

        categories = get_categories(cursor)
        suppliers = get_suppliers(cursor)

        supplier_dict = {
            s["supplier_name"]: s["supplier_id"] for s in suppliers
        }

        with st.form("add_product_form"):
            col1, col2 = st.columns(2)

            with col1:
                p_name = st.text_input("Product Name")
                p_category = st.selectbox("Category", categories)
                p_price = st.number_input("Price", min_value=0.0, step=0.01)

            with col2:
                p_stock = st.number_input("Stock Quantity", min_value=0, step=1)
                p_reorder = st.number_input("Reorder Level", min_value=0, step=1)
                selected_supplier = st.selectbox("Supplier", list(supplier_dict.keys()))

            submitted = st.form_submit_button("Add Product")

            if submitted:
                if not p_name:
                    st.warning("Product name is required.")
                else:
                    try:
                        with st.spinner("Adding product..."):
                            add_new_manual_id(
                                cursor,
                                db,
                                p_name,
                                p_category,
                                p_price,
                                p_stock,
                                p_reorder,
                                supplier_dict[selected_supplier],
                            )
                        st.success("Product added successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ------------------------------------------------
    # PRODUCT HISTORY
    # ------------------------------------------------
    elif selected_task == "Product History":

        st.markdown("### 📜 Product History")

        products = get_all_products(cursor)
        product_dict = {p["product_name"]: p["product_id"] for p in products}

        selected_product = st.selectbox("Select Product", list(product_dict.keys()))

        if selected_product:
            product_id = product_dict[selected_product]
            history = get_product_history(cursor, product_id)

            if history:
                st.dataframe(pd.DataFrame(history), use_container_width=True)
            else:
                st.info("No history found for this product.")

    # ------------------------------------------------
    # PLACE REORDER
    # ------------------------------------------------
    elif selected_task == "Place Reorder":

        st.markdown("### 🔁 Place Reorder")

        products = get_all_products(cursor)
        product_dict = {p["product_name"]: p["product_id"] for p in products}

        selected_product = st.selectbox("Select Product", list(product_dict.keys()))
        reorder_qty = st.number_input("Reorder Quantity", min_value=1, step=1)

        if st.button("Place Order"):
            try:
                with st.spinner("Placing reorder..."):
                    place_reorder(
                        cursor,
                        db,
                        product_dict[selected_product],
                        reorder_qty
                    )
                st.success("Reorder placed successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

    # ------------------------------------------------
    # RECEIVE REORDER
    # ------------------------------------------------
    elif selected_task == "Receive Reorder":

        st.markdown("### 📦 Receive Reorder")

        pending = get_pending_reorders(cursor)

        if not pending:
            st.info("No pending reorders.")
        else:
            reorder_dict = {
                f"Order ID {r['reorder_id']} - {r['product_name']}": r["reorder_id"]
                for r in pending
            }

            selected_order = st.selectbox(
                "Select Reorder",
                list(reorder_dict.keys())
            )

            if st.button("Mark as Received"):
                try:
                    with st.spinner("Updating reorder..."):
                        mark_reorder_as_completed(
                            cursor,
                            db,
                            reorder_dict[selected_order]
                        )
                    st.success("Reorder marked as received.")
                except Exception as e:
                    st.error(f"Error: {e}")