import React, { useMemo } from 'react';
import { Button } from '../../../shared/ui/Button/Button';
import { ProductCard } from '../../../shared/ui/ProductCard/ProductCard';
import { Product, ProductFilter } from '../../../shared/types/product';
import { useProducts } from '../../../shared/hooks/useProducts';
import { getProductsByCategory, getProductsByBrand, searchProducts } from '../../../shared/data/products';
import './catalog.css';

interface CatalogPageProps {
  onNavigateToHome?: () => void;
  isModal?: boolean;
  onClose?: () => void;
  filters?: ProductFilter;
  title?: string;
  onProductSelect?: (product: Product) => void;
  showSelectButton?: boolean;
}

export function CatalogPage({ 
  onNavigateToHome, 
  isModal = false, 
  onClose,
  filters,
  title = "Каталог товаров",
  onProductSelect,
  showSelectButton = false
}: CatalogPageProps) {
  const { products, loading, error, isEmpty } = useProducts();

  const filteredProducts = useMemo(() => {
    let filteredProducts = products;

    if (filters) {
      if (filters.category) {
        filteredProducts = getProductsByCategory(filteredProducts, filters.category);
      }
      if (filters.brand) {
        filteredProducts = getProductsByBrand(filteredProducts, filters.brand);
      }
      if (filters.searchQuery) {
        filteredProducts = searchProducts(filteredProducts, filters.searchQuery);
      }
    }

    return filteredProducts;
  }, [products, filters]);

  const handleViewProduct = (product: Product) => {
    console.log('Просмотр товара:', product);
    // Здесь можно добавить логику для перехода к детальному просмотру товара
  };

  const handleProductSelect = (product: Product) => {
    onProductSelect?.(product);
  };

  const handleClose = () => {
    if (isModal && onClose) {
      onClose();
    } else if (onNavigateToHome) {
      onNavigateToHome();
    }
  };

  return (
    <div className={`catalog-container ${isModal ? 'catalog-modal' : 'catalog-screen'}`}>
      <div className="catalog-header">
        <h1 className="catalog-title">{title}</h1>
        <Button 
          className="close-catalog-btn" 
          onClick={handleClose} 
          type="button"
        >
          {isModal ? '✕' : 'Назад'}
        </Button>
      </div>
      
      <div className="catalog-content">
        {loading && (
          <div className="loading-state">
            <p>Загрузка товаров...</p>
          </div>
        )}
        
        {error && (
          <div className="error-state">
            <p>{error}</p>
          </div>
        )}
        
        {isEmpty && !loading && !error && (
          <div className="empty-state">
            <p>В данный момент товар отсутствует</p>
          </div>
        )}
        
        {!loading && !error && !isEmpty && (
          <div className="products-grid">
            {filteredProducts.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onView={handleViewProduct}
                onSelect={handleProductSelect}
                showSelectButton={showSelectButton}
                selectButtonText="Выбрать"
              />
            ))}
          </div>
        )}
        
        {!loading && !error && !isEmpty && filteredProducts.length === 0 && (
          <div className="no-products">
            <p>Товары не найдены</p>
          </div>
        )}
      </div>
    </div>
  );
}
