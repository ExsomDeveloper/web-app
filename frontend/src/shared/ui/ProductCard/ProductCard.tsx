import React from 'react';
import { Button } from '../Button/Button';
import { Product } from '../../types/product';
import './ProductCard.css';

interface ProductCardProps {
  product: Product;
  onView?: (product: Product) => void;
  onSelect?: (product: Product) => void;
  showSelectButton?: boolean;
  selectButtonText?: string;
}

export function ProductCard({ 
  product, 
  onView, 
  onSelect, 
  showSelectButton = false,
  selectButtonText = "Выбрать"
}: ProductCardProps) {
  const handleView = () => {
    onView?.(product);
  };

  const handleSelect = () => {
    onSelect?.(product);
  };

  return (
    <div className="product-card">
      <div className="product-image-container">
        <img 
          src={product.image} 
          alt={product.name}
          className="product-image"
        />
      </div>
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        {product.price && (
          <p className="product-price">{product.price}</p>
        )}
        {product.brand && (
          <p className="product-brand">{product.brand}</p>
        )}
        <div className="product-actions">
          <Button 
            className="view-product-btn" 
            onClick={handleView}
            type="button"
          >
            Посмотреть
          </Button>
          {showSelectButton && (
            <Button 
              className="select-product-btn" 
              onClick={handleSelect}
              type="button"
            >
              {selectButtonText}
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
