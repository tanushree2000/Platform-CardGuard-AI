'use client';
import {useEffect} from 'react';import posthog from 'posthog-js';
export default function Analytics({children}:{children:React.ReactNode}){useEffect(()=>{const k=process.env.NEXT_PUBLIC_POSTHOG_KEY;if(k)posthog.init(k,{api_host:process.env.NEXT_PUBLIC_POSTHOG_HOST||'https://us.i.posthog.com'});},[]);return <>{children}</>}
export function capture(e:string,p?:Record<string,unknown>){try{posthog.capture(e,p)}catch{}}
