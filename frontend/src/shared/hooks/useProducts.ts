import { useState, useEffect } from 'react';
import { Product } from '../types/product';
import { productsApi, ProductsApiError } from '../api/products';

export interface UseProductsState {
  products: Product[];
  loading: boolean;
  error: string | null;
  isEmpty: boolean;
}

export const useProducts = (): UseProductsState => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const data = await productsApi.getProducts();
        setProducts(data);
      } catch (err) {
        if (err instanceof ProductsApiError) {
          setError(err.message);
        } else {
          setError('Возникла проблема, попробуйте позже');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const isEmpty = !loading && products.length === 0 && !error;

  return {
    products,
    loading,
    error,
    isEmpty
  };
};
