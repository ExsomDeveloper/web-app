import React from 'react';
import { Button } from '../../../shared/ui/Button/Button';
import './home.css';

interface HomePageProps {
  onNavigateToTryOn: () => void;
  onNavigateToCatalog: () => void;
}

export function HomePage({ onNavigateToTryOn, onNavigateToCatalog }: HomePageProps) {
  return (
    <div className="home-screen">
      <div className="home-content">
        <h1 className="home-title">Добро пожаловать!</h1>
        <p className="home-description">
          Попробуйте на себе любую одежду с помощью нашего приложения
        </p>
      </div>
      
      <div className="home-footer">
        <div className="nav-buttons">
          <Button 
            className="nav-button primary" 
            onClick={onNavigateToTryOn}
            type="button"
          >
            Начать примерку
          </Button>
          <Button 
            className="nav-button secondary" 
            onClick={onNavigateToCatalog}
            type="button"
          >
            Каталог товаров
          </Button>
        </div>
      </div>
    </div>
  );
}


