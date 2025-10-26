import React from 'react';

export type TabItem = { key: string; label: string };

type TabsProps = {
  items: TabItem[];
  activeKey: string;
  onChange: (key: string) => void;
  className?: string;
};

export function Tabs({ items, activeKey, onChange, className }: TabsProps) {
  return (
    <div className={`tabs ${className || ''}`.trim()}>
      {items.map((item, idx) => (
        <button
          key={item.key}
          type="button"
          className={`tab ${activeKey === item.key ? 'active' : ''} ${idx < items.length - 1 ? '' : ''}`.trim()}
          onClick={() => onChange(item.key)}
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}


