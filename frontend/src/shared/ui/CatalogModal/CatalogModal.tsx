import React from 'react';
import { CatalogPage } from '../../../pages/catalog/ui/CatalogPage';
import { Product, ProductFilter } from '../../types/product';

interface CatalogModalProps {
  isOpen: boolean;
  onClose: () => void;
  filters?: ProductFilter;
  title?: string;
  onProductSelect?: (product: Product) => void;
  showSelectButton?: boolean;
}

export function CatalogModal({
  isOpen,
  onClose,
  filters,
  title,
  onProductSelect,
  showSelectButton = false
}: CatalogModalProps) {
  if (!isOpen) return null;

  return (
    <CatalogPage
      isModal={true}
      onClose={onClose}
      filters={filters}
      title={title}
      onProductSelect={onProductSelect}
      showSelectButton={showSelectButton}
    />
  );
}
