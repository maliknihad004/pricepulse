
import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "/api";

function App() {
  const [products, setProducts] = useState([]);
  const [url, setUrl] = useState("");
  const [targetPrice, setTargetPrice] = useState("");

  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);
  const [error, setError] = useState("");

  const [editingId, setEditingId] = useState(null);
  const [editingPrice, setEditingPrice] = useState("");

  // --------------------------------------------------
  // API HELPER
  // --------------------------------------------------

  const apiRequest = async (endpoint, options = {}) => {
    const response = await fetch(
      `${API_URL}${endpoint}`,
      {
        headers: {
          "Content-Type": "application/json",
          ...(options.headers || {}),
        },
        ...options,
      }
    );

    let data = null;

    try {
      data = await response.json();
    } catch {
      data = null;
    }

    if (!response.ok) {
      throw new Error(
        data?.detail ||
          data?.message ||
          `Request failed with status ${response.status}`
      );
    }

    return data;
  };

  // --------------------------------------------------
  // FETCH PRODUCTS
  // --------------------------------------------------

  const fetchProducts = async () => {
    try {
      setError("");

      const data = await apiRequest("/products/");

      setProducts(data);
    } catch (err) {
      console.error("Fetch products error:", err);

      setError(
        "Could not connect to PricePulse API."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  // --------------------------------------------------
  // ADD PRODUCT
  // --------------------------------------------------

  const handleAddProduct = async (event) => {
    event.preventDefault();

    if (!url.trim()) {
      setError("Please enter a product URL.");
      return;
    }

    if (
      targetPrice === "" ||
      Number(targetPrice) < 0
    ) {
      setError("Please enter a valid target price.");
      return;
    }

    try {
      setAdding(true);
      setError("");

      const data = await apiRequest(
        "/products/",
        {
          method: "POST",
          body: JSON.stringify({
            url: url.trim(),
            target_price: Number(targetPrice),
          }),
        }
      );

      setProducts((current) => [
        data,
        ...current,
      ]);

      setUrl("");
      setTargetPrice("");
    } catch (err) {
      console.error("Add product error:", err);
      setError(err.message);
    } finally {
      setAdding(false);
    }
  };

  // --------------------------------------------------
  // DELETE PRODUCT
  // --------------------------------------------------

  const handleDelete = async (productId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this product?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");

      await apiRequest(
        `/products/${productId}`,
        {
          method: "DELETE",
        }
      );

      setProducts((current) =>
        current.filter(
          (product) =>
            product.id !== productId
        )
      );
    } catch (err) {
      console.error("Delete product error:", err);
      setError(err.message);
    }
  };

  // --------------------------------------------------
  // EDIT
  // --------------------------------------------------

  const startEditing = (product) => {
    setEditingId(product.id);
    setEditingPrice(
      String(product.target_price)
    );
    setError("");
  };

  const cancelEditing = () => {
    setEditingId(null);
    setEditingPrice("");
  };

  // --------------------------------------------------
  // SAVE TARGET PRICE
  // --------------------------------------------------

  const saveTargetPrice = async (productId) => {
    if (
      editingPrice === "" ||
      Number(editingPrice) < 0
    ) {
      setError(
        "Please enter a valid target price."
      );
      return;
    }

    try {
      setError("");

      const data = await apiRequest(
        `/products/${productId}`,
        {
          method: "PUT",
          body: JSON.stringify({
            target_price: Number(editingPrice),
          }),
        }
      );

      setProducts((current) =>
        current.map((product) =>
          product.id === productId
            ? data
            : product
        )
      );

      cancelEditing();
    } catch (err) {
      console.error(
        "Update product error:",
        err
      );

      setError(err.message);
    }
  };

  // --------------------------------------------------
  // PRODUCT STATUS
  // --------------------------------------------------

  const getProductStatus = (product) => {
    if (
      product.current_price !== null &&
      product.current_price !== undefined &&
      product.current_price <=
        product.target_price
    ) {
      return {
        text: "Target price reached",
        className: "success",
        icon: "✓",
      };
    }

    return {
      text: "Waiting for price drop",
      className: "",
      icon: "↓",
    };
  };

  // --------------------------------------------------
  // IMAGE FALLBACK
  // --------------------------------------------------

  const handleImageError = (event) => {
    event.currentTarget.style.display = "none";

    event.currentTarget.parentElement.classList.add(
      "image-fallback"
    );
  };

  // --------------------------------------------------
  // RENDER
  // --------------------------------------------------

  return (
    <div className="app">

      {/* Background decoration */}
      <div className="background-orb orb-one"></div>
      <div className="background-orb orb-two"></div>

      {/* HEADER */}
      <header className="header">
        <div className="header-inner">

          <div className="brand">
            <div className="logo-icon">
              P
            </div>

            <div>
              <div className="logo">
                PricePulse
              </div>

              <div className="subtitle">
                Smart price tracking
              </div>
            </div>
          </div>

          <div className="header-status">
            <span className="status-dot"></span>
            Tracking active
          </div>

        </div>
      </header>

      {/* MAIN */}
      <main className="container">

        {/* HERO */}
        <section className="hero">

          <div className="eyebrow">
            PRICE TRACKER
          </div>

          <h1>
            Never miss the
            <span> right price.</span>
          </h1>

          <p>
            Track products, monitor price changes,
            and know when your favorite products
            reach the price you want.
          </p>

        </section>

        {/* ADD PRODUCT */}
        <section className="add-card">

          <div className="add-card-top">
            <div>
              <div className="section-eyebrow">
                NEW TRACKER
              </div>

              <h2>
                Track a product
              </h2>

              <p>
                Paste a product URL and set
                your target price.
              </p>
            </div>

            <div className="add-icon">
              +
            </div>
          </div>

          <form
            className="product-form"
            onSubmit={handleAddProduct}
          >

            <div className="input-group">
              <label htmlFor="product-url">
                PRODUCT URL
              </label>

              <div className="input-container">
                <span className="input-icon">
                  ↗
                </span>

                <input
                  id="product-url"
                  type="url"
                  placeholder="https://example.com/product"
                  value={url}
                  onChange={(event) =>
                    setUrl(event.target.value)
                  }
                />
              </div>
            </div>

            <div className="input-group">
              <label htmlFor="target-price">
                TARGET PRICE
              </label>

              <div className="input-container price-input">
                <span className="currency">
                  $
                </span>

                <input
                  id="target-price"
                  type="number"
                  min="0"
                  step="0.01"
                  placeholder="40.00"
                  value={targetPrice}
                  onChange={(event) =>
                    setTargetPrice(
                      event.target.value
                    )
                  }
                />
              </div>
            </div>

            <button
              className="add-button"
              type="submit"
              disabled={adding}
            >
              {adding
                ? "Adding..."
                : "Track Product →"}
            </button>

          </form>

          {error && (
            <div className="error">
              <span>!</span>
              {error}
            </div>
          )}

        </section>

        {/* PRODUCTS */}
        <section className="products-section">

          <div className="section-title">

            <div>
              <div className="section-eyebrow">
                YOUR WATCHLIST
              </div>

              <h2>
                Tracked Products
              </h2>
            </div>

            <div className="count">
              {products.length}
            </div>

          </div>

          {loading ? (

            <div className="state-card">
              <div className="loader"></div>

              <h3>
                Loading your products
              </h3>

              <p>
                Connecting to PricePulse...
              </p>
            </div>

          ) : products.length === 0 ? (

            <div className="state-card">
              <div className="empty-icon">
                ◇
              </div>

              <h3>
                Your watchlist is empty
              </h3>

              <p>
                Add your first product above
                to start tracking prices.
              </p>
            </div>

          ) : (

            <div className="products-grid">

              {products.map((product) => {

                const status =
                  getProductStatus(product);

                return (
                  <article
                    className="product-card"
                    key={product.id}
                  >

                    {/* IMAGE */}
                    <div className="product-image">

                      {product.image_url ? (
                        <img
                          src={product.image_url}
                          alt={product.name}
                          onError={
                            handleImageError
                          }
                        />
                      ) : (
                        <div className="image-placeholder">
                          <span>◇</span>

                          <small>
                            No image
                          </small>
                        </div>
                      )}

                      <div
                        className={`stock-badge ${
                          product.available
                            ? "in-stock"
                            : "out-stock"
                        }`}
                      >
                        <span>
                          ●
                        </span>

                        {product.available
                          ? "In Stock"
                          : "Out of Stock"}
                      </div>

                    </div>

                    {/* CARD CONTENT */}
                    <div className="product-content">

                      <div className="product-category">
                        TRACKED PRODUCT
                      </div>

                      <h3>
                        {product.name}
                      </h3>

                      {/* PRICES */}
                      <div className="prices">

                        <div className="current-price">
                          <span>
                            CURRENT PRICE
                          </span>

                          <strong>
                            {product.current_price !==
                            null &&
                            product.current_price !==
                            undefined
                              ? `$${Number(
                                  product.current_price
                                ).toFixed(2)}`
                              : "Unavailable"}
                          </strong>
                        </div>

                        <div className="target-price">

                          <span>
                            TARGET
                          </span>

                          {editingId ===
                          product.id ? (

                            <div className="edit-price-box">

                              <span>
                                $
                              </span>

                              <input
                                type="number"
                                min="0"
                                step="0.01"
                                value={
                                  editingPrice
                                }
                                onChange={(
                                  event
                                ) =>
                                  setEditingPrice(
                                    event.target.value
                                  )
                                }
                              />

                            </div>

                          ) : (

                            <strong>
                              $
                              {Number(
                                product.target_price
                              ).toFixed(2)}
                            </strong>

                          )}

                        </div>

                      </div>

                      {/* STATUS */}
                      <div
                        className={`price-status ${status.className}`}
                      >
                        <span className="status-icon">
                          {status.icon}
                        </span>

                        {status.text}
                      </div>

                      {/* ACTIONS */}
                      {editingId ===
                      product.id ? (

                        <div className="product-actions">

                          <button
                            className="save-button"
                            onClick={() =>
                              saveTargetPrice(
                                product.id
                              )
                            }
                          >
                            Save Changes
                          </button>

                          <button
                            className="cancel-button"
                            onClick={
                              cancelEditing
                            }
                          >
                            Cancel
                          </button>

                        </div>

                      ) : (

                        <div className="product-actions">

                          <a
                            className="view-button"
                            href={product.url}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            View Product
                            <span>↗</span>
                          </a>

                          <button
                            className="edit-button"
                            onClick={() =>
                              startEditing(
                                product
                              )
                            }
                          >
                            Edit
                          </button>

                          <button
                            className="delete-button"
                            onClick={() =>
                              handleDelete(
                                product.id
                              )
                            }
                          >
                            Delete
                          </button>

                        </div>

                      )}

                    </div>

                  </article>
                );
              })}

            </div>
          )}

        </section>

      </main>

      <footer>
        <div>
          <strong>
            PricePulse
          </strong>

          <span>
            Automated price tracking
          </span>
        </div>

        <span>
          © 2026 PricePulse
        </span>
      </footer>

    </div>
  );
}

export default App;

