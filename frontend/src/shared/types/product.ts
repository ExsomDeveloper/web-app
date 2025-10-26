export interface Product {
  id: number;
  name: string;
  image: string;
  price?: string;
  category?: string;
  brand?: string;
  description?: string;
}

export interface ProductFilter {
  category?: string;
  brand?: string;
  priceRange?: {
    min: number;
    max: number;
  };
  searchQuery?: string;
}

export interface CatalogProps {
  products: Product[];
  filters?: ProductFilter;
  isModal?: boolean;
  onClose?: () => void;
  onProductSelect?: (product: Product) => void;
  title?: string;
}
