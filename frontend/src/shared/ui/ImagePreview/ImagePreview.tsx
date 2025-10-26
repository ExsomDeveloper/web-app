import React from 'react';

type ImagePreviewProps = {
  src?: string | null;
  filename?: string | null;
  tabType?: 'photo1' | 'photo2';
};

export function ImagePreview({ src, filename, tabType }: ImagePreviewProps) {
  if (!src && !filename) {
    const emptyText = tabType === 'photo1' ? 'Загрузите ваше фото' : 'Загрузите фото вещи';
    return <div className="empty">{emptyText}</div>;
  }
  return (
    <div className="preview">
      {src && <img className="previewImage" src={src} alt="preview" />}
      {filename && <span className="filename">{filename}</span>}
    </div>
  );
}


