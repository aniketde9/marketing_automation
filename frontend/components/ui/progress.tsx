'use client';

import * as React from 'react';
import { Progress as RadixProgress } from '@radix-ui/react-progress';
import { cn } from '@/lib/utils';

type ProgressProps = React.ComponentPropsWithoutRef<typeof RadixProgress>;

const Progress = React.forwardRef<
  React.ElementRef<typeof RadixProgress>,
  ProgressProps & { value?: number }
>(({ className, value = 0, ...props }, ref) => (
  <RadixProgress
    ref={ref}
    className={cn('relative h-4 w-full overflow-hidden rounded-full bg-secondary', className)}
    value={value}
    {...props}
  >
    <div
      className="h-full w-full flex-1 bg-primary transition-all"
      style={{ transform: `translateX(-${100 - Math.min(100, value)}%)` }}
    />
  </RadixProgress>
));

Progress.displayName = RadixProgress.displayName;

export { Progress };

