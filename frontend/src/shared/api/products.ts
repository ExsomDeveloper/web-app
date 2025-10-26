import { Product } from '../types/product';

const API_BASE_URL = 'http://localhost:8000/api';

export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

export interface ProductsResponse {
  products: Product[];
}

export interface ProductResponse {
  product: Product;
}

export class ProductsApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = 'ProductsApiError';
  }
}

export const productsApi = {
  async getProducts(): Promise<Product[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/products`);
      
      if (!response.ok) {
        throw new ProductsApiError(
          `Ошибка сервера: ${response.status}`,
          response.status
        );
      }
      
      const data: ProductsResponse = await response.json();
      return data.products;
    } catch (error) {
      if (error instanceof ProductsApiError) {
        throw error;
      }
      
      // Обработка сетевых ошибок
      throw new ProductsApiError(
        'Возникла проблема, попробуйте позже',
        0
      );
    }
  },

  async getProduct(id: number): Promise<Product> {
    try {
      const response = await fetch(`${API_BASE_URL}/products/${id}`);
      
      if (!response.ok) {
        if (response.status === 404) {
          throw new ProductsApiError('Продукт не найден', 404);
        }
        throw new ProductsApiError(
          `Ошибка сервера: ${response.status}`,
          response.status
        );
      }
      
      const data: ProductResponse = await response.json();
      return data.product;
    } catch (error) {
      if (error instanceof ProductsApiError) {
        throw error;
      }
      
      throw new ProductsApiError(
        'Возникла проблема, попробуйте позже',
        0
      );
    }
  }
};
