import { redirect } from 'next/navigation';
import { auth } from '@/lib/auth';

export default async function HomePage() {
  const session = await auth();
  
  // If logged in, redirect to generate page
  if (session?.user) {
    redirect('/generate');
  }
  
  // If not logged in, redirect to login
  redirect('/login');
}
