import React from 'react';

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'outline' | 'primary';
  children?: React.ReactNode;
};

export function Button({ variant = 'outline', className, children, ...rest }: ButtonProps) {
  const classes = [
    'btn',
    variant === 'outline' ? 'btn-outline' : 'btn-primary',
    className || ''
  ].join(' ').trim();
  return (
    <button className={classes} {...rest}>
      {children}
    </button>
  );
}


