import React, { useMemo, useRef, useState } from 'react';
import { Tabs } from '../../../shared/ui/Tabs/Tabs';
import { Button } from '../../../shared/ui/Button/Button';
import { ImagePreview } from '../../../shared/ui/ImagePreview/ImagePreview';
import './tryon.css';

type ActiveTab = 'photo1' | 'photo2' | 'result';

interface TryOnePageProps {
  onNavigateToHome?: () => void;
}

export function TryOnePage({ onNavigateToHome }: TryOnePageProps) {
  const [activeTab, setActiveTab] = useState<ActiveTab>('photo1');
  const [photo1, setPhoto1] = useState<File | null>(null);
  const [photo2, setPhoto2] = useState<File | null>(null);
  const [photo1Url, setPhoto1Url] = useState<string | null>(null);
  const [photo2Url, setPhoto2Url] = useState<string | null>(null);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [messages, setMessages] = useState<Array<{id: number, text: string, isUser: boolean, timestamp: Date}>>([]);
  const [newMessage, setNewMessage] = useState('');
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const activeFile = useMemo(() => (activeTab === 'photo1' ? photo1 : activeTab === 'photo2' ? photo2 : null), [activeTab, photo1, photo2]);
  const activeUrl = useMemo(() => (activeTab === 'photo1' ? photo1Url : activeTab === 'photo2' ? photo2Url : null), [activeTab, photo1Url, photo2Url]);
  const uploadLabel = useMemo(() => {
    if (activeTab === 'photo1') return photo1 ? 'ИЗМЕНИТЬ' : 'ЗАГРУЗИТЬ';
    if (activeTab === 'photo2') return photo2 ? 'ИЗМЕНИТЬ' : 'ЗАГРУЗИТЬ';
    return '';
  }, [activeTab, photo1, photo2]);

  const tabItems = [
    { key: 'photo1', label: 'Ваше фото' },
    { key: 'photo2', label: 'Фото вещи' },
    { key: 'result', label: 'Результат' },
  ];

  function handlePickFile() {
    fileInputRef.current?.click();
  }

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files && event.target.files[0] ? event.target.files[0] : null;
    if (!file) return;

    if (activeTab === 'photo1') {
      if (photo1Url) URL.revokeObjectURL(photo1Url);
      const url = URL.createObjectURL(file);
      setPhoto1(file);
      setPhoto1Url(url);
      setActiveTab('photo2');
    } else if (activeTab === 'photo2') {
      if (photo2Url) URL.revokeObjectURL(photo2Url);
      const url = URL.createObjectURL(file);
      setPhoto2(file);
      setPhoto2Url(url);
    }

    event.target.value = '';
  }

  function handleSendMessage() {
    if (newMessage.trim()) {
      const userMessage = {
        id: Date.now(),
        text: newMessage,
        isUser: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, userMessage]);
      setNewMessage('');
      
      // Симуляция ответа стилиста
      setTimeout(() => {
        const stylistMessage = {
          id: Date.now() + 1,
          text: "Спасибо за ваше сообщение! Я помогу вам с выбором стиля. Расскажите, какой образ вы хотите создать?",
          isUser: false,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, stylistMessage]);
      }, 1000);
    }
  }

  function handleKeyPress(event: React.KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  }

  function fileToBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        const base64 = reader.result as string;
        // Убираем префикс "data:image/...;base64,"
        const base64Data = base64.split(',')[1];
        resolve(base64Data);
      };
      reader.onerror = error => reject(error);
    });
  }

  async function handleTryOn() {
    if (!photo1 || !photo2) {
      alert('Пожалуйста, загрузите оба изображения');
      return;
    }

    setIsLoading(true);
    try {
      const base64Photo1 = await fileToBase64(photo1);
      const base64Photo2 = await fileToBase64(photo2);

      // Автоматическое определение API URL
      const API_URL = window.location.hostname === 'localhost' 
        ? 'http://localhost:8000' 
        : 'https://unslighted-complaisantly-erma.ngrok-free.dev';
      
      const response = await fetch(`${API_URL}/api/tryon`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          photo1: base64Photo1,
          photo2: base64Photo2,
        }),
      });

      if (!response.ok) {
        throw new Error('Ошибка при отправке на сервер');
      }

      const data = await response.json();
      setResultImage(data.result_image);
      setActiveTab('result');
    } catch (error) {
      console.error('Ошибка:', error);
      alert('Произошла ошибка при обработке изображений');
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="screen">
      <Tabs items={tabItems} activeKey={activeTab} onChange={(k) => setActiveTab(k as ActiveTab)} />

      <div className="content">
        {activeTab === 'result' ? (
          <div className="result-container">
            {resultImage ? (
              <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                <img 
                  src={`data:image/png;base64,${resultImage}`} 
                  alt="Результат примерки" 
                  style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
                />
              </div>
            ) : (
              <div className="resultList">
                <div className="resultItem">Ваше фото: <span className="filename">{photo1 ? photo1.name : 'не выбрано'}</span></div>
                <div className="resultItem">Фото вещи: <span className="filename">{photo2 ? photo2.name : 'не выбрано'}</span></div>
              </div>
            )}
          </div>
        ) : (
          <ImagePreview src={activeUrl || undefined} filename={activeFile?.name || null} tabType={activeTab} />
        )}
      </div>

      <div className="footer">
        <div className="footer-buttons">
          {activeTab === 'result' ? (
            <Button 
              className="uploadBtn" 
              onClick={handleTryOn} 
              type="button"
              disabled={isLoading}
            >
              {isLoading ? 'Обработка...' : 'Примерять'}
            </Button>
          ) : (
            <Button className="uploadBtn" onClick={handlePickFile} type="button">{uploadLabel}</Button>
          )}
          <Button 
            className="stylistBtn" 
            onClick={() => setIsChatOpen(!isChatOpen)} 
            type="button"
          >
            Стилист
          </Button>
          {onNavigateToHome && (
            <Button className="backBtn" onClick={onNavigateToHome} type="button">Назад</Button>
          )}
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />
      </div>

      {isChatOpen && (
        <div className="chat-overlay" onClick={(e) => {
          if (e.target === e.currentTarget) {
            setIsChatOpen(false);
          }
        }}>
          <div className="chat-container" onClick={(e) => e.stopPropagation()}>
            <div className="chat-header">
              <h3>Стилист</h3>
              <Button 
                className="close-chat-btn" 
                onClick={() => setIsChatOpen(false)} 
                type="button"
              >
                ✕
              </Button>
            </div>
            <div className="chat-messages">
              {messages.map((message) => (
                <div key={message.id} className={`message ${message.isUser ? 'user-message' : 'stylist-message'}`}>
                  <div className="message-content">
                    {message.text}
                  </div>
                  <div className="message-time">
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>
              ))}
            </div>
            <div className="chat-input">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Напишите сообщение..."
                className="message-input"
              />
              <Button 
                className="send-btn" 
                onClick={handleSendMessage} 
                type="button"
                disabled={!newMessage.trim()}
              >
                Отправить
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
