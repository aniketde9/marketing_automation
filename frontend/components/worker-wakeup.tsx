'use client';

import { useEffect, useState } from "react";

export function WorkerWakeup() {
  const [status, setStatus] = useState<'idle' | 'waking' | 'ready'>('idle');
  const WORKER_URL = process.env.NEXT_PUBLIC_WORKER_URL;

  useEffect(() => {
    if (!WORKER_URL) {
      console.warn('NEXT_PUBLIC_WORKER_URL not set');
      return;
    }

    const wakeWorker = async () => {
      setStatus('waking');

      try {
        await fetch(WORKER_URL, {
          method: 'GET',
          mode: 'no-cors',
        });

        console.log('Worker wakeup request sent');

        setTimeout(() => {
          setStatus('ready');
        }, 30000);
      } catch (error) {
        console.log('Worker wakeup attempted');
        setTimeout(() => {
          setStatus('ready');
        }, 30000);
      }
    };

    wakeWorker();
  }, [WORKER_URL]);

  if (status === 'idle') return null;

  return (
    <div className="fixed bottom-4 right-4 bg-blue-500 text-white px-4 py-2 rounded-lg shadow-lg text-sm z-50">
      {status === 'waking' && 'Preparing worker...'}
      {status === 'ready' && 'Worker ready'}
    </div>
  );
}
