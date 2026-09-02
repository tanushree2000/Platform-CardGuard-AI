import './globals.css';import Link from 'next/link';import Analytics from '@/components/Analytics';
export const metadata={title:'CardGuard AI'};
export default function Layout({children}:{children:React.ReactNode}){return <html><body><Analytics><div className="shell"><nav className="nav"><Link className="brand" href="/">CardGuard AI</Link><div className="navlinks"><Link href="/customer">Customer</Link><Link href="/ops">Fraud Ops</Link></div></nav>{children}</div></Analytics></body></html>}
