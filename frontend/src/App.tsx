import React, { useState } from 'react';
import { HomePage } from './pages/home/ui/HomePage';
import { TryOnePage } from './pages/tryon/ui/TryOnePage';
import { CatalogPage } from './pages/catalog/ui/CatalogPage';
import './App.css';

type CurrentPage = 'home' | 'tryon' | 'catalog';

function App() {
  const [currentPage, setCurrentPage] = useState<CurrentPage>('home');

  const handleNavigateToTryOn = () => {
    setCurrentPage('tryon');
  };

  const handleNavigateToHome = () => {
    setCurrentPage('home');
  };

  const handleNavigateToCatalog = () => {
    setCurrentPage('catalog');
  };

  return (
    <>
      {currentPage === 'home' && (
        <HomePage 
          onNavigateToTryOn={handleNavigateToTryOn} 
          onNavigateToCatalog={handleNavigateToCatalog}
        />
      )}
      {currentPage === 'tryon' && (
        <TryOnePage onNavigateToHome={handleNavigateToHome} />
      )}
      {currentPage === 'catalog' && (
        <CatalogPage onNavigateToHome={handleNavigateToHome} />
      )}
    </>
  );
}

export default App;
